# 1. Клонировать репозиторий
git clone https://github.com/StatusSSS/Litestar_Test.git
cd user-api

# 2. Поднять сервисы
docker-compose up -d

# 3. Применить миграции
docker compose exec app litestar database upgrade

# 4. Открыть Swagger
open http://localhost:8000/schema

Время выполнения: 02:13 🕦
