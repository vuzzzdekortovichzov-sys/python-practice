themes = {
    "переменные": True,
    "условия": True,
    "циклы": True,
    "списки": True,
    "кортежи": True,
    "функции": True,
    "словари": True,
    "файлы": True,
    "ооп": True,
}

learned = sum(themes.values())
total = len(themes)
progress = round(learned / total * 100)

print(f"прогресс: {progress}%")