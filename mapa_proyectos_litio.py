import folium
from folium.plugins import MarkerCluster
import pandas as pd

# Cargar el archivo CSV con la información de los proyectos de litio
file_path = "/Cartera-proyectos-litio.csv"
df = pd.read_csv(file_path, encoding="ISO-8859-1", delimiter=";", quotechar='"')

# Eliminar la primera fila si contiene los encabezados erróneamente como datos
df = df.iloc[1:].reset_index(drop=True)

# Convertir las coordenadas a valores numéricos
df['LATITUD'] = df['LATITUD'].str.replace(",", ".").astype(float)
df['LONGITUD'] = df['LONGITUD'].str.replace(",", ".").astype(float)

# Crear un mapa centrado en Argentina
m = folium.Map(location=[-26, -65], zoom_start=5)

# Crear un cluster para agrupar los proyectos
marker_cluster = MarkerCluster().add_to(m)

# Asignar colores según el estado del proyecto
estado_colors = {
    "Exploración Avanzada": "blue",
    "Producción": "green",
    "Construcción": "orange",
    "Prefactibilidad": "purple",
    "Evaluación económica preliminar": "pink",
}

# Iterar sobre los datos y agregar marcadores al mapa
for _, row in df.iterrows():
    lat, lon = row['LATITUD'], row['LONGITUD']
    provincia = row['PROVINCIA']
    estado = row['ESTADO']
    nombre = row['NOMBRE']

    color = estado_colors.get(estado, "gray")  # Color por estado, gris si no está definido

    folium.Marker(
        location=[lat, lon],
        popup=f"<b>{nombre}</b><br>Provincia: {provincia}<br>Estado: {estado}",
        icon=folium.Icon(color=color)
    ).add_to(marker_cluster)

# Guardar el mapa como HTML
map_path = "mapa_proyectos_litio.html"
m.save(map_path)

print(f"Mapa guardado en: {map_path}")
