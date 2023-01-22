from PySide2.QtGui import *
from PySide2.QtWidgets import *
import csv


def youClicked():
    label.setText("you clicked me")


user_list = {'id': 1, 'name': 'Admin', 'pin': 9999, 'accessLevel': 0, 'payrate': 20, 'hoursWorked': 0}


class User:
    def __init__(self, id, name, pin, accessLevel, payrate, hoursWorked):
        self.id = id
        self.name = name
        self.pin = pin
        self.accessLevel = accessLevel
        self.payrate = payrate
        self.hoursWorked = hoursWorked


user_list = [User(1, 'Admin', 9999, 0, 20, 0)]


app = QApplication([])  # Start an application.


def saveData():
    with open('user_file.csv', mode='w') as user_file:
        fieldnames = ['id', 'name', 'pin', 'accessLevel', 'payrate', 'hoursWorked']
        user_writer = csv.DictWriter(user_file, fieldnames=fieldnames)
        user_writer.writerow(user_list)


saveData()


def setLightMode():
    default_palette = QPalette()


def setDarkMode():
    app.setStyle('Fusion')
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)


window = QWidget()  # Create a window.
layout = QVBoxLayout()  # Create a layout.

button = QPushButton("I'm just a Button man")  # Define a button

label = QLabel('¯\_(ツ)_/¯')
button.clicked.connect(youClicked)
layout.addWidget(QLabel('Hello World!'))  # Add a label
layout.addWidget(button)  # Add the button man
layout.addWidget(label)

window.setLayout(layout)  # Pass the layout to the window
window.show()  # Show window
app.exec_()  # Execute the App
