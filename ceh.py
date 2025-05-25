from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QHBoxLayout, QPushButton, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import Qt

from add_ceh import AddCeh
from db import get_db_connection

class Ceh(QDialog):
    """Management dialog for workshops."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Цеха")
        self.setFixedSize(560, 420)
        self.setWindowIcon(QIcon("assets/aaa.png"))
        self.setStyleSheet("background-color: #FFFFFF; font-family: Segoe UI")

        layout = QVBoxLayout(self)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Сотрудники", "Время (мин)"])
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Добавить")
        btn_del = QPushButton("Удалить")
        btn_edit = QPushButton("Редактировать")

        btn_add.setStyleSheet("background: #67BA80; color: white; padding: 6px;")
        btn_del.setStyleSheet("background: #67BA80; color: white; padding: 6px;")
        btn_edit.setStyleSheet("background: #2196F3; color: white; padding: 6px;")

        btn_add.clicked.connect(self.add_ceh)
        btn_del.clicked.connect(self.delete_ceh)
        btn_edit.clicked.connect(self.edit_ceh)

        btn_layout.addWidget(btn_add); btn_layout.addWidget(btn_del); btn_layout.addWidget(btn_edit)
        layout.addLayout(btn_layout)

        self.load()

    # Data helpers -----------------------------------------------------------------
    def load(self):
        self.table.setRowCount(0)
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id, name_ceh, chelovek, vremya FROM ceh ORDER BY id")
                    for row in cur.fetchall():
                        r = self.table.rowCount()
                        self.table.insertRow(r)
                        self.table.setItem(r, 0, QTableWidgetItem(str(row["id"])))
                        self.table.setItem(r, 1, QTableWidgetItem(row["name_ceh"]))
                        self.table.setItem(r, 2, QTableWidgetItem(str(row["chelovek"])))
                        self.table.setItem(r, 3, QTableWidgetItem(str(row["vremya"])))
        except Exception as exc:
            QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {exc}")

    # CRUD --------------------------------------------------------------------------
    def add_ceh(self):
        dialog = AddCeh()
        if dialog.exec() and dialog.success:
            name, people, minutes = dialog.get_data()
            try:
                with get_db_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("INSERT INTO ceh(name_ceh, chelovek, vremya) VALUES (%s, %s, %s)", 
                                    (name, people, minutes))
                self.load()
            except Exception as exc:
                QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {exc}")

    def delete_ceh(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Выбор", "Выберите цех для удаления")
            return
        ceh_id = self.table.item(row, 0).text()

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM ceh WHERE id = %s", (ceh_id,))
            self.load()
        except Exception as exc:
            QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {exc}")

    def edit_ceh(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Выбор", "Выберите цех для редактирования")
            return
        ceh_id = self.table.item(row, 0).text()

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM ceh WHERE id = %s", (ceh_id,))
                    ceh_data = cur.fetchone()

            dialog = AddCeh()
            dialog.name.setText(ceh_data['name_ceh'])
            dialog.people.setText(str(ceh_data['chelovek']))
            dialog.minutes.setText(str(ceh_data['vremya']))

            if dialog.exec() and dialog.success:
                name, people, minutes = dialog.get_data()
                with get_db_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("UPDATE ceh SET name_ceh=%s, chelovek=%s, vremya=%s WHERE id=%s",
                                    (name, people, minutes, ceh_id))
                self.load()
        except Exception as exc:
            QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {exc}")
