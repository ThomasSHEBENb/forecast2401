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

def get_stock_data(ticker, multiplier=1, timespan="day", limit=500):
    #Получает данные за последние сутки.
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
def get_current_rsi(ticker, limit=1, window=12):
    #Получает rsi за последние сутки
    url = f"https://api.polygon.io/v1/indicators/rsi/{ticker}?adjusted=true&window={window}&series_type=close&order=desc&limit={limit}&apiKey={API_KEY}"
    
    response_rsi = requests.get(url)
    data_rsi = response_rsi.json()
    if "results" in data_rsi and "values" in data_rsi["results"]:
        values = data_rsi["results"]["values"] 

        # Преобразуем в DataFrame
        df_rsi = pd.DataFrame(values)
        if "timestamp" in df_rsi.columns:
            df_rsi["timestamp"] = pd.to_datetime(df_rsi["timestamp"], unit="ms")
            df_rsi.set_index("timestamp", inplace=True)
            return df_rsi
        else:
            print("Ошибка: Нет столбца 'timestamp' в ответе API.")
            return None
    else:
        print("Ошибка: API не вернул ожидаемые данные.", data_rsi)
        return None
    
def get_current_ema(ticker, window=40, limit=1):
    #Получает данные EMA(40)
    url = f"https://api.polygon.io/v1/indicators/ema/{ticker}?adjusted=true&window={window}&series_type=close&order=desc&limit={limit}&apiKey={API_KEY}"

    response_ema = requests.get(url)
    data_ema = response_ema.json()

    if "results" in data_ema and "values" in data_ema["results"]:
        values = data_ema["results"]["values"]

        # Преобразуем в DataFrame
        df_ema = pd.DataFrame(values)
        if "timestamp" in df_ema.columns:
            df_ema["timestamp"] = pd.to_datetime(df_ema["timestamp"], unit="ms")
            df_ema.set_index("timestamp", inplace=True)
            return df_ema
        else:
            print("Ошибка: Нет столбца 'timestamp' в ответе API.")
            return None
    else:
        print("Ошибка: API не вернул ожидаемые данные.", data_ema)
        return None

# Тестируем

# Запрашиваем данные по AAPL для тестов скрипта
#!! ticker_data = get_stock_data(f'{name_from_mainpage}')


print(get_stock_data('AAPL'))
print(get_current_rsi('AAPL'))
print(get_current_ema('AAPL'))