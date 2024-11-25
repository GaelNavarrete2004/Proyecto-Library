import mariadb

def conectar():
        try:
            conn = mariadb.connect(
                user="libraryPy",
                password="michoacan",
                host="64.23.180.219",
                port=3306,
                database="biblioteca"
            )
            return conn
        except Exception as e:
            print("Error al conectar con la base de datos:", e)
            return None