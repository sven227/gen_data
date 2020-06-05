#for symbol in symbol_list:    
#    path = wd + f'/data/{symbol}/daily_{symbol}.csv'
#    print(path)

import os
from functools import reduce
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, date
from alpha_vantage.timeseries import TimeSeries
from time import sleep
import glob


#import api_key_alpha in your main program/notebook by "import myalpha"
#all data retrieved from alpha_vantage is in form of csv and is also stored as csv on a local path
#local path follows this nameconvention: <working-directory>/data/<symbol>/daily_<symbol>.csv
#find your working directory by using this code: import os;  wd  = os.getcwd()
#your working directory is where you write your python notebook in Jupyter lab / Jupyter notebook
#example: for procter&gamble ticker symbol csv is stored in <woring directory path>/data/PG/daily_PG.csv
#you can create a "data" folder if you want if not it will be created for you


#get all daily ticker symbol data for symbol_list from alpha-vantage
def get_alphav_10symbols(symbol_list,api_key_alpha,function):
    num = len(symbol_list)
    if num > 10: raise Exception("no more than 10 symbols allowed")
    #myau.get_alphav_all(symbol_list, api_key_alpha, function)
    _dict = {}

    for symbol in symbol_list:        
            _dict[symbol]=get_alphav_symbol(symbol,api_key_alpha,function)
            print("_____________________________")
            print(symbol+" "+str(len(_dict)))
    write_csv_one_by_one(_dict)
    return   
    

def write_csv_one_by_one(_dict):
    counter = 0
    for symbol, _df in _dict.items():
        counter += counter + 1
        dirName = './data/{0}'.format(symbol)
        _df.index = pd.to_datetime(_df.index)
        if not os.path.exists(dirName):
            os.mkdir(dirName)
            print("Directory " , dirName ,  " Created ")
        else:    
            print("Directory " , dirName ,  " already exists")
        if counter == 1:
            df1 = _df
            df1.to_csv('./data/{0}/daily_{1}.csv'.format(symbol,symbol))
        elif counter == 2:
            df2 = _df
            df2.to_csv('./data/{0}/daily_{1}.csv'.format(symbol,symbol))
        elif counter == 3:
            df3 = _df
            df3.to_csv('./data/{0}/daily_{1}.csv'.format(symbol,symbol))
        elif counter == 4:
            df4 = _df
            df4.to_csv('./data/{0}/daily_{1}.csv'.format(symbol,symbol))
        elif counter == 5:
            df5 = _df
            df5.to_csv('./data/{0}/daily_{1}.csv'.format(symbol,symbol))
        elif counter == 6:
            df6 = _df
            df6.to_csv('./data/{0}/daily_{1}.csv'.format(symbol,symbol))
        elif counter == 7:
            df7 = _df
            df7.to_csv('./data/{0}/daily_{1}.csv'.format(symbol,symbol))
        elif counter == 8:
            df8 = _df
            df8.to_csv('./data/{0}/daily_{1}.csv'.format(symbol,symbol))
        elif counter == 9:
            df9 = _df
            df9.to_csv('./data/{0}/daily_{1}.csv'.format(symbol,symbol))
        elif counter == 10:
            df10 = _df
            df10.to_csv('./data/{0}/daily_{1}.csv'.format(symbol,symbol))
    _modTimesinceEpoc = os.path.getmtime('./data/{0}/daily_{1}.csv'.format(symbol,symbol))
    _modificationTime = datetime.fromtimestamp(_modTimesinceEpoc).strftime('%Y-%m-%d %H:%M:%S')
    print("Last Modified Time : ", _modificationTime)
    del _dict
    return



        
    
          
def get_alphav_symbol(symbol, api_key_alpha,function='TIME_SERIES_DAILY_ADJUSTED'):
    url = (f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&outputsize=full&apikey={api_key_alpha}&datatype=csv')
    name = 'daily'+'_'+symbol
    _df = pd.read_csv(url)
    _df.set_index('timestamp',inplace=True)
    _df.index = pd.to_datetime(_df.index)
    return _df
    
#get last 100 registries of time_series daily from alpha-vantage
def get_alphav_last100(symbol,api_key_alpha,function='TIME_SERIES_DAILY_ADJUSTED',outputsize='compact'):
    url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&outputsize=outputsize&apikey={api_key_alpha}&datatype=csv'
    name = 'daily'+'_'+symbol
    _df = pd.read_csv(url)
    _df.set_index('timestamp',inplace=True)
    _df.index = pd.to_datetime(_df.index)
    return _df

#read from csv - input list of symbol-tickers and returns a dictionary with key <symbol> and dataframe as value
def get_daily(symbol_list, startd, endd,wd=None, usecols=None):
    if wd == None:
        wd  = os.getcwd()
          
    suffixes = list( map( lambda x:  '_'+x ,symbol_list))
    path_list =  {symbol: composePath(wd, '/data/', symbol) for symbol in symbol_list}   
    dict = retrieveDF(path_list, startd, endd, usecols)
    #return dictionary with key=df_<symbol> and the dataframe as value
    return dict   

#read from csv one specific ticke-symbol - calls get_daily -> retrieveDF
def get_daily_symbol(symbol,startd='', endd='',wd=None, usecols=None):
    dict = get_daily([symbol],startd, endd)    
    #key_name = 'df_'+symbol
    key_name =  symbol
    #return panda dataframe
    _df =dict[key_name]
    _df.index = pd.to_datetime(_df.index)
    return _df

def composePath(baseDir, relPath, symbol):
    #symbol_path = baseDir.append(relPath)
    symbol_path = baseDir+relPath+f'{symbol}/daily_{symbol}.csv'
    return symbol_path

#read from csv with path_list  - is called from get_daily
def retrieveDF(path_list, startd, endd, usecols, rename_column=False):
    if startd=='':
        startd = '2000-01-01'
    if endd=='':
        endd = '2020-12-31'
    dict_of_df = {}
    for symbol, path in path_list.items():
        #key_name = 'df_'+symbol
        key_name =  symbol
        _df = pd.read_csv(path,usecols=usecols) 
        _df.set_index('timestamp',inplace=True)
        _df.index = pd.to_datetime(_df.index)
        _df.sort_index(inplace=True)
        #when sorted by date in ascending order the slice by startd:endd is correct
        _df = _df.loc[startd:endd]
        #_df = _df.loc[endd:startd]
        
        if rename_column == True:
            column = f'{symbol}'        
            dict_of_df[key_name]=_df.rename(columns={'adjusted_close':column})
        else:
            dict_of_df[key_name]=_df
    return dict_of_df

def retrieveDFfinal(dict,suffixes):
    dict2list=lambda dic:[(v)for (v) in dic.values()]
    df = reduce(lambda left,right: pd.merge(left,right,on='timestamp', how='outer',suffixes=suffixes), dict2list(dict))
    df.index = pd.to_datetime(df.index)
    return df


def getlastdate(symbol):
    
    dict = get_daily([symbol])    
    #key_name = 'df_'+symbol 
    key_name =  symbol
    pd=dict[key_name].head(1)
    #return pd.index[0]
    return string2date(pd.index[0])


def string2date(date_string, format="%Y-%m-%d"):
    date_time_obj = datetime.strptime(date_string, format)
    return date_time_obj

def date2string(date_time_obj, format="%Y-%m-%d"):
    return date_time_obj.strftime(format)

def update_index2timedate_csv(symbol_list,wd=None,startd='2000-01-01',endd='2020-12-31'):
        _dict = get_daily(symbol_list,startd,endd)
        write_csv_one_by_one(_dict)        
        return


def update_csv(symbol_list,api_key_alpha):
    for symbol in symbol_list:  
            print("")
            print("processing symbol: "+symbol)
            df_latest = get_alphav_last100(symbol,api_key_alpha)
            df_latest.head()
            #df_latest.index
            _xdo=getlastdate(symbol)
            _xdo
            print("this is the last date updated in csv file:")
            _xdo.date()
            print("these are the entries we need to append to csv:")
            df_filtered =df_latest.loc[df_latest.index>_xdo]
            df_from_csv = get_daily_symbol(symbol)
            print("retrieving head data from csv")
            df_from_csv.head()
            if df_filtered.dropna().empty:    
                        print("nothing to append")    
            else:
                        df_updated=df_filtered.append(df_from_csv,verify_integrity=False,sort=False)
                        print("the final csv to be updated")
                        df_updated.head(50)
                        df_updated.index
                        df_updated.to_csv('./data/{0}/daily_{1}.csv'.format(symbol_list[0],symbol_list[0]))
    return

def compose_portfolio(symbol_list,startd='2000-01-01', endd='',usecols=['timestamp','adjusted_close']):
    #loop through dict and join columns with inner join to one new dataframe
    # Pre-req. file must exist in relative path e.g.: ./data/PG/daily_PG.csv
    # get all files with symbols we are interested in into a list
    # read file of symbol one by one into dataframe
    # renanme column_names to close_PG, close_{}.format(symbol) 
    # reset index to timeframe inplace= true
    # join the dataframes into one only using inner join (no NaN)
    # columns: open	high	low	close	adjusted_close	volume	dividend_amount	split_coefficient    
    if (endd==''):
        today=date.today()
        endd = date2string(today)    
    suffixes = list(map(lambda x:  '_'+x ,symbol_list))
    wd = os.getcwd()

    path_list =  {symbol: composePath(wd, '/data/', symbol) for symbol in symbol_list}   
    path_list

    dict = retrieveDF(path_list, startd, endd,usecols, True)
    df_final = retrieveDFfinal(dict,suffixes)
    #df_final.tail()
    return df_final