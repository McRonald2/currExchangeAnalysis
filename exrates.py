"""
                                exrates module
                                --------------
The module implements fetching, saving, and analysis of the historical exchange rates.
The module provides the following functions:

The functions:
-------------
1. _fetch_currencies()
2. _fetch_exrates(date)
3. _save_currencies(currencies)
4. _save_exrates(date, rates)
5. _load_currencies()
6. _load_exrates(date)
7. get_currencies()
8. get_exrates(date)
9. convert(amount, from_curr, to_curr, date)


"""
from bs4 import BeautifulSoup
import urllib3, json, csv, os, sys
import numpy as np
from pprint import pprint
from datetime import datetime

# The datetime object format we want.
date_format = "%Y-%m-%d"

# Defining Errors if a requested date or currency does not exist
class DateDoesntExistError(Exception):
    pass
class CurrencyDoesntExistError(Exception):
    pass

# Definig global URLs.
#for currency list.
urlCurrencies = "http://openexchangerates.org/api/currencies.json"
#for exchange rates list.
urlExrates = "https://openexchangerates.org/api/historical/{}.json?app_id={}"

#If there is no 'app.id' file stop the program and return a proper descriptive message.
try:
    app= open(os.path.join('app.id.txt'), mode="rt", encoding="utf8")
    appid=str(app.read().strip())
except Exception:
    sys.stderr.write("Hello, something went wrong with opening or reading the ID file")
    sys.exit(-17)

def _fetch_currencies():
    """
    A function that fetches the currencies list from here
    (http://openexchangerates.org/api/currencies.json) and returns it as a dictionary.

    parameters:
    ----------
    data: Dictionary
        A dictionary of all currencies names and codes.

    return:
    ------
    data: Dictionary
        Explained above.
    """
    #Don't show any warning signs
    urllib3.disable_warnings()
    #Managing the connection to the host.
    http = urllib3.PoolManager()
    response = http.request('GET', urlCurrencies)
    
    soup = BeautifulSoup(response.data, "html.parser")
    data = json.loads(soup.decode("utf8"))
    return(data)

def _fetch_exrates(date):
    """
    _fetch_exrates(date) that fetches the exchange rates for the date date from the Open
    Exchange Rates (https://openexchangerates.org/) website and returns it as a dictionary.
    date must be in "%Y-%m-%d" format.

    Parameters:
    ----------
    date: string
    the date we want to get exchange rates at.
    date: Dictionary
    A dictionary of all exchange rates values and currencies codes.

    return:
    ------
    A dictionary of exchange rates for 'date'.
    """
    app = open(os.path.join("app.id.txt"), mode="rt", encoding="utf8")
    app_id = str(app.read().strip())
    try:
        urllib3.disable_warnings()
        http = urllib3.PoolManager()
        response = http.request('GET', urlExrates.format(date, app_id))
        soup = BeautifulSoup(response.data, "html.parser")
        data = json.loads(soup.decode("utf8"))
        return(data['rates'])
    except KeyError:
        raise DateDoesntExistError()

def _save_currencies(currency):
    """
    A function that saves the dictionary currencies in the currencies file,
    as described below.

    currency: Dictionary
    A dictionary of currencies' names and codes.
    """
    NewPath = r'data'
    if not os.path.exists(NewPath):
        os.makedirs(NewPath)

    with open(os.path.join(NewPath,'currencies.csv'), mode="wt", encoding="utf8") as currencyFile:
        currencyFile.write(str(",".join(["Code","Name\n"])))

        for key in currency:
            currencyFile. write(key+",")
            currencyFile. write(currency[key]+"\n")

            
def _save_exrates(date, rates):
    """
    A function that saves the exchange rates data for date date in the
    appropriate exchange rates file.

    
    date: String
        A desired date to save exchange rates data.
    rates: Dictionary
        A dictionary of exchange rates for date 'date'.
    """
    NewPath = r'data'
    if not os.path.exists(NewPath):
        os.makedirs(NewPath)

    with open(os.path.join(NewPath, 'rates-{}.csv'.format(date)), mode="wt", encoding="utf8") as exratesFile:
        exratesFile.write(str(",".join(["Code","Rate\n"])))

        for key in rates:
            exratesFile.write(key+",")
            exratesFile.write(str(rates[key])+"\n")


def _load_currencies():
    """
    A function that returns the currencies loaded from the currencies file as a dictionary.
    
    Return:
    ------
    CurrencyDict: Dictionary
        A dictionary that gets all data from the currencies file in 'data' folder.
        than when it's done appending it get returned.
    """
    NewPath = r'data'
    if not os.path.exists(NewPath):
        os.makedirs(NewPath)

    with open(os.path.join(NewPath,'currencies.csv'),mode="rt", encoding="utf8") as currenciesF:
        CurrencyReader = csv.reader(currenciesF, delimiter = ",")
        CurrencyDict = dict()
        for row in CurrencyReader:
            [code, name] = row
            CurrencyDict[code] = name

    return CurrencyDict

def _load_exrates(date):
    """
    A function that returns the exchange rates data for date 'date' loaded from the
    appropriate exchange rates file.

    Parameters:
    ----------
    date: String
       A requested date (that must be in '%Y-%m-%d' format) to get exhange rate
       data for.

    Return:
    ------
    exratesDict: Dictionary
        A dictionary that gets all data from the appropriate file in 'data' folder,
        of exchange rates for date 'date'.
        than when it's done appending it gets returned.
    """
    NewPath = r'data'
    if not os.path.exists(NewPath):
        os.makedirs(NewPath)

    with open(os.path.join(NewPath, 'rates-{}.csv'.format(date)), mode="rt", encoding="utf8") as exratesF:
        exratesReader = csv.reader(exratesF, delimiter = ",")
        exratesDict = dict()
        for row in exratesReader:
            [code, rate] = row
            exratesDict[code] = rate

        return exratesDict

def get_currencies():
    """
    A function that returns the currencies loaded from the currencies file, as a dictionary. If
    the currencies file doesn't exists, the function fetches the data from the internet, saves it to the
    currencies file and then returns it.


    return:
    ------
    A dictionary of all currencies codes and their names.
    """
    #If there is no folder data in the current directory, create one.
    NewPath = r'data'
    if not os.path.exists(NewPath):
        os.makedirs(NewPath)
    #If currencies file exist return it as a dictionary.
    #else download it and then return.
    if os.path.exists(os.path.join(NewPath,'currencies.csv')):
        return _load_currencies()
    else:
        _save_currencies(_fetch_currencies())
        return _load_currencies()
    
def get_exrates(date):
    """
    that returns the exchange rates data for date date loaded from the
    appropriate exchange rates file. If that file doesn't exists, the function fetches the data from the
    internet, saves it to the file, and then returns it.

    return:
    ------
    A dictionary of all exhange rates for a given date 'date'.
    """
    NewPath = r'data'
    if not os.path.exists(NewPath):
        os.makedirs(NewPath)
    if os.path.exists(os.path.join(NewPath,'rates-{}.csv'.format(date))):
        return _load_exrates(date)
    else:
        _save_exrates(date, _fetch_exrates(date))
        return _load_exrates(date)

def convert(amount, from_curr, to_curr, date = str(datetime.today().strftime(date_format))):
    """
    A function that returns the value obtained by converting the amount amount of the currency
    from_curr to the currency to_curr on date 'date'. If date is not given, it defaults
    the current date (you can represent "today" as an empty string).
    The formula is amount * to_value / from_value, where to_value and from_value
    represent the values of the currencies to_curr and from_curr, respectively, on the date date.
    If the exchange rate for either of the currency codes from_curr and to_curr does not exist on
    the date date, the function must raise a custom exception CurrencyDoesntExistError with an
    appropriate message.

    Parameters:
    ----------
    amount: Float
       The amount to convert
    from_curr: String
       The currency code we wnt to convert from.
    to_curr: String
       The currency code we wnt to convert to.
    date: String
       The date we are getting the exchange rates data for the requested currencies.
       It's default value is today.
    from_value: Float
       The exchange rate of currency 'from_curr'.
    to_value: Float
       The exchange rate of currency 'to_curr'.

    Return:
    ------
    res: Float
       The converted value of the amount from 'from_curr' to 'to_curr'.
    """
    
    exratesDict = get_exrates(date)

    from_value = 0
    to_value = 0
    for key in exratesDict:
        if from_curr.upper() == key:
            from_value = float(exratesDict[key])
        if to_curr.upper() == key:
            to_value = float(exratesDict[key])
            
    if from_value == 0 or to_value == 0:
        raise CurrencyDoesntExistError()

    res = amount * to_value / from_value
    return res




        
    
