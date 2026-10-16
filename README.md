Гумерова Лэйла Маратовна, Задача 2

https://drive.google.com/file/d/1GRnuuY3a2SoZNIFauc4oPvBS1KdGEVVy/view?usp=sharing

Приложение для подсчета калорий

Стек: python 3.10, SQLite, Flask

## Запуск

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python app.py

## Тесты
    
    python -m unittest discover tests -v

## Структура

    app.py - точка входа
    requirements.txt

    calories_app/
        __init__.py - Flask-приложение
        models.py - модели данных (Dish, Entry, Goals)
        calculation.py - вычисление КБЖУ
        db.py - работа с БД
        analyze.py - сбор статистики по записям

        routes/
            __init__.py - маркер пакета
            main.py - главная
            dishes.py - маршруты блюд
            diary.py - маршруты дневника
            analyze.py - маршруты статистики и API для графика

        templates/
            base.html - общий каркас с навбаром
            index.html - главная
            dishes.html - блюда
            diary.html - дневник
            analyze.html - статистика
    
    tests/
        __init__.py - маркер пакета
        test_models.py - тесты к моделям
        test_calculation.py - тесты к вычислениям КБЖУ
        test_db.py - тесты к БД
        test_analyze.py - тесты к сбору статистики

## Принятые решения

- **dataclass** - для валидации, автодополнения, типизации

- изначально хотелось сделать поиск по бд регистронезависимым, но потом началось сильное усложнение: подгрузка всех блюд тз бд
  поэтому решила не делать

- **SECRET_KEY** - формально не установлен, так как приложение работает локально, но можно вынести в переменную окружения, при расширении
