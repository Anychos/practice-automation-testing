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

    def product_name(self) -> str:
        product = "Автотест продукт " + self.faker.word(part_of_speech="noun")
        return product

    def product_description(self) -> str:
        return self.faker.text(max_nb_chars=150)

    def image_url(self) -> str:
        return self.faker.image_url(width=150, height=110)

    def price(self) -> int:
        return self.faker.random_int(min=100, max=2000)

    def quantity(self) -> int:
        return self.faker.random_int(min=1, max=10)


fake = DataGenerator(faker=Faker())
