import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from keyboards import StartKeyboard, GamePropertiesKeyboard, GameKeyboard  
from sapper import Sapper
from settings.key import TOKEN, GROUP_ID

class VkBot:

    __FIELDS = {
        "3x3": (3, 3, 3),
        "3x4": (3, 4, 4),
        "3x5": (3, 5, 5),
        "4x4": (4, 4, 6),
        "5x5": (5, 5, 8),
    }

    def __init__(self, token, group_id):
        self.__vk_session = vk_api.VkApi(token=token)
        self.__longpoll = VkBotLongPoll(self.__vk_session, group_id)
        self.__start_menu = False
        self.__game_started = False
        self.__game_properties_menu = False
        self.__opened_cells = set()
        self.__balance = 100
        self.__current_game = None  

    def __send_message_with_keyboard(self, user_id, message: str, keyboard):
        try:
            self.__vk_session.method('messages.send', {
                'user_id': user_id,
                'message': message,
                'keyboard': keyboard.get_keyboard(),
                'random_id': 0,
            })
        except vk_api.exceptions.VkApiError as exc: 
            print(exc)

    def __send_message(self, user_id, message: str):
        try:
            self.__vk_session.method('messages.send', {
                'user_id': user_id,
                'message': message,
                'random_id': 0,
            })
        except vk_api.exceptions.VkApiError as exc: 
            print(exc)

    def __return_to_menu(self, user_id, start_keyboard):
        self.__send_message_with_keyboard(user_id, "Возвращаемся в главное меню", start_keyboard)
        self.__start_menu = True
        self.__game_started = False
        self.__game_properties_menu = False

    def start(self):
        start_keyboard = StartKeyboard()  
        for event in self.__longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                message = event.object.message["text"].lower()
                user_id = event.object.message["from_id"]

                if message == "начать":
                    self.__start_menu = True
                    self.__send_message_with_keyboard(user_id, "Выберите действие:", start_keyboard.get_keyboard())

                elif message == 'баланс' and self.__start_menu:
                    self.__send_message(user_id, f"Ваш баланс: {self.__balance}")

                elif message == "начать игру" and self.__start_menu:
                    self.__start_menu = False
                    self.__game_properties_menu = True
                    self.__opened_cells.clear()
                    prop_keyboard = GamePropertiesKeyboard()
                    self.__send_message_with_keyboard(user_id, "Выберите размеры игрового поля", prop_keyboard.get_keyboard())

                elif message == "вернуться" and self.__game_properties_menu:
                    self.__return_to_menu(user_id, start_keyboard.get_keyboard())

                elif self.__game_properties_menu and message in self.__FIELDS:
                    n, m, mines = self.__FIELDS[message]
                    self.__game_started = True
                    game_keyboard = GameKeyboard(n, m)
                    sapper = Sapper(n, m, mines)
                    sapper.create_gamefield()
                    self.__current_game = (sapper, game_keyboard) 
                    self.__send_message_with_keyboard(user_id, "Игра началась. Выбирай клетки", game_keyboard.get_keyboard())

                elif self.__game_started and message.isdigit():
                    sapper, game_keyboard = self.__current_game  
                    d = int(message)
                    if d not in self.__opened_cells:
                        x = (d-1) // m 
                        y = (d-1) % m
                        result = sapper.open_cell(x, y)
                        self.__opened_cells.add(d)
                        if result == 0:
                            game_keyboard.change_colors(x, y)
                            self.__send_message_with_keyboard(user_id, "Вам повезло. Клетка без мины", game_keyboard.get_keyboard())
                        else:
                            self.__send_message_with_keyboard(user_id, "К сожалению, вы проиграли!", start_keyboard.get_keyboard())
                            self.__return_to_menu(user_id, start_keyboard.get_keyboard())

                    else:
                        self.__send_message(user_id, "Вы уже выбирали эту клетку")

                elif self.__game_started and message == 'прекратить игру':
                    sapper, game_keyboard = self.__current_game 
                    n, m, mines = sapper.get_game_properties()  
                    self.__balance += (mines * len(self.__opened_cells))  
                    self.__send_message_with_keyboard(user_id, "Поздравляю с выигрышем", start_keyboard.get_keyboard())
                    self.__return_to_menu(user_id, start_keyboard.get_keyboard())

if __name__ == '__main__':
    bot = VkBot(TOKEN, GROUP_ID)
    bot.start()