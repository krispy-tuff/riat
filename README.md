# Установка проекта

## Предварительные требования

- Python 3.8+
- Docker
- Docker Compose

## Установка

1. **Клонируйте репозиторий:**

   ```sh
   git clone https://github.com/krispy-tuff/riat.git
   cd yourproject
   ```

2. **Соберите и запустите сервисы:**

   Используйте Docker Compose для сборки и запуска всех сервисов, определенных в `compose.yml`.

   ```sh
   docker-compose up --build
   ```

3. **Доступ к сервисам:**

   - `report_service`: http://localhost:8004/docs
   - `auth_service`: http://localhost:8001/docs
   - `game_service`: http://localhost:8002/docs
   - `finance_service`: http://localhost:8003/docs

## Использование

- Логи сервисов можно найти в `*имя_сервиса*.log` файлах.
- Вы можете взаимодействовать с сервисами через их соответствующие конечные точки.

## Остановка сервисов

Для остановки сервисов выполните:

```sh
docker-compose down
```
