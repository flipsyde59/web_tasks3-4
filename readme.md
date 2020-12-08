# ToDo Сервис AJAX

## Лабораторная работа № 3: ToDo Сервис
> Максимум 10 баллов. Часть Контрольной точки 3: PHP. Разработка динамических web-страниц
### Требуется реализовать простой веб-сайт “ToDo Сервис”
#### Веб-сайт позволяет пользователям создавать задачи (название и описание), просматривать список задач и удалять задачи. Веб-сайт должен быть реализован на традиционных технологиях, при которых содержимое рендерится на стороне сервера посредством шаблонов (на любом языке программирования). В приложении должно быть как минимум две страницы: страница со списком задач и формой добавления задачи, страница просмотра задачи. Можно делать больше страниц

### Критерии:
- [x] (5б) Реализован веб-сайт, позволяющий просматривать, добавлять и удалять задачи;
- [x] (2б) В приложении присутствует регистрация пользователей и авторизация, при которой пользователь может просматривать только свои задачи;
- [x] (2б) Список задач (и пользователей) хранится в БД (SQL или MongoDB), и не теряется при перезапуске сервера;
- [x] (1б) Приложение удовлетворяет минимальным требованиям безопасности: защита от SQL-инъекций, пароль пользователя хранится в хешированном виде, пользователь не может взаимодействовать с чужими задачами.

## Лабораторная работа № 4: ToDo AJAX
> Максимум 10 баллов. Часть Контрольной точки 4: Ajax. Запросы к серверу
### Требуется доработать разработанный в лабораторной работе 3 ToDo сервис
#### Реализовать удаление задач на AJAX. По нажатию на кнопку удалить у задачи в списке задач, соответствующая задача должна быть удалена из БД, а со страницы должен быть удалён её элемент. Добавить задачам логическое свойство состояния (выполнена/не выполнена), а также изменение состоянии задачи на AJAX. На страницу задачи добавить подгружаемые комментарии (Можно имитирует серверную часть либо при помощи мока API (например: https://github.com/ctimmerm/axios-mock-adapter), либо используя placeholder (например: https://jsonplaceholder.typicode.com взять комментарии, связанные с Post с таким же ID, как ID этой задачи)).

### Критерии:
  - [x] (2.5 б.) Реализовано удаление задач на AJAX;
  - [x] (2.5 б.) Реализовано изменение состояния задачи на AJAX;
  - [x] (2.5 б.) Реализовано отображение комментариев у задач;
  - [x] (2.5 б.) Приложение имеет дружелюбный и интерфейс.
