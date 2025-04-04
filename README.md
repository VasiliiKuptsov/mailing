��  m a i l i n g 
 
 Создать администратора
python manage.py csu
Создать пользователя в группе "Пользователи"
python manage.py create_user
Создать пользователя в группе "Менеджеры"
python manage.py create_manager
Технологии:
Python
Bootstrap
Django
PostgreSQL
Redis
Описание:
Чтобы удержать текущих клиентов бизнеса, часто используются вспомогательные, или «прогревающие», рассылки для информирования и привлечения. В этом проекте вам нужно разработать сервис управления рассылками, администрирования и получения статистики.

Техническое задание на разработку веб-приложения с рассылкой сообщений
Создать веб-приложение на Django, которое позволяет пользователям управлять рассылками сообщений для клиентов. Приложение должно включать функциональность для создания, просмотра, редактирования и удаления рассылок, а также отправки сообщений по требованию.

Разработка сервиса:
Управление клиентами

Реализовать возможность добавлять, просматривать, редактировать и удалять получателей рассылки (клиентов).
Сущности системы

Модель «Получатель рассылки»:

Email (строка, уникальное).
Ф. И. О. (строка).
Комментарий (текст).
Модель «Рассылка»:

Дата и время первой отправки (datetime).
Дата и время окончания отправки (datetime).
Статус рассылки: завершена, создана, запущена.
Сообщение (внешний ключ на модель «Сообщение»).
Получатели («многие ко многим», связь с моделью «Получатель»).
Модель «Сообщение»:

Тема письма (строка).
Тело письма (текст).
Модель «Попытка рассылки»:

Дата и время попытки (datetime).
Ответ почтового сервера (текст).
Рассылка (внешний ключ на модель «Рассылка»).
Логика работы попытки рассылки

Попытка рассылки — это запись о каждой попытке отправки сообщения по рассылке. Она содержит информацию о том, была ли попытка успешной, когда она произошла и какой ответ вернул почтовый сервер.
Инициация отправки.

Попытка рассылки создается каждый раз, когда запускается процесс отправки сообщений для конкретной рассылки.
Определение получателей.

Список клиентов, которым должно быть отправлено сообщение, определяется из выбранных клиентов для данной рассылки.
Отправка сообщения:

Для каждого клиента из списка выполняется отправка письма с помощью функции send_mail() из Django. В случае успешной отправки письма создается запись в модели Попытка_рассылки со статусом «успешно». В случае ошибки отправки, например из-за недоступности почтового сервера, создается запись со статусом «не успешно» и текстом ошибки в поле «Ответ почтового сервера». Сбор статистики. Каждая попытка отправки письма фиксируется, что позволяет отслеживать успешные и неуспешные попытки, а также общее количество попыток.
Расширение функциональности
Регистрация и аутентификация пользователей

Реализовать систему регистрации и аутентификации пользователей.
Пользователи должны иметь возможность зарегистрироваться на сайте, подтвердив свой email.
Должна быть реализована функция входа и выхода из системы.
Необходимо предусмотреть возможность восстановления пароля.
Статистика и отчеты

Необходимо собирать и отображать информацию о количестве успешных/неуспешных попыток рассылок пользователя и количестве отправленных сообщений.
Ограничение доступа

Пользователи могут управлять только своими рассылками и клиентами.
Менеджеры могут просматривать все рассылки и клиентов, но не могут редактировать или удалять чужие данные.
Описание ролей и прав доступа:

Пользователь

Создание, просмотр, редактирование и удаление своих клиентов и рассылок.
Просмотр статистики по своим рассылкам.
Менеджер

Просмотр всех клиентов и рассылок.
Просмотр списка пользователей сервиса.
Блокировка пользователей сервиса.
Отключение рассылок.
