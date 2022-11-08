from drf_spectacular.utils import OpenApiExample

EMPTY_LIST_200 = OpenApiExample('empty_data', [], description='Нет данных', response_only=True, status_codes=["200"])

USER_EXISTS_400 = OpenApiExample(
    'user_exists',
    {"username": ["Пользователь с таким именем уже существует."]},
    description='Пользователь с таким **username** уже существует',
    response_only=True,
    status_codes=['400'],
)

INVALID_TOKEN_401 = OpenApiExample(
    'invalid_token',
    {
        "detail": "Given token not valid for any token type",
        "code": "token_not_valid",
        "messages": [{"token_class": "AccessToken", "token_type": "access", "message": "Token is invalid or expired"}],
    },
    description='Неверный токен',
    response_only=True,
    status_codes=["401"],
)

EMPTY_TOKEN_401 = OpenApiExample(
    'empty_token',
    {"detail": "Учетные данные не были предоставлены."},
    description='Без токена',
    response_only=True,
    status_codes=["401"],
)

PAYMENT_REQUIRED_402 = OpenApiExample(
    'opened_bill',
    {'detail': 'Есть неоплаченный счет'},
    description='В случае получения кода без оплаты предыдущего',
    response_only=True,
    status_codes=['402'],
)

NO_PERMISSION_403 = OpenApiExample(
    'no_permission',
    {"detail": "У вас недостаточно прав для выполнения данного действия."},
    response_only=True,
    status_codes=["403"],
)

NOT_FOUND_404 = OpenApiExample(
    'user_not_found',
    {"detail": "Страница не найдена."},
    description='Нет данных по такому id',
    response_only=True,
    status_codes=["404"],
)
