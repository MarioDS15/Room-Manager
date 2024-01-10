from datetime import datetime, timedelta
from data_loader import *
import csv


session_time_limit = timedelta(hours=2)
max_pc_count = 10
screen_size = 10
max_headset_count = 10
max_mouse_count = 10
max_keyboard_count = 10
max_headset_count = 10
max_controller_count = 10
max_mousepad_count = 10

def set_time_limit(new_time_limit):
    global session_time_limit
    update_row(ROOM_FILE, 'Time_limit', new_time_limit)
    session_time_limit = timedelta(hours=int(new_time_limit))

def set_max_pc_count(PC_count):
    global max_pc_count
    update_row(ROOM_FILE, 'PC_count', PC_count)
    max_pc_count = int(PC_count)

def set_headset_count(headset_count):
    global max_headset_count
    update_row(ROOM_FILE, 'Headset_count', headset_count)
    max_headset_count = int(headset_count)

def set_mouse_count(mouse_count):  
    global max_mouse_count
    update_row(ROOM_FILE, 'Mouse_count', mouse_count)
    max_mouse_count = int(mouse_count)
    print("Updated mouse count " + str(max_mouse_count))

def set_keyboard_count(keyboard_count):
    global max_keyboard_count
    update_row(ROOM_FILE, 'Keyboard_count', keyboard_count)
    max_keyboard_count = int(keyboard_count)

def set_headset_count(headset_count):
    global max_headset_count
    update_row(ROOM_FILE, 'Headset_count', headset_count)
    max_headset_count = int(headset_count)

def set_controller_count(controller_count):
    global max_controller_count
    update_row(ROOM_FILE, 'Controller_count', controller_count)
    max_controller_count = int(controller_count)

def set_mousepad_count(mousepad_count):
    global max_mousepad_count
    update_row(ROOM_FILE, 'Mousepad_count', mousepad_count)
    max_mousepad_count = int(mousepad_count)


def load_items():
    settings = csv_to_dict(ROOM_FILE)
    set_time_limit(settings['Time_limit'])
    set_max_pc_count(settings['PC_count'])
    set_headset_count(settings['Headset_count'])
    set_mouse_count(settings['Mouse_count'])
    set_keyboard_count(settings['Keyboard_count'])
    set_controller_count(settings['Controller_count'])
    set_mousepad_count(settings['Mousepad_count'])
    
load_items()


# Add remaining counts here
def get_session_time_limit():
    return session_time_limit

def get_max_pc_count():
    return max_pc_count

def get_screen_size():
    return screen_size

def get_max_headset_count():
    return max_headset_count

def get_max_mouse_count():
    return max_mouse_count

def get_max_keyboard_count():
    return max_keyboard_count

def get_max_controller_count():
    return max_controller_count

def get_max_mousepad_count():
    return max_mousepad_count

