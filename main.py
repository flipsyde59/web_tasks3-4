from app import app

# Запускаем приложение
# Но лучше запускать через Flask

# Порт можно указать любой свободный.
# Если указать 80, то можно будет открывать просто по localhost без указания порта
# (так как 80 - стандартный для http).
# host=127.0.0.1 запустит на localhost, и приложение будет доступно только на нём.
# При запуске с host=0.0.0.0 (несуществующий хост) приложение будет доступно по всем сетевым интерфейсам.
# debug=True позволит красиво выводить ошибки,
# предупреждения и будет перезапускать сервер при изменении исходных файлов.
# Включаем режим разработки (аналог env FLASK_ENV=development)
app.env = 'development'
# Запускаем приложение (http-сервер)
# Будет доступно на http://localhost:3000
app.run(port=3000, host='localhost', debug=True)