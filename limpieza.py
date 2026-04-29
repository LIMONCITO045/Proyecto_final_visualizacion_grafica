import pandas as pd

df_original = pd.read_csv('d3_aire01_49_1.csv')

print(df_original.isnull().sum())
print(f"\nDuplicados: {df_original.duplicated().sum()}")
print(df_original.head())


df = df_original.copy()

# PROBLEMA 1: Columna 'Entidad_federativa' redundante con 'Entidad'
# 'Entidad' tiene el nombre completo correcto 
# 'Entidad_federativa' tiene nombres inconsistentes
# Se elimina 'Entidad_federativa'
df = df.drop(columns=['Entidad_federativa'])

# PROBLEMA 2: Orden de columnas — 'Entidad' quedó al final
# Se reordena para que quede primero
cols = ['Entidad', 'Municipio', 'Tipo_de_Fuente',
        'SO_2', 'CO', 'NOx', 'COV', 'PM_010', 'PM_2_5', 'NH_3']
df = df[cols]

# PROBLEMA 3: Espacios extra en columnas de texto
# Strip en columnas categóricas
for col in ['Entidad', 'Municipio', 'Tipo_de_Fuente']:
    df[col] = df[col].str.strip()

# PROBLEMA 4: 2,453 valores NaN en columnas numéricas
# Todos corresponden exactamente a 'Fuentes naturales',
# que no emite SO_2, CO, PM_010, PM_2_5 ni NH_3 medibles.
# Se reemplazan con 0.0 (semánticamente correcto)
num_cols = ['SO_2', 'CO', 'NOx', 'COV', 'PM_010', 'PM_2_5', 'NH_3']
filas_nulas_antes = df[num_cols].isnull().sum().sum()
df[num_cols] = df[num_cols].fillna(0.0)


print(df.head())

df.to_csv('d3_aire01_49_1_limpio.csv', index=False)

