# FastAPI Kitten Exhibition Service

Проект представляет собой cервис для администратора онлайн выставки котят с поддержкой аутентификации пользователей.

### Зарегистрированный пользователь может:
- Получить список всех котят.
- Получить список всех пород.
- Получить подробную информацию о котенке.
- Получить список котят определенной породы по фильтру.

### Администратор (суперюзер) может:
Все то же, что и зарегистрированный пользователь, а также:
- Добавить нового котенка
- Изменить информацию о котенке
- Удалить котенка
- Добавить новую породу

## Установка и запуск
1. **Клонируйте репозиторий:**
   ```
   git clone https://github.com/ErlanNazarbekov/test-task-fastapi.git
   ```
2. Установите и активируйте виртуальное окружение:
    ```
    python -m venv venv
    source venv/Scripts/activate  - для Windows
    source venv/bin/activate - для Linux
    ```
3. Установите зависимости:
    ```
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```
4. **Создайте файл .env в корне проекта с таким содержимым:**
   ```
   APP_TITLE=Service for the administrator of the online exhibition of kittens
   DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
   SECRET=secret
   FIRST_SUPERUSER_EMAIL=superuser@example.com
   FIRST_SUPERUSER_PASSWORD=superuser1
   ```
5. Запустите проект:
    ```
    uvicorn app.main:app --reload 
    ```
6. Зарегистрируйтесь как суперюзер используя данные:
   ```
   username: superuser@example.com
   password: superuser1
   ```
   
**После запуска приложение будет доступно по адресу http://127.0.0.1:8000,
увидеть спецификацию API вы сможете по адресу http://127.0.0.1:8000/docs/**

## Технологии
- **Python 3.11.7**
- **FastAPI 0.115.0**
- **SQLAlchemy 2.0.29**
- **Alembic 1.13.1**
- **Pydantic 2.7.1**
- **Pytest 8.3.3**

