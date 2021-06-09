import datetime


class DataHelper():
    """Класс позволяет реализовать проверку выполнения необходимого условия в течении заданного времени
    """

    def get_data_with_offset(self, week_offset):
        """ Получить timestamp для даты с заданным смещением с преобразованием в тип int
        :param week_offset: смещение даты в неделях
        """
        data_offset = datetime.timedelta(weeks=week_offset)
        return int((datetime.datetime.now() + data_offset).timestamp())
