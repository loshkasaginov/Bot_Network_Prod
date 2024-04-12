Данный проект является реализацией сети чат ботов в связке с сервераом, которые выполняют функцию оптимизации процессов внутри компании.
В этом файле проект будет описан с трех сторон:

1) структура + немного отсылок на бизнес логику
2) frontend - описание кода ботов и логики построиения запросов
3) backend - описание кода сервера, технологий примененных на бэке

1:

Целью проекта является предоставление компании по ремонту орг-техники удобного интерфейса для взаимодействия кураторов, инженеров и стационарных инженеров.
Суперюзер имеет возможность добавлять, просматривать, удалять кураторов.
Кураторы имеют такой же функционал для инженеров и стационарных инженеров.

Основной сущностью является заказ(Order).
Куратор имеет возможность назначать заказ на инженера, а так же сопровождать заказ по мере его продвижения.
У заказа есть 5 стадий:
1) Согласование - инженер должен внести количество и сами варианты проведения работ, которые он предложил клиенту, а также сумму на которую удалось договориться, или сумму отказа и причину отказа.
2) Предоплата - инженер должен внести сумму предоплаты полученную от клиента.
3) Стационар - инженер имеет возможность сдать заказ в стационар, при этом он должен приложить фотографию техники в сервисном центре, дату до которой нужно сделать, описание проблемы.
4) Оприход - если в процессе починки были куплены детали, была доставка транспортом, и тд., инженер должен отчитаться о всех тратах с предоставлением чеков.
5) Отчет - инженер должен внести общую сумму полученную от клиента, сумму чистыми (без учета запчастей и стационара), приложить фотографию договора.

3 и 4 стадии являются опциональными, в некоторых заказах их может не быть.

схема бд: ![image](https://github.com/loshkasaginov/Bot_Network_Prod/assets/84158585/6172d28d-278a-4e6d-9a28-67503309dfa5)


2:
frontend:
- Aiogram. Библиотека для асинхронной разработки тг-ботов.
- Sqlite. Удобная легкая дб, для хранения access/refresh токенов на фронте
- Logger. Встроенная библиотека для логирования.
- aiohttp. Библиотека для асинхронной работы с requests.

Логика заказа:
1) Куратор создает заказ указывая номер заказа и имя инженера, на которого он хечет навесить этот заказ.
2) Инженер создает согласование.
3) Куратор может либо подтвердить созданное согласование, либо нет, тогда у инженера появляется возможность заного создать согласование. (данная схема подтверждения стадии будет идентична на всех следующих стадиях)
4) Инженер создает предоплату.
5) Куратор проверяет предоплату.
6) Инженер создает стационар.
7) Стационарный инженер видит все заказы в стационаре, может навесить на себя заказ.
8) Куратор может поменять приоритет заказа в стационаре.(по дэфолту 1)
9) Стационарный инженер создает отчет по стационару (сумму за свои работы), заказ переходит обратно инженеру.
10) Инженер создает оприход.
11) Куратор проверяет оприход.
12) Инженер создает отчет.
13) Куратор проверяет оприход.

Стадии стационара и оприхода - опциональные и могут быть пропущены инженером.

Взаимодействие с бэком происходит посредством отправки rest запросов (все rest запросы расположены в модуле asinc_requests.py). 
В sqlite хрятся логины пользователей с access и refresh токенами, которые раз в 20 часов обновляются.
Фотографии хранятся в ввиде ссылки на фотографию в чате бота в тг. Это позволяет избежать больших потерь по памяти, но является не самым практичным и защищенным вариантом,
поэтому критические фотографии (отчетов) сохраняются локально, но после того как отчет был подтвержден куратором.


3:
backend:
- Fastapi. Библиотека для написания сервера, в основе которого лежит асинхронность. Удобный, мощный инструмент.
- Postgresql. Реляционная БД.
- Pytest. Библиотека для написания асинхронных модульных тестов.
- Redis. No-sql база данных, память в оперативной памяти, что существенно ускоряет запись и забор данных. В проекте используется для кеширования.
- Centry. Удобный инструмент для логирования.
- OAuth2. Используется для авторизации/аутентификации с помощью jwt токенов.





