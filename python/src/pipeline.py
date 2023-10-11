# external imports
from datetime import datetime, timedelta
import pymysql
import requests
import pandas as pd
# local imports
import constants as SQL_CONSTANTS

print("----------Executing Pipeline----------")

# local constants
MYSQL_HOST = "db"
MYSQL_USER = "root"
MYSQL_PASSWORD = "simple"
MYSQL_PORT = 3306
HOUSTON_LAT = "29.7604"
HOUSTON_LON = "95.3698"
WEATHER_KEY = "ce6df5cf1424d1115887276848c49d06"
POLLUTION_API = "http://api.openweathermap.org/data/2.5/air_pollution/forecast?" +\
                f"lat={HOUSTON_LAT}&lon={HOUSTON_LON}&appid={WEATHER_KEY}"


def append_columns_to_query(result, cursor):
    """Appends the table column names as a 'header' type row in the returned result object
    Args:
        result (list of tuple): The raw result as returned from the database query
        cursor (connect.cursor): The cursor obj that holds the query's metadata
    Returns:
        result (list of tuple): The raw result + column names inserted into position 0
    """
    colnames = tuple(desc[0] for desc in cursor.description)
    result.insert(0, colnames)

    return result


def format_result(data):
    """Based on type, handle list conversion
    Args:
        data (Obj): Varying items to be converted to list
    Returns:
        list: original data wrapped in list
    """
    if isinstance(data, list):
        return data
    if isinstance(data, int):
        return [data]
    if isinstance(data, tuple):
        return list(data)


def mysql_db_call(sql_statement, values=None, many=False, columns=False):
    """Generic handler for executing queries on the db instance
    Args:
        sql_statement (str): sql query string to be executed
        values (list/tuple, optional): values to be inserted to sql_statement. Defaults to None.
        many (bool, optional): is values inserting many items. Defaults to False.
        columns (bool, optional): t/f to return the result with col names as row[0]. Defaults to False.
    Returns:
        result (list): list representation of the results returned by the database for sql_statement
    """
    # choosing to open/close connection with each call because of problem simplicity
    connection, result = None, None
    try:
        connection = pymysql.connect(user=MYSQL_USER,password=MYSQL_PASSWORD,host=MYSQL_HOST,port=MYSQL_PORT)
        cursor = connection.cursor()
        if many:
            cursor.executemany(sql_statement, values)
            result = format_result(cursor.rowcount)
        else:
            cursor.execute(sql_statement, values)
            result = format_result(cursor.fetchall())
        if columns:
            result = append_columns_to_query(result, cursor)
        connection.commit()
    except pymysql.err.OperationalError as err:
        print(err)
        return None
    except pymysql.err.IntegrityError:
        print('Skipping duplicate data entry...')
        return None
    finally:
        if connection:
            connection.close()

    return result


def init_db():
    """Initialize the database and the necessary tables"""
    mysql_db_call(SQL_CONSTANTS.create_weather_db)
    mysql_db_call(SQL_CONSTANTS.create_pollution_event_table)
    mysql_db_call(SQL_CONSTANTS.create_avg_four_day_forecast_table)


def ingest_pollution_data():
    """Ingests the pollution data from the CONSTANT defined api url
    Returns:
        (requests.response): response object from http get request
    """
    return requests.get(POLLUTION_API, timeout=15)


def parse_forecast_json(data, today_str):
    """Parse the given dict into the expected shape for database insertion
    Args:
        data (dict): the json formatted response of forecasts
        today_str (str): str formatted version of today's date
    Returns:
        forecasts (list of tuple): collection of forecast events for the given date
    """
    forecasts = []
    for row in data.get('list'):
        current = (today_str,
                   # Adjusting UTC to Central Timezone
                   (datetime.fromtimestamp(row['dt'])-timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S'),
                   row['main']['aqi'],
                   row['components']['co'],
                   row['components']['no'],
                   row['components']['no2'],
                   row['components']['o3'],
                   row['components']['so2'],
                   row['components']['pm2_5'],
                   row['components']['pm10'],
                   row['components']['nh3'])
        forecasts.append(current)
    return forecasts


# initialize the database and the necessary tables
init_db()
# ingest public pollution data and parse the response
pollution_response = ingest_pollution_data()
pollution_data = pollution_response.json()
date = datetime.now().strftime('%Y-%m-%d')
insert_vals = parse_forecast_json(pollution_data, date)
# insert pollution forecast events to the respective db table
mysql_db_call(SQL_CONSTANTS.pollution_table_insert, insert_vals, many=True)
# extract the pollution forecast events from the db... in a real system obviously you want to
# use the fact that you already have all of this data and don't need to ask the db for it
pollution_rows = mysql_db_call(SQL_CONSTANTS.pollution_date_select, date, columns=True)
# using pandas, shape the data for next steps and calculate the means
pollution_pdf = pd.DataFrame(pollution_rows[1:], columns=pollution_rows[0])
db_date = pollution_pdf.iloc[0,0].strftime('%Y-%m-%d')
pollution_pdf.drop(columns=['AnalysisDate', 'ForecastTime'], inplace=True)
averages_pdf = pollution_pdf.mean(axis=0).to_frame().T
averages = averages_pdf.values.tolist()[0]
insert_vals = (db_date, int(averages.pop(0)), *averages)
# insert the averaged forecast over the next four days to the respective db table
mysql_db_call(SQL_CONSTANTS.four_day_forecast_insert, insert_vals)
# extract the averaged forecast for today from the db... same further comment as line 112/113
avg = mysql_db_call(SQL_CONSTANTS.four_day_forecast_date_select, db_date)
# print the result of the pipeline
outcome = {1: 'GOOD', 2: 'FAIR', 3: 'MODERATE', 4: 'POOR', 5: 'VERY POOR'}
print("\nOUTCOME:")
print(f"Air Quality over the next 4 days in Houston is expected to be {outcome[avg[0][1]]}")
print("----------Exiting pipeline.py----------")
