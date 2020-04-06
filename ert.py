"""
A program that inputs a date and prints the exchange rates for
that date in a tabular form, sorted by the currencies names, with the first column containing the
string in the form "Name (code)" and the second one containing the exchange rate relative to the
USD, aligned to the right and written to the 5 digits precision. The data has to be retrieved using
the get_exrates function.


parameters:
----------
date: string
    The date which the program prints the list of currencies for. the date must be
    in 'YYYY/MM/DD' format.
currencyDict: dictionary
    A dictionary of all currencies of all times. it is used to match infront the
    exrates file, which currencies exist on a given date.
noData: boolean
    A veriable that is purposed to say if a certain currency code exists on the
    exchage rates list file on a given date.
ert_df: pandas.core.frame.DataFrame
    A pandas module object (A data frame) that is used to read from the csv file
    that was created earlier (ertFile). then it is sorted by the currency codes and displayed in
    a tabular form.


"""

import os, csv, urllib3
import exrates as ex
import pandas as pd

while True:
    try:
        date = str(input("Please enter a year in 'YYYY/MM/DD' format: "))  #forming the requested date in the right format

        ex.get_exrates(date)  #creating an exrates file (if isn't there one already)
        currencyDict = ex.get_currencies()  #All currencies dictionary
        
        #reading from the created exchange rates file and writing to a new ert file.
        #the ert file will eventually be the output data.
        with open(os.path.join("data","rates-{}.csv".format(date)), mode="rt",  encoding="utf8") as exFile,\
             open(os.path.join("data","ert-{}.csv".format(date)), mode="wt",encoding="utf8") as ertFile:

            exReader = csv.reader(exFile, delimiter = ",") #creating a "reader" object for "rates-..." file.
            exFile.readline()
            ertWriter = csv.writer(ertFile , delimiter = ",")#creating a "writer" object for ertFile.

            ertFile.write("Name (code), Exchange Rate\n") #Adding column titles
            for row in exReader: #going through every row in the exchange rate file.
                [code, exrate] = row
                noData = True
                for key in currencyDict:
                    if key == code:      #If there is a match between the currencies and exrates codes, add it to ertFile.
                        ertFile.write("{} ({}),{}\n".format(currencyDict[key],code,exrate))
                        noData = False   # There is a data in that date.
                        break
                if noData == True:       #If the currency does not exist any more, add a line in the format "<unknown> (code)":
                    ertFile.write("<unknown> ({}),{}\n".format(code,exrate))

        ert_df = pd.read_csv(os.path.join("data", "ert-{}.csv".format(date)))
        ert_df = ert_df.sort_values(by = "Name (code)") #The table will be sorted by the currencie names.
        pd.set_option('precision',5) #the exchange rate will be written with 5 digits precision.
        
        print(ert_df.set_index('Name (code)'))
                           
    except ex.DateDoesntExistError:
        print("\nHello, make sure you entered the date correctly.")
        print("Also, make sure you enter a date that exists.\n")
        continue
    except urllib3.exceptions.MaxRetryError:
        print("\nHello, please check your internet connection\n")
        continue
    else:
        break


    

    
