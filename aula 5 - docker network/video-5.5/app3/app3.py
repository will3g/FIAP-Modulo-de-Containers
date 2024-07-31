import os

import requests
import streamlit as st
import pandas as pd

API_URL = os.getenv('API_URL')

def get_ticker_data(ticker):
    response = requests.get(API_URL + ticker.upper())
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error('Ticker não encontrado')
        return None

def format_currency(value):
    return f"R${value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

st.sidebar.title("Opções")

ticker = st.sidebar.text_input('Digite o símbolo da ação:', 'PETR4').upper()

if ticker:
    data = get_ticker_data(ticker)
    if data is not None:
        data['Date'] = pd.to_datetime(data['Date'])
        data['Year'] = data['Date'].dt.year
        data = data.set_index('Date')
        
        all_years = data['Year'].unique().tolist()
        selected_years = st.sidebar.multiselect('Selecione os anos para comparar', all_years, default=all_years)

        data_filtered = data[data['Year'].isin(selected_years)]

        section = st.sidebar.slider(
            'Número de cotações',
            min_value=30,
            max_value=len(data_filtered),
            value=100,
            step=10
        )

        df_temp = data_filtered[-section:]

        sma = st.sidebar.checkbox('Exibir Média Móvel Simples')
        if sma:
            period = st.sidebar.slider('Período da SMA', min_value=5, max_value=200, value=20, step=1)
            df_temp[f'SMA {period}'] = data['Close'].rolling(window=period).mean()
        
        st.subheader(f'Preços de Fechamento e Média Móvel Simples de {ticker}')
        st.line_chart(df_temp[['Close', f'SMA {period}']] if sma else df_temp['Close'], width=700, height=400)
        
        st.subheader(f'Volume de Negociações de {ticker}')
        st.bar_chart(df_temp['Volume'], width=700, height=200)

        st.subheader(f'Dividendos de {ticker}')
        st.bar_chart(df_temp['Dividends'], width=700, height=200)

        if st.sidebar.checkbox('Exibir Estatísticas Descritivas'):
            st.subheader('Estatísticas Descritivas')
            descriptive_stats = df_temp.describe()
            descriptive_stats.loc['mean'] = descriptive_stats.loc['mean'].apply(format_currency)
            descriptive_stats.loc['std'] = descriptive_stats.loc['std'].apply(format_currency)
            descriptive_stats.loc['min'] = descriptive_stats.loc['min'].apply(format_currency)
            descriptive_stats.loc['25%'] = descriptive_stats.loc['25%'].apply(format_currency)
            descriptive_stats.loc['50%'] = descriptive_stats.loc['50%'].apply(format_currency)
            descriptive_stats.loc['75%'] = descriptive_stats.loc['75%'].apply(format_currency)
            descriptive_stats.loc['max'] = descriptive_stats.loc['max'].apply(format_currency)
            st.write(descriptive_stats)
        
        if st.sidebar.checkbox('Exibir Dados Históricos'):
            st.subheader(f'Dados Históricos de {ticker}')
            st.write(df_temp)
