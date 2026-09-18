import customtkinter as ctk
import json
import os
from tkinter import messagebox

DATA_FILE = "progress.json"

topics = [
    {
        "title": "1. переменные и print",
        "theory": "переменная — это коробка для данных.\nprint выводит текст на экран.\n\nпример:\nname = \"тимур\"\nprint(name)",
        "terms": "print — печатать\nvariable — переменная",
        "practice": "name = \"тимур\"\nage = 16\nprint(\"меня зовут\", name)\nprint(\"мне\", age, \"лет\")",
        "output": "меня зовут тимур\nмне 16 лет",
        "errors": "NameError — если print написан с большой буквы.\nSyntaxError — если забыть кавычки."
    },
    {
        "title": "2. ввод данных (input)",
        "theory": "input спрашивает у пользователя текст и сохраняет в переменную.",
        "terms": "input — ввод\nint — целое число",
        "practice": "name = input(\"как тебя зовут? \")\nprint(\"привет, \" + name)",
        "output": "как тебя зовут? тимур\nпривет, тимур",
        "errors": "ValueError — если ввести текст вместо числа."
    },
    {
        "title": "3. условия (if / else)",
        "theory": "if проверяет условие. если правда — одно, иначе — другое.",
        "terms": "if — если\nelse — иначе\nelif — иначе если",
        "practice": "age = 16\nif age >= 18:\n    print(\"взрослый\")\nelse:\n    print(\"малой\")",
        "output": "малой",
        "errors": "SyntaxError — если забыть двоеточие."
    },
    {
        "title": "4. циклы while и for",
        "theory": "while повторяет, пока условие правда.\nfor перебирает элементы.",
        "terms": "while — пока\nfor — для\nrange — диапазон",
        "practice": "for i in range(3):\n    print(i)",
        "output": "0\n1\n2",
        "errors": "бесконечный цикл — если забыть i += 1."
    },
    {
        "title": "5. списки (list)",
        "theory": "список хранит несколько значений.",
        "terms": "list — список\nappend — добавить\nremove — удалить",
        "practice": "games = [\"тарков\", \"дст\"]\ngames.append(\"кс2\")\nfor g in games:\n    print(g)",
        "output": "тарков\nдст\nкс2",
        "errors": "IndexError — если обратиться к несуществующему индексу."
    },
    {
        "title": "6. кортежи (tuple)",
        "theory": "кортеж — как список, но его нельзя менять.",
        "terms": "tuple — кортеж",
        "practice": "days = (\"пн\", \"вт\")\nprint(days[0])",
        "output": "пн",
        "errors": "TypeError — если попытаться изменить кортеж."
    },
    {
        "title": "7. словари (dict)",
        "theory": "словарь хранит пары «ключ: значение».",
        "terms": "dict — словарь\nkey — ключ\nvalue — значение",
        "practice": "country = {\"россия\": \"москва\"}\nprint(country[\"россия\"])",
        "output": "москва",
        "errors": "KeyError — если ключа нет."
    },
    {
        "title": "8. функции (def, return)",
        "theory": "функция — кусок кода с именем.",
        "terms": "def — определить\nreturn — вернуть",
        "practice": "def add(a, b):\n    return a + b\nprint(add(5, 7))",
        "output": "12",
        "errors": "если забыть return — вернётся None."
    },
    {
        "title": "9. работа с ошибками (try / except)",
        "theory": "try пробует, except ловит ошибку.",
        "terms": "try — попробовать\nexcept — исключение",
        "practice": "try:\n    x = int(input())\nexcept:\n    print(\"ошибка\")",
        "output": "ошибка",
        "errors": "ValueError, TypeError, IndexError, KeyError."
    },
    {
        "title": "10. работа с файлами",
        "theory": "open открывает файл. with закрывает автоматически.",
        "terms": "open — открыть\nread — читать\nwrite — писать",
        "practice": "with open(\"test.txt\", \"w\", encoding=\"utf-8\") as f:\n    f.write(\"привет\")",
        "output": "привет",
        "errors": "FileNotFoundError, PermissionError, UnicodeDecodeError."
    },
    {
        "title": "11. модули и библиотеки",
        "theory": "модуль — готовый код, подключается через import.",
        "terms": "import — импорт\nmodule — модуль",
        "practice": "import random\nprint(random.randint(1, 10))",
        "output": "5",
        "errors": "ModuleNotFoundError, AttributeError."
    },
    {
        "title": "12. ооп (классы)",
        "theory": "класс — шаблон для объектов.",
        "terms": "class — класс\nobject — объект\nmethod — метод",
        "practice": "class person:\n    def __init__(self, name):\n        self.name = name\n\np = person(\"тимур\")\nprint(p.name)",
        "output": "тимур",
        "errors": "TypeError — забыл self."
    },
]

commands = [
    {"name": "print", "what": "выводит текст на экран.", "example": "print(\"привет\")"},
    {"name": "input", "what": "спрашивает текст.", "example": "name = input(\"имя: \")"},
    {"name": "int", "what": "превращает в число.", "example": "x = int(\"5\")"},
    {"name": "if / else", "what": "условия.", "example": "if x > 0:\n    print(\"+\")"},
    {"name": "while", "what": "цикл пока.", "example": "while x < 5:\n    x += 1"},
    {"name": "for", "what": "цикл для.", "example": "for i in range(3):\n    print(i)"},
    {"name": "range", "what": "диапазон чисел.", "example": "range(5)"},
    {"name": "list", "what": "список.", "example": "a = [1, 2, 3]"},
    {"name": "append", "what": "добавить в список.", "example": "a.append(4)"},
    {"name": "remove", "what": "удалить из списка.", "example": "a.remove(2)"},
    {"name": "tuple", "what": "кортеж.", "example": "t = (1, 2)"},
    {"name": "dict", "what": "словарь.", "example": "d = {\"a\": 1}"},
    {"name": "def", "what": "определить функцию.", "example": "def f():\n    pass"},
    {"name": "return", "what": "вернуть значение.", "example": "return x"},
    {"name": "try / except", "what": "обработка ошибок.", "example": "try:\n    pass\nexcept:\n    pass"},
    {"name": "open", "what": "открыть файл.", "example": "open(\"f.txt\")"},
    {"name": "with", "what": "автозакрытие файла.", "example": "with open(\"f.txt\") as f:\n    pass"},
    {"name": "\"w\"", "what": "режим записи.", "example": "open(\"f.txt\", \"w\")"},
    {"name": "\"r\"", "what": "режим чтения.", "example": "open(\"f.txt\", \"r\")"},
    {"name": "\"a\"", "what": "режим добавления.", "example": "open(\"f.txt\", \"a\")"},
    {"name": "encoding=\"utf-8\"", "what": "кодировка.", "example": "open(\"f.txt\", encoding=\"utf-8\")"},
    {"name": "read", "what": "читать файл.", "example": "f.read()"},
    {"name": "write", "what": "писать в файл.", "example": "f.write(\"hi\")"},
    {"name": "import", "what": "подключить модуль.", "example": "import random"},
    {"name": "class", "what": "создать класс.", "example": "class a:\n    pass"},
]

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        done = json.load(f)
else:
    done = {}

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("трекер python")
root.geometry("1150x750")
root.minsize(1000, 650)

top_bar = ctk.CTkFrame(root, height=60)
top_bar.pack(fill="x", side="top")

ctk.CTkLabel(top_bar, text="твой путь в python", font=("Arial", 22, "bold")).pack(side="left", padx=20, pady=10)

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

    ctk.CTkLabel(sidebar, text="темы", font=("Arial", 16, "bold")).pack(pady=(5, 10))

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
    ctk.CTkLabel(sidebar, text="команды", font=("Arial", 16, "bold")).pack(pady=(5, 10))

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
    ctk.CTkLabel(content, text="📖 теория\n\n" + topic["theory"], font=("Arial", 16), justify="left", wraplength=750).pack(anchor="w", pady=10, padx=10)
    ctk.CTkLabel(content, text="🔑 термины\n\n" + topic["terms"], font=("Arial", 16), justify="left", wraplength=750).pack(anchor="w", pady=10, padx=10)
    ctk.CTkLabel(content, text="✏️ практика (код)\n\n" + topic["practice"], font=("Consolas", 15), justify="left", wraplength=750).pack(anchor="w", pady=10, padx=10)
    ctk.CTkLabel(content, text="🖥️ что выведет\n\n" + topic["output"], font=("Consolas", 15), justify="left", wraplength=750).pack(anchor="w", pady=10, padx=10)
    ctk.CTkLabel(content, text="⚠️ ошибки и как их читать\n\n" + topic["errors"], font=("Arial", 16), justify="left", wraplength=750).pack(anchor="w", pady=10, padx=10)

    nav = ctk.CTkFrame(content)
    nav.pack(pady=20, anchor="w", padx=10)

    ctk.CTkButton(nav, text="← назад", command=prev_topic, width=120).pack(side="left", padx=5)
    ctk.CTkButton(nav, text="вперёд →", command=next_topic, width=120).pack(side="left", padx=5)

def show_command(cmd):
    for widget in content.winfo_children():
        widget.destroy()

    ctk.CTkLabel(content, text=cmd["name"], font=("Arial", 24, "bold")).pack(anchor="w", pady=(10, 5), padx=10)
    ctk.CTkLabel(content, text="📖 что делает\n\n" + cmd["what"], font=("Arial", 16), justify="left", wraplength=750).pack(anchor="w", pady=10, padx=10)
    ctk.CTkLabel(content, text="✏️ пример\n\n" + cmd["example"], font=("Consolas", 15), justify="left", wraplength=750).pack(anchor="w", pady=10, padx=10)

def toggle_topic(index):
    topic = topics[index]
    title = topic["title"]

    if index > 0 and not done.get(topics[index - 1]["title"]):
        messagebox.showwarning("заблокировано", "сначала пройди предыдущую тему!")
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