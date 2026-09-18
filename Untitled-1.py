# Темы Python и их изучение
themes = {
    "Переменные": True,
    "Условия": True,
    "Циклы": True,
    "Списки": True,
    "Кортежи": False,
    "Функции": False,
    "Словари": False,
    "Файлы": False,
    "ООП": False,
}

learned = sum(themes.values())
total = len(themes)
progress = round(learned / total * 100)

print(f"Прогресс: {progress}%")