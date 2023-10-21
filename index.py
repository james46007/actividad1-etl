import pandas as pd

df = pd.read_csv('mdi_homicidiosintencionales_pm_2023_enero_agosto.csv', sep=';', encoding='latin1')

print(df.info())

# Obtener las columnas de tipo objeto
columns_object = df.select_dtypes(include=['object']).columns.tolist()
# Hacer un trim en las columnas de texto
for column in columns_object:
    df[column] = df[column].str.strip()

# print(df.sample(10))
# Imprimir los valores únicos de todas las columnas
for column in df.columns:
    unique_values = df[column].unique()
    print(f'Valores únicos en la columna {column}: {unique_values}')

# Identificar las provincias, Remplazar valores que estan mal
df.loc[df.Provincia == "LOS RIOS", "Provincia"] = "PROVINCIA DE LOS RÍOS"
df.loc[df.Provincia == "BOLIVAR", "Provincia"] = "PROVINCIA DE BOLÍVAR"
# print(df["Provincia"].unique())

# Libreria para instalar
# pip install SQLAlchemy
# pip install pymysql
import pandas as pd
from sqlalchemy import create_engine, text

# Credentials to database connection
hostname = "209.145.61.41"
dbname = "actividad1"
uname = "usr_maintainer"
pwd = "Tc2;1EE{DBE^oN"

# Create SQLAlchemy engine to connect to MySQL Database
engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                       .format(host=hostname, db=dbname, user=uname, pw=pwd))

# Assuming you want to exclude the column named 'unwanted_column'
columns_to_exclude = ['Cod_prov', 'cod_cantón', 'Med. Edad']
columns_to_keep = [column for column in df.columns if column not in columns_to_exclude]

# Create a new DataFrame without the unwanted column
filtered_df = df[columns_to_keep]

# Convert dataframe to sql table
filtered_df.to_sql('deber', engine, if_exists='replace', index=False)
