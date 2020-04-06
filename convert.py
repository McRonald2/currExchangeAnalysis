
"""
A program that inputs two dates, an amount, and codes of two currencies.
It then prints a table with the amount converted between those currencies,
in both directions,using the exchange rates on the given date period.

Parameters:
----------
date1: String
    The user inputs a date as a string in'YYYY-MM-DD' format.
date2: String
    The user inputs a second date (for comparison) as a string in'YYYY-MM-DD' format.
amount: Float
    The amount of money the user would like to convert
curr1: String
    The first currency code the user would like to see the conversion for.
curr2: String
    The second currency code the user would like to see the conversion for.
convert_df: pandas.core.frame.DataFrame
    A pandas module object (A data frame) that is used to read from the csv file
    that was created earlier (convTable), and display/print a table of the
    amount, dates, and currencies codes.
    

"""

import os, csv, urllib3
import exrates as ex
import pandas as pd
from datetime import timedelta, datetime

while True:
    try:
        date_format = '%Y-%m-%d'
        # Input two dates.
        # If there was no input, take the date of today.
        date1 = str(input("Hello, please input the first date: ")) or datetime.now().strftime(date_format)
        date2 = str(input("Hello, please input the second date: ")) or datetime.now().strftime(date_format)
        # Input the amount we want to convert.
        amount = float(input("Please enter an amount you would like to convert: "))
        # Input the currencies we want to compute the conversion between.
        curr1 = str(input("Please input the first cuurency code: "))
        curr2 = str(input("Please input the second cuurency code: "))
        
        # Writing in a new CSV file, named convert and later on, we will display it.
        with open(os.path.join("data","convert.csv"), mode="wt",  encoding="utf8") as convTable:
            # A csv writer object.
            convWriter = csv.writer(convTable , delimiter = ",")
            
            #writing the first row. the titles.
            convTable.write("Codes to convert, Amount, {}, {}\n".format(date1,date2))
            #Writing the conversion information from onw currency to the other, in both directions.
            convTable.write("{} to {}, {}, {}, {}\n".format(curr1.upper(), curr2.upper(), amount,
                                                            ex.convert(amount, curr1, curr2, date1),
                                                            ex.convert(amount, curr1, curr2, date2)))
            convTable.write("{} to {}, {}, {}, {}\n".format(curr2.upper(), curr1.upper(), amount,
                                                            ex.convert(amount, curr2, curr1, date1),
                                                            ex.convert(amount, curr2, curr1, date2)))

        #creating a pandas object to print the desired table with.
        convert_df = pd.read_csv(os.path.join("data", "convert.csv"), index_col="Codes to convert")
        print(convert_df)
    except ex.DateDoesntExistError:
        print("\nHello, we are afraid there are no exrates for the givven date.")
        print("Make sure you entered a date that exists.\n")
        continue
    except urllib3.exceptions.MaxRetryError:
        print("\nHello, please check your internet connection.\n")
        continue
    except ex.CurrencyDoesntExistError:
        print("\nHello, one or both of the currencies you've entered do not exist.")
        print(" Please check your input and type again.\n")
        continue
    except ValueError:
        print("\nHello, we have encountered a problem. we suggest to check the input:")
        print(" 1. Make sure you entered a number in the amount section")
        print(" 2. Make sure you entered a possible date.\n    make sure the days are not over 31, and the months not over 12.\n")
        continue

    else:
        break
    
    
        
        
            
                            


        




