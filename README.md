# Practice Automation Testing

Учебный проект по автоматизации API-тестирования на Python. Проект находится в разработке: тестовое покрытие и инфраструктура постепенно расширяются.

## Стек

- Python
- pytest
- httpx
- Pydantic и pydantic-settings
- Faker
- Ruff

## Что автоматизируется

В текущей версии реализованы проверки API авторизации и управления пользователями:

- регистрация пользователя;
- вход в систему;
- получение текущего пользователя;
- просмотр, изменение и удаление пользователя администратором.

Код разделён на API-клиенты, Pydantic-схемы, pytest-fixtures, assertions и тесты. Это помогает поддерживать тесты понятными и не дублировать HTTP-запросы в сценариях.

## Подготовка и запуск

1. Создайте и активируйте виртуальное окружение.
2. Установите зависимости:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Создайте локальный файл `.env` с настройками тестового API и учётными данными администратора. Файл не хранится в репозитории.
4. Запустите тесты:

   ```powershell
   python -m pytest -q
   ```

5. Проверьте стиль кода:

   ```powershell
   ruff check .
   ruff format --check .
   ```

## CI

Workflow [api-tests.yml](.github/workflows/api-tests.yml) запускается при `push`, `pull request` и вручную через GitHub Actions. Он скачивает `Anychos/practice-automation-app`, поднимает его тестовый Docker Compose-профиль, ожидает готовности API и затем выполняет проверку стиля и API-тесты.

Публикация или развёртывание приложения в workflow не выполняются: этот репозиторий содержит учебные автотесты, а не исходный код приложения.

## Структура

```text
src/api/clients/     # HTTP-клиенты API
src/api/schemas/     # request/response-схемы Pydantic
src/api/fixtures/    # общие pytest-fixtures
src/api/assertions/  # проверки ответов API
tests/api/           # API-тесты
```
