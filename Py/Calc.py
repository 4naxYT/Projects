print("Result: ",(lambda exp_: eval(exp_))(input("Enter your sum: ")));x=input("")

# one-liner advanced calculator code for (+,-,*,/,**)

# explanation:
#     print() is used to print the result
#     (lambda : )() is a one-line function, ie, a shortened version of "def."
#     eval() evaluates a string/input as code
#     input() takes an input from the user
#     ; basically a new line in code terms
#     x=input("") is for powershell / cmd as it instantly closes if this line isnt aded

# code expanded for understanding:

# def calc(exp_):
#     return eval(exp_)
# exp_ = input("Enter your sum: ")
# result = calc(exp_)
# print("Result: ", result)
# x = input("")
