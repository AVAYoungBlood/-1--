import math

def calculate(expression): #Создаёт главную функцию calculate
    pos = 0 #позицию текущего символа в строке

    def skip_spaces(): #просмотр пробелов
        nonlocal pos #изменяем внешнюю переменную pos, не новую
        while pos < len(expression) and expression[pos] == " ": #не конец и пробел
            pos += 1

    def read_number(): #чтение числа
        nonlocal pos #изменяем внешнюю переменную pos, не новую
        start = pos

        while pos < len(expression) and (expression[pos].isdigit() or expression[pos] == "."):
            pos += 1

        if start == pos:
            raise ValueError("Ожидается число") #выдает ошибку для сивола и числа

        return float(expression[start:pos]) #убирает лишние символы

    def plus_minus():
        nonlocal pos #изменяем внешнюю переменную pos, не новую
        value = multiply_divide() #разбор по переменным по действиям

        while True:
            skip_spaces() #убираем пробелы

            if pos < len(expression) and expression[pos] in "+-": #+ или -
                sign = expression[pos] #cохраняет
                pos += 1
                number = multiply_divide() #cначало старшую операцию

                if sign == "+":
                    value = value + number
                else:
                    value = value - number
            else:
                return value

    def multiply_divide(): #для * и /
        nonlocal pos
        value = unary()

        while True:
            skip_spaces() #пропуск пробела

            if pos < len(expression) and expression[pos] in "*/":
                sign = expression[pos] #сохраняем знак
                pos += 1
                number = unary() #первый множитель или делитель

                if sign == "*":
                    value = value * number
                else:
                    if number == 0:
                        raise ZeroDivisionError("Деление на ноль") #проверка про деление на ноль
                    value = value / number
            else:
                return value

    def unary(): #знак пере числом, скобкой
        nonlocal pos
        skip_spaces()

        if pos < len(expression) and expression[pos] == "-":
            pos += 1
            return -unary() #Рекурсивно вычисляет то, что стоит после минуса, и меняет знак результата

        if pos < len(expression) and expression[pos] == "+":
            pos += 1
            return unary()

        return element() #Если знака нет, переходит к числу, скобке или функции

    def element(): #обработка синуса и экспоненты
        nonlocal pos
        skip_spaces()

        if pos < len(expression) and expression[pos] == "(":
            pos += 1
            value = plus_minus() #Рекурсивно вычисляет всё выражение внутри скобок, скобки имеют наивысший приоритет
            skip_spaces()

            if pos >= len(expression) or expression[pos] != ")":
                raise ValueError("Нет закрывающей скобки")

            pos += 1
            return value

        if expression.startswith("sin", pos):
            pos += 3
            return function_value(math.sin)

        if expression.startswith("exp", pos):
            pos += 3
            return function_value(math.exp)

        return read_number()

    def function_value(function): #расчет синуса и экспоненты
        nonlocal pos
        skip_spaces()

        if pos >= len(expression) or expression[pos] != "(":
            raise ValueError("Нужна открывающая скобка")

        pos += 1
        number = plus_minus()
        skip_spaces()

        if pos >= len(expression) or expression[pos] != ")":
            raise ValueError("Нужна закрывающая скобка")

        pos += 1
        return function(number)

    result = plus_minus()
    skip_spaces()

    if pos != len(expression):
        raise ValueError("Некорректное выражение")

    return result


print("Простой калькулятор")
print("Можно вводить: +, -, *, /, скобки, sin(), exp()")
print("Для выхода введите 0")

while True:
    text = input("\nВведите выражение: ").strip()

    if text.lower() == "0":
        print("Выход")
        break

    try:
        print("Результат:", calculate(text))
    except Exception as error:
        print("Ошибка:", error)