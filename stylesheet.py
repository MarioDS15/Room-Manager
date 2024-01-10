stylesheet = """
QWidget {  
    background-color: #3e424a; /* Background color of the window */
    
}
QLabel {
    color: #979ca6;  /* White text color */
    font: 16px;
}
QPushButton {
    color: white; /* Text color */
    background-color: #02781c; /* Background color */
    font: bold 14px;
    padding: 6px;
}
QPushButton:pressed {
    background-color: #065718; /* Background color when pressed */
    border-style: inset;
}
QLineEdit {
    color: black;  /* Text color */
    background-color: #595f6b;  /* Background color */
    border: 1px solid #686e7a;  /* Border color and width */
    border-radius: 2px;  /* Rounded corners */
    padding: 2px;  /* Spacing around text */
    margin: 4px;  /* Spacing around the widget */
}
QCheckBox {
    spacing: 5px;
    color: #979ca6;  /* White text color */
}
QCheckBox::indicator {
    width: 15px;
    height: 15px;
    border: 3px solid #686e7a; /* Border color for unchecked state */
    border-radius: 5px;
    background: #595f6b; /* Background color for unchecked state */
}

/* Style for checked state */
QCheckBox::indicator:checked {
    background: #3c4047; /* Background color for checked state */
}

/* Style for unchecked state with hover effect */
QCheckBox::indicator:hover:!checked {
    border: 2px solid #595f6b; /* Border color on hover when unchecked */
}

/* Style for checked state with hover effect */
    QCheckBox::indicator:hover:checked {
    border: 2px solid #3c4047; /* Border color on hover when checked */
}
QListWidget::item {
    color: black;  /* Text color */
    background-color: #595f6b;  /* Background color */
}
QListWidget::item:selected {
    color: white; /* Text color */
    background-color: #02781c;
}
self.toolbar.setStyleSheet
    QToolBar { background-color: #595f6b;  }
    QToolButton { background-color: #595f6b; border: none; padding: 4px; }
    QToolButton:hover { background-color: #3c4047; }


"""