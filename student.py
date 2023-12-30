from PyQt5.QtWidgets import QListWidgetItem
from datetime import datetime

class Student:
    def __init__(self, name, id, checked_out_items, status):
        self.name = name
        self.id = id
        self.checked_out_items = checked_out_items
        self.status = status
        self.time = datetime.now().strftime("%H:%M")



    def to_list_widget_item(self):
        # Format the display text for the QListWidgetItem
        display_text = f"{self.name} (ID: {self.id}) - {self.time}"
        # Create and return the QListWidgetItem
        item = QListWidgetItem(display_text)
        return item
    
    def checkoutStudent(self):
        self.status = False
