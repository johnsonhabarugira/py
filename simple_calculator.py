def add(a, b):
    return a + b
def substract(a, b):
    return a - b
def multiply(a, b):
    return a * b
def division(a, b):
    if b == 0:
        return "error: divion by zero"
    return a / b
print("Simple Calculator")
print("Operators: + - / * ")

while True:
    num1 = float(input("Enter Digit one"))
    op = input("enter operator")
    num2 = float(input("inter digit 2"))

    if op == "+":
        print("result:",add(num1, num2))