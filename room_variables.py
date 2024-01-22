from datetime import datetime, timedelta
from data_loader import *
import csv


session_time_limit = timedelta(hours=2)
session_limit = 1

max_pc_count = 10
screen_size = 10
max_headset_count = 10
max_mouse_count = 10
max_keyboard_count = 10
max_headset_count = 10
max_controller_count = 10
max_mousepad_count = 10

PC_in_use = 0
headset_in_use = 0
mouse_in_use = 0
keyboard_in_use = 0
headset_in_use = 0
controller_in_use = 0
mousepad_in_use = 0


def set_time_limit(new_time_limit):
    """Updates the time limit for a session across all students"""
    global session_time_limit
    update_row(get_room_path(), 'Time_limit', new_time_limit)
    session_time_limit = timedelta(hours=int(new_time_limit))

def set_max_pc_count(PC_count):
    """Updates the amount of PCs available in the room"""
    global max_pc_count
    update_row(get_room_path(), 'PC_count', PC_count)
    max_pc_count = int(PC_count)

def set_headset_count(headset_count):
    """Updates the amount of headsets available in the room"""
    global max_headset_count
    update_row(get_room_path(), 'Headset_count', headset_count)
    max_headset_count = int(headset_count)

def set_mouse_count(mouse_count):  
    """Updates the amount of mouses available in the room"""
    global max_mouse_count
    update_row(get_room_path(), 'Mouse_count', mouse_count)
    max_mouse_count = int(mouse_count)
    #print("Updated mouse count " + str(max_mouse_count))

def set_keyboard_count(keyboard_count):
    """Updates the amount of keyboards available in the room"""
    global max_keyboard_count
    update_row(get_room_path(), 'Keyboard_count', keyboard_count)
    max_keyboard_count = int(keyboard_count)

def set_headset_count(headset_count):
    """Updates the amount of headsets available in the room"""
    global max_headset_count
    update_row(get_room_path(), 'Headset_count', headset_count)
    max_headset_count = int(headset_count)

def set_controller_count(controller_count):
    """Updates the amount of controllers available in the room"""
    global max_controller_count
    update_row(get_room_path(), 'Controller_count', controller_count)
    max_controller_count = int(controller_count)

def set_mousepad_count(mousepad_count):
    """Updates the amount of mousepads available in the room"""
    global max_mousepad_count
    update_row(get_room_path(), 'Mousepad_count', mousepad_count)
    max_mousepad_count = int(mousepad_count)

def set_PC_in_use(PC_count):
    """Updates the amount of PCs in use in the room"""
    global PC_in_use
    #print("PC count " + str(PC_count))
    update_row(get_items_path(), 'PC_count', PC_count)
    PC_in_use = int(PC_count)

def set_headset_in_use(headset_count):
    """Updates the amount of headsets in use in the room"""
    global headset_in_use
    update_row(get_items_path(), 'Headset_count', headset_count)
    headset_in_use = headset_count

def set_mouse_in_use(mouse_count):
    """Updates the amount of mice in use in the room"""
    global mouse_in_use
    update_row(get_items_path(), 'Mouse_count', mouse_count)
    mouse_in_use = mouse_count

def set_keyboard_in_use(keyboard_count):
    """Updates the amount of keyboards in use in the room"""
    global keyboard_in_use
    update_row(get_items_path(), 'Keyboard_count', keyboard_count)
    keyboard_in_use = keyboard_count

def set_controller_in_use(controller_count):
    """Updates the amount of controllers in use in the room"""
    global controller_in_use
    update_row(get_items_path(), 'Controller_count', controller_count)
    controller_in_use = controller_count

def set_mousepad_in_use(mousepad_count):
    """Updates the amount of mousepads in use in the room"""
    global mousepad_in_use
    update_row(get_items_path(), 'Mousepad_count', mousepad_count)
    mousepad_in_use = mousepad_count

def load_items():
    """Sets the room variables to the values in the room settings csv"""
    settings = csv_to_dict(get_room_path())
    set_time_limit(settings['Time_limit'])
    set_max_pc_count(settings['PC_count'])
    set_headset_count(settings['Headset_count'])
    set_mouse_count(settings['Mouse_count'])
    set_keyboard_count(settings['Keyboard_count'])
    set_controller_count(settings['Controller_count'])
    set_mousepad_count(settings['Mousepad_count'])
    
def load_items_in_use():
    settings = csv_to_dict(get_items_path())
    set_PC_in_use(settings['PC_count'])
    set_headset_in_use(settings['Headset_count'])
    set_mouse_in_use(settings['Mouse_count'])
    set_keyboard_in_use(settings['Keyboard_count'])
    set_controller_in_use(settings['Controller_count'])
    set_mousepad_in_use(settings['Mousepad_count'])


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

def get_PC_in_use():
    return PC_in_use

def get_headset_in_use():
    return headset_in_use

def get_mouse_in_use():
    return mouse_in_use

def get_keyboard_in_use():
    return keyboard_in_use

def get_controller_in_use():
    return controller_in_use

def get_mousepad_in_use():
    return mousepad_in_use

def get_session_limit():
    print("Session limits: " + str(session_limit))    
    return session_limit

def reset_count():
    global PC_in_use
    global headset_in_use
    global mouse_in_use
    global keyboard_in_use
    global headset_in_use
    global controller_in_use
    global mousepad_in_use
    set_headset_in_use(0)
    set_mouse_in_use(0)
    set_keyboard_in_use(0)
    set_controller_in_use(0)
    set_mousepad_in_use(0)
    set_PC_in_use(0)

#reset_count()