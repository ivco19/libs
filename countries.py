# DEVELOPMENT (plots)

import numpy as np
import pandas as pd
import datetime
from matplotlib import pyplot as plt
import matplotlib.lines as mlines
import matplotlib.ticker as ticker
import seaborn as sns
import itertools
import math as m


def label_line(line, label, x, y, color='0.5', size=12):
    """Add a label to a line, at the proper angle.

    Arguments
    ---------
    line : matplotlib.lines.Line2D object,
    label : str
    x : float
        x-position to place center of text (in data coordinated
    y : float
        y-position to place center of text (in data coordinates)
    color : str
    size : float
    """
    xdata, ydata = line.get_data()
    x1 = xdata[0]
    x2 = xdata[-1]
    y1 = ydata[0]
    y2 = ydata[-1]

    ax = line.get_axes()
    text = ax.annotate(label, xy=(x, y), xytext=(-10, 0),
                       textcoords='offset points',
                       size=size, color=color,
                       horizontalalignment='left',
                       verticalalignment='bottom')

    sp1 = ax.transData.transform_point((x1, y1))
    sp2 = ax.transData.transform_point((x2, y2))

    rise = (sp2[1] - sp1[1])
    run = (sp2[0] - sp1[0])

    slope_degrees = np.degrees(np.arctan2(rise, run))
    text.set_rotation(slope_degrees)
    return text


def load_data():
    """
    LOAD DATA
    """

    base_url = 'https://raw.githubusercontent.com/CSSEGISandData/'\
               'COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'
    COVID_CONFIRMED_URL = base_url + 'time_series_covid19_confirmed_global.csv'
    covid_confirmed = pd.read_csv(COVID_CONFIRMED_URL)
    COVID_DEATHS_URL = base_url + 'time_series_covid19_deaths_global.csv'
    covid_deaths = pd.read_csv(COVID_DEATHS_URL)
    COVID_RECOVERED_URL = base_url + 'time_series_covid19_recovered_global.csv'
    covid_recovered = pd.read_csv(COVID_RECOVERED_URL)

    covid_confirmed_long = pd.melt(covid_confirmed,
                                   id_vars=covid_confirmed.iloc[:, :4],
                                   var_name='date',
                                   value_name='confirmed')

    covid_deaths_long = pd.melt(covid_deaths,
                                id_vars=covid_deaths.iloc[:, :4],
                                var_name='date',
                                value_name='deaths')

    covid_recovered_long = pd.melt(covid_recovered,
                                   id_vars=covid_recovered.iloc[:, :4],
                                   var_name='date',
                                   value_name='recovered')

    covid_df = covid_confirmed_long
    covid_df['deaths'] = covid_deaths_long['deaths']
    covid_df['recovered'] = covid_recovered_long['recovered']
    confirmed_down = covid_df['deaths'] - covid_df['recovered']
    covid_df['active'] = covid_df['confirmed'] - confirmed_down
    covid_df['Country/Region'].replace('Mainland China', 'China', inplace=True)
    covid_df[['Province/State']] = covid_df[['Province/State']].fillna('')
    covid_df.fillna(0, inplace=True)
    grouped = covid_df.groupby(['Country/Region', 'Province/State'])
    covid_countries_df = grouped.max().reset_index()
    grouped = covid_countries_df.groupby('Country/Region')
    covid_countries_df = grouped.sum().reset_index()
    covid_countries_df.drop(['Lat', 'Long'], axis=1, inplace=True)
    grouped = covid_df.groupby(['Country/Region', 'date'], sort=False)
    covid_countries_date_df = grouped.sum().reset_index()
    covid_countries_date_df['Country/Region'].replace(
            'Korea, South', 'South Korea', inplace=True)
    return(covid_countries_date_df)


def get_country(df, country_name):

    # COUNTRIES
    df_pais = df[df['Country/Region'] == country_name]
    return(df_pais)


def plt_1country(df, country_name):
    """
    PLOT: casos confirmados en Argentina
    """

    import matplotlib.pyplot as plt
    import seaborn as sns

    fig, ax = plt.subplots(figsize=(16, 6))

    sns.lineplot(x=df['date'], y=df['confirmed'], sort=False, linewidth=2)
    plt.suptitle("COVID-19", fontsize=16, fontweight='bold', color='white')

    plt.xticks(rotation=45)
    plt.ylabel('casos confirmados')

    ax.legend(['Argentina', 'World except China'])

    fplot = 'plot_' + country_name + '.png'
    fig.savefig(fplot)


def plt_ncountries(df, country_list=['Argentina']):
    """
    normalizado el tiempo al inicio del caso nro 100, la cantidad de
    infectados a la poblacion del pais, x millon de hab.
    """

    covid_ita = df[df['Country/Region'] == 'Italy']
    t = []
    d0 = datetime.datetime.strptime("1/1/20", '%m/%d/%y')
    for d in covid_ita['date']:
        elapsed_days = (datetime.datetime.strptime(d, '%m/%d/%y') - d0).days
        t.append(elapsed_days)
    t = np.array(t)

    country_list = ['Argentina', 'Chile', 'Germany', 'Iran', 'Italy']
    y_all = []
    t_all = []
    for pais in country_list:
        # popu = df_world[df_world['country'] == pais]['population'].values[0]
        # area = df_world[df_world['country'] == pais]['area'].values[0]
        covid_pais = df[df['Country/Region'] == pais]
        z = covid_pais['confirmed']

        # time normalization: 100th patient
        ind = next(x[0] for x in enumerate(z.values) if x[1] > 100)
        patient_100_day = t[ind]
        t_pais = t - patient_100_day

        # count normalization: country population
        y_pais = covid_pais['confirmed']
        y_all.append(y_pais)
        t_all.append(t_pais)

    fig, ax = plt.subplots(figsize=(16, 6))
    ax.set(yscale="log")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(
                                 lambda y, _: '{:g}'.format(y)))

    for t, y in zip(t_all, y_all):
        sns.lineplot(x=t, y=y, sort=False, linewidth=2)

    plt.suptitle("COVID-19 per country cases over the time",
                 fontsize=16, fontweight='bold', color='white')
    plt.title("(logarithmic scale)", color='white')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    plt.xticks(rotation=0)
    plt.ylabel('Casos confirmados por millón de habitantes')
    ax.legend(['Argentina', 'España', 'chile', 'ita'])
    fig.savefig('new_plot.png')
    plt.close()


def plt_continents(df, country_list=['Argentina']):
    """
    normalizado el tiempo al inicio del caso nro 100, la cantidad de
    infectados a la poblacion del pais, x millon de hab.
    """

    df_world = pd.read_csv('databases/pop_area.csv')

    covid_ita = df[df['Country/Region'] == 'Italy']
    t = []
    d0 = datetime.datetime.strptime("1/1/20", '%m/%d/%y')
    for d in covid_ita['date']:
        elapsed_days = (datetime.datetime.strptime(d, '%m/%d/%y') - d0).days
        t.append(elapsed_days)
    t = np.array(t)

    lista_america = ['Argentina', 'Chile', 'US', 'Venezuela', 'Canada']
    lista_europe = ['Germany', 'Iran', 'Italy', 'United Kingdom', 'Israel']
    lista_asia = ['Japan', 'South Korea']
    lista_oceania = []

    lista = lista_america + lista_oceania + lista_europe + lista_asia
    clrs = ['black']*len(lista_america) + ['yellow']*len(lista_oceania) + \
           ['red']*len(lista_europe) + ['blue'] * len(lista_asia)

    lstcycle = ['-', '--', ':', '-.', '-', '-', '-', '-']
    mstyle = lstcycle[0:len(lista_america)]
    mstyle = mstyle + lstcycle[0:len(lista_oceania)]
    mstyle = mstyle + lstcycle[0:len(lista_europe)]
    mstyle = mstyle + lstcycle[0:len(lista_asia)]

    y_all = []
    t_all = []
    critical_number = 100
    for pais in lista:

        print(pais)

        popu = df_world[df_world['country'] == pais]['population'].values[0]
        covid_pais = df[df['Country/Region'] == pais]

        z = covid_pais['confirmed']

        ind = next(x[0] for x in enumerate(z.values) if x[1] > critical_number)
        patient_100_day = t[ind]
        t_pais = t - patient_100_day
        y_pais = covid_pais['confirmed'] / popu * 1.e6
        y_all.append(y_pais)
        t_all.append(t_pais)

    fig, ax = plt.subplots(figsize=(16, 6))
    ax.set(yscale="log")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(
                                 lambda y, _: '{:g}'.format(y)))

    sns.lineplot(x=t_all[0], y=y_all[0],
                 sort=False, linewidth=3, color='black')
    for i in range(len(t_all))[1:]:
        sns.lineplot(x=t_all[i], y=y_all[i], sort=False,
                     linewidth=1, color=clrs[i], linestyle=mstyle[i])

    plt.suptitle("COVID-19 per country cases over the time",
                 fontsize=16, fontweight='bold', color='white')
    plt.title("(logarithmic scale)", color='white')

    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    plt.xticks(rotation=0)
    plt.xlabel('días después de los 100 casos confirmados')
    plt.ylabel('Casos confirmados por millón de habitantes')

    ax.legend(lista)
    fig.savefig('new_plot.png')

    plt.close()


def plt_paises(df, country_list=['Argentina']):
    """
    normalizado el tiempo al inicio del caso nro 100, la cantidad de
    infectados a la poblacion del pais, x millon de hab.
    """

    df_world = pd.read_csv('databases/pop_area.csv')

    covid_ita = df[df['Country/Region'] == 'Italy']
    t = []
    d0 = datetime.datetime.strptime("1/1/20", '%m/%d/%y')
    for d in covid_ita['date']:
        elapsed_days = (datetime.datetime.strptime(d, '%m/%d/%y') - d0).days
        t.append(elapsed_days)
    t = np.array(t)
    lista_america = ['Argentina', 'Chile', 'US', 'Venezuela', 'Canada']
    lista_europe = ['Germany', 'Iran', 'Italy', 'United Kingdom', 'Israel']
    lista_asia = ['Japan', 'South Korea']
    lista_oceania = []
    lista = lista_america + lista_oceania + lista_europe + lista_asia
    clrs = ['black']*len(lista_america) + ['yellow']*len(lista_oceania) + \
           ['red']*len(lista_europe) + ['blue'] * len(lista_asia)

    lstcycle = ['-', '--', ':', '-.', '-', '-', '-', '-']
    mstyle = lstcycle[0:len(lista_america)]
    mstyle = mstyle + lstcycle[0:len(lista_oceania)]
    mstyle = mstyle + lstcycle[0:len(lista_europe)]
    mstyle = mstyle + lstcycle[0:len(lista_asia)]

    y_all = []
    t_all = []
    critical_number = 100
    for pais in lista:
        popu = df_world[df_world['country'] == pais]['population'].values[0]
        covid_pais = df[df['Country/Region'] == pais]
        z = covid_pais['confirmed']
        ind = next(x[0] for x in enumerate(z.values) if x[1] > critical_number)
        patient_100_day = t[ind]
        t_pais = t - patient_100_day
        y_pais = covid_pais['confirmed'] / popu * 1.e6
        y_all.append(y_pais)
        t_all.append(t_pais)

    fig, ax = plt.subplots(figsize=(16, 6))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(
                                 lambda y, _: '{:g}'.format(y)))
    sns.lineplot(x=t_all[0], y=y_all[0],
                 sort=False, linewidth=3, color='black')
    for i in range(len(t_all))[1:]:
        sns.lineplot(x=t_all[i], y=y_all[i], sort=False,
                     linewidth=1, color=clrs[i], linestyle=mstyle[i])

    plt.suptitle("COVID-19 per country cases over the time",
                 fontsize=16, fontweight='bold', color='white')
    plt.title("(logarithmic scale)", color='white')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.set_xlim(0, 50)
    plt.xticks(rotation=0)
    plt.xlabel('días después de los 100 casos confirmados')
    plt.ylabel('Casos confirmados por millón de habitantes')
    ax.legend(lista)
    fig.savefig('new_plot.png')
    plt.close()


def plt_presi(df, critical_number=100, country_list=['Argentina'],
              ccolors=['black'],
              cmarkers=['o'],
              cstyles=['-'],
              cwidths=[1],
              cfaces=['white'],
              calpha=[1.],
              pltname='new_plot.png', ndays=0, norm=False):
    """
    normalizado el tiempo al inicio del caso nro 100, la cantidad de
    infectados a la poblacion del pais, x millon de hab.
    """
    if critical_number >= 1 and norm == 'perc':
        print("please check docs")
        return()

    df_world = pd.read_csv('databases/pop_area.csv')
    covid_ita = df[df['Country/Region'] == 'Italy']
    t = []
    d0 = datetime.datetime.strptime("1/1/20", '%m/%d/%y')
    for d in covid_ita['date']:
        elapsed_days = (datetime.datetime.strptime(d, '%m/%d/%y') - d0).days
        t.append(elapsed_days)
    t = np.array(t)
    if ndays == 0:
        ld = len(t)
    else:
        ld = ndays

    icolors = itertools.cycle(ccolors)
    imarkers = itertools.cycle(cmarkers)
    istyles = itertools.cycle(cstyles)
    iwidths = itertools.cycle(cwidths)
    ifaces = itertools.cycle(cfaces)
    ialpha = itertools.cycle(calpha)

    y_all = []
    t_all = []
    for pais in country_list:
        popu = df_world[df_world['country'] == pais]['population'].values[0]
        covid_pais = df[df['Country/Region'] == pais]
        z = covid_pais['confirmed']
        if norm == 'perc':
            crit = popu * critical_number
        else:
            crit = critical_number
        ind = next(x[0] for x in enumerate(z.values) if x[1] > crit)
        patient_nth_day = t[ind]
        t_pais = t - patient_nth_day
        y_pais = covid_pais['confirmed']
        if norm == 'pop':
            y_pais = y_pais / popu * 1.e6
        if norm == 'perc':
            y_pais = y_pais / popu
        y_all.append(y_pais)
        t_all.append(t_pais)

    fig, ax = plt.subplots(figsize=(16, 6))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(
                                 lambda y, _: '{:g}'.format(y)))
    for i in range(len(t_all)):
        plt.plot(t_all[i][:ld], y_all[i][:ld], color=next(icolors),
                 linewidth=next(iwidths), linestyle=next(istyles),
                 marker=next(imarkers), markerfacecolor=next(ifaces),
                 markeredgewidth=1, markersize=4, markevery=3,
                 alpha=next(ialpha))

    plt.suptitle("COVID-19 per country cases over the time",
                 fontsize=16, fontweight='bold', color='white')
    plt.title("(logarithmic scale)", color='white')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.set_xlim(-1, 60)
    plt.xticks(rotation=0)
    plt.xlabel(f'días después de los {critical_number} casos confirmados',
               fontsize=14, fontweight='bold', color='slategray')
    plt.ylabel('Casos confirmados por millón de habitantes',
               fontsize=14, fontweight='bold', color='slategray')
    if norm == 'perc':
        ax.set_ylim(critical_number, 0.004)
        plt.xlabel('days after a fraction of ' +
                   f'{critical_number}' +
                   ' of the population gets infected',
                   fontsize=12, fontweight='bold', color='slategray')
        plt.ylabel('fraction of the population confirmed infectious',
                   fontsize=12, fontweight='bold', color='slategray')
    ax.set(yscale="log")

    xmin = 0
    xmax = 60
    ymin = 1.e-6
    msg = 'duplicates every'
    ylocs = [1.e-4, 1.e-3, 1.e-3, 1.e-3, 1.e-5]
    for i, d in enumerate([1, 2, 3, 5, 10]):
        ymax = ymin*m.exp(m.log(2)*xmax/d)
        l_trend2 = mlines.Line2D([xmin, xmax], [ymin, ymax],
                                 linewidth=1, color='gainsboro',
                                 linestyle='-', label='_nolegend_')
        ax.add_line(l_trend2)
        yloc = ylocs[i]
        xloc = d * m.log(yloc*1.e6)/m.log(2)

        text = ax.annotate(msg + f' {d} days',
                           xy=(xloc, yloc), xytext=(-10, 10),
                           color='silver',
                           textcoords='offset points',
                           horizontalalignment='left',
                           verticalalignment='bottom')

        sp1 = ax.transData.transform_point((xmin, m.log(ymin)))
        sp2 = ax.transData.transform_point((xmax, m.log(ymax)))
        sp1 = ax.transData.transform_point((xmin, ymin))
        sp2 = ax.transData.transform_point((xmax, ymax))
        rise = (sp2[1] - sp1[1])
        run = (sp2[0] - sp1[0])
        slope_degrees = np.degrees(np.arctan2(rise, run))
        print(slope_degrees)
        text.set_rotation(slope_degrees)
        msg = '...'

    ax.legend(country_list, loc='lower right', frameon=False,
              ncol=3, handlelength=3)
    ax.grid(color='gainsboro', linewidth=.3)
    fig.savefig(pltname)
    fig.tight_layout()
    plt.close()
