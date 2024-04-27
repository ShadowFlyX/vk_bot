from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from abc import ABC, abstractmethod


class Keyboard(ABC):

    def __init__(self):
        self._keyboard = self._create_keyboard()

    @staticmethod
    @abstractmethod
    def _create_keyboard(): ...

    def get_keyboard(self):
        return self._keyboard
    

class StartKeyboard(Keyboard):

    @staticmethod
    def _create_keyboard():
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("Баланс", VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button("Информация о пользователе", VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button("Начать игру", VkKeyboardColor.SECONDARY)
        keyboard.add_button("Прекратить игру", VkKeyboardColor.NEGATIVE)
        return keyboard


class GameKeyboard(Keyboard):

    def __init__(self, n: int = 5, m: int = 5):
        self.n = n
        self.m = m
        self._color_matrix = [[0 for _ in range(m)] for _ in range(n)]
        self._keyboard = self._create_keyboard(n, m, self._color_matrix)

    @staticmethod
    def _create_keyboard(n: int, m: int, color_matrix):
        keyboard = VkKeyboard(one_time=False)
        
        for i in range(n):
            for j in range(m):
                color = VkKeyboardColor.POSITIVE if color_matrix[i][j] == 0 else VkKeyboardColor.SECONDARY
                keyboard.add_button(str((i)*m+j+1), color)
            keyboard.add_line()
        
        keyboard.add_button("Прекратить игру", VkKeyboardColor.NEGATIVE)

        return keyboard
    
    
    def change_colors(self, x, y):
        self._color_matrix[x][y] = 1
        if self._keyboard:
            self._keyboard.keyboard["buttons"][x][y]["color"] = "secondary"


class GamePropertiesKeyboard(Keyboard):

    @staticmethod
    def _create_keyboard():
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button("3x3", VkKeyboardColor.POSITIVE)
        keyboard.add_button("3x4", VkKeyboardColor.POSITIVE)
        keyboard.add_button("3x5", VkKeyboardColor.POSITIVE)
        keyboard.add_button("4x4", VkKeyboardColor.POSITIVE)
        keyboard.add_button("5x5", VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button("Вернуться", VkKeyboardColor.NEGATIVE)
        return keyboard
    