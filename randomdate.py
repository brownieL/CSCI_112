import random

"""
Returns a random date everytime it is called 
It returns a string in the format YYYY-MM-DD
"""
    
def randomizer_date():
    year = random.randint(1980,2021)
    month = random.randint(1,12)
    day = random.randint(1,31)
    
    zero1 = ""
    zero2 = ""
    if month < 10:
        zero1 = '0'
    if day < 10:
        zero2 = '0'
    
    return str(year) + "-" + zero1 + str(month) + "-" + zero2 + str(day)

