import  pymysql

def get_db_connection():
    return pymysql.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "fabrik",
        cursorclass = pymysql.cursors.DictCursor
    )




from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QFormLayout, QPushButton, QMessageBox, QLabel
from PyQt6.QtCore import Qt

from db import get_db_connection


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()

        # ��������� ��������� ����
        self.setWindowTitle("�����������")
        self.setFixedSize(200, 200)
        self.setWindowIcon(QIcon("aaa.png"))
        self.setStyleSheet("background-color: #FFFFFF; font-family: Segoe UI")

        layout = QVBoxLayout(self)

        # �������� � ��������� ��������
        logo = QLabel()
        logo.setPixmap(QPixmap("aaa.png").scaled(150, 50, Qt.AspectRatioMode.KeepAspectRatio))
        layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)

        # ���� ��� ����� ������ � ������
        self.login = QLineEdit()
        self.passw = QLineEdit()
        self.passw.setEchoMode(QLineEdit.EchoMode.Password)

        # ����� ��� ����� �����
        form = QFormLayout()
        form.addRow("�����:", self.login)
        form.addRow("������:", self.passw)
        layout.addLayout(form)

        # ������ �����
        btn = QPushButton("�����")
        btn.clicked.connect(self.verifi)
        layout.addWidget(btn)

        btn.setStyleSheet("background: #67BA80; color: white; padding: 5px;")

    #����� ��� �������� ����������� ������������
    def verifi(self):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("select login, password from manager where login = %s and password = %s",
                                (self.login.text(), self.passw.text()))
                    if cur.fetchone():
                        self.accept()
                    else:
                        QMessageBox.critical(self, "������", "������������ ����� ��� ������, �������� �� �� ��������� ����")
        except Exception as e:
            QMessageBox.critical(self, "������", f"������ ���� ������:{e}")











from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QHBoxLayout, QPushButton, QTableWidgetItem, QMessageBox, \
    QLabel
from PyQt6.QtCore import Qt


from add_product import AddProduct
from db import get_db_connection
from ceh import Ceh


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        #��������� ��������� ����
        self.setWindowTitle("������� ���� ���������")
        self.setFixedSize(900, 600)
        self.setWindowIcon(QIcon("aaa.png"))
        self.setStyleSheet("background-color: #FFFFFF; font-family: Segoe UI")

        layout = QVBoxLayout(self)

        #���������� ��������
        logo = QLabel()
        logo.setPixmap(QPixmap("aaa.png").scaled(150, 50, Qt.AspectRatioMode.KeepAspectRatio))
        layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)

        #�������� ������� ��� ����������� ���������
        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(["����� ��������", "��������", "��� ��������", "�������", "���. ���� ��� ��������", "��� ���������", "����� ������������"])
        layout.addWidget(self.table)

        btn_la = QHBoxLayout()

        #�������� ������ ��� ����������
        add_pr = QPushButton("�������� �������")
        dlt_pr = QPushButton("������� �������")
        edit_pr = QPushButton("������������� �������")
        ceh = QPushButton("���������� ����")

        add_pr.clicked.connect(self.add_pr)
        dlt_pr.clicked.connect(self.dlt_pr)
        edit_pr.clicked.connect(self.edit_pr)
        ceh.clicked.connect(self.ceh)

        btn_la.addWidget(add_pr)
        btn_la.addWidget(dlt_pr)
        btn_la.addWidget(edit_pr)
        btn_la.addWidget(ceh)

        add_pr.setStyleSheet("background: #67BA80; color: white; padding: 5px;")
        dlt_pr.setStyleSheet("background: #67BA80; color: white; padding: 5px;")
        edit_pr.setStyleSheet("background: #2196F3; color: white; padding: 5px;")
        ceh.setStyleSheet("background: #67BA80; color: white; padding: 5px;")

        layout.addLayout(btn_la)

        #�������� ������ � �������
        self.load()

    #����� ��� �������������� ���������� ��������
    def edit_pr(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "������", "�������� ������� ��� ��������������")
            return

        product_id = self.table.item(selected_row, 0).text()

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT * FROM product WHERE id = %s""", (product_id,))
                    product_data = cur.fetchone()

                    if not product_data:
                        QMessageBox.warning(self, "������", "������� �� ������")
                        return

                    dialog = AddProduct()
                    dialog.name.setText(product_data['name'])
                    dialog.articul.setText(product_data['articul'])
                    dialog.min.setText(product_data['min_cena'])

                    for i in range(dialog.tip_pr.count()):
                        if dialog.tip_pr.itemData(i) == product_data['tip_product']:
                            dialog.tip_pr.setCurrentIndex(i)
                            break

                    for i in range(dialog.tip_mat.count()):
                        if dialog.tip_mat.itemData(i) == product_data['tip_material']:
                            dialog.tip_mat.setCurrentIndex(i)
                            break

                    for i in range(dialog.ceh.count()):
                        if dialog.ceh.itemData(i) == product_data['ceh_id']:
                            dialog.ceh.setCurrentIndex(i)
                            break

                    if dialog.exec():
                        if dialog.success:
                            name, tip_pr, articul, min_cena, tip_mat, ceh = dialog.get_data()
                            cur.execute("""UPDATE product SET 
                                        name = %s, 
                                        tip_product = %s, 
                                        articul = %s, 
                                        min_cena = %s, 
                                        tip_material = %s, 
                                        ceh_id = %s 
                                        WHERE id = %s""",
                                        (name, tip_pr, articul, min_cena, tip_mat, ceh, product_id))
                            conn.commit()
                            self.load()
        except Exception as e:
            QMessageBox.critical(self, "������", f"������ ���� ������: {e}")

    #����� ��� �������� ���� ���������� ������
    def ceh(self):
        window = Ceh()
        window.exec()

    #����� �������� ������ � ��������� � �������
    def load(self):
        self.table.setRowCount(0)
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""select p.id, p.name, tp.name_product, p.articul, p.min_cena, m.name_material, c.vremya
                    from product p
                    join tip_product tp on p.tip_product = tp.id
                    join material m on p.tip_material = m.id
                    join ceh c on p.ceh_id = c.id""")
                    for row in cur.fetchall():
                        row_pos = self.table.rowCount()
                        self.table.insertRow(row_pos)
                        self.table.setItem(row_pos, 0, QTableWidgetItem(str(row["id"])))
                        self.table.setItem(row_pos, 1, QTableWidgetItem(row["name"]))
                        self.table.setItem(row_pos, 2, QTableWidgetItem(row["name_product"]))
                        self.table.setItem(row_pos, 3, QTableWidgetItem(row["articul"]))
                        self.table.setItem(row_pos, 4, QTableWidgetItem(row["min_cena"]))
                        self.table.setItem(row_pos, 5, QTableWidgetItem(row["name_material"]))
                        self.table.setItem(row_pos, 6, QTableWidgetItem(row["vremya"]))
        except Exception as e:
            QMessageBox.critical(self, "������", f"������ ���� ������:{e}")

    #����� ��� ���������� ������ ��������
    def add_pr(self):
        dialog = AddProduct()
        if dialog.exec():
            if dialog.success:
                name, tip_pr, articul, min_cena, tip_mat, ceh = dialog.get_data()
                try:
                    with get_db_connection() as conn:
                        with conn.cursor() as cur:
                            cur.execute("insert into product(name, tip_product, articul, min_cena, tip_material, ceh_id) values(%s, %s, %s, %s, %s, %s)",
                                        (name, tip_pr, articul, min_cena, tip_mat, ceh))
                            conn.commit()
                            self.load()
                except Exception as e:
                    QMessageBox.critical(self, "������", f"������ ���� ������:{e}")

    #����� ��� �������� ��������
    def dlt_pr(self):
        scrld = self.table.currentRow()
        if scrld >=0:
            try:
                id = self.table.item(scrld, 0).text()
                with get_db_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("delete from product where id = %s", (id, ))
                        conn.commit()
                        self.load()
            except Exception as e:
                QMessageBox.critical(self, "������", f"������ ���� ������:{e}")








from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QVBoxLayout, QTableWidget, QHBoxLayout, QPushButton, QTableWidgetItem, QMessageBox, \
    QDialog

from add_ceh import AddCeh
from db import get_db_connection


class Ceh(QDialog):
    def __init__(self):
        super().__init__()

        #��������� ��������� ����
        self.setWindowTitle("���� �����")
        self.setFixedSize(500, 400)
        self.setWindowIcon(QIcon("aaa.png"))
        self.setStyleSheet("background-color: #FFFFFF; font-family: Segoe UI")

        layout = QVBoxLayout(self)

        #�������� ������� ��� ����������� �����
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels (["����� ����", "�������� ����", "���������� �������", "����� ����������� �� ����������"])
        layout.addWidget(self.table)

        btn_la = QHBoxLayout()

        #�������� ������ ����������
        add_c = QPushButton("�������� ���")
        dlt_c = QPushButton("������� ���")
        edit_c = QPushButton("������������� ���")

        add_c.clicked.connect(self.add_c)
        dlt_c.clicked.connect(self.dlt_c)
        edit_c.clicked.connect(self.edit_c)

        add_c.setStyleSheet("background: #67BA80; color: white; padding: 5px;")
        dlt_c.setStyleSheet("background: #67BA80; color: white; padding: 5px;")
        edit_c.setStyleSheet("background: #2196F3; color: white; padding: 5px;")

        btn_la.addWidget(add_c)
        btn_la.addWidget(dlt_c)
        btn_la.addWidget(edit_c)

        layout.addLayout(btn_la)

        #�������� ������ � �������
        self.load()

    #����� ��� �������������� ���������� ����
    def edit_c(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "������", "�������� ��� ��� ��������������")
            return

        ceh_id = self.table.item(selected_row, 0).text()

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT * FROM ceh WHERE id = %s""", (ceh_id,))
                    ceh_data = cur.fetchone()

                    if not ceh_data:
                        QMessageBox.warning(self, "������", "��� �� ������")
                        return

                    dialog = AddCeh()
                    dialog.name.setText(ceh_data['name_ceh'])
                    dialog.chelovek.setText(ceh_data['chelovek'])
                    dialog.vremya.setText(ceh_data['vremya'])

                    if dialog.exec():
                        if dialog.success:
                            name, chelovek, vremya = dialog.get_data()
                            cur.execute("""UPDATE ceh SET 
                                        name_ceh = %s, 
                                        chelovek = %s, 
                                        vremya = %s 
                                        WHERE id = %s""",
                                        (name, chelovek, vremya, ceh_id))
                            conn.commit()
                            self.load()
        except Exception as e:
            QMessageBox.critical(self, "������", f"������ ���� ������: {e}")

    #����� �������� ������ � ����� � �������
    def load(self):
        self.table.setRowCount(0)
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""select c.id, c.name_ceh, c.chelovek, c.vremya
                    from ceh c""")
                    for row in cur.fetchall():
                        row_pos = self.table.rowCount()
                        self.table.insertRow(row_pos)
                        self.table.setItem(row_pos, 0, QTableWidgetItem(str(row["id"])))
                        self.table.setItem(row_pos, 1, QTableWidgetItem(row["name_ceh"]))
                        self.table.setItem(row_pos, 2, QTableWidgetItem(row["chelovek"]))
                        self.table.setItem(row_pos, 3, QTableWidgetItem(row["vremya"]))
        except Exception as e:
            QMessageBox.critical(self, "������", f"������ ���� ������:{e}")

    #����� ��� ���������� ������ ����
    def add_c(self):
        dialog = AddCeh()
        if dialog.exec():
            if dialog.success:
                name, chelovek, vremya  = dialog.get_data()
                try:
                    with get_db_connection() as conn:
                        with conn.cursor() as cur:
                            cur.execute ("insert into ceh(name_ceh, chelovek, vremya) values(%s, %s, %s)",
                                        (name, chelovek, vremya))
                            conn.commit()
                            self.load()
                except Exception as e:
                    QMessageBox.critical(self, "������", f"������ ���� ������:{e}")

    #����� ��� �������� ����
    def dlt_c(self):
        scrld = self.table.currentRow()
        if scrld >=0:
            try:
                id = self.table.item(scrld, 0).text()
                with get_db_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("delete from ceh where id = %s", (id,))
                        conn.commit()
                        self.load()
            except Exception as e:
                QMessageBox.critical(self, "������", f"������ ���� ������:{e}")






                

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QMessageBox


class AddCeh(QDialog):
    def __init__(self):
        super().__init__()

        # ��������� ��������� ����
        self.setWindowTitle("���������� ����")
        self.setFixedSize(500, 500)
        self.setWindowIcon(QIcon("aaa.png"))
        self.setStyleSheet("background-color: #FFFFFF; font-family: Segoe UI")

        layout = QVBoxLayout(self)

        # �������� ����� �����
        self.name = QLineEdit()
        self.chelovek = QLineEdit()
        self.vremya = QLineEdit()

        # ���������� �������� � ����� ����� � layout
        layout.addWidget(QLabel("������� �������� ����:"))
        layout.addWidget(self.name)

        layout.addWidget(QLabel("������� ���������� ������� � ����:"))
        layout.addWidget(self.chelovek)

        layout.addWidget(QLabel("������� ����� �� �������� � �������:"))
        layout.addWidget(self.vremya)

        # �������� � ��������� ������ ����������
        btn = QPushButton("���������")
        btn.clicked.connect(self.save)
        layout.addWidget(btn)
        btn.setStyleSheet("background: #67BA80; color: white; padding: 5px;")

        # ���� ��������� ����������
        self.success = False

    def save(self):
        # ��������, ��� ��� ���� ���������
        if not self.name.text() or not self.chelovek.text() or not self.vremya.text():
            QMessageBox.critical(self, "������ ���������� �����", "��������� ��� ����")
            return

        self.success = True

        self.accept()

    def get_data(self):
        return (
            self.name.text(),
            self.chelovek.text(),
            self.vremya.text()
        )





from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QComboBox, QLabel, QPushButton, QMessageBox


from db import get_db_connection


class AddProduct(QDialog):
    def __init__(self):
        super().__init__()

        # ��������� ��������� ����
        self.setWindowTitle("���������� ��������")
        self.setFixedSize(300, 300)
        self.setWindowIcon(QIcon("aaa.png"))
        self.setStyleSheet("background-color: #FFFFFF; font-family: Segoe UI")

        layout = QVBoxLayout(self)

        # �������� ����� ����� � ������
        self.name = QLineEdit()
        self.tip_pr = QComboBox()
        self.articul = QLineEdit()
        self.min = QLineEdit()
        self.tip_mat = QComboBox()
        self.ceh = QComboBox()

        #���������� ���������� �������
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("select id, name_product from tip_product")
                for row in cur.fetchall():
                    self.tip_pr.addItem(row["name_product"], row["id"])

        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("select id, name_material from material")
                for row in cur.fetchall():
                    self.tip_mat.addItem(row["name_material"], row["id"])

        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("select id, name_ceh from ceh")
                for row in cur.fetchall():
                    self.ceh.addItem(row["name_ceh"], row["id"])

        # ���������� ��������� � layout � ���������
        layout.addWidget(QLabel("������� �������� ��������:"))
        layout.addWidget(self.name)

        layout.addWidget(QLabel("�������� ��� �������:"))
        layout.addWidget(self.tip_pr)

        layout.addWidget(QLabel("������� �������:"))
        layout.addWidget(self.articul)

        layout.addWidget(QLabel("������� ����������� ��������� ��� ��������:"))
        layout.addWidget(self.min)

        layout.addWidget(QLabel("�������� ��� ���������:"))
        layout.addWidget(self.tip_mat)

        layout.addWidget(QLabel("�������� ��� ������������:"))
        layout.addWidget(self.ceh)

        # ������ ����������
        btn = QPushButton("���������")
        btn.clicked.connect(self.save)

        btn.setStyleSheet("background: #67BA80; color: white; padding: 5px;")

        layout.addWidget(btn)

        self.success = False

    def save(self):
        # ��������, ��� ��� ���� ���������
        if not self.name.text() or not self.articul.text() or not self.min.text():
            QMessageBox.critical(self, "������ ���������� �����", "��������� ��� ����")
            return
        self.success = True
        self.accept()

    def get_data(self):
        return(
            self.name.text(),
            self.tip_pr.currentData(),
            self.articul.text(),
            self.min.text(),
            self.tip_mat.currentData(),
            self.ceh.currentData()
        )








import sys

from PyQt6.QtWidgets import QApplication

from login_dialog import LoginDialog
from main_window import MainWindow

app = QApplication(sys.argv)
login = LoginDialog()
if login.exec():
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



pip install pyinstaller
pyinstaller --onefile --windowed main.py


pip freeze > requirements.txt





# ������� ���������� ������������� ��� ��������� ������� (PyQt6 + MySQL)

## ����������

### �������� ������
1. �����������
   - ���� �� ������/������
   - �������� ���� �������


2. ���������� ������
   - ����������/�������� �����
   - �������������� ����������:
     - �������� ����
     - ���������� ����������
     - ����� ������������


3. ���������� ����������
   - ������� �������
   - ���������� ����� ���������:
     - ��������
     - �������
     - ��� ��������
     - ��������
     - ���-������������
   - �������������� � ��������


4. ������ � ��
   - �������� ������:
     - ����
     - ���������
     - ���������
     - ������������


## ������� �����
```bash
# ��������� ������������
pip install -r requirements.txt

# ������ ����������
python main.py





# ��������� � ����� �������

git init

git add .

git commit -m "����������"

git remote add origin https://github.com/YaroslavSilyanov/prob

git push -u origin main

# ���� ����� ���������� master:
git push -u origin master