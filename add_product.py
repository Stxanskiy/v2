from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QComboBox, QLabel, QPushButton, QMessageBox

from db import get_db_connection

class AddProduct(QDialog):
    """Dialog to add or edit a product."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Добавление продукта")
        self.setFixedSize(360, 360)
        self.setWindowIcon(QIcon("assets/aaa.png"))
        self.setStyleSheet("background-color: #FFFFFF; font-family: Segoe UI")

        layout = QVBoxLayout(self)

        self.name = QLineEdit()
        self.tip_pr = QComboBox()
        self.articul = QLineEdit()
        self.min_cena = QLineEdit()
        self.tip_mat = QComboBox()
        self.ceh = QComboBox()

        # Populate comboboxes
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name_product FROM tip_product ORDER BY name_product")
                for row in cur.fetchall():
                    self.tip_pr.addItem(row["name_product"], row["id"])

                cur.execute("SELECT id, name_material FROM material ORDER BY name_material")
                for row in cur.fetchall():
                    self.tip_mat.addItem(row["name_material"], row["id"])

                cur.execute("SELECT id, name_ceh FROM ceh ORDER BY name_ceh")
                for row in cur.fetchall():
                    self.ceh.addItem(row["name_ceh"], row["id"])

        layout.addWidget(QLabel("Название продукта:")); layout.addWidget(self.name)
        layout.addWidget(QLabel("Тип продукта:"));      layout.addWidget(self.tip_pr)
        layout.addWidget(QLabel("Артикул:"));           layout.addWidget(self.articul)
        layout.addWidget(QLabel("Мин. цена партнёра:"));layout.addWidget(self.min_cena)
        layout.addWidget(QLabel("Материал:"));          layout.addWidget(self.tip_mat)
        layout.addWidget(QLabel("Цех изготовитель:"));  layout.addWidget(self.ceh)

        btn = QPushButton("Сохранить")
        btn.clicked.connect(self.save)
        btn.setStyleSheet("background: #67BA80; color: white; padding: 6px;")
        layout.addWidget(btn)

        self.success = False

    def save(self):
        if not self.name.text().strip() or not self.articul.text().strip() or not self.min_cena.text().strip():
            QMessageBox.critical(self, "Ошибка", "Заполните все обязательные поля")
            return

        self.success = True
        self.accept()

    def get_data(self):
        return (
            self.name.text().strip(),
            self.tip_pr.currentData(),
            self.articul.text().strip(),
            self.min_cena.text().strip(),
            self.tip_mat.currentData(),
            self.ceh.currentData()
        )
