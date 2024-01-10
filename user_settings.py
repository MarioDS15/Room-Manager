from data_loader import *

military = False
screen_size = 10


def load_settings():
    settings = csv_to_dict(USER_SETTINGS)
    #set_screen_size(settings['Screen_size'])
    set_time_format(settings['Time_format'])


def set_screen_size(screensize): #update
    global screen_size
    screen_size = screensize

def set_time_format(time_format):
    global military
    time_format = time_format

def get_time_format():
    return military