import customtkinter as ctk
import json
import os
from tkinter import messagebox

DATA_FILE = "progress.json"

topics = [
    {
        "title": "1. Переменные и print",
        "theory": "Переменная — это коробка для данных.\nprint выводит текст на экран.\n\nПример:\nname = \"Тимур\"\nprint(name)",
        "terms": "print — печатать\nvariable — переменная",
        "practice": "name = \"Тимур\"\nage = 16\nprint(\"Меня зовут\", name)\nprint(\"Мне\", age, \"лет\")",
        "output": "Меня зовут Тимур\nМне 16 лет",
        "errors": "NameError — если print написан с большой буквы.\nSyntaxError — если забыть кавычки."
    },
    {
        "title": "2. Ввод данных (input)",
        "theory": "input спрашивает у пользователя текст и сохраняет в переменную.",
        "terms": "input — ввод\nint — целое число",
        "practice": "name = input(\"Как тебя зовут? \")\nprint(\"Привет, \" + name)",
        "output": "Как тебя зовут? Тимур\nПривет, Тимур",
        "errors": "ValueError — если ввести текст вместо числа."
    },
    {
        "title": "3. Условия (if / else)",
        "theory": "if проверяет условие. Если правда — одно, иначе — другое.",
        "terms": "if — если\nelse — иначе\nelif — иначе если",
        "practice": "age = 16\nif age >= 18:\n    print(\"Взрослый\")\nelse:\n    print(\"Малой\")",
        "output": "Малой",
        "errors": "SyntaxError — если забыть двоеточие."
    },
    {
        "title": "4. Циклы while и for",
        "theory": "while повторяет, пока условие правда.\nfor перебирает элементы.",
        "terms": "while — пока\nfor — для\nrange — диапазон",
        "practice": "for i in range(3):\n    print(i)",
        "output": "0\n1\n2",
        "errors": "Бесконечный цикл — если забыть i += 1."
    },
    {
        "title": "5. Списки (list)",
        "theory": "Список хранит несколько значений.",
        "terms": "list — список\nappend — добавить\nremove — удалить",
        "practice": "games = [\"Тарков\", \"ДСТ\"]\ngames.append(\"КС2\")\nfor g in games:\n    print(g)",
        "output": "Тарков\nДСТ\nКС2",
        "errors": "IndexError — если обратиться к несуществующему индексу."
    },
    {
        "title": "6. Кортежи (tuple)",
        "theory": "Кортеж — как список, но его нельзя менять.",
        "terms": "tuple — кортеж",
        "practice": "days = (\"Пн\", \"Вт\")\nprint(days[0])",
        "output": "Пн",
        "errors": "TypeError — если попытаться изменить кортеж."
    },
    {
        "title": "7. Словари (dict)",
        "theory": "Словарь хранит пары «ключ: значение».",
        "terms": "dict — словарь\nkey — ключ\nvalue — значение",
        "practice": "country = {\"Россия\": \"Москва\"}\nprint(country[\"Россия\"])",
        "output": "Москва",
        "errors": "KeyError — если ключа нет."
    },
    {
        "title": "8. Функции (def, return)",
        "theory": "Функция — кусок кода с именем.",
        "terms": "def — определить\nreturn — вернуть",
        "practice": "def add(a, b):\n    return a + b\nprint(add(5, 7))",
        "output": "12",
        "errors": "Если забыть return — вернётся None."
    },
    {
        "title": "9. Работа с ошибками (try / except)",
        "theory": "try пробует, except ловит ошибку.",
        "terms": "try — попробовать\nexcept — исключение",
        "practice": "try:\n    x = int(input())\nexcept:\n    print(\"Ошибка\")",
        "output": "Ошибка",
        "errors": "ValueError, TypeError, IndexError, KeyError."
    },
    {
        "title": "10. Работа с файлами",
        "theory": "open открывает файл. with закрывает автоматически.",
        "terms": "open — открыть\nread — читать\nwrite — писать",
        "practice": "with open(\"test.txt\", \"w\", encoding=\"utf-8\") as f:\n    f.write(\"Привет\")",
        "output": "Привет",
        "errors": "FileNotFoundError, PermissionError, UnicodeDecodeError."
    },
    {
        "title": "11. Модули и библиотеки",
        "theory": "Модуль — готовый код, подключается через import.",
        "terms": "import — импорт\nmodule — модуль",
        "practice": "import random\nprint(random.randint(1, 10))",
        "output": "5",
        "errors": "ModuleNotFoundError, AttributeError."
    },
    {
        "title": "12. ООП (классы)",
        "theory": "Класс — шаблон для объектов.",
        "terms": "class — класс\nobject — объект\nmethod — метод",
        "practice": "class Person:\n    def __init__(self, name):\n        self.name = name\n\np = Person(\"Тимур\")\nprint(p.name)",
        "output": "Тимур",
        "errors": "TypeError — забыл self."
    },
]

commands = [
    {"name": "print", "what": "Выводит текст на экран.", "example": "print(\"Привет\")"},
    {"name": "input", "what": "Спрашивает текст.", "example": "name = input(\"Имя: \")"},
    {"name": "int", "what": "Превращает в число.", "example": "x = int(\"5\")"},
    {"name": "if / else", "what": "Условия.", "example": "if x > 0:\n    print(\"+\")"},
    {"name": "while", "what": "Цикл пока.", "example": "while x < 5:\n    x += 1"},
    {"name": "for", "what": "Цикл для.", "example": "for i in range(3):\n    print(i)"},
    {"name": "range", "what": "Диапазон чисел.", "example": "range(5)"},
    {"name": "list", "what": "Список.", "example": "a = [1, 2, 3]"},
    {"name": "append", "what": "Добавить в список.", "example": "a.append(4)"},
    {"name": "remove", "what": "Удалить из списка.", "example": "a.remove(2)"},
    {"name": "tuple", "what": "Кортеж.", "example": "t = (1, 2)"},
    {"name": "dict", "what": "Словарь.", "example": "d = {\"a\": 1}"},
    {"name": "def", "what": "Определить функцию.", "example": "def f():\n    pass"},
    {"name": "return", "what": "Вернуть значение.", "example": "return x"},
    {"name": "try / except", "what": "Обработка ошибок.", "example": "try:\n    pass\nexcept:\n    pass"},
    {"name": "open", "what": "Открыть файл.", "example": "open(\"f.txt\")"},
    {"name": "with", "what": "Автозакрытие файла.", "example": "with open(\"f.txt\") as f:\n    pass"},
    {"name": "\"w\"", "what": "Режим записи.", "example": "open(\"f.txt\", \"w\")"},
    {"name": "\"r\"", "what": "Режим чтения.", "example": "open(\"f.txt\", \"r\")"},
    {"name": "\"a\"", "what": "Режим добавления.", "example": "open(\"f.txt\", \"a\")"},
    {"name": "encoding=\"utf-8\"", "what": "Кодировка.", "example": "open(\"f.txt\", encoding=\"utf-8\")"},
    {"name": "read", "what": "Читать файл.", "example": "f.read()"},
    {"name": "write", "what": "Писать в файл.", "example": "f.write(\"hi\")"},
    {"name": "import", "what": "Подключить модуль.", "example": "import random"},
    {"name": "class", "what": "Создать класс.", "example": "class A:\n    pass"},
]

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        done = json.load(f)
else:
    done = {}

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Трекер Python")
root.geometry("1150x750")
root.minsize(1000, 650)

top_bar = ctk.CTkFrame(root, height=60)
top_bar.pack(fill="x", side="top")

ctk.CTkLabel(top_bar, text="Твой путь в Python", font=("Arial", 22, "bold")).pack(side="left", padx=20, pady=10)

progress_label = ctk.CTkLabel(top_bar, text="", font=("Arial", 16))
progress_label.pack(side="right", padx=20)

progress_bar = ctk.CTkProgressBar(top_bar, width=300)
progress_bar.pack(side="right", padx=10)
progress_bar.set(0)

main_frame = ctk.CTkFrame(root)
main_frame.pack(fill="both", expand=True)

sidebar = ctk.CTkScrollableFrame(main_frame, width=280)
sidebar.pack(side="left", fill="y", padx=(10, 5), pady=10)

content = ctk.CTkScrollableFrame(main_frame)
content.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

current_index = [0]

def save():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(done, f, ensure_ascii=False, indent=2)

def update_progress():
    learned = sum(1 for t in topics if done.get(t["title"]))
    total = len(topics)
    percent = learned / total
    progress_bar.set(percent)
    progress_label.configure(text=f"{round(percent * 100)}% ({learned} из {total})")

def refresh_sidebar():
    for widget in sidebar.winfo_children():
        widget.destroy()

    ctk.CTkLabel(sidebar, text="Темы", font=("Arial", 16, "bold")).pack(pady=(5, 10))

    for i, topic in enumerate(topics):
        unlocked = (i == 0) or done.get(topics[i - 1]["title"], False)
        checked = done.get(topic["title"], False)

        frame = ctk.CTkFrame(sidebar)
        frame.pack(fill="x", pady=3, padx=5)

        cb = ctk.CTkCheckBox(
            frame,
            text=topic["title"],
            command=lambda idx=i: toggle_topic(idx),
            state="normal" if unlocked else "disabled",
            font=("Arial", 13)
        )
        if checked:
            cb.select()
        cb.pack(side="left", padx=5, pady=5)

        btn = ctk.CTkButton(
            frame, text="→", width=40,
            state="normal" if unlocked else "disabled",
            command=lambda idx=i: show_topic(idx)
        )
        btn.pack(side="right", padx=5)

    ctk.CTkLabel(sidebar, text="— — —", font=("Arial", 14)).pack(pady=10)
    ctk.CTkLabel(sidebar, text="Команды", font=("Arial", 16, "bold")).pack(pady=(5, 10))

    for cmd in commands:
        ctk.CTkButton(
            sidebar, text=cmd["name"],
            command=lambda c=cmd: show_command(c),
            anchor="w", fg_color="transparent",
            border_width=1, text_color=("black", "white")
        ).pack(fill="x", pady=2, padx=5)

def show_topic(index):
    current_index[0] = index
    topic = topics[index]

    for widget in content.winfo_children():
        widget.destroy()

    ctk.CTkLabel(content, text=topic["title"], font=("Arial", 24, "bold")).pack(anchor="w", pady=(10, 5), padx=10)
    ctk.CTkLabel(content, text="📖 Теория\n\n" + topic["theory"], font=("Arial", 16), justify="left", wraplength=750).pack(anchor="w", pady=10, padx=10)
    ctk.CTkLabel(content, text="🔑 Термины\n\n" + topic["terms"], font=("Arial", 16), justify="left", wraplength=750).pack(anchor="w", pady=10, padx=10)
    ctk.CTkLabel(content, text="✏️ Практика (код)\n\n" + topic["practice"], font=("Consolas", 15), justify="left", wraplength=750).pack(anchor="w", pady=10, padx=10)
    ctk.CTkLabel(content, text="🖥️ Что выведет\n\n" + topic["output"], font=("Consolas", 15), justify="left", wraplength=750).pack(anchor="w", pady=10, padx=10)
    ctk.CTkLabel(content, text="⚠️ Ошибки и как их читать\n\n" + topic["errors"], font=("Arial", 16), justify="left", wraplength=750).pack(anchor="w", pady=10, padx=10)

    nav = ctk.CTkFrame(content)
    nav.pack(pady=20, anchor="w", padx=10)

    ctk.CTkButton(nav, text="← Назад", command=prev_topic, width=120).pack(side="left", padx=5)
    ctk.CTkButton(nav, text="Вперёд →", command=next_topic, width=120).pack(side="left", padx=5)

def show_command(cmd):
    for widget in content.winfo_children():
        widget.destroy()

    ctk.CTkLabel(content, text=cmd["name"], font=("Arial", 24, "bold")).pack(anchor="w", pady=(10, 5), padx=10)
    ctk.CTkLabel(content, text="📖 Что делает\n\n" + cmd["what"], font=("Arial", 16), justify="left", wraplength=750).pack(anchor="w", pady=10, padx=10)
    ctk.CTkLabel(content, text="✏️ Пример\n\n" + cmd["example"], font=("Consolas", 15), justify="left", wraplength=750).pack(anchor="w", pady=10, padx=10)

def toggle_topic(index):
    topic = topics[index]
    title = topic["title"]

    if index > 0 and not done.get(topics[index - 1]["title"]):
        messagebox.showwarning("Заблокировано", "Сначала пройди предыдущую тему!")
        return

    done[title] = not done.get(title, False)
    save()
    update_progress()
    refresh_sidebar()

def prev_topic():
    if current_index[0] > 0:
        show_topic(current_index[0] - 1)

def next_topic():
    if current_index[0] < len(topics) - 1:
        show_topic(current_index[0] + 1)

update_progress()
refresh_sidebar()
show_topic(0)

root.mainloop()