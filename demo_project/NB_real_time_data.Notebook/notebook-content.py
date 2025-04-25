# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# CELL ********************

%pip install faker

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

%pip install azure.eventhub

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

%pip install azure-identity azure-keyvault-secrets azure-eventhub

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import uuid
import random
import json
import time
import math
from faker import Faker
from azure.eventhub import EventHubProducerClient, EventData
from datetime import datetime
from zoneinfo import ZoneInfo


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from notebookutils import mssparkutils  # Librería de utilidades de Notebook
from trident_token_library_wrapper import PyTridentTokenLibrary  # Token library para Key Vault

# URL de tu Key Vault (usa tu vault 'fabricconn')
vault_url = "https://fabricconn.vault.azure.net/"

# 1. Obtener token de acceso para Key Vault
access_token = mssparkutils.credentials.getToken("keyvault")

# 2. Recuperar secret 'fabricendpoint'
fabricendpoint = PyTridentTokenLibrary.get_secret_with_token(
    vault_url,
    "fabricendpoint",    # nombre de tu secreto fabricendpoint
    access_token
)

# 3. Recuperar secret 'fabriceventhub'
fabriceventhub = PyTridentTokenLibrary.get_secret_with_token(
    vault_url,
    "fabriceventhub",   # nombre de tu secreto fabriceventhub
    access_token
)

# 4. Verificación rápida (Fabric mostrará [REDACTED] en la salida)
print(f"fabricendpoint: {fabricendpoint[:154]}…")
print(f"fabriceventhub: {fabriceventhub[:18]}…")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# 3. Crea el cliente y envía un evento de prueba
producer = EventHubProducerClient.from_connection_string(
    conn_str=fabricendpoint,
    eventhub_name=fabriceventhub
)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Conexión Event Hub
# producer = EventHubProducerClient.from_connection_string(
#    conn_str="Endpoint=sb://retailnovanamespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=SoLmBCL5oRRqT3I4h0gNiXgKO25XBSop6+AEhNs1wes=",eventhub_name="eventhub_first_file"
# )

faker = Faker()

# Catálogos
region_ciudades = {
    'Norte': ['Trujillo', 'Chiclayo'],
    'Centro': ['Junin', 'Apurimac'],
    'Sur': ['Cusco', 'Arequipa'],
    'Este': ['Puno', 'Ucayali'],
    'Oeste': ['Lima', 'Ica']
}
regiones = list(region_ciudades.keys())
tiendas = ['FashionPlus', 'RopaMax', 'UrbanStyle', 'ModaCenter', 'TrendZone']
categorias = ['Camisas', 'Pantalones', 'Vestidos', 'Zapatos', 'Accesorios']
marcas = ['Nike', 'Adidas', 'Zara', 'H&M', 'Levi’s', 'Under Armour', 'Puma', 'Guess']
canales_venta = ['Web', 'App', 'Presencial', 'WhatsApp']


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Control de onda
ciclo = 0
amplitud = 50  # rango de subida/bajada
frecuencia = 0.2  # qué tan rápido sube/baja la onda


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Bucle de generación
while True:
    event_data_batch = producer.create_batch()

    # Control de cantidad de registros por lote según la onda
    variacion = int(amplitud * (math.sin(ciclo * frecuencia) + 1))  # valor entre 0 y 2*amplitud
    n_registros = max(3, variacion)  # mínimo 3 registros por lote

    for _ in range(n_registros):
        region = random.choice(regiones)
        ciudad = random.choice(region_ciudades[region])
        tienda = random.choice(tiendas)
        categoria = random.choice(categorias)
        marca = random.choice(marcas)
        canal_venta = random.choice(canales_venta)
        terminal_origen = random.choice(['Caja 1', 'Caja 2', 'Caja rápida', 'Kiosko autoservicio']) if canal_venta == 'Presencial' else 'Online'

        producto = f"{categoria} {faker.word().capitalize()} {marca}"

        # Simular cambios en precio y cantidad
        base_precio = 100
        factor = 1 + 0.5 * math.sin(ciclo * frecuencia)
        precio_unitario = round(base_precio * factor + random.uniform(-10, 10), 2)
        precio_ultima_compra = round(precio_unitario * random.uniform(0.9, 1.1), 2)
        cantidad = random.randint(1, int(5 * factor))
        descuento_pct = random.choice([0, 5, 10, 15])
        descuento_monto = round(precio_unitario * cantidad * descuento_pct / 100, 2)
        subtotal = round(precio_unitario * cantidad - descuento_monto, 2)
        impuesto_pct = 18
        impuesto_monto = round(subtotal * impuesto_pct / 100, 2)
        total_linea = round(subtotal + impuesto_monto, 2)

        venta = {
            'venta_id': str(uuid.uuid4()),
            'fecha_venta': datetime.now(ZoneInfo("America/Lima")).isoformat(),
            'region': region,
            'ciudad': ciudad,
            'tienda': tienda,
            'categoria': categoria,
            'marca': marca,
            'producto': producto,
            'precio_unitario': precio_unitario,
            'precio_ultima_compra': precio_ultima_compra,
            'cantidad': cantidad,
            'descuento_pct': descuento_pct,
            'descuento_monto': descuento_monto,
            'subtotal': subtotal,
            'impuesto_pct': impuesto_pct,
            'impuesto_monto': impuesto_monto,
            'total_linea': total_linea,
            'canal_venta': canal_venta,
            'terminal_origen': terminal_origen
        }

        venta_json = json.dumps(venta)
        event_data_batch.add(EventData(venta_json))

    producer.send_batch(event_data_batch)
    print(f"📤 Lote enviado con {n_registros} registros (ciclo={ciclo})")
    ciclo += 1
    time.sleep(2)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
