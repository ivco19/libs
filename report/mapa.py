import plotly.express as px
import json
import pandas as pd
from random import random
import arcovid19 as ar

# DATOS DE ARGENTINA ------------------------

df = ar.load_cases()

d1 = ar.PROVINCIAS
d2 = ar.PROVINCIAS_ALIAS
d = dict(ar.PROVINCIAS, **ar.PROVINCIAS_ALIAS)

C = []
A = []
R = []
D = []

for k in d.keys():
    p = d[k]
    C.append(df.loc[(p, 'C')].values[-1])
    A.append(df.loc[(p, 'A')].values[-1])
    R.append(df.loc[(p, 'R')].values[-1])
    D.append(df.loc[(p, 'D')].values[-1])

# MAPA DE ARGENTINA ------------------------
with open('../databases/provincias_argentina_iso_con_geo.geojson') as f:
    arg = json.load(f)

# arreglar cosas a mano
arg['features'][18]['properties']['provincia'] = 'CABA'
arg['features'][7]['properties']['provincia'] = 'Bs As'

prov_ids = []
prov_names = []
prov_values = []
feat = arg['features']

Cs = []
As = []
Rs = []
Ds = []

for i, p in enumerate(feat):
    arg['features'][i]['id'] = i
    prov = p['properties']['provincia']
    prov_ids.append(i)
    prov_names.append(prov)
    prov_values.append(random())
    for j, n in enumerate(d.keys()):
        if prov in n:
            Cs.append(C[j])
            As.append(A[j])
            Rs.append(R[j])
            Ds.append(D[j])

d = {'provincia': prov_names,
     'valores': prov_values,
     'id': prov_ids,
     'C': Cs, 'A': As, 'R': Rs, 'D': Ds
     }
df = pd.DataFrame.from_dict(d)

fig = px.choropleth(df, geojson=arg,
                    locations='id',
                    color="C",
                    color_continuous_scale="Viridis",
                    range_color=(0, 400),
                    scope="south america",
                    hover_name="provincia",
                    labels={'A': 'A', 'R': 'R'}
                    )
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.write_image("fig1.png")
fig.show()
