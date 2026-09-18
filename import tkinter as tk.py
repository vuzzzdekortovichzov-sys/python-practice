import tkinter as tk

root = tk.Tk()
root.title("Менеджер аккаунтов")
root.geometry("400x300")

label = tk.Label(root, text="Здравствуйте, тимур", font=("Arial", 16))
label.pack(pady=20)

def say_hello():
    label.config(text="Работает!")

button = tk.Button(root, text="Нажми меня", command=say_hello)
button.pack()

root.mainloop()