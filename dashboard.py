import streamlit as st
import requests
import pandas as pd
import json
import os

st.title("Dashboard de Uso da Books API")

stats_file = "logs/api.log"
if os.path.exists(stats_file):
    with open(stats_file, "r") as f:
        logs = [json.loads(line) for line in f if line.strip()]
    df = pd.DataFrame(logs)
    st.subheader("Requisições por Endpoint")
    st.bar_chart(df["path"].value_counts())

    st.subheader("Tempo Médio de Processamento")
    st.write(round(df["process_time"].mean(), 4))

    st.subheader("Status Codes")
    st.bar_chart(df["status_code"].value_counts())
else:
    st.warning("Arquivo de log não encontrado.")

st.subheader("Estatísticas da Coleção de Livros (API)")
try:
    response = requests.get("http://localhost:8000/api/v1/stats/overview")
    if response.status_code == 200:
        stats = response.json()
        st.json(stats)
    else:
        st.warning(f"Erro ao buscar estatísticas da API: {response.status_code}")
except Exception as e:
    st.warning(f"Erro ao conectar à API: {e}")

