fruits = {"яблоко": "красное", "банан": "жёлтый"}
fruits["голубика"] = "голубая и кисло-сладкая"
def show_color(fruit):
    return fruits[fruit]
result = show_color("голубика")
i = 1
while i<=3:
    print(result, i)
    i = i + 1

  