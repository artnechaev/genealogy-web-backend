from djoser.constants import Messages


class AuthMessages(Messages):
    CANNOT_CREATE_USER_ERROR = 'Невозможно создать учетную запись.'
    INVALID_PASSWORD_ERROR = 'Неправильный пароль.'
    EMAIL_NOT_FOUND = 'Пользователь с данным адресом электронной почты не существует.'
