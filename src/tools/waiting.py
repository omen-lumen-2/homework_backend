from waiting import wait, TimeoutExpired
from hamcrest import *
import logging


class WaitHelper():
    """
    Класс позволяет реализовать проверку выполнения необходимого условия в течении заданного времени
    """

    def wait_untill(self, functions, matcher, max_time, interval_time, on_poll_message="predicate выполнен"):
        """ Получить timestamp для даты с заданным смещением с преобразованием в тип int
        :param functions: функция, результат которой проверяется заданным matcher
        :param matcher: матчер для сравнение результата выполнения функции с ожидаемым результатом
        :param max_time: суммарное время ожидание
        :param interval_time: интервалы времяни между выполнениями вызова функции
        :param on_poll_message: сообщение после каждого выполнения функции
        """

        on_poll = lambda: logging.info(f"WaitHelper: {on_poll_message}")
        try:
            wait(predicate=lambda: matcher.matches(functions()), timeout_seconds=max_time, sleep_seconds=interval_time,
                 on_poll=on_poll)
        except TimeoutExpired:
            logging.info(f"WaitHelper: Время ожидания ({interval_time}) истекло")

        else:
            assert_that(functions(), matcher)
