import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd

geojson_mx = gpd.read_file('Datasets/mexicoHigh.json')


plt.style.use('ggplot')
df = pd.read_csv('Datasets/d3_aire01_49_1_limpio.csv')
df.info()

contaminantes = ['SO_2', 'CO', 'NOx', 'COV', 'PM_010', 'PM_2_5', 'NH_3']
df_contaminante_fuente = df.groupby('Tipo_de_Fuente')[contaminantes].sum().reset_index()
df_melt = df_contaminante_fuente.melt(id_vars='Tipo_de_Fuente', var_name='Contaminante', value_name='Toneladas')
 
totales = df_melt.groupby('Contaminante')['Toneladas'].transform('sum')
df_melt['Porcentaje'] = df_melt['Toneladas'] / totales * 100
 
fig1 = px.bar(
    df_melt,
    x='Contaminante',
    y='Porcentaje',
    color='Tipo_de_Fuente',
    barmode='stack',
    text=df_melt['Toneladas'].round(1).astype(str) + ' t',
    title='Composición de emisiones por contaminante y tipo de fuente',
    labels={'Porcentaje': '% de emisiones', 'Tipo_de_Fuente': 'Tipo de fuente'},
    hover_data={'Toneladas': ':.1f', 'Porcentaje': ':.1f'}
)
fig1.update_traces(textposition='none')
fig1.show()
fig1.write_html('Resources/emisiones_por_contaminante.html')


df2 = df.groupby(['Entidad', 'Tipo_de_Fuente'])['PM_2_5'].sum().reset_index()
df2_total = df2.groupby('Entidad')['PM_2_5'].sum().reset_index()

df2_total['Entidad'] = df2_total['Entidad'].replace({'Estado de México': 'México'})
df2['Entidad'] = df2['Entidad'].replace({'Estado de México': 'México'})
 
fig2 = px.choropleth(
    df2_total,
    geojson=geojson_mx,
    locations='Entidad',
    featureidkey='properties.name',
    color='PM_2_5',
    color_continuous_scale='Reds',
    title='Emisiones totales de PM₂.₅ por estado',
    labels={'PM_2_5': 'Toneladas de PM₂.₅', 'Entidad': 'Estado'},
    hover_data={'PM_2_5': ':.1f'}
)
fig2.update_geos(fitbounds='locations', visible=False)
fig2.show()
fig2.write_html('Resources/pm25_por_estado.html')
fig2b = px.bar(
    df2.sort_values('PM_2_5', ascending=False),
    x='Entidad',
    y='PM_2_5',
    color='Tipo_de_Fuente',
    barmode='stack',
    title='PM₂.₅ por tipo de fuente en cada estado',
    labels={'PM_2_5': 'Toneladas', 'Tipo_de_Fuente': 'Tipo de fuente'},
    height=500
)
fig2b.update_xaxes(tickangle=45)
fig2b.show()
fig2b.write_html('Resources/pm25_por_fuente_estado.html')
 
estados_clave = ['Ciudad de México', 'Estado de México', 'Jalisco', 'Nuevo León']
df3 = df[df['Entidad'].isin(estados_clave)].groupby(['Entidad', 'Tipo_de_Fuente'])[['NH_3', 'NOx', 'PM_010']].sum().reset_index()
df3_melt = df3.melt(id_vars=['Entidad', 'Tipo_de_Fuente'], var_name='Contaminante', value_name='Toneladas')
 
contaminante_sel = 'NH_3'
fig3 = px.bar(
    df3_melt[df3_melt['Contaminante'] == contaminante_sel],
    x='Entidad',
    y='Toneladas',
    color='Tipo_de_Fuente',
    barmode='group',
    title='Emisiones de NH₃ por tipo de fuente en principales estados',
    labels={'Toneladas': 'Toneladas', 'Tipo_de_Fuente': 'Tipo de fuente'}
)
 

buttons = []
for cont in ['NH_3', 'NOx', 'PM_010']:
    subset = df3_melt[df3_melt['Contaminante'] == cont]
    fuentes = subset['Tipo_de_Fuente'].unique()
    buttons.append(dict(
        label=cont,
        method='update',
        args=[
            {'y': [subset[subset['Tipo_de_Fuente'] == f]['Toneladas'].values for f in fuentes]},
            {'title': f'Emisiones de {cont} por tipo de fuente en principales estados'}
        ]
    ))
 
fig3.update_layout(
    updatemenus=[dict(
        type='buttons',
        direction='right',
        x=0.0, y=1.15,
        buttons=buttons
    )]
)
fig3.show()
fig3.write_html('Resources/estados_clave_fuente.html')