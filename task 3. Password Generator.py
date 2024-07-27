import sys
import random
import string
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QVBoxLayout, QWidget,QSpacerItem,
    QLabel, QPushButton, QLineEdit, QFrame, QSizePolicy, QProgressBar
)

class ThemedContainer(QFrame):
    def __init__(self, title, content_layout, gradient_colors, border_color):
        super().__init__()

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLineWidth(8)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.setStyleSheet(f"""
            background: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 1,
                stop: 0 {gradient_colors[0]}, stop: 1 {gradient_colors[1]}
            );
            border: 2px solid {border_color};
            border-radius: 10px;
            padding: 10px;
        """)

        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(f"font-size: 32px; font-weight: bold; color: #000000;")
        space=QSpacerItem(20,20)
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addSpacerItem(space)
        layout.addLayout(content_layout)

        self.setLayout(layout)

class PasswordGeneratorApp(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(PasswordGeneratorApp, self).__init__(*args, **kwargs)
        self.setGeometry(100, 100, 600, 400)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Password Generator")

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        input_layout1 = QVBoxLayout()
        input_layout2 = QVBoxLayout()
        input_layout3 = QVBoxLayout()

        self.password_input = QLineEdit()
        self.password_input.setFont(QFont("Demon Slayer", 22))
        self.password_input.setPlaceholderText("Your generated password will appear here...")
        self.password_input.setStyleSheet("background-color: #FFF; font-weight: bold;border: 1px solid #A8E6CF; border-radius: 5px; padding: 10px;")
        self.password_input.setReadOnly(True)
        input_layout2.addWidget(self.password_input)

        generate_button = QPushButton("Generate Password")
        generate_button.setFont(QFont("Demon Slayer", 18))
        generate_button.setStyleSheet("""
            background-color: #A8E6CF;
            color: #FFF;
            border: 5px solid #BA68C8;
            border-radius: 12px;
            padding: 10px 20px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        """)
        generate_button.setCursor(Qt.PointingHandCursor)
        generate_button.clicked.connect(self.generate_password)
        input_layout1.addWidget(generate_button)

        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont("Demon Slayer", 18))
        self.result_label.setStyleSheet("color: #000000;font-weight: bold;border: 5px solid #F06292;")
        input_layout2.addWidget(self.result_label)

        
        self.strength_bar = QProgressBar()
        self.strength_bar.setRange(0, 100)
        self.strength_bar.setStyleSheet("""
            QProgressBar {
                border: 7px solid #A8E6CF;
                border-radius: 5px;
                text-align: center;
                color: #FFFFFF;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #A8E6CF;
            }
        """)
        input_layout3.addWidget(self.strength_bar)

        self.themed_container_sanemi = ThemedContainer("Password Strength", input_layout3, ["#A8E6CF", "#81C784"], "#A8E6CF")
        themed_container_obanai = ThemedContainer("Your generated password will appear here...", input_layout2, ["#E1BEE7", "#BA68C8"], "#BA68C8")
        themed_container_mitsuri = ThemedContainer("Password Generator", input_layout1, ["#F8BBD0", "#F06292"], "#F06292")

        layout.addWidget(themed_container_mitsuri)
        layout.addWidget(themed_container_obanai)
        layout.addWidget(self.themed_container_sanemi)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def generate_password(self):
        password = self.create_password()
        self.password_input.setText(password)
        self.result_label.setText(f"Generated Password: {password}")
        self.update_strength_bar(password)

    def create_password(self, length=15):
        chars = string.ascii_letters + string.digits + string.punctuation
        while True:
            password = ''.join(random.choice(chars) for _ in range(length))
            if password[0].isalnum() and password[-1].isalnum():
                break
        return password

    def update_strength_bar(self, password):
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()-_+=" for c in password)

        strength = length * 2 + has_upper * 20 + has_lower * 20 + has_digit * 20 + has_special * 30
        strength = min(strength, 100)
        self.strength_bar.setValue(strength)
        self.themed_container_sanemi.title_label.setText(f"Strength: {strength}%")

def main():
    app = QApplication(sys.argv)
    font_id = QFontDatabase.addApplicationFont("Demon Slayer.ttf")
    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        app.setFont(QFont(font_family))
    else:
        print("Font not loaded")

    window = PasswordGeneratorApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()