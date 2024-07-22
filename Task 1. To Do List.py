import sys
import os
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QFileDialog, QMessageBox,QStyleFactory,
    QToolBar, QPlainTextEdit, QVBoxLayout, QWidget, QListWidget, QGroupBox,QListWidgetItem,
    QLabel, QHBoxLayout, QPushButton, QStatusBar, QFrame, QSizePolicy, QDateEdit, QDialog, QVBoxLayout, QDialogButtonBox
)

class BorderedContainer(QFrame):
    def __init__(self, title, content_layout):
        super().__init__()

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLineWidth(2)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.setStyleSheet("""
            background-color: #FFF;
            border: 2px solid #F9A825;
            border-radius: 10px;
            padding: 10px;
        """)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #333;")

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addLayout(content_layout)

        self.setLayout(layout)

class DateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Due Date")
        self.setModal(True)

        self.date_edit = QDateEdit(self)
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Choose a due date:"))
        layout.addWidget(self.date_edit)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def selected_date(self):
        return self.date_edit.date()

class ToDoApp(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(ToDoApp, self).__init__(*args, **kwargs)
        self.setGeometry(100, 100, 800, 600)
        self.path = None
        self.tasks_due_dates = {}

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Zenitsu's Thunder To-Do List")
        self.setWindowIcon(QIcon("zenitsu_icon.png"))
        self.showFullScreen()

        layout = QVBoxLayout()

        self.feedback_label = QLabel("", self)
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setFont(QFont("Anime Ace", 26))
        self.feedback_label.setStyleSheet("color: #333;")

        feedback_container = BorderedContainer("Enter Your Tasks", QVBoxLayout())
        
        self.editor = QPlainTextEdit()
        self.editor.setFont(QFont("Anime Ace", 16))
        self.editor.setStyleSheet("color: #333;background-color: #FFF; border: 1px solid #F9A825; border-radius: 5px; padding: 10px;")
        layout.addWidget(feedback_container)
        feedback_container.layout().addWidget(self.editor)

        self.todo_list_widget = QListWidget()
        self.todo_list_widget.setFont(QFont("Anime Ace", 16))
        self.todo_list_widget.setStyleSheet("""
            background-color: #FFF;
            color: #333;
            border: 1px solid #F9A825;
            border-radius: 5px;
            padding: 5px;
        """)
        self.todo_list_widget.setSelectionMode(QListWidget.MultiSelection)

        self.feedback_label = QLabel("To-Do List", self)
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setFont(QFont("Anime Ace", 26))
        self.feedback_label.setStyleSheet("color: #333;")

        todo_list_container = BorderedContainer("Existing Task List", QVBoxLayout())
        todo_list_container.layout().addWidget(self.todo_list_widget)
        layout.addWidget(todo_list_container)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Task")
        self.add_button.setFont(QFont("Anime Ace", 18))
        self.add_button.setStyleSheet("""
            QPushButton {background-color: #F9C74F; /* Bright yellow */
            color: #333;
            border: 2px solid #F9A825; /* Darker gold */
            border-radius: 12px;
            padding: 10px 20px;
            }
            QPushButton:hover {background-color: #F9A825; /* Darker gold */
            }
        """)
        self.add_button.clicked.connect(self.add_task)
        button_layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.setFont(QFont("Anime Ace", 18))
        self.remove_button.setStyleSheet("""
            QPushButton {background-color: #F9C74F; /* Bright yellow */
            color: #333;
            border: 2px solid #F9A825; /* Darker gold */
            border-radius: 12px;
            padding: 10px 20px;
            }QPushButton:hover {background-color: #F9A825; /* Darker gold */
            }
        """)
        self.remove_button.clicked.connect(self.remove_selected)
        button_layout.addWidget(self.remove_button)

        button_container = QGroupBox("Actions")
        button_container.setFont(QFont("Anime Ace", 22))
        button_container.setStyleSheet("""
            background-color: #F5F5F5;
            border: 1px solid #F9A825;
            border-radius: 10px;
        """)
        button_container.setLayout(button_layout)
        layout.addWidget(button_container)

        file_toolbar = QToolBar("File")
        self.addToolBar(file_toolbar)
        
        edit_toolbar = QToolBar("Edit")
        self.addToolBar(Qt.LeftToolBarArea, edit_toolbar)
        edit_toolbar.layout().setSpacing(5)
        self.create_actions(file_toolbar, edit_toolbar)
        self.update_title()

        QApplication.setStyle(QStyleFactory.create("Fusion"))

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.apply_theme()
        self.load_due_dates()

        self.show()

    def create_actions(self, file_toolbar, edit_toolbar):
        self.create_action(file_toolbar, "Open", self.file_open, True)
        self.create_action(file_toolbar, "Save", self.file_save, True)
        self.create_action(file_toolbar, "Save As", self.file_saveas, True)
        self.create_action(file_toolbar, "Close", self.close, True)
        
        self.create_action(edit_toolbar, "Load List", self.file_open, False)
        self.create_action(edit_toolbar, "Save List", self.file_save, False)
        self.create_action(edit_toolbar, "Cut", self.editor.cut, False)
        self.create_action(edit_toolbar, "Copy", self.editor.copy, False)
        self.create_action(edit_toolbar, "Paste", self.editor.paste, False)
        self.create_action(edit_toolbar, "Select All", self.editor.selectAll, False)

    def create_action(self, toolbar, text, slot, is_primary=False):
        action = QPushButton(text, self)
        action.clicked.connect(slot)
        action.setFont(QFont("Anime Ace", 16))
        action.setStyleSheet("""
            background-color: #F9C74F; /* Bright yellow */
            color: #333;
            border: 2px solid #F9A825; /* Darker gold */
            border-radius: 10px;
            padding: 8px 16px;
        """)
        toolbar.addWidget(action)
        return action

    def add_task(self):
        items = self.editor.toPlainText().strip()
        if items:
            items_list = items.splitlines()
            for item in items_list:
                list_item = QListWidgetItem(item)
                list_item.setFlags(list_item.flags() | Qt.ItemIsUserCheckable)
                list_item.setCheckState(Qt.Unchecked)
                
                # Create a "Set Due Date" button
                due_date_button = QPushButton("Set Due Date")
                due_date_button.clicked.connect(lambda _, item=list_item: self.set_due_date(item))
                self.todo_list_widget.setItemWidget(list_item, due_date_button)
                
                self.todo_list_widget.addItem(list_item)
            self.editor.clear()

    def remove_selected(self):
        selected_items = self.todo_list_widget.selectedItems()
        for item in selected_items:
            self.tasks_due_dates.pop(item.text(), None)
            self.todo_list_widget.takeItem(self.todo_list_widget.row(item))

    def set_due_date(self, item):
        dialog = DateDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            selected_date = dialog.selected_date()
            self.tasks_due_dates[item.text()] = selected_date.toString(Qt.ISODate)
            self.update_task_item(item)

    def update_task_item(self, item):
        due_date = self.tasks_due_dates.get(item.text())
        if due_date:
            item.setText(f"{item.text()} (Due: {due_date})")
        else:
            item.setText(item.text().split(' (Due: ')[0])

    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text files (*.txt);;All files (*)")
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    text = f.read()
            except Exception as e:
                self.dialog_critical(str(e))
            else:
                self.path = path
                self.todo_list_widget.clear()
                lines = text.splitlines()
                for line in lines:
                    if ' (Due: ' in line:
                        task, due_date = line.split(' (Due: ', 1)
                        due_date = due_date.rstrip(')')
                        self.tasks_due_dates[task] = due_date
                        list_item = QListWidgetItem(task)
                        list_item.setFlags(list_item.flags() | Qt.ItemIsUserCheckable)
                        list_item.setCheckState(Qt.Unchecked)
                        self.update_task_item(list_item)
                        self.todo_list_widget.addItem(list_item)
                self.update_title()
                self.status.showMessage(f"Opened: {path}")

    def file_save(self):
        if self.path is None:
            self.file_saveas()
        else:
            self._save_to_path(self.path)

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text files (*.txt);;All files (*)")
        if path:
            self._save_to_path(path)

    def _save_to_path(self, path):
        items = []
        for i in range(self.todo_list_widget.count()):
            item = self.todo_list_widget.item(i)
            due_date = self.tasks_due_dates.get(item.text().split(' (Due: ')[0])
            if due_date:
                items.append(f"{item.text()} (Due: {due_date})")
            else:
                items.append(item.text())
        text = "\n".join(items)
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(text)
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.path = path
            self.update_title()
            self.status.showMessage(f"Saved to: {path}")

    def update_title(self):
        self.setWindowTitle("%s - Zenitsu's Thunder To-Do List" % (os.path.basename(self.path) if self.path else "Untitled"))

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def apply_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F9F9F9;
                color: #333;
                font-family: 'Anime Ace', sans-serif;
            }
            QToolBar {
                background-color: #F5F5F5;
                color: #333;
                border: 1px solid #F9A825;
                border-radius: 8px;
                "QToolBar{spacing:5px;}"
            }
            QToolBar QPushButton {
                background-color: #F9C74F;
                color: #333;
                border: 2px solid #F9A825;
                border-radius: 10px;
                padding: 8px 16px;
            }
            QToolBar QPushButton:hover {
                background-color: #F9A825;
            }
            QPushButton {
                background-color: #F9C74F;
                color: #333;
                border: 2px solid #F9A825;
                border-radius: 10px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #F9A825;
            }
            QLabel {
                color: #333;
            }
        """)

    def load_due_dates(self):
        # Placeholder for loading due dates from a persistent store if needed
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ToDoApp()
    sys.exit(app.exec())
