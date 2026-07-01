import streamlit as st
import requests
import pandas as pd

st.title("Monitor Meteorológico")
st.write("Aplicación para consultar el clima actual y pronóstico utilizando Open-Meteo API.")

ciudades = {
    "Tegucigalpa, Honduras": {"lat": 14.0818, "lon": -87.2068},
    "San Pedro Sula, Honduras": {"lat": 15.5042, "lon": -88.0250},
    "Miami, Estados Unidos": {"lat": 25.7617, "lon": -80.1918},
    "Madrid, España": {"lat": 40.4165, "lon": -3.7026}
}

ciudad_seleccionada = st.selectbox("Seleccione una ciudad:", list(ciudades.keys()))

lat = ciudades[ciudad_seleccionada]["lat"]
lon = ciudades[ciudad_seleccionada]["lon"]

url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    clima_actual = data["current_weather"]
    
    st.subheader(f"Condiciones actuales en {ciudad_seleccionada}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Temperatura", value=f"{clima_actual['temperature']} °C")
    with col2:
        st.metric(label="Viento", value=f"{clima_actual['windspeed']} km/h")
    with col3:
        st.metric(label="Dirección del viento", value=f"{clima_actual['winddirection']}°")
        
    st.divider()
    
    st.subheader("Pronóstico de temperatura (Próximas 24 horas)")
    
    df_pronostico = pd.DataFrame({
        "Hora": data["hourly"]["time"][:24],
        "Temperatura (°C)": data["hourly"]["temperature_2m"][:24]
    })
    
    df_pronostico["Hora"] = pd.to_datetime(df_pronostico["Hora"]).dt.strftime('%H:%M')
    
    st.line_chart(data=df_pronostico.set_index("Hora"))

else:
    st.error("Error de conexión con la API de Open-Meteo.")