# -*- coding: utf-8 -*-
import sys
import sqlite3
import os
from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect)
from PySide6.QtWidgets import (QApplication, QCheckBox, QLabel, QLineEdit, 
                             QMainWindow, QMenu, QMenuBar, QPushButton, 
                             QStatusBar, QTableWidget, QTableWidgetItem, 
                             QWidget, QMessageBox)

# --- ส่วนที่ 1: คลาสหน้าตาโปรแกรม (UI Class) ---
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(896, 608)
        self.centralwidget = QWidget(MainWindow)
        
        # ตารางแสดงผล
        self.tableWidget = QTableWidget(self.centralwidget)
        # --- ส่วนที่เพิ่มเพื่อแสดงเมนู File ---
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 896, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.menubar.addAction(self.menuFile.menuAction())
        
        # ใส่ชื่อให้เมนู
        self.menuFile.setTitle("File")
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(80, 60, 721, 331))
        self.tableWidget.setColumnCount(4)
        
        # ปุ่มกดต่างๆ
        self.pushButton = QPushButton(self.centralwidget) # ปุ่ม Add
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(450, 430, 81, 26))
        
        self.pushButton_2 = QPushButton(self.centralwidget) # ปุ่ม Update
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(540, 430, 81, 26))
        
        self.pushButton_3 = QPushButton(self.centralwidget) # ปุ่ม Del
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(450, 480, 81, 26))
        
        # ช่องกรอกข้อมูล
        self.lineEdit = QLineEdit(self.centralwidget) # ช่อง Name
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(180, 430, 181, 26))
        
        self.lineEdit_2 = QLineEdit(self.centralwidget) # ช่อง Year
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(180, 480, 151, 26))
        
        self.checkBox = QCheckBox(self.centralwidget) # ช่อง Admin
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(350, 480, 84, 24))

        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(QRect(100, 430, 49, 16))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setGeometry(QRect(100, 480, 49, 16))

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("Student Management System")
        headers = ["ID", "NAME", "YEAR", "ADMIN"]
        for i, h in enumerate(headers):
            item = QTableWidgetItem()
            item.setText(h)
            self.tableWidget.setHorizontalHeaderItem(i, item)
            
        self.pushButton.setText("Add")
        self.pushButton_2.setText("Update")
        self.pushButton_3.setText("Del")
        self.checkBox.setText("Admin")
        self.label.setText("Name")
        self.label_2.setText("Year")

# --- ส่วนที่ 2: ฟังก์ชันการทำงาน (Logic & CRUD) ---
class MyProgram(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # เชื่อมต่อฐานข้อมูล
        self.conn = sqlite3.connect("data.db")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, year TEXT, admin INTEGER)")
        self.conn.commit()

        # --- การเชื่อมต่อ Signal / Slot ---
        self.ui.pushButton.clicked.connect(self.add_user)      # C - Create
        self.ui.pushButton_2.clicked.connect(self.update_user) # U - Update
        self.ui.pushButton_3.clicked.connect(self.delete_user) # D - Delete
        self.ui.tableWidget.itemClicked.connect(self.select_row) # สำหรับเลือกข้อมูล

        self.load_data() # R - Read

    def load_data(self):
        self.cur.execute("SELECT * FROM users")
        rows = self.cur.fetchall()
        self.ui.tableWidget.setRowCount(0)
        for row_idx, row_data in enumerate(rows):
            self.ui.tableWidget.insertRow(row_idx)
            for col_idx, data in enumerate(row_data):
                val = "Yes" if col_idx == 3 and data == 1 else ("No" if col_idx == 3 else str(data))
                self.ui.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(val))

    def add_user(self):
        name = self.ui.lineEdit.text()
        year = self.ui.lineEdit_2.text()
        admin = 1 if self.ui.checkBox.isChecked() else 0
        self.cur.execute("INSERT INTO users (name, year, admin) VALUES (?, ?, ?)", (name, year, admin))
        self.conn.commit()
        self.load_data()
        print("สวัสดีครับ! เพิ่มนักศึกษาเรียบร้อย")

    def select_row(self, item):
        row = item.row()
        self.current_id = self.ui.tableWidget.item(row, 0).text()
        self.ui.lineEdit.setText(self.ui.tableWidget.item(row, 1).text())
        self.ui.lineEdit_2.setText(self.ui.tableWidget.item(row, 2).text())
        self.ui.checkBox.setChecked(True if self.ui.tableWidget.item(row, 3).text() == "Yes" else False)

    def update_user(self):
        if hasattr(self, 'current_id'):
            self.cur.execute("UPDATE users SET name=?, year=?, admin=? WHERE id=?", 
                             (self.ui.lineEdit.text(), self.ui.lineEdit_2.text(), 
                              1 if self.ui.checkBox.isChecked() else 0, self.current_id))
            self.conn.commit()
            self.load_data()

    def delete_user(self):
        if hasattr(self, 'current_id'):
            self.cur.execute("DELETE FROM users WHERE id=?", (self.current_id,))
            self.conn.commit()
            self.load_data()

# --- ส่วนที่ 3: การรันโปรแกรม ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyProgram()
    window.show()
    sys.exit(app.exec())