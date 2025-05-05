import requests
import os
import pandas as pd
from dotenv import load_dotenv
import threading
import time
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
###!!! Для запуска программы нужно перейти в терминале в папку проекта cd metainit (если вы не в нем)
###!!! Ввести команду python manage.py runserver и перейти по ссылке на локалхосте


#функция для формирования графика
def generate_stock_plot(ticker, df):
    import matplotlib.pyplot as plt
    import os
    import pandas as pd

    # Убедимся, что индекс — это datetime
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    # Проверка наличия данных
    if 'c' not in df.columns or df['c'].isna().all():
        print("Нет данных для построения графика")
        return None

    plt.figure(figsize=(20, 6))
    plt.plot(df.index, df['c'], label='Цена закрытия', color='blue')
    plt.title(f'{ticker} Рыночная Цена')
    plt.xlabel('Дата в западном формате')
    plt.ylabel('Цена закрытия')
    plt.grid(True)
    plt.legend()

    # Путь до static/plots для сохранения и будущего использования
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(base_dir, '..', 'static', 'plots')
    os.makedirs(image_dir, exist_ok=True)

    image_path = os.path.join(image_dir, f'{ticker}_plot.png')
    plt.savefig(image_path, bbox_inches='tight')
    plt.close()

    return f'/static/plots/{ticker}_plot.png'




def start_data_update_loop():
    if hasattr(start_data_update_loop, "_started"):
        return  # Поток уже запущен

    start_data_update_loop._started = True

    tickers = ['GOOGL', 'AAPL', 'TSLA']
    ticker_index = 0
    #Обновление кэша
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



def get_stock_data(ticker):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=14)  # запас на выходные

    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}?adjusted=true&sort=asc&limit=10&apiKey={API_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if 'results' not in data:
            return None

        df = pd.DataFrame(data['results'])
        df['t'] = pd.to_datetime(df['t'], unit='ms')  # преобразуем timestamp
        df.set_index('t', inplace=True)
        df.rename(columns={'c': 'c'}, inplace=True)  # 'c' уже — close
        return df

    except Exception as e:
        print(f"Ошибка ЫSпри получении данных для {ticker}: {e}")
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
#формируем кэш для эффективной работы с API
market_data_cache = {
    "AAPL": {
        "result": None,
        "last_close": None,
        "ema100": None,
        "ema50": None,
        "rsi": None,
        "df": None  # датафрейм с ценами для графика
    },
    "GOOGL": {
        "result": None,
        "last_close": None,
        "ema100": None,
        "ema50": None,
        "rsi": None,
        "df": None
    },
    "TSLA": {
        "result": None,
        "last_close": None,
        "ema100": None,
        "ema50": None,
        "rsi": None,
        "df": None
    }
}

#Основная функция для вынесения прогноза
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
    #Попытка получчения нужных данных из датафрейма
    try:
        ema100 = ema100_data['value'].iloc[-1]
        ema50 = ema50_data['value'].iloc[-1]
        rsi = rsi_data['value'].iloc[-1]
        last_close = stock_data['c'].iloc[-1]
    except Exception as e:
        return f"Ошибка при обработке данных: {e}"
    #Вынесение решения на основе индикаторов
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

    #Формирование кэша для визуализации данных
    market_data_cache[ticker] = result
    market_data_cache[f"{ticker}_details"] = {
        "last_close": last_close,
        "ema100": ema100,
        "ema50": ema50,
        "rsi": rsi
    }
    market_data_cache[f"{ticker}_df"] = stock_data

    return result



