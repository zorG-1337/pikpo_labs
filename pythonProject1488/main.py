# Подключаем приложение Flask из пакета labapp (см. модуль инициализации __init__.py)
from labapp import app

"""
    Этот модуль запускает web-приложение
"""

# if __name__ == '__main__':

    # app.run(host='0.0.0.0', port=8000)


import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from labapp.processor.dataprocessor_service import DataProcessorService
import os
import requests
from multiprocessing import Process
flag = False

class MyHandler(FileSystemEventHandler):

    def __init__(self, data_folder):
        self.data_folder = data_folder

    def handle_new_file(self, file_path):
        # Обработка нового файла
        # server.terminate()
        flag = True
        temp = os.path.basename(file_path)
        print(f"New file created: {file_path}")
        service = DataProcessorService(datasource=temp,
                                       db_connection_url="sqlite:///C:\\Users\\bossv\\PycharmProjects\\pythonProject1488\\pikpo_2.db")
        service.run_service(flag)
        # server = Process(target=app.run(host='0.0.0.0', threaded=True, port=8000))
        # server.start()
    def on_created(self, event):
        if event.is_directory:
            return None
        self.handle_new_file(event.src_path)




if __name__ == '__main__':
    service = DataProcessorService(datasource="COVID-19_Case_Surveillance_Public_Use_Data.csv",
                                   db_connection_url="sqlite:///C:\\Users\\bossv\\PycharmProjects\\pythonProject1488\\pikpo_2.db")
    service.run_service(flag)
    # app.run(host='0.0.0.0', port=8000)
    data_folder = "C:\\Users\\bossv\\PycharmProjects\\pythonProject1488\\data"
    event_handler = MyHandler(data_folder)
    observer = Observer()
    observer.schedule(event_handler, data_folder, recursive=False)
    server = Process(target=app.run(host='0.0.0.0', threaded=True, port=8000))
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

