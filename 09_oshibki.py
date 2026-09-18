try:
    x = int(input("введи число: "))
    print("ты ввёл:", x)
except ValueError:
    print("это не число!")
except Exception as e:
    print("ошибка:", e)