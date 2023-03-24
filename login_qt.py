import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QSpacerItem
from PyQt5.QtGui import QPixmap, QIcon, QImage, QPainter, QColor, QBrush, QFont
from PyQt5.QtCore import Qt, QSize

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(800, 550))
        self.setWindowTitle('Login Form')

        # Set the background image
        background_label = QLabel(self)
        background_pixmap = QPixmap('C:\\HarvestAudit\\images\\bg\\working.jpg')
        background_label.setPixmap(background_pixmap)
        background_label.setGeometry(0, 0, 800, 550)
        background_label.setScaledContents(True)  # resize the pixmap to fit the label
        
        # Create the left layout
        left_widget = QWidget(background_label)
        left_widget.setGeometry(0, 0, 400, 550)
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        left_layout.setAlignment(Qt.AlignCenter)
        left_widget.setStyleSheet('background-color: rgba(28, 46, 74, 0.6);')

        logo_label = QLabel()
        logo_pixmap = QPixmap('C:\\HarvestAudit\\images\\logo\\PCSP_Light.png')
        logo_label.setPixmap(logo_pixmap)
        logo_label.setFixedSize(QSize(288, 192))
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet('background-color: transparent;')
        
        logo_label.setScaledContents(True)

        left_layout.addWidget(logo_label)

        # Create the right layout
        right_widget = QWidget(background_label)
        right_widget.setGeometry(400, 0, 400, 550)
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 20, 0, 20)
        right_layout.setSpacing(20)
        right_layout.setAlignment(Qt.AlignCenter)
        right_widget.setStyleSheet('background-color: rgba(28, 46, 74, 0.9);')

        # Bring the background label to the front
        background_label.raise_()

        # Set the login form as the central widget
        self.setCentralWidget(background_label)

        # Add spacer item to the top of the layout
        spacer_top = QSpacerItem(0, 20)
        right_layout.addSpacerItem(spacer_top)

        # Welcome label
        welcome_label = QLabel('Welcome!')
        welcome_label.setStyleSheet('font-size: 24pt; color: white; background-color: transparent;')
        welcome_label.setFixedSize(QSize(200, 40))
        right_layout.addWidget(welcome_label)

        # Add spacer item
        spacer_middle = QSpacerItem(0, 40)
        right_layout.addSpacerItem(spacer_middle)
        
        # Define the font for the QLineEdit widgets
        font = QFont()
        font.setPointSize(14)

        # Username and Password labels and entry widgets
        username_label = QLabel('Username:')
        username_label.setStyleSheet('font-size: 14pt; color: white; background-color: transparent;')
        username_label.setFixedSize(QSize(100, 20))
        username_entry = QLineEdit()
        username_entry.setFixedSize(QSize(300, 40))
        username_entry.setStyleSheet('font-size: 14pt; color: white; background-color: transparent; border: 0px solid #26242f;')
        password_label = QLabel('Password:')
        password_label.setStyleSheet('font-size: 14pt; color: white; background-color: transparent;')
        password_label.setFixedSize(QSize(100, 20))
        password_entry = QLineEdit()
        password_entry.setFixedSize(QSize(300, 40))
        password_entry.setStyleSheet('font-size: 14pt; color: white; background-color: transparent; border: 0px solid #26242f;')
        password_entry.setEchoMode(QLineEdit.Password)

        username_entry.setStyleSheet('QLineEdit:focus {background-color: #26242f; color: white; font-size: 14pt;}')
        password_entry.setStyleSheet('QLineEdit:focus {background-color: #26242f; color: white; font-size: 14pt;}')
        username_entry.setStyleSheet('QLineEdit:hover {border: 2px solid #ffffff; color: white; font-size: 14pt;}')
        password_entry.setStyleSheet('QLineEdit:hover {border: 2px solid #ffffff; color: white; font-size: 14pt;}')
        # Add a hover effect to the username entry widget
        # Add hover effect to username_entry widget
        

        right_layout.addWidget(username_label)
        right_layout.addWidget(username_entry)
        right_layout.addWidget(password_label)
        right_layout.addWidget(password_entry)

        # Add spacer item
        spacer_bottom = QSpacerItem(0, 20)
        right_layout.addSpacerItem(spacer_bottom)
        

        # Login button
        login_button = QPushButton('Login')
        login_button.setStyleSheet('font-size: 12pt; color: white; background-color: #4f4e5d;')
        login_button.clicked.connect(self.login)
        right_layout.addWidget(login_button)

    def login(self):
        print('Login button clicked')
        # username = username_entry.text()
        # password = password_entry.text()
        # Do login validation here
        
# # Define the stylesheets for the QLineEdit widgets
# line_edit_style = '''
#     font-size: 12pt;
#     color: white;
#     background-color: transparent;
#     border: 1px solid white;
# '''

# # Define the stylesheets for the QLineEdit widgets when they are hovered
# line_edit_hover_style = '''
#     font-size: 12pt;
#     color: white;
#     background-color: rgba(255, 255, 255, 0.2);
#     border: 1px solid white;
# '''

# # Define the stylesheets for the QLineEdit widgets when they are active
# line_edit_active_style = '''
#     font-size: 12pt;
#     color: white;
#     background-color: rgba(255, 255, 255, 0.4);
#     border: 1px solid white;
# '''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())


