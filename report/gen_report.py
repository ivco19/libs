import jinja2
import os
import subprocess as sp

# ______________________________________________________________________
# 1. Generar plots

import sys
from importlib import reload
import countries as co
if co not in sys.modules:
    co = reload(co)

df_countries = co.load_data()

# plot 01: argentina
df_arg = co.get_country(df_countries, 'Argentina')
fplot_01 = 'plot_01.png'
co.plt_1country(df_arg, 'argentina', fplot=fplot_01)

# plot 02: argentina en el mundo
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
fplot_02 = 'plot_02.png'

co.plt_presi(df_countries,
             country_list=country_list,
             ccolors=ccolors, cmarkers=cmarkers, cstyles=cstyles,
             cwidths=cwidths, cfaces=cfaces, calpha=calpha,
             critical_number=1.e-6, norm='perc',
             pltname=fplot_02)

fplot_03 = 'plot_03.png'
co.plt_ncountries(df_countries, 'argentina', fplot_03)

fplot_04 = 'plot_04.png'
co.plt_continents(df_countries, 'argentina', fplot_04)

fplot_05 = 'plot_05.png'
co.plt_paises(df_countries, ['argentina'], fplot_05)

# ______________________________________________________________________
# 2. Generar informe
source_dir = '../report/'
report_dir = '../report/'
template_file = 'template.tex'
templateLoader = jinja2.FileSystemLoader(searchpath=report_dir)

latex_jinja_env = jinja2.Environment(
    block_start_string=r"\BLOCK{",
    block_end_string='}',
    variable_start_string=r'\VAR{',
    variable_end_string='}',
    comment_start_string=r'\#{',
    comment_end_string='}',
    line_statement_prefix='%%',
    line_comment_prefix='%#',
    trim_blocks=True,
    autoescape=False,
    loader=templateLoader
)

# Make LaTeX file

template_intro = latex_jinja_env.get_template(template_file)
Nplots = 5

plts = ['plot_01.png',
        'plot_02.png',
        'plot_03.png',
        'plot_04.png',
        'plot_05.png']

captions = [""]*5
captions[0] = "Likelihood map from LIGO alert"
captions[1] = "Masked likelihood map from LIGO alert"
captions[2] = "Gnomon--projected detail of the likelihood map from LIGO alert"
captions[3] = "Distribution of targets in observable sky"
captions[4] = "Histogram of the RA of targets"

# write to file
filename = os.path.join(report_dir, 'report.tex')
target = open(filename, 'w')
target.write(template_intro.render(Nplots=Nplots, plts=plts,
             captions=captions))
target.close()

cmd = ['pdflatex', '-interaction', 'nonstopmode', 'report.tex']
proc = sp.Popen(cmd)
proc.communicate()
os.chdir(source_dir)
