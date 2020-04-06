"""
A program that inputs two dates, a comma-separated list of currency codes,
and a file name. It then saves the exchange rates relative to the USD
between those two dates for the given currencies in CSV file of the given
name (in the current directory if no path is given).

Parameters:
----------
date_format: String
    A string to store the date format to define the datetime object later.
    It contains only a year, month and a day ('YYYY-MM-DD').
date1: String --> Datetime object
    The user inputs the first date as a string. Then it is converted to a datetime object.
    we use a real date object so we can go through every day between date1 and date2 easily.
date2: String --> Datetime object
    The second date the user inputs.
tempdate: Datetime object
    A temporary date that is used to help switch between date1's and date2's values,
    if date1 is later than date2.
currLst: List
    A list of desired currencies, that the user want to get data about their exchange rates.
file_name: String
    The name of the file we save in the data about the currencies and the exchange rates.
currDict: Dictionary
    A dictionary of all currencies of all times. Later on, it is used to check for every
    currency code which the user entered if it exists.
fixed_currLst: List
    A temporary list that is used to store all currencies codes that the user entered, and
    that exist on the currencies list of all times.
finish: Boolean
    A veriable which tells us that we are on the last date, and after we finish writing
    the current row in the csv file ('file_name') we break the loop and finish.
tempLst: List
    A temporary list which contains (one row at a time) the exchange rates of the currency codes
    in 'currLst' for a certain date.
ratesDict: Dictionary
    A dictionary that gets updated everytime 'date1' changes. it is used to get info. about
    the exchange rates of the currency codes on 'currLst'.


"""

import os, csv, urllib3
import exrates as ex
import pandas as pd
from datetime import timedelta, datetime

while True:
    try:
        date_format = "%Y-%m-%d"
        # Input the dates, the desired currency list and the desired file name to save the data to.
        date1 = str(input("Hello, please input the first date: "))
        date1 = datetime.strptime(date1, date_format)
        date2 = str(input("Hello, please input the second date: "))
        date2 = datetime.strptime(date2, date_format)
        currLst = str(input("Please enter all currencies' codes you want to check (comma-separated): "))
        file_name = str(input("Please enter a path or just a file name to store the data: "))
        
        # If date1 is later, switch the values between date1 and date2
        if date1 > date2:
            tempdate = date2
            date2 = date1
            date1 = tempdate
            
        # Getting reed of any unnecessary white sapces in currLst.
        currLst = (" ".join(currLst.split(","))).split() 

        currDict = ex.get_currencies()
        fixed_currLst = list() # A new list to store only the currencies that exist in currencies list (currDict).
        # Every currency that did not ever exist we ignore. we add only existent currency codes.
        for i in range(len(currLst)):
            if currLst[i].upper() in currDict:
                fixed_currLst.append(currLst[i])
        # updating currLst and adding only existent currencies.
        currLst = fixed_currLst
        
        # If there are no valid currencies, the input is considered invalid.
        if currLst == list():
            raise ValueError()

        #Uppercasing all currLst's values.
        currLst = [element.upper() for element in currLst]

        # Creating the desired file.
        with open("{}.csv".format(file_name), mode="wt", encoding="utf8") as histFile:
            
            histWriter = csv.writer(histFile, delimiter = ",")
            #Write the first row of titles in the created file.
            histFile.write("Date, {}\n".format(",".join(currLst)))

            #Going through every day between date1 and date2.
            while date1 <= date2:
                finish = False
                tempLst = list()
                if date1 == date2:
                    finish = True
                    #Write the current date.
                    histFile.write("{},".format(date1.strftime(date_format)))
                    #Get the exchange rates data for the current date.
                    ratesDict = ex.get_exrates(date1.strftime(date_format))
                    #If there is data for the codes on currLst on that date, write them in the file.
                    #Else write "-" instead.
                    for i in range(len(currLst)):
                        if currLst[i] in ratesDict:
                            tempLst.append(ratesDict[currLst[i]])
                        else:
                            tempLst.append("-")
                    histFile.write("{}\n".format(",".join(tempLst)))
                if finish:
                    break

                #Write the current date.
                histFile.write("{},".format(date1.strftime(date_format)))
                #Get the exchange rates data for the current date.
                ratesDict = ex.get_exrates(date1.strftime(date_format))
                #If there is data for the codes on currLst on that date, write them in the file.
                #Else write "-" instead.
                for i in range(len(currLst)):
                    if currLst[i] in ratesDict:
                        tempLst.append(ratesDict[currLst[i]])
                    else:
                        tempLst.append("-")
                histFile.write("{}\n".format(",".join(tempLst)))
                date1 = date1 + timedelta(days=1)
                        
                        

    except ValueError:
        print("Hey, CHECK your input")
        continue
    except urllib3.exceptions.MaxRetryError:
        print("\nHello, please check your internet connection\n")
        continue
    except ex.CurrencyDoesntExistError:
        print("\n----->Hello, no such currency exist. Please check your input.")
        continue
    except ex.DateDoesntExistError:
        print("\nHello, we are afraid there are no exrates for the given date.")
        print("Make sure you entered a date that exists. Try again\n")
        continue
    except PermissionError:
        print("\nHello, we can't make any changes while the file you're asking is still open")
        print("Please close the file and try again:\n")
        continue
    
    else:
        break

    


