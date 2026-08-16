# 📱 Case Study: Análisis Comercial y Logístico en el Nicho de Smartphones (Mercado Libre)
> **Extracción vía API pública (Python) + Modelado de Datos y Dashboard en Power BI (DAX)**  
> **Nicho Exclusivo:** Celulares y Smartphones (`MLA1055`)  
> **Autor:** Analista de Datos Jr  

---

## 📌 1. Planteamiento del Problema Comercial (Business Task)

El objetivo de este estudio es realizar un **análisis homogéneo enfocado en un solo nicho comercial de alto valor (Smartphones)** para entender qué factores comerciales y logísticos impulsan el volumen de ventas y permiten cobros con sobreprecio (*premium pricing*).

Se evaluaron cuatro preguntas clave de negocio:

1. **"El Efecto Nivelador de Full":** ¿Un vendedor estándar (sin medalla Platinum) que utiliza **Envío Full** logra igualar el volumen de ventas de un **MercadoLíder** con envío tradicional?
2. **Elasticidad por Financiamiento:** ¿Ofrecer **Cuotas sin Interés** justifica un sobreprecio en los celulares sin penalizar la demanda?
3. **Poder de Marca por Gama:** ¿Cómo cambia la concentración de ventas entre las gamas **Baja (< $300k ARS)**, **Media ($300k - $700k ARS)** y **Alta (> $700k ARS)**?
4. **Barrera de Envío Gratis:** ¿A partir de qué rango de precio el envío gratuito se vuelve un estándar obligatorio en el mercado de celulares?

---

## 🛠️ 2. Arquitectura & Metodología Técnica

El proyecto se estructuró en un flujo end-to-end homogéneo:

```
[1. Preguntas de Negocio] ➔ [2. Extracción API (Python)] ➔ [3. Limpieza y Modelado] ➔ [4. Dashboard Power BI] ➔ [5. Insights]
```

1. **Fase 2 - Extracción (Python):** Script `01_extraer_datos_meli.py` que consulta el catálogo del nicho Celulares (`MLA1055`), capturando 500 publicaciones con atributos de precio, unidades vendidas (`sold_quantity`), tipo de logística (`fulfillment`), reputación (`power_seller_status`) y cuotas.
2. **Fase 3 - Limpieza & DAX:** Segmentación por gama de precio, cálculo de la columna `facturacion_estimada_ars` y medidas **DAX** en Power BI (`[Ticket_Promedio_Smartphones]`, `[Pct_Penetracion_Full]`, `[Indice_Sobreprecio_Cuotas]`).
3. **Fase 4 & 5 - Visualización Power BI:** Dashboard interactivo compuesto por KPIs homogéneos, gráfico de barras combinadas, scatter plot (Precio vs Ventas) y segmentadores por Marca y Gama.

---

## 📊 3. Visualización del Dashboard en Power BI

![Power BI Overview](dashboard_mercadolibre_overview.jpg)

---

## 💻 4. Código Destacado

### Script de Extracción Python (Fase 2)
```python
import requests
import pandas as pd

# Consulta a la API pública de Mercado Libre - Nicho Smartphones (MLA1055)
url = "https://api.mercadolibre.com/sites/MLA/search?category=MLA1055&limit=50"
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
data = response.json()

items = []
for item in data.get('results', []):
    items.append({
        'id': item['id'],
        'titulo': item['title'],
        'precio': item['price'],
        'vendidos': item['sold_quantity'],
        'logistica': item['shipping']['logistic_type'],
        'medalla': item['seller']['seller_reputation']['power_seller_status']
    })
```

### Medida DAX Destacada: Índice de Sobreprecio por Cuotas en Smartphones
```dax
Indice_Sobreprecio_Cuotas = 
VAR Precio_Cuotas = CALCULATE(AVERAGE(mercadolibre_dataset_limpio[precio_actual]), mercadolibre_dataset_limpio[cuotas_sin_interes] = "Sí")
VAR Precio_Contado = CALCULATE(AVERAGE(mercadolibre_dataset_limpio[precio_actual]), mercadolibre_dataset_limpio[cuotas_sin_interes] = "No")
RETURN
DIVIDE(Precio_Cuotas - Precio_Contado, Precio_Contado, 0)
```

---

## 📈 5. Principales Descubrimientos (Insights)

1. **"El Efecto Nivelador de Full en Celulares":** La logística **Envío Full** compensa la falta de antigüedad. Un *Vendedor Estándar con Envío Full* alcanza un volumen promedio de **810 ventas**, superando a un *MercadoLíder Gold* sin Full (**520 ventas**).
2. **Elasticidad por Financiación (+24.8%):** En el nicho de celulares, ofrecer **6 cuotas sin interés** permite aplicar un sobreprecio promedio del **+24.8%** sin resentir las ventas, ya que el consumidor prioriza la previsibilidad de la cuota mensual.
3. **Dominio por Gamas:** **Apple** domina el 74% de la facturación en Gama Alta (> $700k ARS), mientras que **Samsung y Motorola** lideran el volumen físico de unidades en la Gama Media ($300k - $700k ARS).

---

## 💡 6. Recomendaciones Estratégicas para Vendedores del Nicho

1. **Adopta Envío Full desde el primer día:** En Smartphones, la rapidez de entrega es un factor decisivo. Usar Full te permite competir cara a cara con vendedores Platinum.
2. **Financia a cambio de Margen:** Utiliza cuotas sin interés absorbiendo la comisión de Mercado Libre a través de un sobreprecio calibrado (+20% a +25%).
3. **Asegura Envío Gratis:** En el nicho de celulares (donde casi todos los productos superan los $30.000 ARS), el envío gratis es una **condición obligatoria de mercado** para no perder posicionamiento orgánico.

---
*(Proyecto desarrollado por Analista de Datos Jr para portafolio profesional).*
