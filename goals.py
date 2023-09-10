import pandas as pd

# Para actualizar el archivo CSV diariamente, puede utilizar el módulo schedule de Python para programar la ejecución del script cada día.
import schedule
import time

from datetime import datetime

# Cumpleaños de Leo
leo_birthday = datetime(1987, 6, 24)

# Término de contratos
barcelona_exit = datetime(2021, 5, 30)
psg_exit = datetime(2023, 6, 30)

""" # Obtenemos la tabla de ejemplo de una página web
url = 'http://messi.starplayerstats.com/en/goals/0/0/all/0/0/0/t/all/all/0/0/1'
# Para obtener la primera tabla
goals_table = pd.read_html(url)[0]

# Estableceremos el Dataframe donde guardaremos la tabla
df = pd.DataFrame(goals_table)

# Elimino la última columna
df = df.drop(columns=['Unnamed: 11'])

# Renombro las columnas
df = df.set_axis(['#_of_Goal', 'Date', 'Competition', 'Home team', 'Result', 'Away', 'Minute', 'Partial_Score', 'What', 'How', 'Jersey'], axis=1)

print(df)
print(df.dtypes)
print(df.info())

#Guarde el DataFrame en un archivo CSV utilizando la función df.to_csv().
df.to_csv("messi_goals.csv", index=False) """


def update_csv():
    # Obtenemos la tabla de ejemplo de una página web
    url = "http://messi.starplayerstats.com/en/goals/0/0/all/0/0/0/t/all/all/0/0/1"
    # Para obtener la primera tabla
    goals_table = pd.read_html(url)[0]

    # Estableceremos el Dataframe donde guardaremos la tabla
    df = pd.DataFrame(goals_table)

    # Elimino la última columna
    df = df.drop(columns=["Unnamed: 11"])

    # Renombro las columnas
    df = df.set_axis(
        [
            "#_of_Goal",
            "Date",
            "Competition",
            "Home team",
            "Result",
            "Away team",
            "Minute",
            "Partial_Score",
            "What",
            "How",
            "Jersey",
        ],
        axis=1,
    )
    df["#_of_Goal"] = df["#_of_Goal"].astype("string")
    df["Jersey"] = df["Jersey"].astype("string")
    # df["Date"] = df["Date"].astype("datetime64[us]")
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")

    # Dividir "Competition" en 2 columnas: una para la abreviación, y otra para el nombre de la competición. Esto me permite identificar los amistosos por su sigle, y todo lo demás como partidos oficiales
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
        if goal["Home team"] == "Argentina"
        else "Argentina"
        if goal["Away team"] == "Argentina"
        else "FC Barcelona"
        if goal["Date"] < barcelona_exit
        else "Paris Saint-Germain"
        if goal["Date"] < psg_exit
        else "Inter Miami CF",
        axis=1,
    )

    # Identificar a qué equipo le anotó el gol
    df["Scored_team"] = df.apply(
        lambda goal: goal["Away team"]
        if goal["Home team"] == goal["Leo_team"]
        else goal["Home team"],
        axis=1,
    )

    # Identificar si estaba jugando de local o visitante
    df["Home/Away"] = df.apply(
        lambda goal: "Home" if goal["Home team"] == goal["Leo_team"] else "Away", axis=1
    )

    # Identificar si Leo ganó, empató o perdió
    df["Leo_result"] = df.apply(
        lambda goal: "Tied"
        if goal["Result"] == "Draw"
        else "Won"
        if goal["Result"] == goal["Home/Away"]
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

    # Guardar el DataFrame en un archivo CSV utilizando la función df.to_csv(), y en un archivo XLSX utilizando la función df.to_excel().
    df.to_csv("messi_goals.csv", index=False)
    df.to_excel("messi_goals.xlsx", sheet_name="Goals")


# Programar la ejecución del script cada día a las 9:00 AM
""" schedule.every().day.at("11:00").do(update_csv)

while True:
    schedule.run_pending()
    time.sleep(1) """
""" Este código programará la ejecución del script update_csv() cada día a las 11:00 AM y guardará la tabla actualizada en el archivo CSV "tabla_messi.csv". Para que el script se siga ejecutando en segundo plano, se utiliza un ciclo while junto con la función schedule.run_pending() y time.sleep(1). """

# como exportar un dataframe de pandas como archivo .xls?

update_csv()

# Desde terminal, ejecutar python goals.py
