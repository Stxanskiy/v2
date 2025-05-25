from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QFormLayout, QPushButton, QMessageBox, QLabel
from PyQt6.QtCore import Qt

from db import get_db_connection


class LoginDialog(QDialog):
    """Simple username / password dialog relying on the *manager* table."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Авторизация")
        self.setFixedSize(240, 220)
        self.setWindowIcon(QIcon("assets/aaa.png"))
        self.setStyleSheet("background-color: #FFFFFF; font-family: Segoe UI")

        layout = QVBoxLayout(self)

        logo = QLabel()
        logo.setPixmap(QPixmap("assets/aaa.png").scaled(150, 50, Qt.AspectRatioMode.KeepAspectRatio))
        layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)

        self.login = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        form = QFormLayout()
        form.addRow("Логин:", self.login)
        form.addRow("Пароль:", self.password)
        layout.addLayout(form)

        btn = QPushButton("Войти")
        btn.clicked.connect(self.verify)
        btn.setStyleSheet("background: #67BA80; color: white; padding: 6px;")
        layout.addWidget(btn)

    def verify(self):
        """Validate credentials. Accepts the dialog on success."""
        username = self.login.text().strip()
        pwd = self.password.text().strip()

        if not username or not pwd:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """SELECT 1 FROM manager WHERE login = %s AND password = %s LIMIT 1""", 
                        (username, pwd)
                    )
                    if cur.fetchone():
                        self.accept()
                    else:
                        QMessageBox.critical(self, "Ошибка", "Неправильный логин или пароль")
        except Exception as exc:
            QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {exc}")
