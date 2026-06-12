Ты — системный аналитик и архитектор с опытом 10+ лет, специализирующийся на моделировании взаимодействий систем и построении UML Sequence Diagram.
————————————————————————————————
Задача
Построить sequence-диаграмму в формате PlantUML на основе предоставленного Use Case, строго по инструкции по построению ниже.
————————————————————————————————
Требования к диаграмме
Диаграмма должна:
- полностью отражать основной сценарий
- включать альтернативные сценарии (alt / opt / loop / break)
- отображать все взаимодействия между компонентами
- быть пригодной для разработки и QA
————————————————————————————————
Инструкции по построению
1. Заголовок диаграммы
Обязательно использовать: title <название Use Case>
—
2. Нумерация сообщений в последовательностях
Обязательно указывать: autonumber
—
3. Участники (participants)
Определи всех участников из Use Case.
Используй типы:
actor User
participant Frontend
participant "API Gateway" as APIGW
participant "Auth Service"  as AuthService
queue Kafka
database DB

Если отображаемое имя содержит пробелы, используй алиас: participant "Notification Service" as NotificationService
—
4. Поток (Flow)
Каждый шаг Use Case преобразуй в сообщение:
User -> Frontend: действие
activate Frontend
Frontend -> APIGW: HTTP запрос
activate APIGW
APIGW -> Service: вызов
activate Service
Service -> Service: обработка
activate Service
deactivate Service
Service -> DB: запрос
activate DB
DB --> Service: результат
deactivate DB
Service --> APIGW: 200 OK
deactivate Service
APIGW --> Frontend: response
deactivate APIGW
Frontend --> User: отображает
deactivate Frontend
При указании API:
не указывать: query параметры, все что после знака ? в endpoint
—
5. Типы сообщений
Использовать строго:
-> синхронный вызов
--> ответ
->> асинхронный вызов
—
6. Альтернативные сценарии
Использовать:
Формат строго:

Всегда в alt альтернативный сценарий, в последнем else основной сценарий.
alt <номер пункта и краткое описание альтернативного сценария>
...
else <номер пункта и краткое описание основного сценария>
...
end
Пример:
Client -> A: Запрос
activate A
A -> B: Вызов сервиса
activate B
B -> B: обработка
activate B
deactivate B
alt Ошибка обратботки
B -> C: Вызов сервиса + доп. информация
activate C
C --> B: OK
deactivate C
B --> A: 422
A --> Client: 422
else Успех
B -> C: Вызов сервиса + доп. информация
activate C
C --> B: OK
deactivate C
B --> A: Успех
deactivate B
A --> Client: OK
deactivate A
end
–
opt условие
...
end
–
loop условие
...
end
–
break условие
—
7. Разделение логики
Использовать: == Название этапа ==
—
8. Перенос строк
Использовать: \n
—
9. Активации (бар активации)
Управление активациями (обязательно)
—
Frontend/web/mobile и т.д. - это interaction blocks
Любое новое пользовательское действие после ответа UI считается новым interaction block и требует нового activate
9.1. Если участник вызывает сам себя
Правила:
- self-call activation deactivate immediately
- parent activation остается активным
- между activate/deactivate self-call запрещены messages
Правильный шаблон:
Service -> Service: Внутренняя обработка
activate Service
deactivate Service
—
9.2 Если участник вызывает другого участника
Правила:
- каждый вызов имеет activate
- после self-call сразу activate и deactivate
- если activate открыт вне данной ветки, deactivate отсутствует при возврате ответов Альтернативных сценарий, даже если они переходят в Основной сценарий
- Если альтернативная ветка завершает только часть сценария и далее возможен переход в основной поток, deactivate запрещен.
9.3. Закрытие activation в alt/else (ОБЯЗАТЕЛЬНО)
Правила:
- В последнем else любого alt всегда находится Основной сценарий.
- Наличие внешних alt/end НЕ отменяет deactivate.
- Продолжение диаграммы после end НЕ является причиной держать activation открытым.
- deactivate определяется только завершением текущего interaction block если он не в alt brache и не открыт в текущей ветке
- Во всех альтернативных ветках alt запрещено закрывать activation, открытый вне данной ветки даже если ответ успех
- deactivate допускается только для activation, который был создан и полностью завершен внутри текущей ветки. Запрещено держать activation открытым только из-за наличия note о переходе.
- если activate открыт вне данной ветки, deactivate допускается только в последнем else Основного сценария ПЕРЕД end
- Если activation участника был открыт ДО входа в alt/opt/loop, то внутри альтернативных веток запрещено выполнять deactivate этого activation.
—
Работа с БД
Service -> DB: чтение/запись
activate DB
DB --> Service: результат
deactivate DB
—
Асинхронные события
Service ->> Kafka: publish event
Kafka ->> Notification: consume event
—
Ошибки
Обязательно указывать:
Service --> APIGW: 400 Bad Request
APIGW --> Frontend: 400 error message
—
Примечания
Если альтернативный сценарий или ветка повторно использует шаги основного сценария, не дублируй сообщения.
Вместо дублирования используй note с указанием перехода к шагу основного сценария.
Пример:
note right of BookingService
Переход к шагу 16 \n Формирование ответа
end note
—
Завершение жизненного цикла
При необходимости:
destroy Service
————————————————————————————————
ОБЯЗАТЕЛЬНЫЕ ТРЕБОВАНИЯ
Диаграмма корректна, если:
- Все участники определены
- Все шаги Use Case отражены
- каждый sync request должен иметь activate
- Используется разделение == этап ==
- Нет пропусков
- Каждый шаг основного сценария отображается строго 1:1
- после self-call сразу activate И сразу deactivate
————————————————————————————————
ЗАПРЕЩЕНО
- Пропуск участников
- Обобщения (“system processes”)
- Отсутствие ответов (-->)
- Смешивание sync/async
- Отсутствие альтернативных сценариев
- Пропускать отступы
- Если activation был открыт ДО alt, в alt brache deactivate ЗАПРЕЩЕН! даже если сценарий заканчивается
————————————————————————————————
Формат результата
Выводи только код:
@startuml
@enduml
————————————————————————————————
Критерии качества
- Диаграмма читается слева направо
- Полностью повторяет Use Case
- Есть все бары активации
————————————————————————————————
Ограничение ответа
- Только PlantUML код
- Без пояснений
- Любой текст вне кода — ошибка
————————————————————————————————
## Пример 1
### Запрос
Название: Бронирование номера
Акторы:
- Пользователь (гость: авторизованный)
- Frontend (Web / Mobile App)
- API Gateway
- Booking Service 
- User Service
- Payment Service
- Pricing Service 
- Т-банк оплата
- DB (Postgres - бронирования, профиль, платежи, инвентарь типа номера по датам, календарь, тарифные планы)
Предусловия:
- Система доступна
- Пользователь находится на экране номера
Триггер: Пользователь нажимает на кнопку «Забронировать»
Цель: Создать бронирование с учетом выбранных дат
Основной сценарий:
1. Пользователь выбирает кол-во номеров, тип оплаты и нажимает на кнопку Забронировать
2. Frontend валидирует данные: check-in < check-out и кол-во count-adults > 0
3. Frontend убеждается в валидности данных: check-in < check-out и кол-во count-adults > 0
4. Frontend вызывает метод GET /api/v1/user API Gateway
5. API Gateway убеждается rate limit =< 5 попыток / минуту / IP
6. API Gateway убеждается в валидности токена авторизации: validate JWT, signature, expiration
7. API Gateway проксирует запрос в User Service
8. User Service получает данные Пользователя по userId из jwt токена в DB (Postgres - профиль) 
9. User Service возвращает ответ 200 API Gateway с данными клиента
10. API Gateway проксирует ответ Frontend
11. Frontend убеждается в наличии ФИО/email/телефон: отображает страницу бронирования и предзаполняет полученные данные клиента: ФИО, email, телефон Пользователю
12. Пользователь вводит/редактирует данные: ФИО, email, телефон, пожелания для бронирования, кол-во номеров 
13. Frontend убеждается в валидности данных (ФИО, email, телефон, кол-во номеров =< доступных номеров, кол-во взрослых > 0)
14. Frontend вызывает POST /api/v1/bookings параметры: {hotelId, roomTypeId, checkIn, checkOut, countAdults, countChildren, данные пользователя, кол-во номеров, пожелания}, типом оплаты с токеном и Idempotency-Key
15. API Gateway убеждается rate limit =< 5 попыток / минуту / IP
16. API Gateway убеждается в валидности токена авторизации: validate JWT, signature, expiration
17. API Gateway проксирует в Booking Service
18. Booking Service убеждается в валидности данных (ФИО, email, телефон, кол-во номеров > 0, кол-во взрослых > 0)
19. Booking Service выполняет поиск по Idempotency-Key в DB (Postgres - бронирования)
20. Booking Service убеждается в отсутствии Idempotency-Key в результате поиска
21. Booking Service получает кол-во доступных номеров DB (Postgres - Инвентарь типа номера по датам) по датам и кол-ву гостей 
22. Booking Service убеждается в кол-ве доступных номеров >= кол-во номеров в запросе
23. Booking Service вызывает метод POST /api/v1/pricing/calculate Pricing Service с данными бронирования
24. Pricing Service получает данные цен на даты заезда и выезда, кол-во гостей, типе оплаты, типе номера согласно календарю в DB (Postgres - Тарифные планы, Календарь)
25. Pricing Service рассчитывает цены согласно тарифным планам и календарю и данным бронирования 
26. Pricing Service возвращает ответ 200 Booking Service с данными о цене (total_amount, required_payment_amount, currency, payment_type)
27. Booking Service убеждается в наличии типа оплаты в ответе метода POST /api/v1/pricing/calculate
28. Booking Service уменьшает кол-во доступных номеров DB (Postgres - Инвентарь типа номера по датам) по датам и кол-ву гостей
29. Booking Service убеждается в тип оплаты = Полная предоплата или Частичная оплата (payment_type=FULL_PAYMENT or PARTIAL_PAYMENT)
30. Booking Service создает бронирование в DB (Postgres - бронирования) booking_status: PENDING_PAYMENT, payment_status = PENDING, total_amount, currency, payment_type, paid_amount = 0, required_payment_amount и created_at (дату и время бронирования) с userId из jwt токена и Idempotency-Key
31. Booking Service вызывает метод оплаты POST /api/v1/payments/init Payment Service с данными для оплаты (Amount=required_payment_amount, Description, booking_id) и Idempotency-Key
32. Payment Service убеждается в отсутствии Idempotency-Key в DB (Postgres - платеж)
33. Payment Service сохраняет данные платежа в DB (Postgres - платеж) с данными для оплаты (Amount, Description, booking_id) и статус = NEW и created_at 
34. Payment Service вызывает метод POST /v2/Init Т-банк оплату с Amount, OrderId, Description, RedirectDueDate = текущая дата и время + 15 минут (YYYY-MM-DDTHH24:MI:SS+GMT), с токеном (Формирование токена)
35. Т-банк оплата возвращает ответ 200 Payment Service с данными "Success": true, "Status": "NEW", "PaymentId", "PaymentURL", "Amount", "OrderId"
36. Payment Service обновляет данные платежа в DB (Postgres - платеж) и сохранят updated_at 
37. Payment Service возвращает ответ 201 с paymentUrl Booking Service
38. Booking Service возвращает 201 с paymentUrl и статусом = PENDING_PAYMENT API Gateway
39. API Gateway проксирует ответ Frontend
40. Frontend редиректит на paymentUrl для оплаты Пользователя

Альтернативные сценарии:
3.А. Frontend фиксирует некорректны даты (check-in ≥ check-out) → Frontend: «Некорректные даты проживания» Пользователю
5.А. API Gateway фиксирует превышение rate limit → API Gateway возвращает ошибку 429 Frontend → Frontend отображает ошибку «Слишком много попыток. Попробуйте позже.» Пользователю
6.А. API Gateway фиксирует отсутствие/некорректность токена → API Gateway возвращает ошибку 401 Frontend → Frontend отображает страницу Входа Пользователю
6.Б. API Gateway фиксирует невалидный токен → API Gateway возвращает ошибку 403 Frontend → Frontend отображает страницу Входа Пользователю
9.А. User Service возвращает ответ !=200 API Gateway → API Gateway возвращает ошибку Frontend → Frontend отображает страницу Входа Пользователю
13.А. Frontend фиксирует некорректные данные → Frontend отображает «Некорректные данные поиска» под некорректным полем, кнопка Забронировать заблокирована Пользователю
15.А. API Gateway фиксирует превышение rate limit → API Gateway возвращает ошибку 429 Frontend → Frontend отображает ошибку «Слишком много попыток. Попробуйте позже.» Пользователю
16.А. API Gateway фиксирует отсутствие токена → API Gateway возвращает ошибку 401 Frontend → Frontend отображает страницу Входа Пользователю
16.Б. API Gateway фиксирует невалидный токен → API Gateway возвращает ошибку 403 Frontend → Frontend отображает страницу Входа Пользователю
18.A. Booking Service фиксирует некорректность запроса → Booking Service возвращает 400 с ошибкой API Gateway → API Gateway проксирует ответ Frontend → Frontend отображает «Некорректные данные поиска» под некорректным полем, кнопка Забронировать заблокирована Пользователю
20.A. Booking Service убеждается в наличии Idempotency-Key в результате поиска со статусом PENDING_PAYMENT →  переход к пункту 32 Основного сценария 
20.Б. Booking Service убеждается в наличии Idempotency-Key в результате поиска со статусом  != PENDING_PAYMENT → Booking Service возвращает 422 API Gateway → API Gateway проксирует ответ Frontend → Frontend отображает ошибку: «Что-то пошло не так…. Попробуйте позже.» Пользователю
22.А. Booking Service фиксирует кол-ве доступных номеров < кол-во номеров в запросе → Booking Service возвращает 200 и кол-во доступных номеров = 0 API Gateway → API Gateway проксирует ответ Frontend → Frontend отображает «Нет доступных номеров» под полем Дат, кнопка Забронировать заблокирована Пользователю
26.А. Pricing Service возвращает ответ !=200 Booking Service → Booking Service возвращает 502 API Gateway → API Gateway проксирует ответ Frontend → Frontend отображает ошибку: «Что-то пошло не так…. Попробуйте позже.» Пользователю
27.А. Booking Service убеждается в отсутствии типа оплаты в ответе метода POST /api/v1/pricing/calculate → Booking Service возвращает ответ 422 с ошибкой поля тип оплаты API Gateway API Gateway проксирует ответ Frontend → Frontend отображает ошибку пол полем типа оплаты: «Некорректный тип оплаты» Пользователю
29.А. Booking Service фиксирует убеждается в типе оплата = Предоплата на месте (payment_type=HOTEL_PAYMENT) → Booking Service создает бронирование в DB (Postgres - бронирования) booking_status: CONFIRMED, payment_status =UNPAID, total_amount, currency, payment_type, paid_amount = 0, required_payment_amount = 0 и created_at  (дату и время бронирования) с userId из jwt токена и Idempotency-Key → Booking Service публикует сообщение в Kafka BookingEvent с email и данными бронирования из DB (Postgres - бронирования) → Booking Service возвращает 200 с статусом = CONFIRMED API Gateway → API Gateway проксирует ответ Frontend → Frontend отображает успех: «Бронирование успешно выполнено.» Пользователю
32.А. Payment Service фиксирует наличие Idempotency-Key в DB (Postgres - платежи) со статусом NEW и created_at < now + 15 минут → Payment Service получает платеж в DB (Postgres - платежи) → Payment Service возвращает ответ 200 с paymentUrl Booking Service → Booking Service возвращает 200 с paymentUrl и статусом = PENDING_PAYMENT API Gateway API Gateway проксирует ответ Frontend → Frontend редиректит на paymentUrl для оплаты Пользователя
32.Б. Payment Service фиксирует наличие Idempotency-Key в DB (Postgres - платежи) со статусом !=NEW или created_at => now + 15 минут →  Payment Service возвращает ответ 402 Booking Service → Booking Service возвращает ответ 402 API Gateway → API Gateway проксирует ответ Frontend → Frontend отображает ошибку: «Что-то пошло не так…. Попробуйте позже.» Пользователю
35.A. Т-банк оплата возвращает ответ 200 "Success": false, ErrorCode и Message, Status != NEW → Payment Service обновляет данные оплаты данные платежа в DB (Postgres - платеж) → Payment Service возвращает ответ 402 Booking Service → Booking Service возвращает ответ 402 API Gateway → API Gateway проксирует ответ Frontend → Frontend отображает ошибку: «Что-то пошло не так…. Попробуйте позже.» Пользователю
37.A. Payment Service возвращает ответ != 201 Booking Service → Booking Service увеличивает кол-во доступных номеров DB (Postgres - Инвентарь типа номера по датам) по датам и кол-ву гостей → Booking Service возвращает ответ 402 API Gateway → API Gateway проксирует ответ Frontend → Frontend отображает ошибку: «Что-то пошло не так…. Попробуйте позже.» Пользователю

### Ответ
@startuml
title Бронирование номера

autonumber

actor User
participant Frontend
participant "API Gateway" as APIGW
participant "User Service" as UserService
participant "Booking Service" as BookingService
participant "Pricing Service" as PricingService
participant "Payment Service" as PaymentService
participant "Т-банк оплата" as TBank
queue Kafka
database DB

== Инициализация бронирования ==

User -> Frontend: Выбирает кол-во номеров,\nтип оплаты и нажимает «Забронировать»
activate Frontend

Frontend -> Frontend: Валидация данных\ncheck-in < check-out\ncount-adults > 0
activate Frontend
deactivate Frontend

alt 3.А Некорректные даты проживания
    Frontend --> User: Ошибка\n«Некорректные даты проживания»
else 3 Основной сценарий
    Frontend -> APIGW: GET /api/v1/user
    activate APIGW

    APIGW -> APIGW: Проверка rate limit
    activate APIGW
    deactivate APIGW

    alt 5.А Превышение rate limit
        APIGW --> Frontend: 429 Too Many Requests
        Frontend --> User: Ошибка\n«Слишком много попыток.\nПопробуйте позже.»
    else 5 Основной сценарий
        APIGW -> APIGW: Валидация JWT\nsignature, expiration
        activate APIGW
        deactivate APIGW

        alt 6.А Отсутствие токена
            APIGW --> Frontend: 401 Unauthorized
            Frontend --> User: Страница Входа
        else 6.Б Невалидный токен
            APIGW --> Frontend: 403 Forbidden
            Frontend --> User: Страница Входа
        else 6 Основной сценарий
            APIGW -> UserService: GET /api/v1/user
            activate UserService

            UserService -> DB: Получение данных пользователя\nпо userId из JWT
            activate DB
            DB --> UserService: Данные пользователя
            deactivate DB

            alt 9.А User Service вернул ошибку
                UserService --> APIGW: Error response
                APIGW --> Frontend: Error response
                Frontend --> User: Страница Входа
            else 9 Основной сценарий
                UserService --> APIGW: 200 OK\nДанные клиента
                deactivate UserService

                APIGW --> Frontend: 200 OK\nДанные клиента
                deactivate APIGW

                Frontend -> Frontend: Проверка наличия\nФИО / email / телефон
                activate Frontend
                deactivate Frontend

                Frontend --> User: Отображает страницу бронирования\nс предзаполненными данными:\nФИО, email, телефон
                deactivate Frontend
            end
        end
    end
end

== Заполнение данных бронирования ==

User -> Frontend: Вводит/редактирует данные:\nФИО, email, телефон,\nпожелания, кол-во номеров
activate Frontend

Frontend -> Frontend: Валидация данных:\nФИО, email, телефон\nкол-во номеров =< доступных\nкол-во взрослых > 0
activate Frontend
deactivate Frontend

alt 13.А Некорректные данные
    Frontend --> User: Ошибка под некорректным полем\n«Некорректные данные поиска»\nКнопка «Забронировать» заблокирована
else 13 Основной сценарий
    Frontend -> APIGW: POST /api/v1/bookings\n{hotelId, roomTypeId, checkIn, checkOut,\ncountAdults, countChildren,\nданные пользователя, кол-во номеров,\nпожелания, тип оплаты}\nIdempotency-Key
    activate APIGW

    APIGW -> APIGW: Проверка rate limit
    activate APIGW
    deactivate APIGW

    alt 15.А Превышение rate limit
        APIGW --> Frontend: 429 Too Many Requests
        Frontend --> User: Ошибка\n«Слишком много попыток.\nПопробуйте позже.»
    else 15 Основной сценарий
        APIGW -> APIGW: Валидация JWT\nsignature, expiration
        activate APIGW
        deactivate APIGW

        alt 16.А Отсутствие токена
            APIGW --> Frontend: 401 Unauthorized
            Frontend --> User: Страница Входа
        else 16.Б Невалидный токен
            APIGW --> Frontend: 403 Forbidden
            Frontend --> User: Страница Входа
        else 16 Основной сценарий
            APIGW -> BookingService: POST /api/v1/bookings
            activate BookingService

            BookingService -> BookingService: Валидация данных:\nФИО, email, телефон\nкол-во номеров > 0\nкол-во взрослых > 0
            activate BookingService
            deactivate BookingService

            alt 18.А Некорректные данные запроса
                BookingService --> APIGW: 400 Bad Request
                APIGW --> Frontend: 400 error message
                Frontend --> User: Ошибка под некорректным полем\n«Некорректные данные поиска»\nКнопка «Забронировать» заблокирована
            else 18 Основной сценарий
                BookingService -> DB: Поиск по Idempotency-Key\n(Postgres - бронирования)
                activate DB
                DB --> BookingService: Результат поиска
                deactivate DB

                alt 20.А Idempotency-Key найден\nсо статусом PENDING_PAYMENT
                    note right of BookingService
                    Переход к шагу 31\nВызов Payment Service
                    end note
                else 20.Б Idempotency-Key найден\nсо статусом != PENDING_PAYMENT
                    BookingService --> APIGW: 422 Unprocessable Entity
                    APIGW --> Frontend: 422 error message
                    Frontend --> User: Ошибка\n«Что-то пошло не так…\nПопробуйте позже.»
                else 20 Основной сценарий — Idempotency-Key отсутствует

                    BookingService -> DB: Получение кол-ва доступных номеров\nпо датам и кол-ву гостей\n(Postgres - Инвентарь типа номера по датам)
                    activate DB
                    DB --> BookingService: Кол-во доступных номеров
                    deactivate DB

                    alt 22.А Доступных номеров недостаточно
                        BookingService --> APIGW: 200 OK\nкол-во доступных номеров = 0
                        APIGW --> Frontend: 200 OK\nкол-во доступных номеров = 0
                        Frontend --> User: «Нет доступных номеров»\nпод полем Дат\nКнопка «Забронировать» заблокирована
                    else 22 Основной сценарий

                        BookingService -> PricingService: POST /api/v1/pricing/calculate
                        activate PricingService

                        PricingService -> DB: Получение цен по датам,\nкол-ву гостей, типу оплаты,\nтипу номера\n(Postgres - Тарифные планы, Календарь)
                        activate DB
                        DB --> PricingService: Тарифные планы и календарь
                        deactivate DB

                        PricingService -> PricingService: Расчет цен согласно\nтарифным планам и календарю
                        activate PricingService
                        deactivate PricingService

                        alt 26.А Pricing Service вернул ошибку
                            PricingService --> BookingService: Error response
                            BookingService --> APIGW: 502 Bad Gateway
                            APIGW --> Frontend: 502 error message
                            Frontend --> User: Ошибка\n«Что-то пошло не так…\nПопробуйте позже.»
                        else 26 Основной сценарий
                            PricingService --> BookingService: 200 OK\ntotal_amount, required_payment_amount,\ncurrency, payment_type
                            deactivate PricingService

                            BookingService -> BookingService: Проверка наличия\nтипа оплаты в ответе
                            activate BookingService
                            deactivate BookingService

                            alt 27.А Тип оплаты отсутствует
                                BookingService --> APIGW: 422 Unprocessable Entity\nОшибка поля тип оплаты
                                APIGW --> Frontend: 422 error message
                                Frontend --> User: Ошибка под полем типа оплаты:\n«Некорректный тип оплаты»
                            else 27 Основной сценарий — тип оплаты присутствует
                                BookingService -> DB: Уменьшение кол-ва доступных номеров\nпо датам и кол-ву гостей\n(Postgres - Инвентарь типа номера по датам)
                                activate DB
                                DB --> BookingService: OK
                                deactivate DB

                                BookingService -> BookingService: Проверка типа оплаты:\nFULL_PAYMENT / PARTIAL_PAYMENT\nили HOTEL_PAYMENT
                                activate BookingService
                                deactivate BookingService

                                alt 29.А Тип оплаты = HOTEL_PAYMENT
                                    BookingService -> DB: Создание бронирования\nbooking_status: CONFIRMED\npayment_status: UNPAID\ntotal_amount, currency, payment_type\npaid_amount = 0\nrequired_payment_amount = 0\ncreated_at, userId, Idempotency-Key\n(Postgres - бронирования)
                                    activate DB
                                    DB --> BookingService: OK
                                    deactivate DB

                                    BookingService ->> Kafka: publish BookingEvent\n{email, данные бронирования}

                                    BookingService --> APIGW: 200 OK\nstatus = CONFIRMED
                                    APIGW --> Frontend: 200 OK\nstatus = CONFIRMED
                                    Frontend --> User: «Бронирование успешно выполнено.»
                                else 29 Основной сценарий — FULL_PAYMENT или PARTIAL_PAYMENT
                                    BookingService -> DB: Создание бронирования\nbooking_status: PENDING_PAYMENT\npayment_status: PENDING\ntotal_amount, currency, payment_type\npaid_amount = 0\nrequired_payment_amount\ncreated_at, userId, Idempotency-Key\n(Postgres - бронирования)
                                    activate DB
                                    DB --> BookingService: OK
                                    deactivate DB

                                    BookingService -> PaymentService: POST /api/v1/payments/init\n{Amount=required_payment_amount,\nDescription, booking_id}\nIdempotency-Key
                                    activate PaymentService

                                    PaymentService -> DB: Поиск по Idempotency-Key\n(Postgres - платежи)
                                    activate DB
                                    DB --> PaymentService: Результат поиска
                                    deactivate DB

                                    alt 32.А Idempotency-Key найден\nсо статусом NEW\nи created_at < now + 15 мин
                                        PaymentService -> DB: Получение данных платежа\n(Postgres - платежи)
                                        activate DB
                                        DB --> PaymentService: Данные платежа с paymentUrl
                                        deactivate DB

                                        PaymentService --> BookingService: 200 OK\npaymentUrl
                                        BookingService --> APIGW: 200 OK\npaymentUrl, status = PENDING_PAYMENT
                                        APIGW --> Frontend: 200 OK\npaymentUrl
                                        Frontend --> User: Редирект на paymentUrl\nдля оплаты
                                    else 32.Б Idempotency-Key найден\nсо статусом != NEW\nили created_at >= now + 15 мин
                                        PaymentService --> BookingService: 402 Payment Required
                                        BookingService --> APIGW: 402 Payment Required
                                        APIGW --> Frontend: 402 error message
                                        Frontend --> User: Ошибка\n«Что-то пошло не так…\nПопробуйте позже.»
                                    else 32 Основной сценарий — Idempotency-Key отсутствует
                                        PaymentService -> DB: Сохранение данных платежа\n{Amount, Description, booking_id}\nстатус = NEW, created_at\n(Postgres - платежи)
                                        activate DB
                                        DB --> PaymentService: OK
                                        deactivate DB

                                        PaymentService -> TBank: POST /v2/Init\n{Amount, OrderId, Description,\nRedirectDueDate = now + 15 мин}
                                        activate TBank

                                        alt 35.А Т-банк вернул Success = false\nили Status != NEW
                                            TBank --> PaymentService: 200 OK\nSuccess: false, ErrorCode, Message
                                            deactivate TBank

                                            PaymentService -> DB: Обновление данных платежа\n(Postgres - платежи)
                                            activate DB
                                            DB --> PaymentService: OK
                                            deactivate DB

                                            PaymentService --> BookingService: 402 Payment Required
                                            BookingService --> APIGW: 402 Payment Required
                                            APIGW --> Frontend: 402 error message
                                            Frontend --> User: Ошибка\n«Что-то пошло не так…\nПопробуйте позже.»
                                        else 35 Основной сценарий
                                            TBank --> PaymentService: 200 OK\nSuccess: true, Status: NEW\nPaymentId, PaymentURL\nAmount, OrderId
                                            deactivate TBank

                                            PaymentService -> DB: Обновление данных платежа\nupdated_at\n(Postgres - платежи)
                                            activate DB
                                            DB --> PaymentService: OK
                                            deactivate DB

                                            alt 37.А Payment Service вернул ошибку
                                                PaymentService --> BookingService: Error response
                                               
                                                BookingService -> DB: Увеличение кол-ва доступных номеров\nпо датам и кол-ву гостей\n(Postgres - Инвентарь типа номера по датам)
                                                activate DB
                                                DB --> BookingService: OK
                                                deactivate DB

                                                BookingService --> APIGW: 402 Payment Required
                                                APIGW --> Frontend: 402 error message
                                                Frontend --> User: Ошибка\n«Что-то пошло не так…\nПопробуйте позже.»
                                            else 37 Основной сценарий
                                                PaymentService --> BookingService: 201 Created\npaymentUrl
                                                deactivate PaymentService

                                                BookingService --> APIGW: 201 Created\npaymentUrl, status = PENDING_PAYMENT
                                                deactivate BookingService

                                                APIGW --> Frontend: 201 Created\npaymentUrl
                                                deactivate APIGW

                                                Frontend --> User: Редирект на paymentUrl\nдля оплаты
                                                deactivate Frontend
                                            end
                                        end
                                    end
                                end
                            end
                        end
                    end
                end
            end
        end
    end
end

@enduml

## Пример 2
### Запрос
Название: Регистрация пользователя
Акторы:
- Frontend (Web / Mobile App)
- API Gateway
- Auth Service (регистрация, код, статус)
- DB Postgres (Users)
- DB Redis (Verification Codes)
- Notification Service (Email)
- Message Broker (Kafka)
Предусловия:
- Пользователь не авторизован
- Email сервис доступен
- Backend сервисы доступны
Триггер: Пользователь нажимает кнопку "Зарегистрироваться"
Цель: Создать новую учетную запись пользователя
Основной сценарий:
1.  Пользователь вводит: email, пароль, подтвердить пароль и нажимает Зарегистрироваться
2.  Frontend проверяет валидность данных: email корректный, пароли совпадают, минимальную сложность пароля
3.  Frontend убеждается в валидности данных: email корректный, пароли совпадают, минимальную сложность пароля
4.  Frontend вызывает метод POST /api/v1/auth/register API Gateway
5.  API Gateway проверяет rate limit (5 попыток / 10 минут / email и 5 попыток / минуту / IP)
6.  API Gateway убеждается в непревышение rate limit 
7.  API Gateway проксирует запрос в Auth Service
8.  Auth Service проверяет валидность данных: email корректный, пароли совпадают, минимальную сложность пароля
9.  Auth Service убеждается в валидности данных
10. Auth Service нормализует email (lowercase и trim)
11. Auth Service проверяет непревышение количества отправленных email в сутки attempts < 5 в DB Redis (Verification Codes) auth:email_limit
12. Auth Service убеждается в непревышение количества отправленных email в сутки
13. Auth Service проставляет ограничение на отправку email в сутки в DB Redis (Verification Codes): auth:email_limit:user@gmail.com → +=1 с TTL 24 часа
14. Auth Service проверяет отсутствие email DB Postgres (Users) 
15. Auth Service убеждается уникальности email DB Postgres (Users)
16. Auth Service хеширует пароль и сохраняет в DB Postgres (Users) данные с email со статусом PENDING_VERIFICATION
17. Auth Service генерирует уникальный код и registration_id, сохраняет данные с email с TTL (10 минут) и attempt = 0 в DB Redis (Verification Codes): auth:verification: {email} → {"registration_id": "55DE358F-45F1-E311-93EA-00269E58F20D", "code": "code", "attempts": 0}
18. Auth Service фиксирует ограничение на повторную отправку кода с TTL 120 секунд в DB Redis (Verification Codes): auth:resend_cooldown:user@gmail.com → 1
19. Auth Service публикует сообщение в Kafka UserVerificationRequestedEvent с кодом и email
20. Auth Service возвращает ответ 200 API Gateway с registration_id и email
21. API Gateway проксирует ответ Frontend
22. Frontend отображает страницу ввода кода с таймером на кнопку «Повторная отправка» (120 сек) и email Пользователю
23. Notification Service получает сообщение UserVerificationRequestedEvent из Kafka
24. Notification Service направляет письмо Пользователю с кодом на email
25. Пользователь вводит код
26. Frontend вызывает метод POST /api/v1/auth/verify API Gateway с email, registration_id и кодом
27. API Gateway проверяет rate limit (5 попыток / 10 минут / email и 5 попыток / минуту / IP и 5 попыток / 10 минут / registration_id)
28. API Gateway убеждается непревышение rate limit
29. API Gateway проксирует запрос в Auth Service
30. Auth Service проверяет валидность данных
31. Auth Service убеждается в валидности данных
32. Auth Service нормализует email (lowercase и trim)
33. Auth Service находит email в DB Postgres (Users) 
34. Auth Service убеждается в статусе PENDING_VERIFICATION у email
35. Auth Service находит email в DB Redis (Verification Codes)
36. Auth Service проверяет кол-во попыток attempts < 5 в DB Redis (Verification Codes): auth:verification 
37. Auth Service убеждается attempts < 5
38. Auth Service обновляет attempts +=1 в DB Redis (Verification Codes): auth:verification
39. Auth Service проверяет код и registration_id совпадает с сохраненным в DB Redis (Verification Codes)
40. Auth Service убеждается в совпадении код и registration_id с сохраненным в DB Redis (Verification Codes) 
41. Auth Service изменяет статус на ACTIVE в DB Postgres (Users) у email
42. Auth Service удаляет запись с кодом в DB Redis (Verification Codes)
43. Auth Service генерирует access (JWT) и refresh токен
44. Auth Service сохраняет refresh токен в DB Postgres (refresh_tokens)
45. Auth Service возвращает ответ 200 API Gateway "status": «ACTIVE», access и refresh токены
46. API Gateway проксирует ответ Frontend
47. Frontend отображает Успех и редиректит (логинит) на Главную страницу Пользователю

Альтернативный сценарий:
3.А. Frontend фиксирует некорректный email/несовпадение паролей → отображает ошибку Пользователю: "Введите корректный email"/ "Пароли не совпадают"/"Введите более сложных пароль" Пользователю
6.А. API Gateway фиксирует превышение rate limit → API Gateway возвращает ошибку 429 Frontend → Frontend отображает ошибку «Слишком много попыток. Попробуйте позже.» и страницу Регистрации Пользователю
9.А. Auth Service фиксирует некорректные данные → Auth Service возвращает 400 API Gateway → API Gateway проксирует ответ Frontend → Frontend отображает ошибку: "Некорректные данные» Пользователю
12.А. Auth Service фиксирует превышение количества отправленных email в сутки → Auth Service возвращает ошибку 429 API Gateway с заголовком Retry-After: TTL → Frontend отображает ошибку «Слишком много попыток. Регистрация заблокирована на Retry-After» и Главную страницу Пользователю
15.А. Auth Service фиксирует наличие email со статусом !=PENDING_VERIFICATION в DB Postgres (Users) → Auth Service публикует сообщение в Kafka: AccountAlreadyExistsNotificationRequested с email →  
Auth Service генерирует registration_id → Auth Service возвращает ответ 200 API Gateway с registration_id и email
 → API Gateway проксирует ответ Frontend → Frontend отображает страницу ввода кода с таймером на кнопку «Повторная отправка» (120 сек) и email Пользователю
15.Б. Auth Service фиксирует наличие email со статусом PENDING_VERIFICATION или DELETED в DB Postgres (Users) → Auth Service хеширует пароль и обновляет в DB Postgres (Users) данные, проставляет статус PENDING_VERIFICATION у email → Auth Service убеждается в отсутствии записи в DB Redis (Verification Codes) по email, если найдена - удаляет ее → пункт 18 Основного сценария
20.А. Auth Service возвращает ответ != 200 API Gateway → API Gateway проксирует ответ Frontend →  Frontend отображает ошибку: «Что-то пошло не так…. Попробуйте позже.» Пользователю
28.А. API Gateway фиксирует превышение rate limit → API Gateway возвращает ошибку 429 Frontend → Frontend отображает ошибку «Слишком много попыток. Попробуйте позже.» и страницу с вводом кода Пользователю
30.А. Auth Service фиксирует некорректные данные → Auth Service возвращает 400 API Gateway → API Gateway проксирует ответ Frontend → Frontend отображает ошибку: "Некорректные данные» Пользователю
34.А. Auth Service фиксирует у email статус !=PENDING_VERIFICATION или отсутствие в DB Postgres (Users) → Auth Service возвращает ответ 200 API Gateway и email → API Gateway проксирует ответ Frontend → Frontend отображает страницу ввода кода с таймером на кнопку Повторная отправка (120 сек) и email Пользователю
37.А. Auth Service фиксирует attempts >= 5 в DB Redis (Verification Codes): auth:verification → Auth Service удаляет ключ с кодом в DB Redis (Verification Codes): auth:verification → Auth Service возвращает 400 Frontend "errorCode": "VERIFICATION_CODE_EXPIRED" в API Gateway → API Gateway проксирует ответ Frontend → Frontend отображает ошибку: "Код истек", разблокирует кнопку «Повторная отправка» Пользователю
37.Б. Auth Service фиксирует истечение срока действия кода (не найден код) → Auth Service возвращает 400 Frontend "errorCode": "VERIFICATION_CODE_EXPIRED" API Gateway → API Gateway проксирует ответ Frontend → Frontend отображает ошибку: "Код истек", разблокирует кнопку «Повторная отправка» Пользователю
40.А. Auth Service фиксирует невалидный код или registration_id → Auth Service возвращает 400 Frontend "errorCode": "CODE_INVALID" в API Gateway → API Gateway проксирует ответ Frontend → Frontend отображает ошибку: «Неверный код» Пользователю
45.А. Auth Service возвращает ответ != 200 API Gateway → API Gateway проксирует ответ Frontend → Frontend отображает главную страницу и тост «Что-то пошло не так…. Попробуйте позже.» Пользователю
 
### Ответ
@startuml

title Регистрация пользователя

autonumber

actor User
participant Frontend
participant "API Gateway" as APIGW
participant "Auth Service" as AuthService
queue Kafka
database "DB Postgres (Users)" as DBPostgres
database "DB Redis (Verification Codes)" as DBRedis
participant "Notification Service" as NotificationService

== Ввод данных регистрации ==

User -> Frontend: Вводит email, пароль,\nподтверждение пароля\nи нажимает «Зарегистрироваться»
activate Frontend

Frontend -> Frontend: Валидация данных:\nemail корректный,\nпароли совпадают,\nсложность пароля
activate Frontend
deactivate Frontend

alt 3.А Некорректные данные на Frontend
    Frontend --> User: Ошибка\n«Введите корректный email» /\n«Пароли не совпадают» /\n«Введите более сложный пароль»
else 3 Основной сценарий

    Frontend -> APIGW: POST /api/v1/auth/register
    activate APIGW

    APIGW -> APIGW: Проверка rate limit\n5 попыток / 10 мин / email\n5 попыток / мин / IP
    activate APIGW
    deactivate APIGW

    alt 6.А Превышение rate limit
        APIGW --> Frontend: 429 Too Many Requests
        Frontend --> User: Ошибка\n«Слишком много попыток.\nПопробуйте позже.»\nСтраница регистрации
    else 6 Основной сценарий

        APIGW -> AuthService: POST /api/v1/auth/register
        activate AuthService

        AuthService -> AuthService: Валидация данных:\nemail корректный,\nпароли совпадают,\nсложность пароля
        activate AuthService
        deactivate AuthService

        alt 9.А Некорректные данные в Auth Service
            AuthService --> APIGW: 400 Bad Request
            APIGW --> Frontend: 400 error message
            Frontend --> User: Ошибка\n«Некорректные данные»
        else 9 Основной сценарий

            AuthService -> AuthService: Нормализация email\n(lowercase и trim)
            activate AuthService
            deactivate AuthService

            AuthService -> DBRedis: Проверка суточного лимита\nauth:email_limit:{email}
            activate DBRedis
            DBRedis --> AuthService: Кол-во отправленных email
            deactivate DBRedis

            alt 12.А Превышение суточного лимита отправки email
                AuthService --> APIGW: 429 Too Many Requests\nRetry-After: TTL
                APIGW --> Frontend: 429 error message
                Frontend --> User: Ошибка\n«Слишком много попыток.\nРегистрация заблокирована на Retry-After»\nГлавная страница
            else 12 Основной сценарий

                AuthService -> DBRedis: Инкремент суточного лимита\nauth:email_limit:{email} +=1\nTTL 24 часа
                activate DBRedis
                DBRedis --> AuthService: OK
                deactivate DBRedis

                AuthService -> DBPostgres: Проверка наличия email
                activate DBPostgres
                DBPostgres --> AuthService: Результат поиска email
                deactivate DBPostgres

                alt 15.А Email существует со статусом != PENDING_VERIFICATION
                    AuthService ->> Kafka: publish AccountAlreadyExistsNotificationRequested\n{email}

                    AuthService -> AuthService: Генерация registration_id
                    activate AuthService
                    deactivate AuthService

                    AuthService --> APIGW: 200 OK\nregistration_id, email
                    APIGW --> Frontend: 200 OK\nregistration_id, email
                    Frontend --> User: Страница ввода кода\nТаймер кнопки «Повторная отправка» (120 сек)\nemail

                else 15.Б Email существует со статусом PENDING_VERIFICATION или DELETED

                    AuthService -> AuthService: Хеширование пароля
                    activate AuthService
                    deactivate AuthService

                    AuthService -> DBPostgres: Обновление пароля,\nстатус PENDING_VERIFICATION
                    activate DBPostgres
                    DBPostgres --> AuthService: OK
                    deactivate DBPostgres

                    AuthService -> DBRedis: Проверка записи\nauth:verification:{email}
                    activate DBRedis
                    DBRedis --> AuthService: Результат поиска
                    deactivate DBRedis

                    opt Запись найдена — удалить
                        AuthService -> DBRedis: Удаление\nauth:verification:{email}
                        activate DBRedis
                        DBRedis --> AuthService: OK
                        deactivate DBRedis
                    end

                    note right of AuthService
                    Переход к шагу 18\nОсновного сценария
                    end note

                else 15 Email не существует

                    AuthService -> AuthService: Хеширование пароля
                    activate AuthService
                    deactivate AuthService

                    AuthService -> DBPostgres: Сохранение пользователя\nстатус PENDING_VERIFICATION
                    activate DBPostgres
                    DBPostgres --> AuthService: OK
                    deactivate DBPostgres

                    == Генерация кода верификации ==

                    AuthService -> AuthService: Генерация кода\nи registration_id
                    activate AuthService
                    deactivate AuthService

                    AuthService -> DBRedis: Сохранение\nauth:verification:{email} →\n{registration_id, code, attempts: 0}\nTTL 10 минут
                    activate DBRedis
                    DBRedis --> AuthService: OK
                    deactivate DBRedis

                    AuthService -> DBRedis: Установка cooldown\nauth:resend_cooldown:{email} → 1\nTTL 120 секунд
                    activate DBRedis
                    DBRedis --> AuthService: OK
                    deactivate DBRedis

                    AuthService ->> Kafka: publish UserVerificationRequestedEvent\n{email, code}

                    alt 20.А Auth Service вернул ошибку
                        AuthService --> APIGW: 5xx Error
                        APIGW --> Frontend: error response
                        Frontend --> User: Ошибка\n«Что-то пошло не так…\nПопробуйте позже.»
                    else 20 Основной сценарий
                        AuthService --> APIGW: 200 OK\nregistration_id, email
                        deactivate AuthService

                        APIGW --> Frontend: 200 OK\nregistration_id, email
                        deactivate APIGW

                        Frontend --> User: Страница ввода кода\nТаймер кнопки «Повторная отправка» (120 сек)\nemail
                        deactivate Frontend
                    end
                end
            end
        end
    end
end

== Доставка письма с кодом ==

Kafka ->> NotificationService: consume UserVerificationRequestedEvent\n{email, code}
activate NotificationService

NotificationService --> User: Email с кодом верификации
deactivate NotificationService

== Ввод кода верификации ==

User -> Frontend: Вводит код верификации
activate Frontend

Frontend -> APIGW: POST /api/v1/auth/verify\n{email, registration_id, code}
activate APIGW

APIGW -> APIGW: Проверка rate limit\n5 попыток / 10 мин / email\n5 попыток / мин / IP\n5 попыток / 10 мин / registration_id
activate APIGW
deactivate APIGW

alt 28.А Превышение rate limit
    APIGW --> Frontend: 429 Too Many Requests
    Frontend --> User: Ошибка\n«Слишком много попыток.\nПопробуйте позже.»\nСтраница ввода кода
else 28 Основной сценарий

    APIGW -> AuthService: POST /api/v1/auth/verify\n{email, registration_id, code}
    activate AuthService

    AuthService -> AuthService: Валидация данных
    activate AuthService
    deactivate AuthService

    alt 30.А Некорректные данные в Auth Service
        AuthService --> APIGW: 400 Bad Request
        APIGW --> Frontend: 400 error message
        Frontend --> User: Ошибка\n«Некорректные данные»
    else 30 Основной сценарий

        AuthService -> AuthService: Нормализация email\n(lowercase и trim)
        activate AuthService
        deactivate AuthService

        AuthService -> DBPostgres: Поиск email
        activate DBPostgres
        DBPostgres --> AuthService: Статус пользователя
        deactivate DBPostgres

        alt 34.А Статус != PENDING_VERIFICATION или email не найден
            AuthService --> APIGW: 200 OK\nemail
            APIGW --> Frontend: 200 OK\nemail
            Frontend --> User: Страница ввода кода\nТаймер кнопки «Повторная отправка» (120 сек)\nemail
        else 34 Основной сценарий

            AuthService -> DBRedis: Поиск\nauth:verification:{email}
            activate DBRedis
            DBRedis --> AuthService: {registration_id, code, attempts}
            deactivate DBRedis

            alt 37.Б Код не найден (истёк срок действия)
                AuthService --> APIGW: 400 Bad Request\nerrorCode: VERIFICATION_CODE_EXPIRED
                APIGW --> Frontend: 400 error message
                Frontend --> User: Ошибка\n«Код истек»\nКнопка «Повторная отправка» разблокирована
            else 37.А attempts >= 5

                AuthService -> DBRedis: Удаление\nauth:verification:{email}
                activate DBRedis
                DBRedis --> AuthService: OK
                deactivate DBRedis

                AuthService --> APIGW: 400 Bad Request\nerrorCode: VERIFICATION_CODE_EXPIRED
                APIGW --> Frontend: 400 error message
                Frontend --> User: Ошибка\n«Код истек»\nКнопка «Повторная отправка» разблокирована
            else 37 attempts < 5

                AuthService -> DBRedis: Обновление attempts +=1\nauth:verification:{email}
                activate DBRedis
                DBRedis --> AuthService: OK
                deactivate DBRedis

                alt 40.А Невалидный код или registration_id
                    AuthService --> APIGW: 400 Bad Request\nerrorCode: CODE_INVALID
                    APIGW --> Frontend: 400 error message
                    Frontend --> User: Ошибка\n«Неверный код»
                else 40 Код и registration_id совпадают

                    == Активация аккаунта ==

                    AuthService -> DBPostgres: Обновление статуса\nна ACTIVE для email
                    activate DBPostgres
                    DBPostgres --> AuthService: OK
                    deactivate DBPostgres

                    AuthService -> DBRedis: Удаление\nauth:verification:{email}
                    activate DBRedis
                    DBRedis --> AuthService: OK
                    deactivate DBRedis

                    AuthService -> AuthService: Генерация\naccess (JWT) и refresh токенов
                    activate AuthService
                    deactivate AuthService

                    AuthService -> DBPostgres: Сохранение refresh токена\nв refresh_tokens
                    activate DBPostgres
                    DBPostgres --> AuthService: OK
                    deactivate DBPostgres

                    alt 45.А Auth Service вернул ошибку
                        AuthService --> APIGW: 5xx Error
                        APIGW --> Frontend: error response
                        Frontend --> User: Главная страница\nТост «Что-то пошло не так…\nПопробуйте позже.»
                    else 45 Основной сценарий
                        AuthService --> APIGW: 200 OK\nstatus: ACTIVE\naccess token, refresh token
                        deactivate AuthService

                        APIGW --> Frontend: 200 OK\naccess token, refresh token
                        deactivate APIGW

                        Frontend --> User: Успех\nРедирект на Главную страницу
                        deactivate Frontend
                    end
                end
            end
        end
    end
end

@enduml


## Пример 3
### Запрос
Название: Просмотр типа номера
Акторы:
- Пользователь (гость: авторизованный / неавторизованный)
- Frontend (Web / Mobile App)
- API Gateway
- Booking Service 
- Hotel Service
- Pricing Service
- DB (Postgres - инвентарь типа номера, тип номера, календарь, тарифные планы)
Предусловия:
- Система доступна
- Пользователь находится на экране типов номеров
Триггер: Пользователь нажимает на кнопку “Просмотр”
Цель: Отобразить подробную информацию о номере
Основной сценарий:
1.  Пользователь выбирает тип номера и нажимает на кнопку “Просмотр”    
2.  Frontend валидирует данные: check-in < check-out и кол-во count-adults > 0    
3.  Frontend убеждается в валидности данных: check-in < check-out и кол-во count-adults > 0    
4.  Frontend вызывает метод GET /api/v1/hotels/{hotelId}/room-types/{roomTypeId} API Gateway    
5.  API Gateway убеждается rate limit =< 5 попыток / минуту / IP    
6.  API Gateway проксирует запрос в Hotel Service    
7.  Hotel Service получает данные типа номера в DB (Postgres - Тип номера)    
8.  Hotel Service возвращает ответ 200 API Gateway с подробной информацией о типе номера    
9.  API Gateway проксирует ответ Frontend    
10.  Frontend вызывает GET /api/v1/hotels/{hotelId}/room-types/{roomTypeId}?check-in={checkIn}&check-out={checkOut}&count-adults={countAdults}&count-children={countChildren} API Gateway   
11.  API Gateway проверяет rate limit (5 попыток / минуту / IP)    
12.  API Gateway проксирует запрос в Booking Service    
13.  Booking Service убеждается в валидности запроса, кол-во count-adults >0, check-in < check-out    
14.  Booking Service убеждается в доступности типов номеров в DB (Postgres - Инвентарь типа номера по датам) по датам    
15.  Booking Service вызывает метод POST /api/v1/pricing/calculate Pricing Service с данными бронирования (hotelId, roomTypeId, checkIn, checkOut, countAdults, countChildren)    
16.  Pricing Service получает данные цен на даты заезда и выезда, кол-во гостей согласно календарю в DB (Postgres - Тарифные планы, Календарь)    
17.  Pricing Service рассчитывает цены согласно тарифным планам и календарю и данным бронирования    
18.  Pricing Service возвращает ответ 200 Booking Service с данными о цене и типами оплаты    
19.  Booking Service формирует ответ с кол-вом свободных номеров, цены и типы оплаты    
20.  Booking Service возвращает ответ 200 с данными API Gateway    
21.  API Gateway проксирует ответ Frontend    
22.  Frontend убеждается в наличии цены и типов оплаты: отображает тип номера с фото, типом, подробным описанием, ценой и типом оплаты, информацию о поиске и кнопку Забронировать Пользователю

Альтернативные сценарии:
3.А. Frontend фиксирует некорректны даты (check-in ≥ check-out) → Frontend: «Некорректные даты проживания» 
5.А. API Gateway фиксирует превышение rate limit -> API Gateway возвращает ошибку 429 Frontend → Frontend отображает ошибку «Слишком много попыток. Попробуйте позже.» Пользователю
8.А. Hotel Service возвращает ответ != 200 API Gateway API Gateway → API Gateway проксирует ответ Frontend → Frontend отображает «Что-то пошло не так. Попробуйте позже.» Пользователю
11.А. API Gateway фиксирует превышение rate limit -> API Gateway возвращает ошибку 429 Frontend → Frontend отображает ошибку «Слишком много попыток. Попробуйте позже.» Пользователю
13.A. Booking Service фиксирует некорректность запроса → Booking Service возвращает 400 с ошибкой API Gateway → API Gateway проксирует ответ Frontend → Frontend отображает «Некорректные данные поиска» под некорректным полем, кнопка Забронировать заблокирована Пользователю
14.А. Booking Service фиксирует отсутствие доступных номеров → Booking Service возвращает 200 и кол-во доступных номеров = 0 API Gateway → API Gateway проксирует ответ Frontend → Frontend отображает «Нет доступных номеров» под полем Дат, кнопка Забронировать заблокирована Пользователю
18.А. Pricing Service возвращает ответ !=200 Booking Service → Booking Service формирует ответ с кол-вом свободных номеров → переход к пункту 20 Основного сценария 
22.А. Frontend убеждается в отсутствии цены и типа оплаты: отображает тип номера с фото, типом, подробным описанием и кнопку Забронировать заблокированной, и вместо цены и типы оплаты отображает “Не удалось загрузить цену” Пользователю

### Ответ
@startuml
title Просмотр типа номера

autonumber

actor User
participant Frontend
participant "API Gateway" as APIGW
participant "Hotel Service" as HotelService
participant "Booking Service" as BookingService
participant "Pricing Service" as PricingService
database DB

== Запрос подробной информации о типе номера ==

User -> Frontend: Выбирает тип номера\nи нажимает кнопку «Просмотр»
activate Frontend

Frontend -> Frontend: Валидация данных:\ncheck-in < check-out\ncount-adults > 0
activate Frontend
deactivate Frontend

alt 3.А Некорректные даты проживания
    Frontend --> User: Ошибка\n«Некорректные даты проживания»
else 3 Основной сценарий
    Frontend -> APIGW: GET /api/v1/hotels/{hotelId}/room-types/{roomTypeId}
    activate APIGW

    APIGW -> APIGW: Проверка rate limit\n<= 5 попыток / минуту / IP
    activate APIGW
    deactivate APIGW

    alt 5.А Превышение rate limit
        APIGW --> Frontend: 429 Too Many Requests
        Frontend --> User: Ошибка\n«Слишком много попыток.\nПопробуйте позже.»
    else 5 Основной сценарий
        APIGW -> HotelService: GET /api/v1/hotels/{hotelId}/room-types/{roomTypeId}
        activate HotelService

        HotelService -> DB: Получение данных типа номера\n(Postgres - Тип номера)
        activate DB
        DB --> HotelService: Данные типа номера
        deactivate DB

        alt 8.А Hotel Service вернул ошибку
            HotelService --> APIGW: 500 Internal Server Error
            APIGW --> Frontend: 500 error message
            Frontend --> User: Ошибка\n«Что-то пошло не так.\nПопробуйте позже.»
        else 8 Основной сценарий
            HotelService --> APIGW: 200 OK\nПодробная информация о типе номера
            deactivate HotelService

            APIGW --> Frontend: 200 OK\nПодробная информация о типе номера
            deactivate APIGW

            Frontend -> APIGW: GET /api/v1/hotels/{hotelId}/room-types/{roomTypeId}
            activate APIGW

            APIGW -> APIGW: Проверка rate limit\n<= 5 попыток / минуту / IP
            activate APIGW
            deactivate APIGW

            alt 11.А Превышение rate limit
                APIGW --> Frontend: 429 Too Many Requests
                Frontend --> User: Ошибка\n«Слишком много попыток.\nПопробуйте позже.»
            else 11 Основной сценарий
                APIGW -> BookingService: GET /api/v1/hotels/{hotelId}/room-types/{roomTypeId}
                activate BookingService

                BookingService -> BookingService: Валидация запроса:\ncount-adults > 0\ncheck-in < check-out
                activate BookingService
                deactivate BookingService

                alt 13.А Некорректные данные запроса
                    BookingService --> APIGW: 400 Bad Request
                    APIGW --> Frontend: 400 error message
                    Frontend --> User: Ошибка под некорректным полем\n«Некорректные данные поиска»\nКнопка «Забронировать» заблокирована
                else 13 Основной сценарий
                    BookingService -> DB: Проверка доступности типов номеров\nпо датам\n(Postgres - Инвентарь типа номера по датам)
                    activate DB
                    DB --> BookingService: Данные о доступности
                    deactivate DB

                    alt 14.А Доступные номера отсутствуют
                        BookingService --> APIGW: 200 OK\nКол-во доступных номеров = 0
                        APIGW --> Frontend: 200 OK\nКол-во доступных номеров = 0
                        Frontend --> User: «Нет доступных номеров»\nпод полем Дат\nКнопка «Забронировать» заблокирована
                    else 14 Основной сценарий
                        BookingService -> PricingService: POST /api/v1/pricing/calculate
                        activate PricingService

                        PricingService -> DB: Получение цен на даты заезда и выезда,\nкол-во гостей\n(Postgres - Тарифные планы, Календарь)
                        activate DB
                        DB --> PricingService: Данные тарифов и календаря
                        deactivate DB

                        PricingService -> PricingService: Расчет цен согласно\nтарифным планам, календарю\nи данным бронирования
                        activate PricingService
                        deactivate PricingService

                        alt 18.А Pricing Service вернул ошибку
                            PricingService --> BookingService: 500 Internal Server Error
                            deactivate PricingService

                            BookingService -> BookingService: Формирование ответа\nс кол-вом свободных номеров
                            activate BookingService
                            deactivate BookingService

                            note right of BookingService
                            Переход к шагу 20 \n Возврат ответа в API Gateway
                            end note
                        else 18 Основной сценарий
                            PricingService --> BookingService: 200 OK\nДанные о цене и типах оплаты
                            deactivate PricingService

                            BookingService -> BookingService: Формирование ответа\nс кол-вом свободных номеров,\nценой и типами оплаты
                            activate BookingService
                            deactivate BookingService
                        end

                        BookingService --> APIGW: 200 OK\nДанные о доступности,\nцене и типах оплаты
                        deactivate BookingService

                        APIGW --> Frontend: 200 OK\nДанные о доступности,\nцене и типах оплаты
                        deactivate APIGW

                        alt 22.А Цена и типы оплаты отсутствуют
                            Frontend --> User: Отображает тип номера с фото,\nтипом, подробным описанием,\nинформацией о поиске,\nкнопкой «Забронировать» заблокированной,\nвместо цены и типов оплаты:\n«Не удалось загрузить цену»
                        else 22 Основной сценарий
                            Frontend --> User: Отображает тип номера с фото,\nтипом, подробным описанием,\nценой и типом оплаты,\nинформацией о поиске\nи кнопку «Забронировать»
                            deactivate Frontend
                        end
                    end
                end
            end
        end
    end
end

@enduml