## 1. Клонировать репозиторий
```bash
git clone https://github.com/StatusSSS/Litestar_Test.git

cd Litestar_Test
```
## 2. Поднять сервисы

```bash
docker compose up -d --build
```

## 3. Применить миграции
```bash
docker compose exec app litestar --app app.asgi:app database upgrade
```

## 4. Открыть Swagger
### open http://localhost:8000/schema

### Время выполнения: 02:13 🕦
