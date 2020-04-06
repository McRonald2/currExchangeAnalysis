"""
A program that inputs a date and prints the list of currencies for
which there is a data on that date.

Parameters:
----------
date: String
    A string which contains the chosen date to fetch the data from.
    It must be input in 'YYYY/MM/DD' format, or else the input will be ivalid.
currencyDict: Dictionary
    A dictionary of all currencies of all times. the keys are the codes of the currencies.
    the elements are the names of the currencies.
exratesDict: Dictionary
    A dictionary of all exchange rates that exist on a certain date.
noData: Boolean
    A veriable that if it's True, it means there is no data for a certain currency on a given date.
    If it's False then it means we found data for the currency.

"""

import pprint, urllib3
import exrates as ex

while True:
    try:
        date = str(input("Please enter a year in 'YYYY/MM/DD' format: "))

        currencyDict = ex.get_currencies() # Getting the currencies' list.
        exratesList = sorted(ex.get_exrates(date)) # Getting a sorted exchange rates data for the given date.

        for el in exratesList: #Going through every currency code (key) in the exrates dictionary.
            noData = True
            for key in currencyDict: #Comparing every code on exratesList to the codes (keys) on currencyDict.
                if el == key:
                    #If the data exists, print it's name and code. set the noData to False because there is data.
                    print("{} ({})".format(currencyDict[key],key))
                    noData = False
                    break
            #If there is no data for a certain currency print this:
            if noData == True:
                print("<unknown> ({})".format(el))
                
                        
    except ValueError:
        print("\nDear sir, please make sure you input in right format")
        continue
    except ex.DateDoesntExistError:
        print("\nHello, we are afraid there are no exrates for the given date.")
        print("Make sure you entered a date that exists. Try again\n")
        continue
    except urllib3.exceptions.MaxRetryError:
        print("\nHello, please check your internet connection\nand try again :).")
        continue
    else:
        break
