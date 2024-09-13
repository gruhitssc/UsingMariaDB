from constants import get_dbconstants
from gsheet import df_to_gsheet
import pymysql
import pandas as pd

# TODO
# 1. Add it to cron job to run every day
# 2. configure it to run every 2 weeks a day
# 3. Set the start_time and end_time of 2 week span for each employee
# 4. In google sheet columns [name, number of hours, donor name(if possible), total count of donors]

db_constants = get_dbconstants()

connection = pymysql.connect(
    host=db_constants.host,
    user=db_constants.user,
    password=db_constants.password,
    database=db_constants.database
)

def duration_to_hhmm(duration: int):
    """
    Function to conver the durations to proper time in HH:mm format
    Arguments:
        duration(int): Total duration worked by the user in seconds

    Returns:
        hour and minute corresponding to duration
    """
    fractional_time = duration/60**2

    # Extract the minute proportion from the time in fractional format
    minute_proportion = fractional_time%1

    # Remove the minute proportion to get hour
    hours = int(fractional_time - minute_proportion)

    # obtain minute by multiplying minute_proportion to the whole portion
    minute = int(60*minute_proportion)

    return f"{hours}:{minute}"

try:
    with connection:
        with connection.cursor() as fetch_cursor:
            query = """
                SELECT 
                    user, kimai2_users.username as username, kimai2_users.alias as fullname, start_time, end_time, duration
                FROM
                    kimai2_timesheet
                INNER JOIN kimai2_users ON
                    kimai2_timesheet.user = kimai2_users.id
                WHERE
                    start_time >= '2024-09-06 00:00:00' AND
                    end_time <= '2024-09-07 00:00:00'
                ORDER BY
                    fullname ASC
                LIMIT 
                    10
            """

            fetch_cursor.execute(query)
            results = [(*row, duration_to_hhmm(row[-1])) for row in fetch_cursor.fetchall()]
            columns = ['user_id', 'username', 'fullname', 'start_time', 'end_time', 'duration', 'time']
            df = pd.DataFrame.from_records(results, columns=columns)
            df_to_gsheet(df, "2024-09-06 00:00:00")
            
            
except Exception as e:
    print(e)    