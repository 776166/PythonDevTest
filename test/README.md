**Комментарии**
Хотел сдеать всё, но не успеваю по личным обстоятельствам.

Основные моменты сделаны, прочие являются производными. Например, импорт из внешнего источника по ссылке.

Паджинатор работает с результатами поиска тоже. И экспорт тоже можно сделать по выборке поиска.

Есть генератор записей в базу и удалятор из неё.

API реализовано через батарейку. Проще и быстрее было сделать руками, но я хотел порпобовать батарейку. Получилось как-то… Ну как-то получилось, но надо копать глубже. Делал первый раз таким образом, так что там только личинка API. Но я понимаю, зачем это в тесте, и как это всё повлияет на рефакторинг кода. Много кропотливой работы, не думаю, что в ней есть смысл.

Организации отдельной сущностью делать не стал, не вижу там ничего особо инновационного, кроме поиска и большого геморроя, на который тратить время в тесте не очень хочется.

Валидация телефона происходит преимущественно на серверной стороне. Бодаться с google библиотеками на клиентской для самого общего случая я не стал (да и врач мой это запрещает), а ставить проверку только для России тоже как-то некузяво, хотя она есть и прекрасно работает на других поектах. Зато на серверной стороне всё есть в полном объёме.

Файлики импорта сохраняются для потомков. По-хорошему, надо было ещё сохранять экспорт, класть в лог и заодно отдавать с хорошими именами: включающими в себя строку поиска, но газки уже в кучку.

И ещё пожидился на тесты и на систему разворачивания в репозиторий. За тесты переживаю, за devops — нет. :)

Работающая версия: https://forget-me-not.dev.madget.net/. Работает в режиме devserver.