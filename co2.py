import pandas as pd

def crear_co2(nombre_origen_co2, archivo_co2):
    """
    Esta función selecciona los datos de interés del archivo csv que contiene los datos de emisiones de CO2 (descargado de la página de Red Eléctrica como los datos de un año en intervalos horarios) y los guarda en un nuevo archivo csv.

    Se ha diseñado teniendo en cuenta la existencia de las siguientes columnas:
        'id'
        'name'
        'geoid'
        'geoname'
        'value' (en toneladas de CO2 por MWh)
        'datetime' (ej. '2023-01-01T00:00:00+01:00')

    Parámetros:
        nombre_origen_co2 (str): Nombre del archivo (con extensión) en el que se encuentran los datos de emisiones de CO2 (ej. "CO2 2023.csv").
        archivo_co2 (str): Nombre del archivo csv de salida donde se guardarán los datos filtrados (ej. "CO2_2023_tratado.csv").
    
    Retorna:
        co2_filtrado(dataframe): Dataframe con los datos de interés para calcular las emisiones de CO2.
    """
    try:
        co2 = pd.read_csv(nombre_origen_co2, sep=';', low_memory=False)
        
        # Verificar si las columnas esperadas están en el DataFrame
        columnas_esperadas = {"id", "name", "geoid", "geoname", "value", "datetime"}
        if not columnas_esperadas.issubset(co2.columns):
            raise ValueError("El archivo CSV no contiene las columnas esperadas.")

        co2['fecha_utc_co2'] = pd.to_datetime(co2['datetime'], errors='coerce', utc=True)

        # Eliminar las columnas innecesarias
        co2.drop(columns=["id", "name", "geoid", "geoname"], inplace=True)

        # Reordenar las columnas para que las columnas de fechas sean las primeras
        co2_filtrado = co2[['fecha_utc_co2', 'value']].copy()

        # Cambiar el nombre de la columna 'value' a 'CO2 Kg/kWh', ya que es el mismo valor que toneladas de CO2 por MWh, pero más conveniente para el análisis
        co2_filtrado.rename(columns={'value': 'CO2 Kg/kWh'}, inplace=True)

        # Guardar el DataFrame filtrado en un nuevo archivo CSV
        co2_filtrado.to_csv(archivo_co2, index=False)

        return co2_filtrado
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        return None