from PyQt5.QtWidgets import QListWidget, QMenu, QAction, QListWidgetItem
from PyQt5.QtCore import Qt
#from gui import checkOut 

class StudentWidget(QListWidgetItem):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

    def student_widget(text, parent=None):
        return StudentWidget(text, parent)

    def createContextMenu(self):
        menu = QMenu()
        action1 = QAction('Checkout Student', menu)
        action2 = QAction('Check Items', menu)
        action3 = QAction('Edit Items', menu)
        menu.addAction(action1)
        menu.addAction(action2)
        menu.addAction(action3)
        return menu, action1, action2, action3

    def action_triggered(self, item, action_name):
        print(f"{action_name} triggered for {item.text()}")
        self.c
        if action_name == "Action 1":
            self.checkOut()

