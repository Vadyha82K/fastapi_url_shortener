from abc import (
    ABC,
    abstractmethod,
)


class AbstractUsersHelper(ABC):
    """
    Что мне нужно от обертки:
    - получение пароля по username;
    - совпадает ли пароль с переданным;
    -
    """

    @abstractmethod
    def get_user_password(
        self,
        username: str,
    ) -> str | None:
        """
        По переданному username, находит пароль.
        Возвращает пароль, если он найден.

        :param username: - имя пользователя
        :return: пароль пользователя, либо None, если пароля нет
        """

    @classmethod
    def check_password_match(
        cls,
        password1: str,
        password2: str,
    ) -> bool:
        return password1 == password2

    def validate_user_password(
        self,
        username: str,
        password: str,
    ) -> bool:
        """
        Проверяет переданный пароль, на соответствие паролю, хранящемуся в БД
        под переданным username

        :param username: - чей пароль проверить
        :param password: - переданный пароль. Сверить с тем, что хранится в БД
        :return: - если пароль прошел валидацию, возвращает True, иначе False
        """
        db_password = self.get_user_password(username)
        if db_password is None:
            return False
        return self.check_password_match(
            password1=db_password,
            password2=password,
        )
