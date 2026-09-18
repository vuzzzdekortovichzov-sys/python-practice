import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("моё первое окно")
root.geometry("400x300")

label = ctk.CTkLabel(root, text="Добрый День!", font=("Arial", 18))
label.pack(pady=20)

root.mainloop()