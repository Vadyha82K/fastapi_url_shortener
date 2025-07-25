import secrets
from abc import ABC, abstractmethod


class AbstractTokensHelper(ABC):
    """
    Что мне нужно от обертки:
    - проверять на наличие токена;
    - добавлять токен в хранилище;
    - сгенерировать и добавить токены.
    """

    @abstractmethod
    def token_exists(
        self,
        token: str,
    ) -> bool:
        """
        Проверяет, существует ли токен.

        :param token: str
        :return: bool
        """

    @abstractmethod
    def get_tokens(self) -> list[str]:
        """
        Вывод всех токенов

        :return: Выводит список всех токенов
        """

    @abstractmethod
    def add_token(
        self,
        token: str,
    ) -> None:
        """
        Сохраняет токен в хранилище.

        :param token: str
        :return: None
        """

    @classmethod
    def generate_token(cls) -> str:
        return secrets.token_urlsafe(16)

    def generate_and_save_token(self) -> str:
        token = self.generate_token()
        self.add_token(token)
        return token

    @abstractmethod
    def delete_token(
        self,
        token: str,
    ) -> None:
        """
        Удаляет токен
        :param token: - ожидается токен, который необходимо удалить
        :return: None
        """
