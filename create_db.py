import sqlite3

def crear_base_de_datos(nombre_archivo):
    # Conexión a la base de datos (crea un archivo si no existe)
    conexion = sqlite3.connect(nombre_archivo)
    cursor = conexion.cursor()

    # Crear tabla (si no existe)
    cursor.execute('''CREATE TABLE IF NOT EXISTS goals (
                    N_of_Goal INTEGER,
                    Date DATE,
                    Home_team TEXT,
                    Away_team TEXT,
                    Minute INTEGER,
                    What TEXT,
                    How TEXT,
                    Jersey INTEGER,
                    Competition_abb TEXT,
                    Competition_name TEXT,
                    Goals_H INTEGER,
                    Goals_A INTEGER,
                    Result TEXT,
                    Leo_age INTEGER,
                    Leo_team TEXT,
                    Scored_team TEXT,
                    Home_or_Away TEXT,
                    Leo_result TEXT,
                    Partial_Score_H INTEGER,
                    Partial_Score_A INTEGER
                    );''')

    # Guardar cambios y cerrar conexión
    conexion.commit()
    conexion.close()

# Llamar a la función para crear la base de datos
nombre_archivo = 'messi_goals.db'
crear_base_de_datos(nombre_archivo)
print(f'Se ha creado la base de datos "{nombre_archivo}" correctamente.')
