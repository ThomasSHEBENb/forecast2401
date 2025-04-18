from django.shortcuts import render
from .polygon_api import market_data_cache
import csv
import os
from django.http import JsonResponse  


def main_page(request):
    result = None
    if request.method == 'POST':
        ticker = request.POST.get('instrument')
        if ticker in market_data_cache:
            result = market_data_cache[ticker]
            details = market_data_cache.get(f"{ticker}_details")

            # Логируем данные, если есть подробности
            if details:
                log_path = os.path.join(os.path.dirname(__file__), 'log.csv')
                file_exists = os.path.isfile(log_path)

                with open(log_path, 'a', newline='', encoding='utf-8-sig') as csvfile:
                    fieldnames = ['ID', 'Ticker', 'Last Close', 'EMA100', 'EMA50','RSI','Decision']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    if not file_exists:
                        writer.writeheader()

                    # Считаем номер записи
                    with open(log_path, 'r') as f:
                        lines = f.readlines()
                        count = len(lines) if file_exists else 1  # Учитываем заголовок

                    writer.writerow({
                        'ID': count,
                        'Ticker': ticker,
                        'Last Close': round(details['last_close'], 2),
                        'EMA100': round(details['ema100'], 2),
                        'EMA50': round(details['ema50'], 2),
                        'RSI': round(details['rsi'], 2),
                        'Decision': result
                    })
        else:
            result = "Нет данных для этого тикера."

    return render(request, 'main.html', {'result': result})


def contact_page(request):
    return render(request, 'contact.html')

def about_page(request):
    return render(request, 'about.html')
