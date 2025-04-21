# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# CELL ********************

import uuid
import random
import json
import datetime
from faker import Faker
from azure.eventhub import EventHubProducerClient, EventData
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Configuración de conexión
producer = EventHubProducerClient.from_connection_string(
    conn_str="Endpoint=sb://retailnovanamespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=SoLmBCL5oRRqT3I4h0gNiXgKO25XBSop6+AEhNs1wes=",
    eventhub_name="eventhub_first_file"
#    conn_str="Endpoint=sb://demoeventuhb.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=QCm9NYdwDh9LjhMK+WxuMA11r8h+DvGmY+AEhNd6r5c=",
#    eventhub_name="retailnovaeventhub"
)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Generador de datos ficticios
faker = Faker()


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Parámetros de ejemplo
regiones = ['Norte', 'Sur', 'Este', 'Oeste', 'Centro']
ciudades = ['Lima', 'Arequipa', 'Trujillo', 'Cusco', 'Chiclayo']
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

# Crear un batch
event_data_batch = producer.create_batch()


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Generar 150 registros
for _ in range(150):
    region = random.choice(regiones)
    ciudad = random.choice(ciudades)
    tienda = random.choice(tiendas)
    categoria = random.choice(categorias)
    marca = random.choice(marcas)
    canal_venta = random.choice(canales_venta)

    if canal_venta == 'Presencial':
        terminal_origen = random.choice(['Caja 1', 'Caja 2', 'Caja rápida', 'Kiosko autoservicio'])
    else:
        terminal_origen = 'Online'

    producto = f"{categoria} {faker.word().capitalize()} {marca}"
    precio_unitario = round(random.uniform(30, 300), 2)
    precio_ultima_compra = round(precio_unitario * random.uniform(0.9, 1.1), 2)
    cantidad = random.randint(1, 5)
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

    # Convertir a JSON y agregar al batch
    venta_json = json.dumps(venta)
    event_data_batch.add(EventData(venta_json))


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Enviar al Event Hub
producer.send_batch(event_data_batch)
producer.close()

print("✅ Datos enviados al Event Hub.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
