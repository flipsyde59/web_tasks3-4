from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from .entities import User, Todo
from .storage import Storage
import re, json
# Создаём приложение
app = Flask(__name__)

# Конфигурируем
# Устанавливаем ключ, необходимый для шифрования куки сессии
app.secret_key = b'the-super-secret-key'


# Статичные файлы (css, js) доступны по /static
# https://flask.palletsprojects.com/en/1.1.x/quickstart/#static-files


# Описываем основные маршруты и их обработчики
# https://flask.palletsprojects.com/en/1.1.x/quickstart/#routing


# Главная страница
@app.route('/', methods=['GET'])
def home():
    # Пользователя получаем из сессии
    # https://flask.palletsprojects.com/en/1.1.x/quickstart/#sessions
    # Здесь сессия - это зашифрованные данные, хранящиеся в куках. Так эти данные есть во всех запросах этого сеанса.
    # Хотя можно работать с куки напрямую
    # https://flask.palletsprojects.com/en/1.1.x/quickstart/#cookies
    user=None
    todo=None
    list_l = 0
    if 'user_id' in session:
        user_id = session['user_id']
        # Получили пользователя из БД по ID
        user = Storage.get_user_by_id(user_id)
        todo = Storage.get_user_todos(user_id)
        if todo:
            list_l=len(todo)
        # Ренедрим страницу по шаблону
        # https://flask.palletsprojects.com/en/1.1.x/quickstart/#rendering-templates
        # https://jinja.palletsprojects.com/en/2.10.x/templates/
    return render_template('pages/index.html', user=user, len=list_l, todo=todo)
    #else:
        # Если пользователь не авторизован - перебрасываем на login
        #return redirect('/login')


# Страница с формой входа
@app.route('/login', methods=['GET'])
def login():
    # Если пользователь уже авторизован, перебросим на главную
    if 'user_id' in session:
        return redirect('/')
    return render_template('pages/login.html', page_title='Аuthentification')


# Обработка формы входа (не обязательно та же страница, но в этом случае так удобно вернуть ошибку)
# Шаблон с формой логина будет иметь не только форму, но и место для вывода ошибок
@app.route('/login', methods=['POST'])
def login_action():
    page_title = 'Вход | App'

    # Введённые данные получаем из тела запроса
    # https://flask.palletsprojects.com/en/1.1.x/quickstart/#accessing-request-data
    # Но сначала проверяем, что они вообще есть
    if not request.form['email']:
        return render_template('pages/login.html', page_title=page_title, error="Требуется ввести Email")
    if not request.form['password']:
        return render_template('pages/login.html', page_title=page_title, error="Требуется ввести пароль")

    # Ищем пользователя в БД с таким email и паролем
    user = Storage.get_user_by_email_and_password(request.form['email'], request.form['password'])

    # Неверный пароль
    if not user:
        return render_template('pages/login.html', page_title=page_title, error="Неверный пароль")

    # Сохраняем пользователя в сессии
    session['user_id'] = user.id

    # Перенаправляем на главную страницу
    # https://flask.palletsprojects.com/en/1.1.x/quickstart/#redirects-and-errors
    # Перенаправлять можно не только по URL, но и по имени роута
    return redirect(url_for('home'))


# Форма регистрации
@app.route('/registration', methods=['GET'])
def registration():
    return render_template('pages/registration.html', page_title='Регистрация | App')


# Обработка формы регистрации
@app.route('/registration', methods=['post'])
def registration_action():
    page_title = 'Регистрация | App'
    error = None
    # Проверяем данные
    if not request.form['email']:
        error = "Требуется ввести Email"
    if not request.form['password']:
        error = "Требуется ввести пароль"
    if not request.form['password2']:
        error = "Требуется ввести повтор пароля"
    if request.form['password'] != request.form['password2']:
        error = "Пароли не совпадают"
    # В случае ошибки рендерим тот же самый шаблон, но с текстом ошибки
    if Storage.is_user_registered(request.form['email']):
        err_text = 'Пользователь с таким email уже зарегистрирован'
    pattern_password = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$')
    if not pattern_password.match(request.form['password']):
        err_text = 'Пароль должен быть от 8-ми до 20 символов, содержать хотя бы одно число, ' \
                'хотя бы одну латинскую букву в нижнем и верхнем регистре, хотя бы один спец символ'
    if error:
        return render_template('pages/registration.html', page_title=page_title, error=error)
    # Добавляем пользователя
    Storage.add_user(User(None, request.form['email'], request.form['password']))
    # Делаем вид, что добавление всегда без ошибки
    # Перенаправляем на главную
    return redirect(url_for('home'))


# Выход пользователя
@app.route('/logout')
def logout():
    # Просто выкидываем его из сессии
    session.pop('user_id')
    return redirect(url_for('home'))

# Добавление/удаление задачи
@app.route('/', methods=['POST', 'DELETE', 'PATCH'])
def home_action():
    list_l = 0
    user_id = session['user_id']
    user = Storage.get_user_by_id(user_id)
    # AJAX Delete
    if request.method == 'DELETE':
        search = request.get_json()
        Storage.delete_todo(search['todo_id'])
        return jsonify(search)
    # AJAX Update
    if request.method == 'PATCH':
        search = request.get_json()
        Storage.update_todo_status(search['todo_id'], search['action'])
        return jsonify(search)
    todo = Storage.get_user_todos(user_id)
    if todo:
        list_l = len(todo)
    if not request.form['todo_name']:
        return render_template('pages/index.html', user=user, todo=todo, len=list_l,
                               error="Введите название для задачи")
    #if not request.form['todo_description']:
    #    return render_template('pages/index.html', user=user, todo=todo, len=list_l,
    #                           error="Введите описание для задачи")
    Storage.add_todo(Todo(None, request.form['todo_name'], user_id, 0))
    return redirect(url_for('home'))


# Получение задачи
@app.route('/getTodos', methods=['GET'])
def get_todos():
    user_id = session['user_id']
    todo = Storage.get_user_todos(user_id)
    todoList = [t.serialize() for t in todo]
    print(todoList)
    return json.dumps(todoList)

