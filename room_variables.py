from datetime import datetime, timedelta

session_time_limit = timedelta(hours=2)
max_pc_count = 10
screen_size = 10
max_headset_count = 10
max_mouse_count = 10
max_keyboard_count = 10

military = False
def set_time_limit(new_time_limit):
    global session_time_limit
    session_time_limit = new_time_limit

def get_time_limit():
    return session_time_limit

def set_max_pc_count(PC_count):
    global max_pc_count
    max_pc_count = PC_count

def get_max_pc_count():
    return max_pc_count

def set_screen_size(screensize):
    global screen_size
    screen_size = screensize

def set_time_format(time_format):
    global military
    time_format = time_format

def get_time_format():
    return military

# Add remaining counts here