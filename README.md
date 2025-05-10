# SERVER-OPT
web server for serving the database and users and roles

## Secure Server with 2FA Authentication and File Encryption

## Описание
# Это полноценный сервер для безопасного хранения и управления файлами с поддержкой:
- ✅ Регистрация и аутентификация пользователей
- ✅ Ролевой модели доступа (Admin, Uploader, Viewer)
- ✅ Двухфакторной аутентификации (2FA)
- ✅ Шифрования документов (AES)
- ✅ API для загрузки, поиска и скачивания документов
- ✅ Веб-интерфейса (HTML + CSS + JS)

## Быстрый старт

## Установка зависимостей
pip install flask cryptography

## Запуск сервера
python server.py

# Сервер будет доступен по адресу: http://127.0.0.1:5000

## 🌐 Веб-страницы
| URL          | Назначение               |
|---------------|--------------------------|
| /auth         | Страница входа и регистрации |
| /2fa           | Подтверждение 2FA        |
| /dashboard     | Панель управления файлами |

## Основные API маршруты
| Метод  | Endpoint         | Описание                  |
|--------|------------------|---------------------------|
| POST   | /api/register    | Регистрация пользователя  |
| POST   | /api/login       | Вход и получение токена   |
| POST   | /api/verify-2fa  | Проверка 2FA (код 123456) |
| POST   | /api/upload      | Загрузка файла            |
| GET    | /api/download/<id> | Скачивание файла         |
| GET    | /api/search      | Поиск файлов              |

 ## 2FA (Двухфакторная Аутентификация)
- Тестовый код подтверждения: 123456
- Для интеграции с Email или Telegram — настройте в auth.py.

## Работа с Docker
docker-compose up --build

## Структура проекта
SERVER_OPT/
├── server.py
├── modules/
├── templates/
├── static/
├── uploads/
├── logs/
├── secure_storage.db
├── docker-compose.yml
└── Dockerfile

