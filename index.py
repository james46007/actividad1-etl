# pip install pandas
import pandas as pd

df = pd.read_csv('mdi_homicidiosintencionales_pm_2023_enero_agosto.csv', sep=';', encoding='latin1')

print(df.info())

# Obtener las columnas de tipo objeto
columns_object = df.select_dtypes(include=['object']).columns.tolist()
# Hacer un trim en las columnas de texto
for column in columns_object:
    df[column] = df[column].str.strip()

# Imprimir los valores únicos de todas las columnas
for column in df.columns:
    unique_values = df[column].unique()
    print(f'Valores únicos en la columna {column}: {unique_values}')

# Identificar las provincias, Remplazar valores que estan mal
df.loc[df.Provincia == "LOS RIOS", "Provincia"] = "PROVINCIA DE LOS RÍOS"
df.loc[df.Provincia == "BOLIVAR", "Provincia"] = "PROVINCIA DE BOLÍVAR"

# Convertir el campo fecha
df['Fecha Infracción'] = pd.to_datetime(df['Fecha Infracción'], format='%d/%m/%Y', errors='ignore')
df['Fecha Infracción'] = df['Fecha Infracción'].dt.date

# Libreria para instalar
# pip install SQLAlchemy
# pip install pymysql
from sqlalchemy import create_engine

# Credenciales para la conexión de la base de datos
hostname = "209.145.61.41"
dbname = "actividad1"
uname = "usr_maintainer"
pwd = "Tc2;1EE{DBE^oN"

# Cree el motor SQLAlchemy para conectarse a la base de datos MySQL
engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                       .format(host=hostname, db=dbname, user=uname, pw=pwd))

# Suponiendo que desea excluir la columna denominada 'columna_no_deseada'
columns_to_exclude = ['Cod_prov', 'cod_cantón', 'Med. Edad']
columns_to_keep = [column for column in df.columns if column not in columns_to_exclude]

# Cree un nuevo DataFrame sin la columna no deseada
filtered_df = df[columns_to_keep]

# Convertir marco de datos a tabla SQL
filtered_df.to_sql('deber', engine, if_exists='replace', index=False)
