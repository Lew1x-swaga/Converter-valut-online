import streamlit as st
from currency import CurrencyData

# Настройка страницы
st.set_page_config(page_title="Конвертер валют", layout="wide")

# Инициализация класса для работы с валютами
@st.cache_resource
def get_curr_data():    
    return CurrencyData()

currency_data = get_curr_data()

# Заголовок приложения
st.title("Конвертер валют")

try:
    currencies = currency_data.get_curr_rates()

    currency_options = []
    for code in currencies:
        name = currencies[code]['name']
        currency_options.append(f"{code} - {name}")

    col1, col2 = st.columns(2)
    
    with col1:
        selected_from = st.selectbox("Из валюты:", currency_options, index = 0)
        from_curr = selected_from.split(" - ")[0]

    with col2:
        selected_to = st.selectbox("В валюту:", currency_options, index = 1)   #default - eur
        to_curr = selected_to.split(" - ")[0]
    
    amount = st.number_input(
        "Сумма:",
        min_value=0.01,
        value=100.0,
        step=1.0
    )
    
    # Кнопка конвертации
    convert_button = st.button("Конвертировать")

    # Результат конвертации
    if convert_button:
        try:
            result = currency_data.convert_curr(amount, from_curr, to_curr)
            st.success(f"{amount} {from_curr} = {result} {to_curr}")
        except Exception as e:
            st.error(f"Ошибка при конвертации: {str(e)}")

except Exception as e:
    st.error(f"Ошибка при загрузке данных: {str(e)}")