import requests
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta
from sys import stdout
stdout.reconfigure(encoding='utf-8')



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
        df = df.drop(['vw', 'h', 'l', 'n', 'o'], axis=1)
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
    
def get_current_ema100(ticker, window=100, limit=1):
    #Получает данные EMA(100)
    url = f"https://api.polygon.io/v1/indicators/ema/{ticker}?adjusted=true&window={window}&series_type=close&order=desc&limit={limit}&apiKey={API_KEY}"

    response_ema = requests.get(url)
    data_ema100 = response_ema.json()

    if "results" in data_ema100 and "values" in data_ema100["results"]:
        values = data_ema100["results"]["values"]

        # Преобразуем в DataFrame
        df_ema100 = pd.DataFrame(values)
        if "timestamp" in df_ema100.columns:
            df_ema100["timestamp"] = pd.to_datetime(df_ema100["timestamp"], unit="ms")
            df_ema100.set_index("timestamp", inplace=True)
            return df_ema100
        else:
            print("Ошибка: Нет столбца 'timestamp' в ответе API.")
            return None
    else:
        print("Ошибка: API не вернул ожидаемые данные.", data_ema100)
        return None
    


def get_current_ema50(ticker, window=50, limit=1):
    #Получает данные EMA(50)
    url = f"https://api.polygon.io/v1/indicators/ema/{ticker}?adjusted=true&window={window}&series_type=close&order=desc&limit={limit}&apiKey={API_KEY}"

    response_ema = requests.get(url)
    data_ema50 = response_ema.json()

    if "results" in data_ema50 and "values" in data_ema50["results"]:
        values = data_ema50["results"]["values"]

        # Преобразуем в DataFrame
        df_ema50 = pd.DataFrame(values)
        if "timestamp" in df_ema50.columns:
            df_ema50["timestamp"] = pd.to_datetime(df_ema50["timestamp"], unit="ms")
            df_ema50.set_index("timestamp", inplace=True)
            return df_ema50
        else:
            print("Ошибка: Нет столбца 'timestamp' в ответе API.")
            return None
    else:
        print("Ошибка: API не вернул ожидаемые данные.", data_ema50)
        return None


# Тестируем

# Запрашиваем данные по AAPL для тестов скрипта
#!! ticker_data = get_stock_data(f'{name_from_mainpage}')

def make_market_decision(ticker):
    ema100_data = get_current_ema100(ticker)
    ema50_data = get_current_ema50(ticker)
    rsi_data = get_current_rsi(ticker)
    stock_data = get_stock_data(ticker)
    ema100 = ema100_data['value'].iloc[0]
    ema50 = ema50_data['value'].iloc[0]
    rsi = rsi_data['value'].iloc[0]

    if 'c' not in stock_data:
        return "Ошибка: В stock_data нет закрытых цен"

    last_close = stock_data['c'].iloc[0]

    if rsi > 70:
        return "актив перекуплен, воздержитесь от входа в ближайшее время"
    elif rsi < 30:
        return "актив перепродан, воздержитесь от входа в ближайшее время"
    elif last_close < ema100 and last_close < ema50 and ema50 != ema100:
        return "виден нисходящий тренд"
    elif last_close > ema100 and last_close > ema50 and ema50 != ema100:
        return "виден восходящий тренд"
    elif abs(ema50 - ema100) < 5:
        return "есть признаки разворота тренда по EMA"

    return "нет явного тренда"

print(make_market_decision('AAPL'))
