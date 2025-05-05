import threading
from .polygon_api import start_data_update_loop
import os
#работа только с основным потоком в целях избежания ошибок API
if os.environ.get('RUN_MAIN') == 'true':  # Только основной поток
    threading.Thread(target=start_data_update_loop, daemon=True).start()
