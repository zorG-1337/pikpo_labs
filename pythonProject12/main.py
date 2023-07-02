# from processor.dataprocessor_service import DataProcessorService


"""
    Main-модуль, т.е. модуль запуска приложений ("точка входа" приложения)
"""


# if __name__ == '__main__':
   #  service = DataProcessorService(datasource="COVID-19_Case_Surveillance_Public_Use_Data.csv", db_connection_url="sqlite:///pikpo.sqlite")
    # service.run_service()

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from processor.dataprocessor_service import DataProcessorService
import os


flag = False

class MyHandler(FileSystemEventHandler):

    def __init__(self, data_folder):
        self.data_folder = data_folder

    def handle_new_file(self, file_path):
        # Обработка нового файла
        flag = True
        temp = os.path.basename(file_path)
        print(f"New file created: {file_path}")
        service = DataProcessorService(datasource=temp,
                                       db_connection_url="sqlite:///pikpo_2.sqlite")
        service.run_service(flag)

    def on_created(self, event):
        if event.is_directory:
            return None
        self.handle_new_file(event.src_path)


if __name__ == '__main__':
    service = DataProcessorService(datasource="COVID-19_Case_Surveillance_Public_Use_Data.csv",
                                   db_connection_url="sqlite:///pikpo_2.sqlite")
    service.run_service(flag)

    data_folder = "C:\\Users\\bossv\\PycharmProjects\\pythonProject12\\data"
    event_handler = MyHandler(data_folder)
    observer = Observer()
    observer.schedule(event_handler, data_folder, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
