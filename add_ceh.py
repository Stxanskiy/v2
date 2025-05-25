from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QMessageBox

class AddCeh(QDialog):
    """Dialog to create / edit a 'ceh' (workshop)."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Добавление цеха")
        self.setFixedSize(360, 260)
        self.setWindowIcon(QIcon("assets/aaa.png"))
        self.setStyleSheet("background-color: #FFFFFF; font-family: Segoe UI")

        layout = QVBoxLayout(self)

        self.name = QLineEdit()
        self.people = QLineEdit()
        self.minutes = QLineEdit()

        layout.addWidget(QLabel("Название цеха:"));        layout.addWidget(self.name)
        layout.addWidget(QLabel("Количество человек:"));    layout.addWidget(self.people)
        layout.addWidget(QLabel("Время (мин):"));          layout.addWidget(self.minutes)

        btn = QPushButton("Сохранить")
        btn.clicked.connect(self.save)
        btn.setStyleSheet("background: #67BA80; color: white; padding: 6px;")
        layout.addWidget(btn)

        self.success = False

    def save(self):
        if not self.name.text().strip() or not self.people.text().strip() or not self.minutes.text().strip():
            QMessageBox.critical(self, "Ошибка", "Заполните все поля")
            return

        self.success = True
        self.accept()

    def get_data(self):
        return self.name.text().strip(), self.people.text().strip(), self.minutes.text().strip()
