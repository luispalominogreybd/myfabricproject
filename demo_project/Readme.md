# 🛍️ RetailNova Demo Project
Este proyecto simula un entorno completo de análisis de ventas en tiempo real utilizando tecnologías de Microsoft Fabric, como Notebooks, Event Hub, KQL Database, Lakehouse y Power BI.

## 📌 Objetivo
Proveer una demostración de punta a punta sobre cómo generar, transmitir, almacenar, consultar y visualizar datos de ventas simulados en un entorno de retail, con cambios dinámicos y variación controlada en tiempo real.

## 🏗️ Estructura del proyecto
```
demo_project/
├── KQL_EventHouse.Eventhouse               # Contenedor de eventos de entrada
├── KQL_EventHouse.KQLDatabase              # Base de datos en KQL
├── KQL_EventHouse_queryset.KQLQueryset     # Conjunto de consultas KQL
├── KQL_EventStream.Eventstream             # Flujo de eventos conectado al Event Hub
├── KQL_RetailNova.KQLQueryset              # Consultas analíticas del negocio
├── LH_RetailNovaDemo.Lakehouse             # Lakehouse para almacenamiento estructurado
├── NB_real_time_data.Notebook              # Notebook que simula y envía los datos
├── Report_DirectQuery.Report               # Reporte Power BI conectado por DirectQuery
├── Report_DirectQuery.SemanticModel        # Modelo semántico del reporte
```

## 🚀 Entorno Azure
Deben crearse los siguientes servicios: 
```
Resource group/
├── Event_Hubs.Namespace                               # Servicio Event Hubs
├── ├── Event_Hubs.Instance (eventhub_first_file)      # Servicio de escucha
```

## 🚀 Simulación de datos
Se utiliza un Notebook en Python para generar datos de ventas con lógica de variación controlada (onda sinusoidal) para simular picos y caídas.

Cada evento incluye atributos como:
- región, ciudad, tienda
- categoría, marca, producto
- cantidad, precio, descuento, impuestos
- canal y terminal de venta

Relación entre regiones y ciudades está controlada por reglas lógicas:
- **Norte**: Trujillo, Chiclayo  
- **Centro**: Junín, Apurímac  
- **Sur**: Cusco, Arequipa  
- **Este**: Puno, Ucayali  
- **Oeste**: Lima, Ica

## 🔁 Flujo de procesamiento
1. **NB_real_time_data.Notebook**: genera y envía datos cada 2 segundos a Event Hub.
2. **KQL_EventStream**: recibe eventos en streaming.
3. **KQL_EventHouse**: almacena los datos en una base KQL para consultas.
4. **LH_RetailNovaDemo**: datos procesados y almacenados para análisis históricos.
5. **Report_DirectQuery**: Power BI conectado para análisis en tiempo real.

## 📦 Módulos Python
El notebook "NB_real_time_data" carga al inicio los siguientes módulos:
```
faker
azure.eventhub
azure-identity
azure-keyvault-secrets
azure-eventhub
```

## 🔄 Automatización
Este proyecto incluye el notebook "NB_real_time_data" en Microsoft Fabric que al ejecutarlo manualmente envía cada 2 segundos, la simulación de una carga continua de datos como demo, entrando en un loop hasta que el proceso se detenga tambien manualmente.

## 📊 Visualización
El reporte Power BI (`Report_DirectQuery`) permite analizar las ventas en tiempo real segmentadas por:
- Región / Ciudad / Tienda
- Marca / Categoría
- Canal de venta
- Rangos de precios y cantidades

## 📂 Archivos clave
| Archivo | Descripción |
|--------|-------------|
| `NB_real_time_data.Notebook` | Generador de eventos con variación controlada |
| `Report_DirectQuery` | Reporte Power BI con conexión DirectQuery |

## 👨‍💻 Autor
**Luis Palomino Vallvé**  
Especialista en soluciones de datos con casi 30 años de experiencia en TI.  
Apasionado por integrar inteligencia de negocio con tecnologías modernas en la nube.

## 📄 Licencia
Este proyecto es solo para fines de demostración técnica.  
No incluye información real ni comercial.
