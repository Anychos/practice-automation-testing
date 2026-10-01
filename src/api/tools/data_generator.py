from faker import Faker
from pydantic import EmailStr


class DataGenerator:
    def __init__(self, faker: Faker):
        self.faker = faker

    def email(self) -> EmailStr:
        return self.faker.email()

    def password(self) -> str:
        return self.faker.password()

    def username(self) -> str:
        return self.faker.user_name()


fake = DataGenerator(faker=Faker())
