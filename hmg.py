"""
A program that inputs two integers, year and month, a comma-separated list of
currency codes (for example, "ILS,GBP,eur,cAd"), and a file name.
It then saves the graph of the exchange rates changes (in percentage (%))
relative to the USD for the given month and year, in a png file.

Parameters:
----------
year: Integer
    The year we want to get the change percentage to.
month: Integer
    The month we want to get the change percentage to.
currLst: List
    A list of desired currencies, that the user want to get data about.
file_name: String
    The file name or the path to the file with it's name.
date: String
    represents the first day of the month 'month'.
until_date: String
    represents the first day of the next month after 'month'.
    we want to go through every day of a chosen month.
currDict: Dictionary
    A dictionary of all currencies of all times. Later on, it is used to check for every
    currency code which the user entered if it exists.
fixed_currLst: List
    A temporary list that is used to store all currencies codes that the user entered, and
    that exist on the currencies list of all times.
finish: Boolean
    A veriable which tells us that we are on the last date, and after we finish writing
    the current row in the csv file ('file_name') we break the loop and finish.
PreratesDict: Dictionary
    A dictionary that gets updated everytime 'date' changes. it always gets a date one day
    before 'date' so we could compare and find the change in percentage of exchange rates
    between the current day 'date' and the day before.
ratesDict: Dictionary
    A dictionary that gets updated everytime 'date' changes. it is used to get info. about
    the exchange rates of the currency codes on 'currLst'.
tempLst: List
    This list represents a row of values to append to the file we are creating.
    every day it gets updated with the values of the date and the change (in %) of
    the exchange rate relatively to the day before.
hmg_df: pandas.core.frame.DataFrame
    A pandas module object (A data frame) that is used to read from the csv file
    that was created earlier (hmgFile), and display/print a graph that represents
    all the change (in %) of every currency that the user requested and there was
    information on.

"""

import os, csv, urllib3
import exrates as ex
import pandas as pd
from datetime import timedelta, datetime
import matplotlib as mpl
import matplotlib.pyplot as plt

while True:
    try:
        # Input a year, a month, a currency list and a file name.
        year = int(input("Hi, please enter a preferable year: "))
        month = int(input("Hi, please enter a preferable month: "))
        currLst = str(input("Please enter all currencies' codes you want to check (comma-separated): "))
        if currLst == "": # If the list of currencies is empty, the input is invalid.
            raise ValueError()
        file_name = str(input("Please enter a path or just a file name to store the data: "))

        # Building a date veriable to start from (the first of the month), and
        # a date as the first of the next month to finish.
        if month < 10:
            date = "{}-0{}-{}".format(year,month,"01")
            if month != 9:
                until_date = "{}-{}-01".format(year,month+1)
            else:
                until_date = "{}-10-01".format(year)
        else:
            date = "{}-{}-{}".format(year,month,"01")

        if month == 12:
            until_date = "{}-01-01".format(year+1)

        #converting 'date' and 'until_date' to datetime objects.    
        date_format = "%Y-%m-%d"
        date = datetime.strptime(date, date_format)
        until_date = datetime.strptime(until_date, date_format)

        # Getting reed of any unnecessary white sapces in currLst.
        currLst = (" ".join(currLst.split(","))).split() 

        currDict = ex.get_currencies()
        fixed_currLst = list() # A new list to store only the currencies that exist in currencies list (currDict).
        for i in range(len(currLst)):
            if currLst[i].upper() in currDict:
                fixed_currLst.append(currLst[i])
        currLst = fixed_currLst

        # Check again. If the list of currencies is empty, the input is invalid.
        if currLst == list():
            raise ValueError()

        currLst = [element.upper() for element in currLst] #uppercasing all currLst elemnts.


        with open("{}.csv".format(file_name), mode="wt", encoding="utf8") as hmgFile:
            hmgWriter = csv.writer(hmgFile, delimiter = ",")
            hmgFile.write("Date, {}\n".format(",".join(currLst)))

            # Starting calculating the change from day two.
            date = date +timedelta(days=1) 
            #Going through every day between date and until_date.
            while date < until_date:
                tempLst = list()
                #Write the current date in the current row
                hmgFile.write("{},".format(date.strftime(date_format)))
                #Getting the exchange rates data for the current day and the previous one.
                PreratesDict = ex.get_exrates((date-timedelta(days=1)).strftime(date_format))
                ratesDict = ex.get_exrates(date.strftime(date_format))
                
                # Going through every currency code in currLst.
                # If there is data of exchange rate for the currency for the current date
                # and the previous one, compute the change pecentage.
                # If not, consider it as zero change.
                for i in range(len(currLst)):
                    if currLst[i] in ratesDict and currLst[i] in PreratesDict:
                        tempLst.append(str((float(ratesDict[currLst[i]])/float(PreratesDict[currLst[i]])-1)*100))
                    else:
                        tempLst.append("0")
                hmgFile.write("{}\n".format(",".join(tempLst)))
                date = date + timedelta(days=1)
        # Read the csv file we created ('hmgFile')
        hmg_df = pd.read_csv('{}.csv'.format(file_name), encoding='utf8', parse_dates=['Date'], dayfirst=True, index_col='Date')
        # Plot hmg_df table.
        hmg_df.plot()
        plt.grid(True)
        #Give a title and a label.
        plt.title("History of one Month Graph changes")
        plt.ylabel("Change of exrates (in %)")
        plt.legend()
        # Save the graph as a 'png' file in the current directory.
        plt.savefig('hmg_Graph.png')
        plt.show()        
    except urllib3.exceptions.MaxRetryError:
        print("\n----->Hello, please check your internet connection\nand try again :).")
        continue
    except ex.CurrencyDoesntExistError:
        print("\n----->Hello, no such currency exist. Please check your input.")
        continue
    except ex.DateDoesntExistError:
        print("\nHello, we are afraid there are no exrates for the given date.")
        print("Make sure you entered a date that exists. Try again\n")
        continue
    except ValueError:
        print("\nHi, it looks like somthing wrong. try again and check the following things:")
        print("1. Make sure to write a year in YYYY format.")
        print("2. Make sure you enter a month as a simple number (Example: '3').")
        print("3. Make sure you entered at least one currency to analyze.")

    else:
        break








