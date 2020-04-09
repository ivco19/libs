
# DEVELOPMENT (plots)

import numpy as np
import pandas as pd
import datetime
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# LOAD DATA
def load_data():


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
    covid_df['active'] = covid_df['confirmed'] - covid_df['deaths'] - covid_df['recovered']

    covid_df['Country/Region'].replace('Mainland China', 'China', inplace=True)
    covid_df[['Province/State']] = covid_df[['Province/State']].fillna('')
    covid_df.fillna(0, inplace=True)

    #---

    covid_countries_df = covid_df.groupby(['Country/Region', 'Province/State']).max().reset_index()
    covid_countries_df = covid_countries_df.groupby('Country/Region').sum().reset_index()
    covid_countries_df.drop(['Lat', 'Long'], axis=1, inplace=True)

    covid_countries_date_df = covid_df.groupby(['Country/Region', 'date'], sort=False).sum().reset_index()

    covid_countries_date_df['Country/Region'].replace('Korea, South', 'South Korea', inplace=True)

    return(covid_countries_date_df)


def get_country(df, country_name):

    # COUNTRIES
    df_pais = df[df['Country/Region'] == country_name]
    return(df_pais)


# PLOT ----------------------- casos confirmados en Argentina
def plt_1country(df, country_name):

    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    import seaborn as sns

    fig, ax = plt.subplots(figsize=(16, 6))

    sns.lineplot(x=df['date'], y=df['confirmed'], sort=False, linewidth=2)
    plt.suptitle("COVID-19", fontsize=16, fontweight='bold', color='white')

    plt.xticks(rotation=45)
    plt.ylabel('casos confirmados')

    ax.legend(['Argentina', 'World except China'])

    fplot = 'plot_' + country_name + '.png'
    fig.savefig(fplot)

# ------------------

def plt_ncountries(df, country_list=['Argentina']):
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

    country_list = ['Argentina', 'Chile', 'Germany', 'Iran', 'Italy']
    y_all = []
    t_all = []
    for pais in country_list:
        #popu = df_world[df_world['country'] == pais]['population'].values[0]
        #area = df_world[df_world['country'] == pais]['area'].values[0]
        covid_pais = df[df['Country/Region'] == pais]    
        z = covid_pais['confirmed']

        # time normalization: 100th patient
        ind = next(x[0] for x in enumerate(z.values) if x[1] > 100)
        patient_100_day = t[ind]
        t_pais = t - patient_100_day

        # count normalization: country population
        y_pais = covid_pais['confirmed'] #/ popu * 1.e6   
        
        y_all.append(y_pais)
        t_all.append(t_pais)

    fig, ax = plt.subplots(figsize=(16, 6))
    ax.set(yscale="log")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

    for t, y in zip(t_all, y_all):
        sns.lineplot(x=t, y=y, sort=False, linewidth=2)

    plt.suptitle("COVID-19 per country cases over the time", fontsize=16, fontweight='bold', color='white')
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

    lista_america = ['Argentina', 'Chile','US','Venezuela','Canada']
    lista_europe = ['Germany', 'Iran', 'Italy','United Kingdom','Israel']
    lista_asia = ['Japan','South Korea']
    lista_africa = ['South Africa']
    lista_oceania = []

    lista = lista_america + lista_oceania + lista_europe + lista_asia 
    clrs = ['black']*len(lista_america) + ['yellow']*len(lista_oceania) + \
           ['red']*len(lista_europe) + ['blue'] * len(lista_asia)

    lstcycle = ['-','--',':','-.','-','-','-','-']
    mstyle = lstcycle[0:len(lista_america)] + lstcycle[0:len(lista_oceania)] + \
           lstcycle[0:len(lista_europe)] + lstcycle[0:len(lista_asia)]

    y_all = []
    t_all = []
    critical_number = 100
    for pais in lista:

        print(pais)

        popu = df_world[df_world['country'] == pais]['population'].values[0]
        area = df_world[df_world['country'] == pais]['area'].values[0]
        covid_pais = df[df['Country/Region'] == pais]
        
        z = covid_pais['confirmed']


        print(z.values)


        ind = next(x[0] for x in enumerate(z.values) if x[1] > critical_number)

        patient_100_day = t[ind]
        t_pais = t - patient_100_day   
        y_pais = covid_pais['confirmed'] / popu * 1.e6
        
        y_all.append(y_pais)
        t_all.append(t_pais)

    fig, ax = plt.subplots(figsize=(16, 6))
    ax.set(yscale="log")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

    #for t, y in zip(t_all, y_all):
    sns.lineplot(x=t_all[0], y=y_all[0], sort=False, linewidth=3, color='black')
    for i in range(len(t_all))[1:]:
        sns.lineplot(x=t_all[i], y=y_all[i], sort=False, linewidth=1, color=clrs[i], linestyle=mstyle[i])
        
    plt.suptitle("COVID-19 per country cases over the time", fontsize=16, fontweight='bold', color='white')
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

    lista_america = ['Argentina', 'Chile','US','Venezuela','Canada']
    lista_europe = ['Germany', 'Iran', 'Italy','United Kingdom','Israel']
    lista_asia = ['Japan','South Korea']
    lista_africa = ['South Africa']
    lista_oceania = []

    lista = lista_america + lista_oceania + lista_europe + lista_asia 
    clrs = ['black']*len(lista_america) + ['yellow']*len(lista_oceania) + \
           ['red']*len(lista_europe) + ['blue'] * len(lista_asia)

    lstcycle = ['-','--',':','-.','-','-','-','-']
    mstyle = lstcycle[0:len(lista_america)] + lstcycle[0:len(lista_oceania)] + \
           lstcycle[0:len(lista_europe)] + lstcycle[0:len(lista_asia)]

    y_all = []
    t_all = []
    critical_number = 100
    for pais in lista:

        print(pais)

        popu = df_world[df_world['country'] == pais]['population'].values[0]
        area = df_world[df_world['country'] == pais]['area'].values[0]
        covid_pais = df[df['Country/Region'] == pais]
        
        z = covid_pais['confirmed']


        print(z.values)


        ind = next(x[0] for x in enumerate(z.values) if x[1] > critical_number)

        patient_100_day = t[ind]
        t_pais = t - patient_100_day   
        y_pais = covid_pais['confirmed'] / popu * 1.e6
        
        y_all.append(y_pais)
        t_all.append(t_pais)
             

    fig, ax = plt.subplots(figsize=(16, 6))
    #ax.set(yscale="log")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

    #for t, y in zip(t_all, y_all):
    sns.lineplot(x=t_all[0], y=y_all[0], sort=False, linewidth=3, color='black')
    for i in range(len(t_all))[1:]:
        sns.lineplot(x=t_all[i], y=y_all[i], sort=False, linewidth=1, color=clrs[i], linestyle=mstyle[i])
        
    plt.suptitle("COVID-19 per country cases over the time", fontsize=16, fontweight='bold', color='white')
    plt.title("(logarithmic scale)", color='white')

    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.set_xlim(0, 50)
    plt.xticks(rotation=0)
    plt.xlabel('días después de los 100 casos confirmados')
    plt.ylabel('Casos confirmados por millón de habitantes')

    ax.legend(lista)
    fig.savefig('new_plot.png')

    plt.close()

