from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QHBoxLayout, QPushButton, QTableWidgetItem, QMessageBox, QLabel
from PyQt6.QtCore import Qt

from add_product import AddProduct
from db import get_db_connection
from ceh import Ceh

class MainWindow(QWidget):
    """Main application window: products list."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Продукция")
        self.setFixedSize(940, 620)
        self.setWindowIcon(QIcon("assets/aaa.png"))
        self.setStyleSheet("background-color: #FFFFFF; font-family: Segoe UI")

        layout = QVBoxLayout(self)

        logo = QLabel()
        logo.setPixmap(QPixmap("assets/aaa.png").scaled(160, 54, Qt.AspectRatioMode.KeepAspectRatio))
        layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)

        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Тип", "Артикул", "Мин. цена", "Материал", "Время (мин)"])
        layout.addWidget(self.table)

        # Buttons ------------------------------------------------------------------
        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Добавить")
        btn_del = QPushButton("Удалить")
        btn_edit = QPushButton("Редактировать")
        btn_ceh = QPushButton("Цеха")

        for b in (btn_add, btn_del, btn_edit, btn_ceh):
            b.setStyleSheet("background: #67BA80; color: white; padding: 6px;")

        btn_edit.setStyleSheet("background: #2196F3; color: white; padding: 6px;")

        btn_add.clicked.connect(self.add_product)
        btn_del.clicked.connect(self.delete_product)
        btn_edit.clicked.connect(self.edit_product)
        btn_ceh.clicked.connect(self.open_ceh)

        btn_layout.addWidget(btn_add); btn_layout.addWidget(btn_del); btn_layout.addWidget(btn_edit); btn_layout.addWidget(btn_ceh)
        layout.addLayout(btn_layout)

        self.load()

    # -------------------------------------------------------------------------
    def load(self):
        self.table.setRowCount(0)
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT p.id, p.name, tp.name_product, p.articul, p.min_cena,
                                        m.name_material, c.vremya
                                     FROM product p
                                     JOIN tip_product tp ON p.tip_product = tp.id
                                     JOIN material m    ON p.tip_material = m.id
                                     JOIN ceh c         ON p.ceh_id      = c.id
                                     ORDER BY p.id""")
                    for row in cur.fetchall():
                        r = self.table.rowCount()
                        self.table.insertRow(r)
                        self.table.setItem(r, 0, QTableWidgetItem(str(row['id'])))
                        self.table.setItem(r, 1, QTableWidgetItem(row['name']))
                        self.table.setItem(r, 2, QTableWidgetItem(row['name_product']))
                        self.table.setItem(r, 3, QTableWidgetItem(row['articul']))
                        self.table.setItem(r, 4, QTableWidgetItem(str(row['min_cena'])))
                        self.table.setItem(r, 5, QTableWidgetItem(row['name_material']))
                        self.table.setItem(r, 6, QTableWidgetItem(str(row['vremya'])))
        except Exception as exc:
            QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {exc}")

    # CRUD ---------------------------------------------------------------------
    def add_product(self):
        dialog = AddProduct()
        if dialog.exec() and dialog.success:
            name, tip_pr, articul, min_cena, tip_mat, ceh_id = dialog.get_data()
            try:
                with get_db_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("""INSERT INTO product(name, tip_product, articul, min_cena, tip_material, ceh_id)
                                        VALUES (%s, %s, %s, %s, %s, %s)""", 
                                    (name, tip_pr, articul, min_cena, tip_mat, ceh_id))
                self.load()
            except Exception as exc:
                QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {exc}")

    def delete_product(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Выбор", "Выберите продукт для удаления")
            return
        prod_id = self.table.item(row, 0).text()

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM product WHERE id = %s", (prod_id,))
            self.load()
        except Exception as exc:
            QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {exc}")

    def edit_product(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Выбор", "Выберите продукт для редактирования")
            return
        prod_id = self.table.item(row, 0).text()

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM product WHERE id = %s", (prod_id,))
                    data = cur.fetchone()
            if not data:
                QMessageBox.warning(self, "Ошибка", "Продукт не найден")
                return

            dialog = AddProduct()
            dialog.name.setText(data['name'])
            dialog.articul.setText(data['articul'])
            dialog.min_cena.setText(str(data['min_cena']))

            # Select correct indices in combos
            def set_combo_by_value(combo, value):
                for i in range(combo.count()):
                    if combo.itemData(i) == value:
                        combo.setCurrentIndex(i)
                        break

            set_combo_by_value(dialog.tip_pr,  data['tip_product'])
            set_combo_by_value(dialog.tip_mat, data['tip_material'])
            set_combo_by_value(dialog.ceh,     data['ceh_id'])

            if dialog.exec() and dialog.success:
                name, tip_pr, articul, min_cena, tip_mat, ceh_id = dialog.get_data()
                with get_db_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("""UPDATE product SET name=%s, tip_product=%s, articul=%s, 
                                                      min_cena=%s, tip_material=%s, ceh_id=%s 
                                        WHERE id=%s""", 
                                    (name, tip_pr, articul, min_cena, tip_mat, ceh_id, prod_id))
                self.load()
        except Exception as exc:
            QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {exc}")

    # -------------------------------------------------------------------------
    def open_ceh(self):
        dlg = Ceh()
        dlg.exec()
