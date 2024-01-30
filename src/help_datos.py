import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text, Integer
import re
import warnings
from unidecode import unidecode

warnings.filterwarnings("ignore")

''' Este archivo incluye estas funciones:

    Mapear nombre de equipos.

    Crear DataFrame: 
    datos: seran los extraidos
    columnas: declaradas por nosotros segun la pagina escrapeada
    
    parametro por defecto: equipo
    parametro2: jugadores
    parametro3: estadistica equipo
    parametro4: clasificacion
    parametro5: estadistica_libero
    parametro6: estadistica_colocador
    parametro7: estadistica_central
    parametro8: estadistica_opuesto
    parametro9: estadistica_receptor

    '''

def mapear_nombres(equipo):
    mapeo = {
        'Arenal Emevé': 'Arenal Emevé',
        'Arenal Emevé ': 'Arenal Emevé',
        'Barça Voleibol': 'Barça Voleibol',
        'Barcelona': 'Barça Voleibol',
        'Feníe Energía Mallorca Volei Palma': 'Voley Palma',
        'Urbia Uenergia Voley Palma':'Voley Palma',
        'Voley Palma' : 'Voley Palma',
        'Urbia Voley Palma':'Voley Palma',
        'Club Vóley Palma':'Voley Palma',
        'Conectabalear CV Manacor': 'Manacor',
        ' Conectabalear CV Manacor': 'Manacor',
        'Conectabalear CV Manacor ': 'Manacor',
        'Manacor': 'Manacor',
        'CV Guaguas': 'Guaguas',
        'Guaguas': 'Guaguas',
        'Léleman VB Valencia': 'Conqueridor Valencia',
        'Valencia': 'Conqueridor Valencia',
        'UPV Leleman Conqueridor':'Conqueridor Valencia',
        'Léleman Conqueridor Valencia':'Conqueridor Valencia',
        'Conqueridor Valencia':'Conqueridor Valencia',
        'Melilla Sport Capital': 'CV Melilla',
        'CV Melilla': 'CV Melilla',
        'Club Voleibol Teruel': 'CV Teruel',
        'CV Teruel': 'CV Teruel',
        'Pamesa Teruel Voleibol':'CV Teruel',
        'Rio Duero Soria': 'Rio Duero Soria',
        'Grupo Herce Soria':'Rio Duero Soria',
        'Rotogal Boiro': 'Rotogal Boiro',
        'Rotogal Boiro ': 'Rotogal Boiro',
        'Boiro': 'Rotogal Boiro',
        'Unicaja Costa de Almeria': 'Unicaja Almería',
        'Unicaja Costa de Almería': 'Unicaja Almería',
        'Unicaja Almería': 'Unicaja Almería',
        'Voley Textil Santanderina': 'Voley Textil Santanderina',
        'Textil Santanderina': 'Voley Textil Santanderina',
        'UD Ibiza Ushuaïa Volley' : 'Ibiza Voley',
        'Ushuaïa Ibiza Voley' : 'Ibiza Voley',
        'Ibiza Voley': 'Ibiza Voley',
        'UD Ibiza Ushuaia Volley':'Ibiza Voley',
        'Intasa San Sadurniño' : 'Intasa',
        'San Sadurnino' : 'Intasa',
        'Grau':'Grau',
        'UBE L´Illa Grau':'Grau',
       "UBE L'Illa Grau" : 'Grau',
        'Almoradí':'Voleibol Almoradí',
        'Voleibol Almoradí':'Voleibol Almoradí',
        'Vecindario ACE GC':'Vecindario Las Palmas',
        'Vecindario ACE GC ':'Vecindario Las Palmas',
        ' Vecindario ACE GC':'Vecindario Las Palmas',
        'Vecindario':'Vecindario Las Palmas',
        'Gámiz Padilla Aaron':'Gámiz Padilla Aharon',
        'Cisneros Alter':'Cisneros Alter',
        'CV San Roque':'CV San Roque',
        'San Roque - Batán':'CV San Roque',
        'Volei Villena Petrer':'CV Villena Petrer',
        'Santo Domingo VB Petrer':'CV Villena Petrer',



    }

    equipo['Equipo'] = equipo['Equipo'].map(mapeo)

    return equipo



def crear_df(datos,columna ,parametro):
    if parametro == 'equipo':
        filas = [i for i in datos[::3]]

        df = pd.DataFrame(filas, columns=columna)
        print('DataFrame creado!')
        return df

    elif parametro == 'jugadores':
        filas_organizadas = []
        for equipo in datos:
            datos_filas = equipo[7:]
            filas_equipo = [datos_filas[i:i + len(columna)] for i in range(0, len(datos_filas), len(columna))]
            filas_organizadas.extend(filas_equipo)
        jugadores = pd.DataFrame(filas_organizadas, columns=columna)
        return jugadores

    elif parametro =='estadistica':
        trozos = [datos[i:i+27] for i in range(2, len(datos), 27)]
        estadistica = pd.DataFrame(trozos, columns=columna)
        convertir = estadistica.columns.difference(['Equipo'])
        columns_to_convert = ['Efic_Ataque', 'Excelente_Ataque', 'Efic_Recepcion', 'Excelente_Recepcion']
        estadistica[columns_to_convert] = estadistica[columns_to_convert].replace('%', '', regex=True)
        estadistica[convertir] = estadistica[convertir].applymap(lambda x: int(x) if str(x).isdigit() else x)
        columns_to_convert = ['Efic_Ataque', 'Excelente_Ataque', 'Efic_Recepcion', 'Excelente_Recepcion', 'Puntos_por_set_Saque', 'Efic_Saque','Puntos_Set_Bloqueo']
        estadistica[columns_to_convert] = estadistica[columns_to_convert].replace({'%': '', ',': '.'}, regex=True).astype(float)
        return estadistica
    
    elif parametro == 'clasificacion':
        rows = [datos[i:i+13] for i in range(0, len(datos), 13)] # algunas veces es 12 el ultimo numero.
        clasificacion = pd.DataFrame(rows, columns=columna)
        return clasificacion
        

    elif parametro == 'estadistica_libero':
        datos = [datos[i:i+13] for i in range(3, len(datos), 13)]
        libero = pd.DataFrame(datos, columns=columna)
        return libero
    
    elif parametro == 'estadistica_receptor':
        datos = [datos[i:i+18] for i in range(3, len(datos), 18)]
        receptor = pd.DataFrame(datos, columns=columna)
        return receptor
    
    elif parametro == 'estadistica_opuesto':
        datos = [datos[i:i+18] for i in range(3, len(datos), 18)]
        opuesto = pd.DataFrame(datos, columns=columna)
        return opuesto
    
    elif parametro == 'estadistica_central':
        datos = [datos[i:i+18] for i in range(3, len(datos), 18)]
        central = pd.DataFrame(datos, columns=columna)
        return central
    
    elif parametro == 'estadistica_colocador':
        datos = [datos[i:i+13] for i in range(3, len(datos), 13)]
        colocador = pd.DataFrame(datos, columns=columna)
        return colocador
    
    else:
        None

def normalizar(ruta):
    df = pd.read_csv(ruta)
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].apply(lambda x: unidecode(str(x), 'utf-8') if pd.notnull(x) else x)
    df.columns = [unidecode(col, 'utf-8') for col in df.columns]
    return df


def normalizar_df(df):
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].apply(lambda x: unidecode(str(x), 'utf-8') if pd.notnull(x) else x)
    df.columns = [unidecode(col, 'utf-8') for col in df.columns]
    return df