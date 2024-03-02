import pandas as pd

# Para actualizar el archivo CSV diariamente se utiliza el módulo schedule de Python para programar la ejecución del script cada día.
import schedule
import time

from datetime import datetime

# Cumpleaños de Leo
leo_birthday = datetime(1987, 6, 24)

# Término de contratos
barcelona_exit = datetime(2021, 5, 30)
psg_exit = datetime(2023, 6, 30)


# Definir df como una variable global
df = None

def update_csv():
    global df  # Definir df como una variable global
    # Obtenemos la tabla de ejemplo de una página web
    url = "http://messi.starplayerstats.com/en/goals/0/0/all/0/0/0/t/all/all/0/0/1"
    # Para obtener la primera tabla
    goals_table = pd.read_html(url)[0]

    # Estableceremos el Dataframe donde guardaremos la tabla
    df = pd.DataFrame(goals_table)

    # Elimino la última columna (son las flechas que me llevan al detalle del partido)
    df = df.drop(columns=["Unnamed: 11"])

    # Renombro las columnas
    df = df.set_axis(
        [
            "N_of_Goal",
            "Date",
            "Competition",
            "Home_team",
            "Result",
            "Away_team",
            "Minute",
            "Partial_Score",
            "What",
            "How",
            "Jersey",
        ],
        axis=1,
    )
    df["N_of_Goal"] = df["N_of_Goal"].astype("int")
    df["Jersey"] = df["Jersey"].astype("int")
    # df["Date"] = df["Date"].astype("datetime64[us]")
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")


    # Dividir "Competition" en 2 columnas: una para la abreviación, y otra para el nombre de la competición. Esto me permite identificar los amistosos por su sigla, y todo lo demás como partidos oficiales
    def split_competition(val):
        return val[:3], val[4:]

    # Aplicar la función personalizada a la columna "Competition"
    df[["Competition_abb", "Competition_name"]] = (
        df["Competition"].apply(split_competition).apply(pd.Series)
    )
    # Eliminar la columna "column_name"
    df = df.drop("Competition", axis=1)


    # Dividir los goles del resultado en 2 columnas
    df[["Goals_H", "Goals_A"]] = df["Result"].str.split("-", expand=True)
    # Convertir los "result" en int
    df["Goals_H"] = df["Goals_H"].astype("int")
    df["Goals_A"] = df["Goals_A"].astype("int")
    # Eliminar la columna "column_name"
    df = df.drop("Result", axis=1)

    # Crear una nueva columna "Result" que contenga los valores "Home", "Away" o "Draw" dependiendo de los valores de "Goals_H" y "Goals_A"
    df["Result"] = df.apply(
        lambda number: "Home"
        if number["Goals_H"] > number["Goals_A"]
        else "Away"
        if number["Goals_H"] < number["Goals_A"]
        else "Draw",
        axis=1,
    )


    # Calcular la edad de Leo en cada gol
    from dateutil.relativedelta import relativedelta

    df["Leo_age"] = df["Date"].apply(
        lambda goal: relativedelta(goal.date(), leo_birthday.date()).years
    )


    # Identificar en qué equipo estaba jugando Leo cuando marcó el gol
    df["Leo_team"] = df.apply(
        lambda goal: "Argentina"
        if goal["Home_team"] == "Argentina"
        else "Argentina"
        if goal["Away_team"] == "Argentina"
        else "FC Barcelona"
        if goal["Date"] < barcelona_exit
        else "Paris Saint-Germain"
        if goal["Date"] < psg_exit
        else "Inter Miami CF",
        axis=1,
    )


    # Identificar a qué equipo le anotó el gol
    df["Scored_team"] = df.apply(
        lambda goal: goal["Away_team"]
        if goal["Home_team"] == goal["Leo_team"]
        else goal["Home_team"],
        axis=1,
    )


    # Identificar si estaba jugando de local o visitante
    df["Home_or_Away"] = df.apply(
        lambda goal: "Home" if goal["Home_team"] == goal["Leo_team"] else "Away", axis=1
    )


    # Identificar si Leo ganó, empató o perdió
    df["Leo_result"] = df.apply(
        lambda goal: "Tied"
        if goal["Result"] == "Draw"
        else "Won"
        if goal["Result"] == goal["Home_or_Away"]
        else "Lost",
        axis=1,
    )


    # Dividir los goles del resultado parcial en 2 columnas
    df[["Partial_Score_H", "Partial_Score_A"]] = df["Partial_Score"].str.split(
        "-", expand=True
    )
    # Convertir los "result" en int
    df["Partial_Score_H"] = df["Partial_Score_H"].astype("int")
    df["Partial_Score_A"] = df["Partial_Score_A"].astype("int")
    # Eliminar la columna "column_name"
    df = df.drop("Partial_Score", axis=1)


    # Agregar una nueva columna "Minute_adjusted" al DataFrame df
    df['Minute_adjusted'] = df['Minute']

    # Definir una función para ajustar los minutos en caso de tiempo adicional
    def adjust_minute(minute):
        if '+' in minute:
            # Dividir el tiempo adicional en dos partes y sumarlas
            parts = minute.split('+')
            adjusted_minute = sum(int(part) for part in parts)
            return adjusted_minute
        else:
            # Mantener el mismo valor si no hay tiempo adicional
            return int(minute)

    # Aplicar la función adjust_minute a la columna "Minute_adjusted"
    df['Minute_adjusted'] = df['Minute_adjusted'].apply(adjust_minute)

    # Convertir la columna "Goal_time_period" al tipo de datos texto
    df['Minute_adjusted'] = df['Minute_adjusted'].astype('int')


    # Agregar una nueva columna "Goal_time_period" al DataFrame df
    df['Goal_time_period'] = df['Minute']

    # Definir una función para determinar el período de tiempo del gol
    def determine_time_period(minute):
        if '+' in minute:
            return 'Additional time'
        elif int(minute) <= 45:
            return 'First half'
        elif int(minute) <= 90:
            return 'Second half'
        else:
            return 'Additional time'

    # Aplicar la función determine_time_period a la columna "Goal_time_period"
    df['Goal_time_period'] = df['Goal_time_period'].apply(determine_time_period)

    # Convertir la columna "Goal_time_period" al tipo de datos texto
    df['Goal_time_period'] = df['Goal_time_period'].astype('str')


    # Guardar el DataFrame en un archivo CSV utilizando la función df.to_csv(), y en un archivo XLSX utilizando la función df.to_excel().
    df.to_csv("messi_goals.csv", index=False)
    df.to_excel("messi_goals.xlsx", sheet_name="Goals")
    return df


# Programar la ejecución del script cada día a las 9:00 AM
""" schedule.every().day.at("11:00").do(update_csv)

while True:
    schedule.run_pending()
    time.sleep(1) """
""" Este código programará la ejecución del script update_csv() cada día a las 11:00 AM y guardará la tabla actualizada en el archivo CSV "tabla_messi.csv". Para que el script se siga ejecutando en segundo plano, se utiliza un ciclo while junto con la función schedule.run_pending() y time.sleep(1). """

# Actualizar df
df = update_csv()

#######################################################################################################################################

'''
Código para volcar la inscriptformación anterior en una base de datos
'''

# Llamar al script create_db.py para crear la db si no existe
# Módulos para actualizar la base de datos
import sqlite3
import os
import subprocess

def verificar_y_ejecutar_creacion_db():
    # Verificar si el archivo messi_goals.db ya existe
    if not os.path.exists('messi_goals.db'):
        # Si no existe, llamar al script create_db.py
        subprocess.run(['python', 'create_db.py'])
        print("Se ha creado la base de datos 'messi_goals.db'.")
    else:
        print("La base de datos 'messi_goals.db' ya existe.")

verificar_y_ejecutar_creacion_db()

# Actualizar la base de datos SQLite messi_goals.db con la información que se encuentra en el DataFrame df
def actualizar_base_de_datos(df, nombre_archivo):
    # Conexión a la base de datos
    conexion = sqlite3.connect(nombre_archivo)
    cursor = conexion.cursor()

    try:
        # Truncar la tabla antes de insertar nuevos datos
        cursor.execute('''DELETE FROM goals''')
        conexion.commit()
        print("Se han eliminado todas las filas existentes en la tabla 'goals'.")
    except Exception as e:
        # Si hay algún error, imprimirlo
        print(f"Error al truncar la tabla 'goals': {e}")
        conexion.rollback()
        conexion.close()
        return

    try:
        # Insertar datos en la tabla
        for index, fila in df.iterrows():
            # Convertir las columnas de tipo Timestamp a formato de cadena de texto en formato ISO
            fila['Date'] = fila['Date'].isoformat()

            # Insertar datos
            cursor.execute('''
                INSERT INTO goals (N_of_Goal, Date, Home_team, Away_team, Minute, What, How, Jersey, Competition_abb, Competition_name,  
                Goals_H, Goals_A, Result, Leo_age, Leo_team, 
                Scored_team, Home_or_Away, Leo_result, Partial_Score_H, Partial_Score_A, Minute_adjusted, Goal_time_period) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', tuple(fila))
        
        # Guardar cambios y cerrar conexión
        conexion.commit()
        print("Se han insertado los nuevos datos en la tabla 'goals'.")
    except Exception as e:
        # Si hay algún error durante la inserción, imprimirlo
        print(f"Error al insertar nuevos datos en la tabla 'goals': {e}")
        conexion.rollback()
    finally:
        conexion.close()

# Llamar a la función para actualizar la base de datos
nombre_archivo = 'messi_goals.db'
actualizar_base_de_datos(df, nombre_archivo)
print(f'Se han actualizado los datos en la base de datos "{nombre_archivo}" correctamente.')
