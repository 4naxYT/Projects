"""
Task given on : 14-07-2026 (d/m/y)
In class.

Added more functionality and safety + a one-liner
"""

def bill_return(previous,latest,rate=6.85,tax=0.06): # all variables we'll use + constants
    """ Documentation for `return`
    
    :      initiates formatting 
    ,      adds comma in thousands place 
    2f     is 2 points of decimal precision (also rounds to the closest)

    """
    try:
        curr = float(previous) - float(latest)
        sub_total = curr * rate
        tax_amt = sub_total * tax
        total = sub_total + tax_amt
        return f"\nBill Amount: ₹{total:,.2f}"
    except Exception as err:
        return f"\nError Occurred: [ {err} ]"

# Takes Input and calculates result
Result = bill_return(input('Enter Previous Price: '),
                     input('Enter latest Price: '  ))

# f string magic for formatting and inserting my var
print(Result)

input("\nPress Enter to Exit...") # powershell happi :3


r'''  One Liner, you can execute in `IDLE` : (no try/except)

bill_return = lambda p, l, r=6.85, t=0.06: f"{((p-l)*r*(1+t)):,.2f}"; Result = bill_return(float(input('Enter Previous Price: ')), float(input('Enter latest Price: '))); print(f"\nBill Amount: ₹{Result}"); input("\nPress Enter to Exit...")
'''
