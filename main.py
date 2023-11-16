import requests
import pandas as pd
import json
from datetime import datetime
import pyodbc
import time


def extraccion_fixture(league,season,team):
    """
        Funcion que extrae el fixture de un determinado equipo.
        Entrada: league(el ID de la liga) season(el ID de la temporada, por ejemplo 2023) team(el ID del equipo)
        Salida: data(los datos en formato json) y un archivo JSON con los datos.
    """
    with open("api_key.json") as f:
        api_key = json.load(f)       
        key = api_key["key"]

    url = f"https://v3.football.api-sports.io/fixtures?league={league}&season={season}&team={team}"
    headers = {"x-apisports-key": key}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()      
    else:
        print(response.status_code, response.content)
    
    with open("data/raw_data/fixture.json", 'w') as archivo:
            json.dump(data, archivo)
    return data        

def extraccion_estadisticas(data_fixture, team):
    """
        Funcion que extrae las estadisticas de cada partido.
        Entrada: data_fixture(json que contiene todo el fixture), team(el ID del equipo)
        Salida: Se almacenan los datos crudos en un archivo JSON por cada fecha obtenida en el fixture
    """
    
    lista_ids = [data_fixture['response'][fecha]['fixture']['id'] for fecha in range(len(data_fixture['response']))]
    
    with open("api_key.json") as f:
        api_key = json.load(f)       
        key = api_key["key"]
    
    for id in lista_ids:
        url = f"https://v3.football.api-sports.io/fixtures/statistics?fixture={id}&team={team}"
        headers = {"x-apisports-key": key}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:            
            data = response.json()    
        else:
            print(response.status_code, response.content)     
        
        with open(f"data/raw_data/{id}_estadisticas.json", 'w') as archivo:
            json.dump(data, archivo)
        
        time.sleep(10)
  
def transformacion(team):
    """
        Funcion que genera la estructura del DF y limpieza de datos
        Entrada: team(el ID del equipo)
        Salida: Se almacenan los datos limpios en un archivo CSV y se retorna el DF.
    """
    # ACCEDO A LOS ARCHIVOS FIXTURE Y ESTADISTICAS PARA CREAR UN DICCIONARIO DE DATOS 
    with open("data/raw_data/fixture.json", 'r') as file_fix:
        fixture = json.load(file_fix)
    
    dic = {'id_partido':[],'id_liga':[],'id_local':[],'id_visitante':[],'id_tiempo':[],'fecha_partido':[],'gol_local':[],'gol_visitante':[],'remates_arco':[],
       'remates_fuera':[],'remates_total':[],'remates_bloqueados':[],'fouls':[],'corners':[],'offsides':[],
       'posesion':[],'amarillas':[],'rojas':[],'atajadas':[],'total_pases':[],'pases_precisos':[],'porcentaje_pases':[]}
    
    nro_fechas = len(fixture['response'])

    for partido in range(nro_fechas):        

        status = fixture['response'][partido]['fixture']['status']['short']

        if status == "FT":
                        
            id_partido = fixture['response'][partido]['fixture']['id']
            fecha_partido = fixture['response'][partido]['fixture']['date']
            id_liga = fixture['response'][partido]['league']['id']
            id_local = fixture['response'][partido]['teams']['home']['id']
            id_visitante = fixture['response'][partido]['teams']['away']['id']
            gol_local = fixture['response'][partido]['goals']['home']
            gol_visitante = fixture['response'][partido]['goals']['away']          

            dic['id_partido'].append(id_partido)            
            dic['id_liga'].append(id_liga)
            dic['id_local'].append(id_local)
            dic['id_visitante'].append(id_visitante)            
            dic['id_tiempo'].append(1)
            dic['fecha_partido'].append(fecha_partido)
            dic['gol_local'].append(gol_local)
            dic['gol_visitante'].append(gol_visitante)
        
            with open(f"data/raw_data/{id_partido}_estadisticas.json", 'r') as file_est:
                estadisticas = json.load(file_est)

            dic['remates_arco'].append(estadisticas['response'][0]['statistics'][0]['value'])
            dic['remates_fuera'].append(estadisticas['response'][0]['statistics'][1]['value'])
            dic['remates_total'].append(estadisticas['response'][0]['statistics'][2]['value'])
            dic['remates_bloqueados'].append(estadisticas['response'][0]['statistics'][3]['value'])
            dic['fouls'].append(estadisticas['response'][0]['statistics'][6]['value'])
            dic['corners'].append(estadisticas['response'][0]['statistics'][7]['value'])
            dic['offsides'].append(estadisticas['response'][0]['statistics'][8]['value'])
            dic['posesion'].append(estadisticas['response'][0]['statistics'][9]['value'])
            dic['amarillas'].append(estadisticas['response'][0]['statistics'][10]['value'])
            dic['rojas'].append(estadisticas['response'][0]['statistics'][11]['value'])
            dic['atajadas'].append(estadisticas['response'][0]['statistics'][12]['value'])
            dic['total_pases'].append(estadisticas['response'][0]['statistics'][13]['value'])
            dic['pases_precisos'].append(estadisticas['response'][0]['statistics'][14]['value'])
            dic['porcentaje_pases'].append(estadisticas['response'][0]['statistics'][15]['value'])

    # CREO UN DATAFRAME CON EL DICCIONARIO OBTENIDO
    df = pd.DataFrame(dic)

    # ORDENO EL DF POR FECHA DE PARTIDO
    df['fecha_partido'] = pd.to_datetime(df['fecha_partido'])
    df['fecha_partido'] = df['fecha_partido'].dt.strftime('%Y-%m-%d')
    df = df.sort_values(by='fecha_partido', ascending=True)
    
    # MODIFICAR VALORES NULOS DEL TIPO NaN A VALOR CERO
    df = df.fillna(0)
    
    # ELIMNAR EL SIMBOLO PORCENTAJE Y DEJAR SOLO EL NUMERO
    df['posesion'] = df['posesion'].str.replace('%', '')
    df['porcentaje_pases'] = df['porcentaje_pases'].str.replace('%', '')
    
    # ALMACENAR LOS DATOS LIMPIOS DEL DF EN UN ARCHIVO CSV
    df.to_csv('data/clean_data/data_final.csv', index=False)      
    return df

def carga(df):
    """
        Funcion que carga los datos (DF) al Datawarehouse (SQL SERVER)
        Entrada: df (dataframe)
        Salida: Almacena los datos en el Datawarehouse, no retorna valores.
    """
       
    server = "LAPTOP-PCS5TK5G"
    database = "FUTBOL_DW"
    #username = "PGB"
    #password = "PGB"
    driver = "ODBC Driver 17 for SQL Server"
    
    # String de conexion con SQL Server
    connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes"
    #connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};pwd={password}"
           
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        connection.autocommit = True
        
        try:        
            for index, row in df.iterrows():

                query = f"""INSERT INTO fact_estadisticas (id_partido,id_liga,id_local,id_visitante,
                    id_tiempo,fecha_partido,gol_local,gol_visitante,remates_arco,remates_fuera,
                    remates_total,remates_bloqueados,fouls,corners,offsides,posesion,amarillas,
                    rojas,atajadas,total_pases,pases_precisos,porcentaje_pases)
                    VALUES (
                    {row['id_partido']},{row['id_liga']},{row['id_local']},{row['id_visitante']},
                    {row['id_tiempo']},'{row['fecha_partido']}',{row['gol_local']},{row['gol_visitante']},
                    {row['remates_arco']},{row['remates_fuera']},{row['remates_total']},
                    {row['remates_bloqueados']},{row['fouls']},{row['corners']},{row['offsides']},
                    {row['posesion']},{row['amarillas']},{row['rojas']},{row['atajadas']},{row['total_pases']},
                    {row['pases_precisos']},{row['porcentaje_pases']}
                );"""
                          
                cursor.execute(query)                

        except Exception as e:
            print(f"Error al cargar los datos en la tabla: {e}")           
        
    except pyodbc.Error as e:
        print("Error de conexion:", e)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    
# INICIO

# PARAMETROS
league = 1032
season = 2023
team = 451

# EJECUCION
print("Iniciando la extracción de los datos correspodiente al fixture...")
data_fixture = extraccion_fixture(league,season,team)
print("Iniciando la extracción de los datos correspodiente a las estadisticas de cada fecha...")
data_estadisticas = extraccion_estadisticas(data_fixture,team)
print("Datos crudos extraidos y almacenados!")

print("************************************************")

print("Iniciando la transformacion de los datos...")
clean_data = transformacion(team)
print("Datos limpios!")

print("************************************************")

print("Iniciando la carga de datos al Data Warehouse...")
carga(clean_data)
print("Datos almacenados en Data Warehouse!")