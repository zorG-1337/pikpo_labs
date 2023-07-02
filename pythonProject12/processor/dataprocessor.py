from abc import ABC, abstractmethod     # подключаем инструменты для создания абстрактных классов
from typing import List

import pandas   # пакет для работы с датасетами

"""
    В данном модуле реализуются классы обработчиков для 
    применения алгоритма обработки к различным типам файлов (csv или txt).
    
    ВАЖНО! Если реализация различных обработчиков занимает большое 
    количество строк, то необходимо оформлять каждый класс в отдельном файле
"""


class DataProcessor(ABC):
    """ Родительский класс для обработчиков файлов """

    def __init__(self, datasource: str):
        # общие атрибуты для классов обработчиков данных
        self._datasource = datasource   # путь к источнику данных
        self._dataset = None            # входной набор данных
        self.result = None              # выходной набор данных (результат обработки)

    # Все методы, помеченные декоратором @abstractmethod, ОБЯЗАТЕЛЬНЫ для переопределения в классах-потомках
    @abstractmethod
    def read(self) -> bool:
        """ Метод, инициализирующий источник данных """
        pass

    @abstractmethod
    def run(self) -> None:
        """ Метод, запускающий обработку данных """
        # Создаем пустой DataFrame в атрибуте класса для сохранения результатов обработки
        self.result = pandas.DataFrame()
        # удаляем ненужные колонки из входного набора данных
        cleaned_result = self.remove_col_by_name(self._dataset, ["A", "P", "C"])
        target_values = [1, 2, 3]  # значения колонки "target" для фильтрации
        for t in target_values:
            # фильтруем строки по каждому возможному значению колонки "target" и вычисляем среднее
            mean_result = self.get_mean_value_by_filter(cleaned_result, f"target == {t}")
            # полученный результат (DataFrame) на каждой итерации добавляем в результирующий DataFrame в self.result
            self.result = pandas.concat([self.result, mean_result], ignore_index=True)

    """
        Ниже представлены примеры различных методов для обработки набора данных.
        Основные методы для работы с объектом DataFrame см. здесь: 
        https://pandas.pydata.org/docs/reference/general_functions.html
        
        ВАЖНО! Следует логически разделять методы обработки, например, отдельный метод для сортировки, 
        отдельный метод для удаления "пустот" в датасете (очистка) и т.д. Это позволит гибко применять необходимые
        методы при переопределении метода run для того или иного типа обработчика.
        
        Также обратите внимание на то, что названия методов и функций для обработки должны быть ОСМЫСЛЕННЫМИ, т.е. 
        предоставлять информацию о том, что конкретно выполняет данный метод или функция.
    """

    def sort_data_by_col(self, df: pandas.DataFrame, colname: str, asc: bool) -> pandas.DataFrame:
        """
            Метод sort_data_by_col просто сортирует входной датасет по наименованию
            заданной колонки (аргумент colname) и устанвливает тип сортировки:
            ascending = True - по возрастанию, ascending = False - по убыванию
        """
        return df.sort_values(by=[colname], ascending=asc)

    def remove_col_by_name(self, df: pandas.DataFrame, col_name: List[str]):
        """
            Метод remove_col_by_name принимает входной набор данных и список имён колонок для удаления.
            Возвращает набор данных с удалёнными колонками.
        """
        return df.drop(col_name, axis=1)

    def get_mean_value_by_filter(self, df: pandas.DataFrame, filter_expr: str) -> pandas.DataFrame:
        """
            Метод get_mean_value_by_filter выбирает из входного набора данных строки с заданным условием
            (фильтр), используя инструкцию DataFrame.query(), применяет к получившимся значением функцию
            mean (считает среднее значения в колонках) и возвращает результат в виде нового DataFrame.

            Подробнее по фильтрации строк с помощью query() см.: https://sparkbyexamples.com/pandas/pandas-filter-by-column-value/
        """
        result = df.query(filter_expr)
        return result.mean(axis=0, skipna=True).to_frame().T

    @abstractmethod
    def print_result(self) -> None:
        """ Абстрактный метод для вывода результата на экран """
        pass


class CsvDataProcessor(DataProcessor):
    """ Реализация класса-обработчика csv-файлов """

    def __init__(self, datasource: str):
        # Переопределяем конструктор родительского класса
        DataProcessor.__init__(self, datasource)    # инициализируем конструктор родительского класса для получения общих атрибутов
        self.separators = [';', ',', '|']        # список допустимых разделителей

    """
        Переопределяем метод инициализации источника данных.
        Т.к. данный класс предназначен для чтения CSV-файлов, то используем метод read_csv
        из библиотеки pandas
    """

    def run(self):
        # cleaned_result = self.remove_col_by_name(self._dataset, ["data_postavki", "cdc_report_dt", "pos_spec_dt", "onset_dt"])
        target_values = ["sex"]
        for t in target_values:
            cleaned_result = self.sort_data_by_col(self._dataset, t, False)
            self.result = pandas.concat([self.result, cleaned_result], ignore_index=True)


    def read(self):
        try:
            # Пытаемся преобразовать данные файла в pandas.DataFrame, используя различные разделители
            for separator in self.separators:
                self._dataset = pandas.read_csv(self._datasource, sep=separator, header='infer', names=None, encoding="utf-8")
                # Читаем имена колонок из файла данных
                col_names = self._dataset.columns
                # Если количество считанных колонок > 1 возвращаем True
                if len(col_names) > 1:
                    print(f'Columns read: {col_names} using separator {separator}')
                    return True
        except Exception as e:
            print(e)
        return False

    def print_result(self):
        print(f'Running CSV-file processor!\n', self.result)


class TxtDataProcessor(DataProcessor):
    """ Реализация класса-обработчика txt-файлов """

    def read(self):
        """ Реализация метода для чтения TXT-файла (разедитель колонок - пробелы) """
        try:
            self._dataset = pandas.read_table(self._datasource, sep='\s+', engine='python')
            col_names = self._dataset.columns
            if len(col_names) < 2:
                return False
            return True
        except Exception as e:
            print(str(e))
            return False

    def print_result(self):
        print(f'Running TXT-file processor!\n', self.result)
