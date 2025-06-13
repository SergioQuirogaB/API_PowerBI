import os
import pyodbc
from azure.identity import DefaultAzureCredential
from azure.mgmt.consumption import ConsumptionManagementClient
from dotenv import load_dotenv

# Cargar variables desde archivo .env
load_dotenv()

# Credenciales Azure
subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")

# Conexión SQL Server
server = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

connection_string = """
DRIVER={ODBC Driver 17 for SQL Server};
SERVER=konbpp.database.windows.net;
DATABASE=PowerBi-Costo;
UID=koncilia;
PWD=skit$2006
"""

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Azure Auth
credential = DefaultAzureCredential()
client = ConsumptionManagementClient(credential, subscription_id)

# Obtener datos de consumo
usage = client.usage_details.list_expand(
    scope=f"/subscriptions/{subscription_id}",
    expand="properties/meterDetails"
)

# Insertar datos en SQL Server
for item in usage:
    cursor.execute("""
        INSERT INTO consumos_azure (
            subscription_id, start_date, end_date,
            usage_quantity, meter_name, category, unit, currency
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        subscription_id,
        item.usage_start.strftime('%Y-%m-%d'),
        item.usage_end.strftime('%Y-%m-%d'),
        item.usage_quantity,
        item.meter_details.meter_name if item.meter_details else None,
        item.meter_details.meter_category if item.meter_details else None,
        item.unit,
        item.currency
    ))

conn.commit()
cursor.close()
conn.close()
print("✅ Datos guardados exitosamente.")