from dataclasses import dataclass
from faker import Faker

fake = Faker()

@dataclass
class LoginCredentials:
    username: str
    password: str

class DataFactory:

    @staticmethod
    def valid_user() -> LoginCredentials:
        return LoginCredentials(
            username="tomsmith",
            password="SuperSecretPassword!"
        )

    @staticmethod
    def invalid_user() -> LoginCredentials:
        return LoginCredentials(
            username="wronguser",
            password="wrongpass"
        )