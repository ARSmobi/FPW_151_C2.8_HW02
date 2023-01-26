class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return 'Вы пытаетесь выстрелить за пределы поля.'


class BoardDoubleShotException(BoardException):
    def __str__(self):
        return 'Вы стреляли сюда ранее.'


class BoardPlaceShipException(BoardException):
    pass
