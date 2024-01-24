import threading 

local_event = threading.Event()

lock = threading.Lock()

log_lock = threading.Lock()
item_lock = threading.Lock()
room_lock = threading.Lock()
