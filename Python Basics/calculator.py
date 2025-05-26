a = 10
while(a > 0):
    num1 = int(input("Enter first number : "))
    opr = input("Enter operator")
    num2 = int(input("Enter second number : "))
    if(opr == "+"):
        print(num1 + num2)
    elif(opr == "-"):
        print(num1 - num2)
    elif(opr == "*"):
        print(num1 * num2)
    elif(opr == "/"):
        print(num1 / num2)
    elif(opr == "**"):
        print(num1**num2)
    elif(opr == "%"):
        print(num1 % num2)
    else:
        print("Invalid Operator")
    a = a - 1
