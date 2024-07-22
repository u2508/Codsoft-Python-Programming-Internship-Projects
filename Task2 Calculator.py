from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel,QListWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import qdarkstyle
import math

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Advanced Calculator')
        self.showFullScreen()  # Set the window to full screen

        self.layout = QVBoxLayout()
        self.result = QLineEdit()
        self.result.setAlignment(Qt.AlignRight)
        self.result.setReadOnly(True)
        self.result.setFixedHeight(90)  # Increase height for better visibility
        self.result.setFont(QFont("Orbitron",40 , QFont.Bold))
        self.layout.addWidget(self.result)

        self.history_label = QLabel("History:")
        self.history_label.setStyleSheet("font-weight: bold; font-size: 40px;")

        self.history_list = QListWidget()
        self.history_list.setFixedWidth(340)
        #self.history_list.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.history_list.setFont(QFont("Orbitron", 18, QFont.Bold))
        #self.layout.addWidget(self.history_list)

        self.grid = QGridLayout()

        buttons = [
            ('7', 0, 0, 1, 1), ('8', 0, 1, 1, 1), ('9', 0, 2, 1, 1), ('/', 0, 3, 1, 1),
            ('4', 1, 0, 1, 1), ('5', 1, 1, 1, 1), ('6', 1, 2, 1, 1), ('*', 1, 3, 1, 1),
            ('1', 2, 0, 1, 1), ('2', 2, 1, 1, 1), ('3', 2, 2, 1, 1), ('-', 2, 3, 1, 1),
            ('0', 3, 0, 1, 1), ('.', 3, 1, 1, 1), ('=', 3, 2, 1, 1), ('+', 3, 3, 1, 1),
            ('sqrt', 4, 0, 1, 1), ('^', 4, 1, 1, 1), ('Backspace', 4, 2, 1, 1), ('Clear all', 4, 3, 1, 1),
            ('Clear History', 5, 0, 1, 4)  # Clear History button spanning across all columns
        ]

        for text, row, col, rowspan, colspan in buttons:
            button = QPushButton(text)
            button.setFixedHeight(100)
            button.setFont(QFont("Orbitron", 16, QFont.Bold))
            button.clicked.connect(self.on_click)
            self.grid.addWidget(button, row, col, rowspan, colspan)
        self.grid.addWidget(self.history_label,0,4,1,1)
        self.grid.addWidget(self.history_list,1,4,5,1)
        self.layout.addLayout(self.grid)
        self.setLayout(self.layout)

        # Apply QDarkStyle
        self.setStyleSheet(qdarkstyle.load_stylesheet())

    def calculate(self):
        try:
            current_text = self.result.text()
            expression = current_text.replace('^', '**').replace('×', '*').replace('÷', '/')
            if 'sqrt' in expression:
                expression = expression.replace('sqrt', 'math.sqrt(')+')'
                
            result = str(eval(expression))  # Evaluate the expression
            self.result.setText(result)
            self.add_to_history(f"{current_text}\n\t = {result}")
        except Exception as e:
            self.result.setText(f"Error:{e}")

    def on_click(self):
        sender = self.sender()
        text = sender.text()
        current_text = self.result.text()

        if text == 'Clear all':
            self.result.clear()
        elif text == '=':
            self.calculate()
        elif text == 'Backspace':
            self.result.setText(self.result.text()[:-1])
        elif text == 'Clear History':
            self.clear_history()
        else:
            if text in "+-*/^" and (current_text == "" or current_text[-1] in "+-*/^"):
                return
            self.result.setText(current_text + text)

    def add_to_history(self, entry):
            self.history_list.addItem( entry)
        

    def show_history(self):
        self.history_list.setVisible(True)

    def clear_history(self):
        self.history_list.clear()

    def keyPressEvent(self, event):
        key = event.key()
        key_map = {
            Qt.Key_0: '0', Qt.Key_1: '1', Qt.Key_2: '2', Qt.Key_3: '3',
            Qt.Key_4: '4', Qt.Key_5: '5', Qt.Key_6: '6', Qt.Key_7: '7',
            Qt.Key_8: '8', Qt.Key_9: '9', Qt.Key_Plus: '+', Qt.Key_Minus: '-',
            Qt.Key_Asterisk: '*', Qt.Key_Slash: '/', Qt.Key_Equal: '=', 
            Qt.Key_Backspace: '\b', Qt.Key_Return: '=', Qt.Key_Enter: '='
        }

        if key in key_map:
            text = key_map[key]
            current=str(self.result.text() + str(text))
            print(current)
            if text == '\b':
                self.result.setText(self.result.text()[:-1])
            elif text == '=':
                    self.calculate()
            else:
                self.result.setText(current)
                
        elif key == Qt.Key_Escape:
            self.result.clear()
        event.accept()

if __name__ == '__main__':
    app = QApplication([])
    calculator = Calculator()
    calculator.show()
    app.exec_()
