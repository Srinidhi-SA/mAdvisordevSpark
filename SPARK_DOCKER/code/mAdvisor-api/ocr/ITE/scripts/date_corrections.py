#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from dateutil.parser import parser, parse
import pandas as pd
import numpy as np
import datetime 
# Check if passed date is complete and valid
def is_date_complete (date,day_first_flag=False ,must_have_attr=("year","month","day")):
    date_details={"year_found":False,"year":None,"month_found":False,"month":None,"day_found":False,"day":None}
    parse_res, _ = parser()._parse(date,dayfirst=day_first_flag)
    # If date is invalid `_parse` returns (None,None)
    if parse_res is None:
        return False,date_details
    # For a valid date `_result` object is returned. E.g. _parse("Sep 23") returns (_result(month=9, day=23), None)
    if getattr(parse_res,"year") is not None:
        date_details.update({"year_found":True,"year":parse_res.year})
    if getattr(parse_res,"month") is not None:
        date_details.update({"month_found":True,"month":parse_res.month})
    if getattr(parse_res,"day") is not None:
        date_details.update({"day_found":True,"day":parse_res.day})
    
    for attr in must_have_attr:
        if getattr(parse_res,attr) is None:
            return False,date_details
    return True,date_details


def check_if_date_corrections_needed(col_names_as_list,day_first_flag=False):
    """
    function to check if the detected dates need's corrections like
    augmenting the month and year information from elsewhere
    """
    dates_operations=[]
    corrections_needed=False
    for date in col_names_as_list:
        date_comp,daaaate_details=is_date_complete(date,day_first_flag)
        dates_operations.append(daaaate_details)
        print(date,daaaate_details)
        if not date_comp:
            corrections_needed=True
    return corrections_needed,dates_operations



def extract_available_year(dates_dict):
    store_years=[]
    for date in dates_dict:
        if date["year_found"]:
            store_years.append(date["year"])
    return store_years


def extract_available_month(dates_dict):
    store_months=[]
    for date in dates_dict:
        if date["month_found"]:
            store_months.append(date["month"])
    return store_months

def extract_available_days(dates_dict):
    store_days=[]
    for date in dates_dict:
        if date["day_found"]:
            store_days.append(date["day"])
    return store_days


def date_operations(df,default_year,default_month):
    print("date corrections executing")
#    columns_as_list=df.iloc[0]
    columns_as_list=list(df.columns)
    set_day_first=check_if_day_first(df)
    correction_needed,dates_in_dict=check_if_date_corrections_needed(columns_as_list,day_first_flag=set_day_first)
    correction_needed=True
    print("dates_in_dict:\n",dates_in_dict)
    print("#"*10)
    if correction_needed:
        
        for date in dates_in_dict:
            if date["day_found"]:
                if not date["year_found"]:
                    date["year"]=default_year
                    date["year_found"]=True
                if not date["month_found"]:
                    date["month"]=default_month
                    date["month_found"]=True
            else:
                pass
            print(date)
    else:
        print("no corrections needed")
    return dates_in_dict


def create_Date_using_dict(date_dict):
    if date_dict["year_found"] ==True and date_dict["month_found"]==True and date_dict["day_found"]==True:
        return datetime.date(date_dict["year"],date_dict["month"],date_dict["day"])##year,month,day
    else:
        print("cannot create date with incomplete information")
        print("date_info : ",date_dict["year"],date_dict["month"],date_dict["day"])
        return None

def write_new_dates_to_dataframe(df_org,date_as_dict):
    df=df_org.copy()
    for count,date in enumerate(list(df.columns)):
        old_date=date
        new_date=create_Date_using_dict(date_as_dict[count])
        if new_date:
            
            df.rename(columns={old_date:str(new_date)}, inplace=True)
        else:
            print("new_date:",new_date)
    return df

def year_finder(dates_list):
    
    dates_operations=[]
    for date in dates_list:
        date_comp,daaaate_details=is_date_complete(date)
        dates_operations.append(daaaate_details)
    unique_years,count_of_entries=np.unique(extract_available_year(dates_operations),return_counts=True)
    if list(unique_years):
        return True,unique_years[list(count_of_entries).index(max(list(count_of_entries)))]
    else:
        return False,0

def month_finder(dates_list):

    dates_operations=[]
    for date in dates_list:
        date_comp,daaaate_details=is_date_complete(date)
        dates_operations.append(daaaate_details)
    unique_month,count_of_entries=np.unique(extract_available_month(dates_operations),return_counts=True)
    if list(unique_month):

        return True,unique_month[list(count_of_entries).index(max(list(count_of_entries)))]
    else:
        return False,0


def check_if_day_first(df):
    columns_as_list=list(df.columns)
    correction_needed,dates_in_dict=check_if_date_corrections_needed(columns_as_list)
    unique_months,count_of_entries=np.unique(extract_available_month(dates_in_dict),return_counts=True)
    months_without_days_first_flag=unique_months
    
    correction_needed,dates_in_dict=check_if_date_corrections_needed(columns_as_list,day_first_flag=True)
    unique_months,count_of_entries=np.unique(extract_available_month(dates_in_dict),return_counts=True)
    months_with_days_first_flag=unique_months
    
    if (len(months_without_days_first_flag)>=len(months_with_days_first_flag)):
        return True
    else:
        return False
