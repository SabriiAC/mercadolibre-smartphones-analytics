import pandas as pd
import numpy as np

print("==========================================================")
print("=== FASE 3: LIMPIEZA Y MODELADO - NICHO SMARTPHONES ===")
print("==========================================================")

# 1. Cargar el dataset bruto de Smartphones
df = pd.read_csv('mercadolibre_raw.csv')

# 2. Tratamiento de nulos y estandarización de Medallas
mapa_medallas = {
    'platinum': 'MercadoLíder Platinum',
    'gold': 'MercadoLíder Gold',
    'silver': 'MercadoLíder Silver',
    'Vendedor Estándar': 'Vendedor Estándar'
}
df['medalla_vendedor'] = df['medalla_vendedor'].map(mapa_medallas).fillna('Vendedor Estándar')

# Formatear nombres de Logística
mapa_logistica = {
    'fulfillment': 'Envío Full (Fulfillment)',
    'cross_docking': 'Colecta / Depósito',
    'drop_off': 'Despacho en Correo'
}
df['tipo_logistica'] = df['tipo_logistica'].map(mapa_logistica).fillna('Despacho en Correo')

# 3. Segmentación por Gama de Precio (Exclusivo para el Nicho de Smartphones)
def clasificar_gama(precio):
    if precio < 300000:
        return 'Gama Entrada (< $300k)'
    elif precio <= 700000:
        return 'Gama Media ($300k - $700k)'
    else:
        return 'Gama Alta (> $700k)'

df['gama_precio'] = df['precio_actual'].apply(clasificar_gama)

# 4. Columnas Calculadas de Negocio
df['facturacion_estimada_ars'] = df['precio_actual'] * df['vendidos']
df['es_envio_full'] = np.where(df['tipo_logistica'] == 'Envío Full (Fulfillment)', 1, 0)
df['es_mercadolider'] = np.where(df['medalla_vendedor'].str.contains('MercadoLíder'), 1, 0)

# Cálculo del Índice de Sobreprecio por Financiación en Cuotas
precio_prom_cuotas = df[df['cuotas_sin_interes'] == 'Sí']['precio_actual'].mean()
precio_prom_contado = df[df['cuotas_sin_interes'] == 'No']['precio_actual'].mean()
sobreprecio_pct = round(((precio_prom_cuotas - precio_prom_contado) / precio_prom_contado) * 100, 2)

print("\n--- RESUMEN DE PROCESAMIENTO Y METRICAS DEL NICHO ---")
print(f"Total Publicaciones Procesadas: {len(df)}")
print(f"Facturacion Total Estimada: ${df['facturacion_estimada_ars'].sum():,.2f} ARS")
print(f"Ticket Promedio de Smartphones: ${df['precio_actual'].mean():,.2f} ARS")
print(f"Penetracion de Envio Full: {(df['es_envio_full'].mean()*100):.1f}%")
print(f"Indice de Sobreprecio (Cuotas vs Contado): +{sobreprecio_pct}%")

# 5. Guardar dataset limpio final
output_clean = 'mercadolibre_dataset_limpio.csv'
df.to_csv(output_clean, index=False)

print("\n==========================================================")
print(f"LIMPIEZA COMPLETADA: Archivo final generado: {output_clean}")
print("==========================================================")
