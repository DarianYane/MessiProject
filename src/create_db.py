import mysql.connector
from mysql.connector import errorcode

#Agregando una conexion a una base de datos SQL
def connect_sql():

    try:
        _mydb = mysql.connector.connect(
            user="root",
            password="messiGOAT",
            #host='127.0.0.1',
            #port='4810'
            host='db',
            port='3306'
        )
        _cursor = _mydb.cursor()
        return _mydb, _cursor
    
    except mysql.connector.Error as err:
        raise

def crear_base_de_datos():
    # Conexión a la base de datos (crea un archivo si no existe)
    
    _mydb, _cursor = connect_sql()

    # Crear base de datos (si no existe)
    _cursor.execute('''CREATE DATABASE IF NOT EXISTS messi;''')
    _mydb.commit()


    # Crear tabla (si no existe)
    _cursor.execute('''CREATE TABLE IF NOT EXISTS messi.goals (
                    N_of_Goal INT,
                    Date DATE,
                    Home_team TEXT,
                    Away_team TEXT,
                    Minute varchar(20),
                    What TEXT,
                    How TEXT,
                    Jersey INT,
                    Competition_abb TEXT,
                    Competition_name TEXT,
                    Goals_H INT,
                    Goals_A INT,
                    Result TEXT,
                    Leo_age INT,
                    Leo_team TEXT,
                    Scored_team TEXT,
                    Home_or_Away varchar(10),
                    Leo_result varchar(10),
                    Partial_Score_H INT,
                    Partial_Score_A INT,
                    Minute_adjusted INT,
                    Goal_time_period varchar(20)
                    );''')

    # Guardar cambios y cerrar conexión
    _mydb.commit()
    _cursor.close()
    _mydb.close()