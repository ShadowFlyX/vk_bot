# vk_bot
В общем, мой первый опыт работы с вк апи.

Описание бота:
-
Бот позволяет сыграть в этакую версию сапёра, где мы просто открываем поля, на которых может быть мина
Взаимодействие с игрой происходит через кнопки

Чтобы запустить взаимодействие с ботом, нужно сначала написать __"Начать"__

Затем можно будем выбрать размеры игрового поля, насколько это позволяет разметка кнопок ботов

Далее происходит генерация игры и вывод игрового поля в панель с кнопками.
Пользователь может нажимать на кнопку и в зависимости от типа клетки, произойдет следующее:
- Если это пустая клетка, кнопка покрасится в серый
- Если это клетка с миной, игра окончена
  
Пользователю предоставляется возможность досрочно завершить игру, нажав соответствующую кнопку

Как установить и запустить
-
Для работы бота достаточно одной лишь библиотеки vk_api

После скачивания всех файлов к себе в репозиторий в файле __main.py__
нужно будет ввести api-токен, id-группы вконтакте

Далее просто запускаем и радуемся работающему боту

