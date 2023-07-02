# Подключаем объект приложения Flask из __init__.py
from labapp import app
# Подключаем библиотеку для "рендеринга" html-шаблонов из папки templates
from flask import render_template, make_response, request, jsonify

import labapp.webservice as webservice   # подключаем модуль с реализацией бизнес-логики обработки запросов

"""
    Модуль регистрации обработчиков маршрутов, т.е. здесь реализуется обработка запросов
    при переходе пользователя на определенные адреса веб-приложения
"""


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    """ Обработка запроса к индексной странице """
    # Пример вызова метода с выборкой данных из БД и вставка полученных данных в html-шаблон
    processed_files = webservice.get_source_files_list()
    # "рендеринг" (т.е. вставка динамически изменяемых данных) в шаблон index.html и возвращение готовой страницы
    return render_template('index.html',
                           title='MY BEST WEBSERVICE!!1',
                           page_name='HOME',
                           navmenu=webservice.navmenu,
                           processed_files=processed_files)


@app.route('/contact', methods=['GET'])
def contact():
    """ Обработка запроса к странице contact.html """
    return render_template('contact.html',
                           title='MY BEST WEBSERVICE!!1',
                           page_name='CONTACT US',
                           navmenu=webservice.navmenu)


@app.route('/data/<int:source_file_id>', methods=['GET'])
def get_data(source_file_id: int):
    """
        Вывод данных по идентификатору обработанного файла.
        Функция также пытается получить значение GET-параметра pageNum
        из запроса типа: http://127.0.0.1:8000/data/16?pageNum=2
    """

    processed_data = []
    pageNum = request.args.get('pageNum')
    if pageNum is not None:
        processed_data = webservice.get_processed_data(source_file=source_file_id, page_num=int(pageNum))
    else:
        processed_data = webservice.get_processed_data(source_file=source_file_id)
    return render_template('data.html',
                           title='MY BEST WEBSERVICE!!1',
                           page_name=f'DATA_FILE_{source_file_id}',
                           navmenu=webservice.navmenu,
                           processed_data=processed_data)


@app.route('/api/contactrequest', methods=['POST'])
def post_contact():
    """ Пример обработки POST-запроса для демонстрации подхода AJAX (см. formsend.js и ЛР№5 АВСиКС) """
    request_data = request.json     # получаeм json-данные из запроса
    # Если в запросе нет данных или неверный заголовок запроса (т.е. нет 'application/json'),
    # или в этом объекте, например, не заполнено обязательное поле 'firstname'
    if not request_data or request_data['firstname'] == '':
        # возвращаем стандартный код 400 HTTP-протокола (неверный запрос)
        return bad_request()
    # Иначе отправляем json-ответ с сообщением об успешном получении запроса
    else:
        msg = request_data['firstname'] + ", ваш запрос получен !"
        my_file = open("clients.txt", "a+")
        my_file.write(request_data["firstname"] + '\n')
        my_file.close()
        return jsonify({'message': msg})


@app.route('/notfound', methods=['GET'])
def not_found_html():
    """ Возврат html-страницы с кодом 404 (Не найдено) """
    return render_template('404.html', title='404', err={'error': 'Not found', 'code': 404})


def bad_request():
    """ Формирование json-ответа с ошибкой 400 протокола HTTP (Неверный запрос) """
    return make_response(jsonify({'message': 'Bad request !'}), 400)


@app.route("/shutdown", methods=['GET'])
def shutdown():
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        raise RuntimeError('Not running werkzeug')
    shutdown_func()
    return "Shutting down..."