import requests
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta
import threading
import time

market_data_cache = {}

def start_data_update_loop():
    if hasattr(start_data_update_loop, "_started"):
        return  # Поток уже запущен

    start_data_update_loop._started = True

    tickers = ['GOOGL', 'AAPL', 'TSLA']
    ticker_index = 0

    def update_data():
        nonlocal ticker_index
        while True:
            ticker = tickers[ticker_index]
            try:
                print(f"Обновление данных для: {ticker}")
                result = make_market_decision(ticker)
                market_data_cache[ticker] = result
                print(f"Результат сохранён: {ticker} → {result}")
            except Exception as e:
                print(f"Ошибка при обновлении {ticker}: {e}")
            ticker_index = (ticker_index + 1) % len(tickers)
            time.sleep(65)

    threading.Thread(target=update_data, daemon=True).start()


# Загружаем ключ API
load_dotenv()
API_KEY = os.getenv("POLYGON_API_KEY")



def get_stock_data(ticker, multiplier=1, timespan="day", limit=500):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?adjusted=true&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "results" in data and data["results"]:
        df = pd.DataFrame(data["results"])
        df["t"] = pd.to_datetime(data["results"][0]["t"], unit="ms")
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

market_data_cache = {
    "AAPL": None,
    "GOOGL": None,
    "TSLA": None,
}


def make_market_decision(ticker):
    ema100_data = get_current_ema100(ticker)
    time.sleep(3)
    ema50_data = get_current_ema50(ticker)
    time.sleep(3)
    rsi_data = get_current_rsi(ticker)
    time.sleep(3)
    stock_data = get_stock_data(ticker)
    time.sleep(3)

    if (
        ema100_data is None or ema100_data.empty or
        ema50_data is None or ema50_data.empty or
        rsi_data is None or rsi_data.empty or
        stock_data is None or stock_data.empty
    ):
        return f"Ошибка: Не удалось получить данные для {ticker}"
    
    try:
        ema100 = ema100_data['value'].iloc[0]
        ema50 = ema50_data['value'].iloc[0]
        rsi = rsi_data['value'].iloc[0]
        last_close = stock_data['c'].iloc[0]
    except Exception as e:
        return f"Ошибка при обработке данных: {e}"


    if rsi > 70:
        result = "актив перекуплен, воздержитесь от входа в ближайшее время"
    elif rsi < 30:
        result = "актив перепродан, воздержитесь от входа в ближайшее время"
    elif last_close < ema100 and last_close < ema50 and ema50 != ema100:
        result = "виден нисходящий тренд"
    elif last_close > ema100 and last_close > ema50 and ema50 != ema100:
        result = "виден восходящий тренд"
    elif abs(ema50 - ema100) < 5:
        result = "есть признаки разворота тренда по EMA"
    else:
        result = "нет явного тренда"


    market_data_cache[ticker] = result
    market_data_cache[f"{ticker}_details"] = {
        'last_close': last_close,
        'ema100': ema100,
        'ema50': ema50,
        'rsi': rsi
    }

    return result




