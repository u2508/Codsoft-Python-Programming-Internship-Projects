import sys
from PyQt5.QtGui import QFont, QIcon, QFontDatabase
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QVBoxLayout, QWidget,
        QLabel, QPushButton, QLineEdit, QFrame, QSizePolicy
        )

class BorderedContainer(QFrame):
            def __init__(self, title, content_layout, color):
                    super().__init__()

                    self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
                    self.setLineWidth(2)
                    self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
                    self.setStyleSheet(f"""
                        background-color: #FFF;
                        border: 2px solid {color};
                        border-radius: 10px;
                        padding: 10px
                    """)

                    title_label = QLabel(title)
                    title_label.setAlignment(Qt.AlignCenter)
                    title_label.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {color};")

                    layout = QVBoxLayout()
                    layout.addWidget(title_label)
                    layout.addLayout(content_layout)

                    self.setLayout(layout)

class PasswordGeneratorApp(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(PasswordGeneratorApp, self).__init__(*args, **kwargs)
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Demon Slayer Password Generator")
        self.setWindowIcon(QIcon("demon_slayer_icon.png"))

        layout = QVBoxLayout()

        title_label = QLabel("Password Generator")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Demon Slayer", 26))
        title_label.setStyleSheet("color: #333;")

        input_container = BorderedContainer("Mitsuri Kanroji", QVBoxLayout(), "#FF66B2")
        input_layout = QVBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setFont(QFont("Demon Slayer", 16))
        self.password_input.setStyleSheet("background-color: #FFF; border: 1px solid #FF66B2; border-radius: 5px; padding: 10px;")
        input_layout.addWidget(self.password_input)

        generate_button = QPushButton("Generate Password")
        generate_button.setFont(QFont("Demon Slayer", 18))
        generate_button.setStyleSheet("""
                 background-color: #FF66B2;
           color: #FFF;
                       border: 2px solid #FF66B2;
                                   border-radius: 12px;
                                               padding: 10px 20px;
                   box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
                                       """)
        generate_button.clicked.connect(self.generate_password)
        input_layout.addWidget(generate_button)
        input_container.layout().addLayout(input_layout)

        layout.addWidget(title_label)
        layout.addWidget(input_container)

        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont("Demon Slayer", 18))
        self.result_label.setStyleSheet("color: #333;")
        layout.addWidget(self.result_label)

        obanai_container = BorderedContainer("Obanai Iguro", QVBoxLayout(), "#4A4A4A")
        obanai_layout = QVBoxLayout()
        obanai_label = QLabel("Obanai Style Container")
        obanai_label.setAlignment(Qt.AlignCenter)
        obanai_label.setFont(QFont("Demon Slayer", 16))
        obanai_label.setStyleSheet("color: #4A4A4A;")
        obanai_layout.addWidget(obanai_label)
        obanai_container.layout().addLayout(obanai_layout)

        layout.addWidget(obanai_container)

        sanemi_container = BorderedContainer("Sanemi Shinazugawa", QVBoxLayout(), "#4CAF50")
        sanemi_layout = QVBoxLayout()
        sanemi_label = QLabel("Sanemi Style Container")
        sanemi_label.setAlignment(Qt.AlignCenter)
        sanemi_label.setFont(QFont("Demon Slayer", 16))
        sanemi_label.setStyleSheet("color: #4CAF50;")
        sanemi_layout.addWidget(sanemi_label)
        sanemi_container.layout().addLayout(sanemi_layout)

        layout.addWidget(sanemi_container)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def generate_password(self):
    # Add your password generation logic here
        password = "GeneratedPassword123"
        self.password_input.setText(password)
        self.result_label.setText(f"Generated Password: {password}")

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


