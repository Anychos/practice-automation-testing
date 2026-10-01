from enum import StrEnum


class Route(StrEnum):
    REGISTER = "/auth/register"
    LOGIN = "/auth/login"
    USERS = "/users"
