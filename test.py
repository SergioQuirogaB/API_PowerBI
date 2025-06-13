import pyodbc

try:
    conn = pyodbc.connect("""
        DRIVER={ODBC Driver 17 for SQL Server};
        SERVER=konbpp.database.windows.net;
        DATABASE=PowerBi-Costo;
        UID=koncilia;
        PWD=skit$2006
    """)
    print("✅ Conexión exitosa")
    conn.close()
except Exception as e:
    print("❌ Error de conexión:")
    print(e)
