# 1. Клонировать репозиторий
git clone <ваша_ссылка>
cd user-api

# 2. Поднять сервисы
docker-compose up -d

# 3. Применить миграции
docker compose exec app litestar database upgrade
# (при первом запуске auto-generate ревизии тоже можно:
# docker compose exec app litestar database migrate -m "init"
# но в проект уже добавлена директория migrations после первого локального запуска)

# 4. Открыть Swagger
open http://localhost:8000/schema
