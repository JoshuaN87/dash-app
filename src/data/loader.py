import pandas as pd
from functools import reduce
from typing import Callable

Preprocessor = Callable[[pd.DataFrame], pd.DataFrame]

class DataSchema:
    AMOUNT = 'gross_sales'
    SALES = 'number_of_sales'
    ESTIMATES = 'number_of_estimates'
    ESTIMATES_PROCESSED = 'estimates_processed'
    DATE = 'date_time'
    YEAR = 'year'
    MONTH = 'month'
    WEEK = 'week'
    DAY = 'day'
    HOUR = 'hour'
    REPS = 'sales_rep'
    FISCAL_YEAR = 'fiscal_year'
    TIME_DAY = 'time_of_day'

def clean_convert(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(index=df.index[-1], axis=0)
    df = df.query("type != 'Estimate'")
    return df

def convert_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.DATE] = pd.to_datetime(df[DataSchema.DATE])
    df[DataSchema.SALES] = df[DataSchema.SALES].astype('float64')
    return df

def create_year_column(df: pd.DataFrame) ->pd.DataFrame:
    df[DataSchema.YEAR] = df[DataSchema.DATE].dt.year.astype(str)
    return df

def create_month_column(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.MONTH] = df[DataSchema.DATE].dt.month.astype(str)
    return df

def create_day_column(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.DAY] = df[DataSchema.DATE].dt.day_name().astype('category')
    return df

def create_hour_column(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.HOUR] = df[DataSchema.DATE].dt.hour.astype(int)
    return df

def time_of_day(value):
    if value < 11:
        return "Morning"
    if 11 <= value < 17:
        return "Afternoon"
    elif value >= 16:
        return "Evening"

def create_time_day(df: pd.DataFrame) ->pd.DataFrame:
    df[DataSchema.TIME_DAY] = df[DataSchema.HOUR].map(time_of_day)
    return df


def fiscal_year(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.FISCAL_YEAR] = df[DataSchema.DATE] < '2022-12-26'
    df[DataSchema.FISCAL_YEAR] = df[DataSchema.FISCAL_YEAR].map({True: 22, False: 23})
    return df

def compose(*functions: Preprocessor) -> Preprocessor:
    return reduce(lambda f, g: lambda x: g(f(x)), functions)

def load_transaction_data(path: str) -> pd.DataFrame:
    #loading data from the CSV File
    data = pd.read_csv(
        path,
        dtype={
            DataSchema.AMOUNT: float,
            DataSchema.DATE: str,
            DataSchema.DAY: str,
            DataSchema.REPS: str
        },
        parse_dates=[DataSchema.DATE]
    )
    preprocesser = compose(
        clean_convert,
        convert_dtypes,
        create_year_column,
        create_month_column,
        create_day_column,
        create_hour_column,
        create_time_day,
        fiscal_year
    )
    return preprocesser(data)

def load_additional_data(path: str) -> pd.DataFrame:
    data_ad = pd.read_csv(
        path,
        dtype={
            DataSchema.AMOUNT: float,
            DataSchema.DATE: str,
            DataSchema.DAY: str,
        },
        parse_dates=[DataSchema.DATE]
    )
    preprocesser = compose(
        convert_dtypes,
        create_year_column,
        create_month_column,
        create_day_column,
        create_hour_column,
        fiscal_year
    )
    return preprocesser(data_ad)

def merge(data: pd.DataFrame, data_ad: pd.DataFrame) ->pd.DataFrame:
    studio_df = data
    web_df = data_ad

    merged = pd.concat([studio_df, web_df], ignore_index=True, sort=False)
    merged.fillna({'type':'Web', 'sales_rep':'Web'}, inplace=True)
    merged.fillna(0, inplace = True)

    return merged
'''

def load_transaction_data(path: str) -> pd.DataFrame:
    #loading data from the CSV File
    data = pd.read_csv(
        path,
        dtype={
            DataSchema.AMOUNT: float,
            DataSchema.DATE: str,
            DataSchema.DAY: str,
            DataSchema.REPS: str
        },
        parse_dates=[DataSchema.DATE]
    )
    
    data = data.drop(index=data.index[-1], axis=0)
    data = data.query("type != 'Estimate'").copy()

    
    def time_of_day(value):
        if value < 11:
            return "Morning"
        if 11 <= value < 17:
            return "Afternoon"
        elif value >= 16:
            return "Evening"
        

    data[DataSchema.SALES] = data[DataSchema.SALES].astype('float64')
    data[DataSchema.DATE] = pd.to_datetime(data[DataSchema.DATE])
    data[DataSchema.YEAR] = data[DataSchema.DATE].dt.year.astype(str)
    data[DataSchema.MONTH] = data[DataSchema.DATE].dt.month.astype(str)
    data[DataSchema.DAY] = data[DataSchema.DATE].dt.day_name().astype('category')
    data[DataSchema.HOUR] = data[DataSchema.DATE].dt.hour.astype(int)

    data[DataSchema.TIME_DAY] = data[DataSchema.HOUR].map(time_of_day)
    data[DataSchema.FISCAL_YEAR] = data[DataSchema.DATE] < '2022-12-26'
    data[DataSchema.FISCAL_YEAR] = data[DataSchema.FISCAL_YEAR].map({True: 22, False: 23})


    return data

def load_additional_data(path: str) -> pd.DataFrame:
    data_ad = pd.read_csv(
        path,
        dtype={
            DataSchema.AMOUNT: float,
            DataSchema.DATE: str,
            DataSchema.DAY: str,
        },
        parse_dates=[DataSchema.DATE]
    )
    
    #data_ad = data_ad.drop(index=data_ad.index[-1], axis=0)

    data_ad[DataSchema.SALES] = data_ad[DataSchema.SALES].astype('float64')
    data_ad[DataSchema.DATE] = pd.to_datetime(data_ad[DataSchema.DATE])
    data_ad[DataSchema.YEAR] = data_ad[DataSchema.DATE].dt.year.astype(str)
    data_ad[DataSchema.MONTH] = data_ad[DataSchema.DATE].dt.month.astype(str)
    data_ad[DataSchema.DAY] = data_ad[DataSchema.DATE].dt.day_name().astype('category')
    data_ad[DataSchema.HOUR] = data_ad[DataSchema.DATE].dt.hour.astype(int)

    data_ad[DataSchema.FISCAL_YEAR] = data_ad[DataSchema.DATE] < '2022-12-26'
    data_ad[DataSchema.FISCAL_YEAR] = data_ad[DataSchema.FISCAL_YEAR].map({True: 22, False: 23})

    return data_ad

def merge(data: pd.DataFrame, data_ad: pd.DataFrame) ->pd.DataFrame:
    studio_df = data
    web_df = data_ad

    merged = pd.concat([studio_df, web_df], ignore_index=True, sort=False)
    merged.fillna({'type':'Web', 'sales_rep':'Web'}, inplace=True)
    merged.fillna(0, inplace = True)

    print(merged)
    return merged
'''