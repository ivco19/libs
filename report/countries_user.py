import sys
from importlib import reload
import countries as co
if co not in sys.modules:
    co = reload(co)

df_countries = co.load_data()

# df_arg = co.get_country(df_countries, 'Argentina')
# co.plt_1country(df_arg, 'argentina')
# co.plt_ncountries(df_countries, 'argentina')
# co.plt_continents(df_countries, 'argentina')
# co.plt_paises(df_countries, ['argentina'])

country_list = ['Argentina', 'Brazil', 'Chile', 'US', 'Peru',
                'Spain', 'Italy', 'Germany', 'France', 'United Kingdom',
                'South Korea', 'China', 'Japan', 'Russia', 'Iran']
ccolors = ['steelblue', 'peru', 'darkmagenta',
           'darkcyan', 'slateblue', 'mediumpurple', 'firebrick', 'slategray']
ccolors = ['steelblue']*5 + ['peru']*5 + ['darkmagenta']*5

cmarkers = ['o', '.', 'o', 'x', 'D']
cstyles = ['-', '-', '--', '--', ':']
cwidths = [2, 1, 1, 1, 2]
cwidths = [3] + [1]*20
cfaces = ccolors[:]
for i in range(len(cfaces)):
    if i % 5 == 0 or i % 5 == 4:
        cfaces[i] = 'white'

calpha = [1.0]*5 + [1.0]*5 + [1.0]*5

pltname = f'new_plot.png'

co.plt_presi(df_countries,
             ccolors=ccolors,
             cmarkers=cmarkers,
             cstyles=cstyles,
             cwidths=cwidths,
             cfaces=cfaces,
             calpha=calpha,
             country_list=country_list,
             critical_number=1.e-6,
             norm='perc',
             pltname=pltname)


# for i in range(0, 100, 5):
#     critical = i
#     print(i)
#     pltname = f'new_plot_grow_{i}.png'
#     co.plt_presi(df_countries, critical_number=100,
#             country_list=country_list, clrs=colors,
#             ndays = i,
#             pltname=pltname)
