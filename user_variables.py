from datetime import datetime, timedelta

session_time_limit = timedelta(hours=2)

def change_time_limit(new_time_limit):
    global session_time_limit
    session_time_limit = new_time_limit

def get_time_limit():
    return session_time_limit