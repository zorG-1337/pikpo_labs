from typing import List

from .connector import StoreConnector
from datetime import datetime
from pandas import DataFrame, Series
"""
    В данном модуле реализуется API (Application Programming Interface)
    для взаимодействия с БД с помощью объектов-коннекторов.
    
    ВАЖНО! Методы должны быть названы таким образом, чтобы по названию
    можно было понять выполняемые действия.
"""


def select_all_from_source_files(connector: StoreConnector) -> List[tuple]:
    """ Вывод списка обработанных файлов с сортировкой по дате в порядке убывания (DESCENDING) """
    query = f'SELECT * FROM source_files ORDER BY processed DESC'
    result = connector.execute(query).fetchall()
    return result


def select_rows_from_processed_data(connector: StoreConnector, source_file: int, offset: int = None, limit: int = 10) -> List[tuple]:
    """ Выборка строк из таблицы с обработанными данными.
        offset - смещение строк при выборке.
        limit - количество строк в выбоке.
        Например, при запросе: SELECT * FROM processed_data WHERE source_file = {source_file} LIMIT 20,10
        будет выбрано 10 строк, начиная с 21-ой.
    """
    result = []
    if limit is None or offset is None:
        result = connector.execute(f"SELECT * FROM processed_data WHERE source_file = {source_file}").fetchall()
    else:
        result = connector.execute(f"SELECT * FROM processed_data WHERE source_file = {source_file} "
                                   f"LIMIT {offset*limit},{limit}").fetchall()
    return result

def select_all_from_processed_data(connector: StoreConnector) -> List[tuple]:
    """ Вывод списка обработанных файлов с сортировкой по дате в порядке убывания (DESCENDING) """
    # query = f'SELECT * FROM source_files ORDER BY processed DESC'
    query = f'SELECT * FROM processed_data'
    result = connector.execute(query).fetchall()
    return result

def insert_into_source_files(connector: StoreConnector, filename: str):
    """ Вставка в таблицу обработанных файлов """
    now = datetime.now()        # текущая дата и время
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")   # преобразуем дату в формат SQL, например, '2022-11-15 22:03:16'
    query = f'INSERT INTO source_files (filename, processed) VALUES (\'{filename}\', \'{date_time}\')'
    result = connector.execute(query)
    return result

def insert_rows_into_processed_data(connector: StoreConnector, dataframe: DataFrame):
    """ Вставка строк из DataFrame в БД с привязкой данных к последнему обработанному файлу (по дате) """
    rows = dataframe.to_dict('records')
    files_list = select_all_from_source_files(connector)    # получаем список обработанных файлов
    # т.к. строка БД после выполнения SELECT возвращается в виде объекта tuple, например:
    # row = (1, 'seeds_dataset.csv', '2022-11-15 22:03:16'),
    # то значение соответствующей колонки можно получить по индексу, например id = row[0]
    last_file_id = files_list[0][0]  # получаем индекс последней записи из таблицы с файлами
    if len(files_list) > 0:
        for row in rows:
            connector.execute(
                'INSERT INTO processed_data (current_status, sex, age_group, race_ethnicity_combined, hosp_yn, icu_yn, death_yn, medcond_yn, source_file) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}");'.format(
                    row["current_status"],
                    row["sex"],
                    row["age_group"],
                    row["race_ethnicity_combined"],
                    row["hosp_yn"],
                    row["icu_yn"],
                    row["death_yn"],
                    row["medcond_yn"],
                    last_file_id


                )
            )
            #connector.execute(f'INSERT INTO processed_data (current_status, sex, age_group, race_ethnicity_combined, hosp_yn, icu_yn, death_yn, medcond_yn, source_file) VALUES (\'{row["current_status"]}\', \'{row["sex"]}\', \'{row["age_group"]}\',\'{row["race_ethnicity_combined"]}\',\'{row["hosp_yn"]}\',\'{row["icu_yn,death_yn"]}\', \'{row["medcond_yn"]}\'{last_file_id})')
        print('Data was inserted successfully')
    else:
        print('File records not found. Data inserting was canceled.')

def create_table(connector: StoreConnector, table: str):
    """ Создание таблицы в БД"""
    connector.execute(
        'CREATE TABLE "{}"'.format(
            table
        )
    )
    print('Table was created successfully')


def update_rows_into_processed_data_by_condition(connector: StoreConnector, new_row: dict, condition: str):
    """ Обновление записей в БД"""
    connector.execute(
        'UPDATE processed_data SET current_status = "{}", sex = "{}", age_group = "{}", race_ethnicity_combined = "{}", hosp_yn = "{}", icu_yn = "{}", death_yn = "{}", medcond_yn = "{}" WHERE {};"'.format(
                                                                                                                           new_row["current_status"],
                                                                                                                           new_row["sex"],
                                                                                                                           new_row["age_group"],
                                                                                                                           new_row["race_ethnicity_combined"],
                                                                                                                           new_row["hosp_yn"],
                                                                                                                           new_row["icu_yn"],
                                                                                                                           new_row["death_yn"],
                                                                                                                           new_row["medcond_yn"],


                                                                                                                           condition
                                                                                                                           )
    )
    print('Data was updated successfully')

def delete_all_in_processed_data(connector: StoreConnector):
    """ Удаление всех данных из таблицы"""
    connector.execute(
        'DELETE FROM processed_data;'
    )

def update_rows(connector: StoreConnector, old: str, new: str):
    """ Обновление записей в БД"""
    connector.execute(
        f'UPDATE processed_data SET sex={new} WHERE sex={old}'
    )

