# AntiCafe API

## Запуск

### Подготовка окружения

Надо создать `.env` файл данной командой

```commandline
make env
```

После чего, заполнить его по шаблону

### Запуск

API будет на хосте `http://localhost:8001/`

Чтобы запустить контейнеры

```commandline
make up
```

Чтобы подтянуть локальные изменения можно запустить

```commandline
make up-build
```

### Дроп

```commandline
make down
```

### Создание нового образа

```commandline
make build
```

### Посмотреть OpenAPI

```commandline
make swagger
```

Запустит по адресу `http://localhost:80/` Swagger для удобного рендера схемы

**Дропнуть** контейнер с Swagger

```commandline
make swagger-down
```
