import requests
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Загружаем ключ API
load_dotenv()
API_KEY = os.getenv("POLYGON_API_KEY")

def get_previous_business_day(date):
    while date.weekday() in [5, 6]:  # 5 - суббота, 6 - воскресенье
        date -= timedelta(days=1)
    return date

# Определяем диапазон дат
end_date = get_previous_business_day(datetime.today()).strftime('%Y-%m-%d')
start_date = get_previous_business_day(datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

def get_stock_data(ticker, multiplier=15, timespan="minute", limit=500):
    """Получает 15-минутные свечи за последние 24 часа."""
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{start_date}/{end_date}?adjusted=true&sort=asc&limit={limit}&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if "results" in data:
        df = pd.DataFrame(data["results"])
        df["t"] = pd.to_datetime(df["t"], unit="ms") 
        df.set_index("t", inplace=True)
        return df
    else:
        print("Ошибка:", data)
        return None

# Запрашиваем данные по AAPL для тестов скрипта
df = get_stock_data("AAPL")
"""Будущая функция"""
#!! df = get_stock_data(f'{name_from_mainpage}')

# Выводим результат
if df is not None:
    print(df.tail())  # Вывод последних 5 строк
else:
    print("Данных нет или ошибка в запросе.")
