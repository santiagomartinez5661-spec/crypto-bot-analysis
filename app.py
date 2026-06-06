import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from groq import Groq

# Configuración
st.title(" Analizador de Criptomonedas con IA")
st.write("Ingresa una criptomoneda y obtén un análisis en tiempo real")

# Input del usuario
cripto = st.selectbox("Selecciona una criptomoneda", ["bitcoin", "ethereum", "solana"])
dias = st.slider("¿Cuántos días analizar?", 7, 90, 30)
api_key = st.text_input("ingresa la api key:", type="password")

if st.button("Analizar"):
    with st.spinner("Jalando datos..."):

        # Obtener datos
        url = f"https://api.coingecko.com/api/v3/coins/{cripto}/market_chart"
        params = {"vs_currency": "usd", "days": dias, "interval": "daily"}
        data = requests.get(url, params=params).json()

        precios = pd.DataFrame(data["prices"], columns=["timestamp", "precio"])
        precios["fecha"] = pd.to_datetime(precios["timestamp"], unit="ms")
        precios = precios.drop("timestamp", axis=1)

        # Estadísticas
        precio_actual = precios["precio"].iloc[-1]
        precio_maximo = precios["precio"].max()
        precio_minimo = precios["precio"].min()
        precio_promedio = precios["precio"].mean()
        variacion = precio_maximo - precio_minimo

        # Métricas
        st.subheader(f" Resumen de {cripto.capitalize()}")
        col1, col2, col3 = st.columns(3)
        col1.metric("Precio actual", f"${precio_actual:,.2f}")
        col2.metric("Máximo", f"${precio_maximo:,.2f}")
        col3.metric("Mínimo", f"${precio_minimo:,.2f}")

        # Gráfica
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(precios["fecha"], precios["precio"], color="orange", linewidth=2)
        ax.fill_between(precios["fecha"], precios["precio"], alpha=0.2, color="orange")
        ax.set_title(f"{cripto.capitalize()} - Últimos {dias} días")
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

        # Análisis con IA
        if api_key:
            with st.spinner("Analizando con IA..."):
                client = Groq(api_key=api_key)
                respuesta = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": "Eres un analista financiero experto en criptomonedas. Responde en español de forma clara y concisa."
                        },
                        {
                            "role": "user",
                            "content": f"""Analiza estos datos de {cripto} de los últimos {dias} días:
                            - Precio actual: ${precio_actual:,.2f}
                            - Precio máximo: ${precio_maximo:,.2f}
                            - Precio mínimo: ${precio_minimo:,.2f}
                            - Precio promedio: ${precio_promedio:,.2f}
                            - Variación total: ${variacion:,.2f}
                            ¿Qué tendencia ves? ¿Es buen momento para comprar o vender?"""
                        }
                    ]
                )
                st.subheader(" Análisis de IA")
                st.write(respuesta.choices[0].message.content)
        else:
            st.warning("Ingresa tu API Key de Groq para obtener el análisis con IA")