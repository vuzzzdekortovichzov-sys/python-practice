with open("test.txt", "w", encoding="utf-8") as f:
    f.write("я учу python")

with open("test.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)