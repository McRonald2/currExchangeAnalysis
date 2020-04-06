"""
A program that inputs two dates, and list of currencies (allow them to be given as lower or upper
case strings). It analyzes the change (in %) of the exchange rate during that period, and prints a
table that lists for each currency the maximal exchange rate, the minimal exchange rate and the diff
between the maximal exchange rate to the minimal exchange rate. The table is then sorted in
descending order of the diff between max to min.


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
fixed_currLst: List
    A temporary list that is used to store all currencies codes that the user entered, and
    that exist on the currencies list of all times.
minChange: Float
    The minimum change of a currency in 'currLst' exchange rate (in %) between dates 'date1' and 'date2'.
maxChange: Float
    The maximum change of a currency in 'currLst' exchange rate (in %) between dates 'date1' and 'date2'.
todayChange: Float
    An absolute change of a currency in 'currLst' exchange rate (in %) between 'date1' and 'tempdate'.
    every time todayChange change it may effect the values of maxChange and minChange.
maxDiff: Float
    A veriable that represents the maximum change there was for a certain currency.
difference: Float
    The difference between maxChange and minChange in USD.
PreratesDict: Dictionary
    A dictionary of exchange rates for date 'date1'. through out the program, it is always
    compared to RatesDict elements to messure the change.
RatesDict: Dictionary
    A dictionary that gets updated everytime 'tempdate' changes. it is used to get info. about
    the exchange rates of the currency codes on 'currLst'.
analyze_df: pandas.core.frame.DataFrame
    A pandas module object (A data frame) that is used to read from the csv file
    that was created earlier ('analyze.csv'), and display/printtable that lists for
    each currency the maximal exchange rate, the minimal exchange rate and the diff
    between the maximal exchange rate to the minimal exchange rate.
"""

import os, csv, urllib3
import exrates as ex
import pandas as pd
from datetime import timedelta, datetime

while True:
    try:
        #Setting a date format for the datetime class objects.
        date_format = "%Y-%m-%d"

        #The program inputs two dates and a list currency codes.
        date1 = str(input("Hello, please input the first date: ")) or datetime.now().strftime(date_format)
        date1 = datetime.strptime(date1, date_format)
        date2 = str(input("Hello, please input the second date: ")) or datetime.now().strftime(date_format)
        date2 = datetime.strptime(date2, date_format)
        currLst = str(input("Please enter all currencies' codes you want to check (comma-separated): "))

        #Raise error because there is no change in currencies' change rates on the same date.
        if date1 == date2: 
            raise ValueError()

        #'date1'must always be the earlier date.
        if date1 > date2:
            tempdate = date2
            date2 = date1
            date1 = tempdate

        #creating a list of the desired currencies (deleting whitespaces)
        currLst = (" ".join(currLst.split(","))).split()

        # A dictionary of all currencies that ever been.
        currDict = ex.get_currencies()
        
        # A new list to store only the currencies that exist in currencies list (currDict).
        fixed_currLst = list()
        for i in range(len(currLst)):
            if currLst[i].upper() in currDict:
                fixed_currLst.append(currLst[i])
        currLst = fixed_currLst
        print(currLst)

        #If the list of currencies is empty, the input is invalid.
        if currLst == list():
            raise ex.CurrencyDoesntExistError()
        
        #uppercasing all currLst elements.
        currLst = [element.upper() for element in currLst]

        #Create a csv file 'analyze.csv'.
        #We store all our information in this file so we can print it later.
        with open(os.path.join("data","analyze.csv"), mode="wt",  encoding="utf8") as analyzeFile:
                    analyzeWriter = csv.writer(analyzeFile , delimiter = ",")

                    #Write the first columns titles.
                    analyzeFile.write("Currency, Min. Change, Max. Change,Difference\n")
                    
                    # Setting a temporary date to run through all the dates.
                    # It's first value is one day after 'date1' because we measure change.
                    tempDate = date1 + timedelta(days=1)
                    
                    for i in range(len(currLst)):

                        # A temporary float veriable to store the minimum change of a certain currency.
                        minChange = 0.0
                        # A temporary float veriable to store the minimum change of a certain currency.
                        maxChange = 0.0
                        # A temporary float veriable to store the difference between the maximum value
                        # of a certain currency compared to the value on 'date1'.
                        maxDiff = 0.0
                        # A temporary float veriable to store the difference between the max and min change.
                        difference = 0.0

                        #Finding the Maximal change
                        while tempDate <= date2:
                            # Setting dictionries of exchange rates for a current day and the previous.
                            PreRatesDict = ex.get_exrates(date1.strftime(date_format))
                            RatesDict = ex.get_exrates(tempDate.strftime(date_format))

                            #The currency code must exist in the exchange rates dictionaries,
                            #else it get zero as a value because there was no currency and the difference is zero.
                            if currLst[i] in RatesDict and currLst[i] in PreRatesDict:

                                #Every time 'tempDate' changes, 'todayChange' gets updated too.
                                #The change is represented with %.
                                todayChange = abs(float(RatesDict[currLst[i]])/float(PreRatesDict[currLst[i]])-1)*100

                                #Every time there is a change bigger than maxChange, update maxChange.
                                if maxChange < todayChange:
                                    maxChange = todayChange
                                    maxDiff = float(RatesDict[currLst[i]]) - float(PreRatesDict[currLst[i]])
                                    
                            #Set tempDate to the next day.
                            tempDate = tempDate + timedelta(days=1)

                        #Finding the Minimal change
                        tempDate = date1 + timedelta(days=1)
                        while tempDate <= date2:
                            
                            # Setting dictionries of exchange rates for a current day and the previous.
                            PreRatesDict = ex.get_exrates(date1.strftime(date_format))
                            RatesDict = ex.get_exrates(tempDate.strftime(date_format))
                            
                            #The currency code must exist in the exchange rates dictionaries,
                            #else it gets zero as a value because there was no currency and the difference is zero.
                            if currLst[i] in RatesDict and currLst[i] in PreRatesDict:
                                
                                #Here also, every time 'tempDate' changes, 'todayChange' gets updated too.
                                #The change is represented with %.
                                todayChange = abs(float(RatesDict[currLst[i]])/float(PreRatesDict[currLst[i]])-1)*100

                                #If 'todayChange' is zero, it means that there will be no smaller change.
                                #so the minimum change is '0' and finish gets True, so we break the loop, because we are done.
                                finish = False
                                if todayChange == 0:
                                    minChange = 0
                                    difference = maxDiff
                                    finish = True
                            if finish == True:
                                break

                            # If minChange is '0' (because it is it's first value), update it to be equal to todayChange.
                            if currLst[i] in RatesDict and currLst[i] in PreRatesDict:
                                if minChange == 0:
                                    minChange = todayChange
                                    #update 'difference'
                                    difference = str(float(maxDiff) - (float(RatesDict[currLst[i]])- float(PreRatesDict[currLst[i]])))

                                # If 'minChange' is greater than 'todayChange', update it to be the 'todayChange'.
                                elif minChange > todayChange:
                                    minChange = todayChange
                                    difference = str(float(maxDiff) - (float(RatesDict[currLst[i]])- float(PreRatesDict[currLst[i]])))

                            # If the currency code's exchange rate doesn't exist, and there was no change in min change
                            elif minChange == 0:
                                difference = maxDiff

                            tempDate = tempDate + timedelta(days=1)
                        
                        analyzeFile.write("{},{}%,{}%,{}\n".format(currLst[i],minChange, maxChange, difference))
                        tempDate = date1 + timedelta(days=1)

        analyze_df = pd.read_csv(os.path.join("data", "analyze.csv"))
        analyze_df = analyze_df.sort_values(by = 'Difference', ascending = False)
        pd.set_option('precision',5)
        print(analyze_df.set_index('Currency'))
                        
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
    except ValueError:
        print("\nHi, it looks like somthing wrong. try again and check the following things:")
        print("1. Make sure to write dates in YYYY-MM-DD format")
        print("2. Make sure you entered at least one currency to analyze.")
        print("3. Make sue to enter the currency code correctly.")

    else:
        break
