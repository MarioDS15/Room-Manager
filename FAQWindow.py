


from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QScrollArea, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

faq_content = [
    ("Why does the application take some time to respond randomly?",
        "In order to make sure the application has the latest information for the room, every five minutes the application downloads the latest room data from the cloud and every action is queued until the retrieval of data is done."),
    ("Can more than one leadership member use the application at once",
        "I highly recommend not doing that, while I did put some fail safes if that happened, I could not test it to the fullest of my capabilities."),
    ("Where is the data stored?",
        "The data is stored on a private google sheet that is connected to the application via google cloud programming API. It is important to not edit data directly in there."),
    ("What is the reset button in room stats for?",
        "The reset button is only there incase an unforeseen bug regarding item tracking is encountered, if there are any items that have a negative count, still check if there is more available inventory than is recorded in the room stats, if there is more inventory than accounted for, go to room settings to update the amount of inventory."),
    ("How can I see the logs?",
        "Besides the log window on the application, I have given the Assistant Director [ Chris Kumke ] the link to the google sheet. It is highly important to not edit ANY thing in the google sheet [ If there are any sheets labelled with \"conflict\" and they contain no logs, you may delete those]."),
    ("Why does this application require names?",
        "The requirement of names both makes it easier for leadership members to identify community members and to make it more obvious whose time is up."),
    ("Why can I not open more than window?",
    "I would have had to work around my current implementation of how to open windows, I wanted to get this application out by the first week of office hours and I did not have time to implement that."),
    ("I have some feedback to give about the application, what do I do?",
        "Whether its a bug, visual updates or QOL changes, please contact me at huskyds on discord."),
    ("Someone is interested in seeing the code or even wanting to improve it, what do we do?",
        "That is awesome! I have no issues with them contacting me for more info at huskyds on discord."),
    ("Why make this application in the first place?",
        "Multiple reasons. The previous way of logging people in seemed to only be for checking if something went wrong or stolen. This application lets leadership members keep track of who should be in the room and who is overstaying their welcome. As GMU esports grows, and moves into the JC the likelihood of using 3rd party software to keep track of stuff and handling the setups will increase, I wanted to make this application as the first part of that process and to test-run such environments. Lastly, I wanted to give back to the community <3")
]

class FAQWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FAQ Window')

        # Create a scroll area for the content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        
        # Create a container widget for the scroll area
        scroll_container = QWidget()
        scroll_area.setWidget(scroll_container)
        
        # Create a QVBoxLayout for the container
        main_layout = QVBoxLayout(scroll_container)

        # Add a title label at the top
        title_label = QLabel("FAQ")
        title_font = QFont()
        title_font.setPointSize(35)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        
        # Add the title label to the layout
        main_layout.addWidget(title_label)



        # Add the FAQ content to the layout
        for question, answer in faq_content:
            question_label = QLabel(f"<b>{question}</b>")
            question_label.setStyleSheet("color: #05a31a;")  # Change the color as needed
            question_label.setWordWrap(True)
            question_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
            
            answer_label = QLabel(answer)
            answer_label.setWordWrap(True)
            answer_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)

            main_layout.addWidget(question_label)
            main_layout.addWidget(answer_label)

        # Set the layout for the container
        scroll_container.setLayout(main_layout)

        # Set the scroll area as the central widget of the window
        self.setCentralWidget(scroll_area)

        # Adjust the size of the window to show more content
        self.resize(800, 600)  # Adjust the size as needed

if __name__ == '__main__':
    app = QApplication([])
    faq_window = FAQWindow()
    faq_window.show()
    app.exec_()