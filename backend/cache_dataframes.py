import pandas as pd
from sqlalchemy import create_engine

## datos servidor
server = 'servidorpruebasqlkhorne.database.windows.net'
database = 'sqlkhorne'
username = 'adminsql'
password = 'Termineitor123@'
driver = '{ODBC Driver 18 for SQL Server}'

odbc_params = f'DRIVER={driver};SERVER=tcp:{server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
connection_string = f'mssql+pyodbc:///?odbc_connect={odbc_params}'
engine = create_engine(connection_string)
engine_sqlite = create_engine('sqlite:///database.db', echo=True)

# df1 = pd.read_sql('select * from vendedores', con=engine)

# df1.to_sql('demo', con=engine_sqlite, index=False, if_exists='replace')

# def get_data(query, table_name):
    
    
try:
    df = pd.read_sql('select * from demo', con=engine)
    print('encontrado')
except:
    print('no encontrado')