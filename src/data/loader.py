import pandas as pd
from functools import reduce
from typing import Callable

Preprocessor = Callable[[pd.DataFrame], pd.DataFrame]

class DataSchema:
    AMOUNT = 'gross_sales'
    SALES = 'number_of_sales'
    DATE = 'date_time'
    YEAR = 'year'
    MONTH = 'month'
    WEEK = 'week'
    DAY = 'day'
    HOUR = 'hour'
    REPS = 'sales_rep'
    FISCAL_YEAR = 'fiscal_year'
    TIME_DAY = 'time_of_day'
    PCT_CHANGE = 'pct_change'
    DIFF = 'change'

def clean_convert(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(index=df.index[-1], axis=0)
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

def business_year(value):
    if value < '2021-12-27':
        return "Fiscal Year 2021" 
    if '2021-12-27' <= value < '2022-12-26':
        return "Fiscal Year 2022"
    elif value >= '2022-12-26':
        return "Fiscal Year 2023"

def fiscal_year(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.DATE] = df[DataSchema.DATE].astype(str)      
    df[DataSchema.FISCAL_YEAR] = df[DataSchema.DATE].map(business_year)
    df[DataSchema.FISCAL_YEAR] = df[DataSchema.FISCAL_YEAR].astype(str)     
    return df

def percent_change(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.PCT_CHANGE] = df[DataSchema.AMOUNT].pct_change()
    df[DataSchema.DIFF] = df[DataSchema.AMOUNT].diff()

    return df
def create_studio_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.query("sales_rep != 'LT Internet Sale'")
    return df

def create_web_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.query("sales_rep == 'LT Internet Sale'")
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
        convert_dtypes,
        create_year_column,
        create_month_column,
        create_day_column,
        fiscal_year,
        create_studio_df,
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
        fiscal_year,
        create_web_df,
    )
    print(preprocesser(data_ad))
    return preprocesser(data_ad)

def load_blended_data(path: str) -> pd.DataFrame:
    data_blend= pd.read_csv(
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
        fiscal_year,
    )
    return preprocesser(data_blend)

def merge(data: pd.DataFrame, data_ad: pd.DataFrame) ->pd.DataFrame:
    studio_df = data
    web_df = data_ad

    merged = pd.concat([studio_df, web_df], ignore_index=True, sort=False)
    merged.fillna({'type':'Web', 'sales_rep':'Web'}, inplace=True)
    merged.fillna(0, inplace = True)

    return merged