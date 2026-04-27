import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
plt.style.use('ggplot')
df = pd.read_csv('d3_aire01_49_1_limpio.csv')
df.info()

estados = df['Entidad'].unique()
municipios = df['Municipio'].unique()
fuentes = df['Tipo_de_Fuente'].unique()
df_emisiones_estado = df.groupby(['Entidad'])[['SO_2','CO','NOx','COV','PM_010','PM_2_5','NH_3']].sum()
print(df_emisiones_estado)

media_emisiones_estado = df_emisiones_estado.mean()
print(media_emisiones_estado)

colores = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink']
media_emisiones_estado.plot(kind= 'barh' , color = colores, grid = True)
plt.xlabel('Emisiones')
plt.ylabel('Emisiones')
plt.title('Media de Emisiones')
#Grafica de barras para comparar las emisiones por estado
df_emisiones_estado.plot(kind= 'bar')
plt.show()