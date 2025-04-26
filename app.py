# (Desktop)Application Design here.
# pip3 install pyqt6
#QWidget: Main Window, QLabel: labels for box, QPushButton: buttons, QLineEdit: user input
from pydoc import describe
from unicodedata import category

from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QLineEdit, QComboBox,
QDateEdit, QDateEdit, QTableWidget, QVBoxLayout, QHBoxLayout,
QMessageBox, QTableWidgetItem, QHeaderView)

from PyQt6.QtCore import QDate, Qt
from database import get_expense, add_expanses,delete_expenses

class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__() #initializes the Superclass (QWidget)
        self.settings()
        self.initUI()
        self.load_table_data()

    def settings(self):
            self.setGeometry(400, 300, 550, 500)
            self.setWindowTitle("Expense Tracker App")

    #Design: create all object for everything I wanna see
    def initUI(self):
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()

        #Buttons
        self.btn_add = QPushButton("Add Expense")
        self.btn_delete = QPushButton("Delete Expense")
        #Table to reflect db and table headers
        self.table = QTableWidget(0,5) # of columns in table
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Category", "Amount", "Description"])
        #edit table width
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.populate_dropdown()
        self.btn_add.clicked.connect(self.add_expense)
        self.btn_delete.clicked.connect(self.delete_expense)
        #Add Widgets to a Layout (Row/Column)
        self.setup_layout()

    def setup_layout(self):
        masterLayout = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        #Row1
        row1.addWidget(QLabel("Date"))
        row1.addWidget(self.date_box)
        row1.addWidget(QLabel("Category"))
        row1.addWidget(self.dropdown)

        #Row2
        row2.addWidget(QLabel("Amount $"))
        row2.addWidget(self.amount)
        row2.addWidget(QLabel("Description"))
        row2.addWidget(self.description)

        #Row3
        #Buttons
        row3.addWidget(self.btn_add)
        row3.addWidget(self.btn_delete)

        masterLayout.addLayout(row1)
        masterLayout.addLayout(row2)
        masterLayout.addLayout(row3)
        masterLayout.addWidget(self.table)

        self.setLayout(masterLayout)

    def populate_dropdown(self):
        categories = ["Food", "Rent", "Bills", "Entertainment", "Shopping"]
        self.dropdown.addItems(categories)

    def load_table_data(self):
        expenses = get_expense()
        self.table.setRowCount(0)
        for row_index, expense in enumerate(expenses):
            self.table.insertRow(row_index)
            for column_index, data in enumerate(expense):
                self.table.setItem(row_index,column_index,QTableWidgetItem(str(data)))

    def clear_inputs(self):
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()

    def add_expense(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        category = self.dropdown.currentText() #QComboBox used
        amount = self.amount.text() #QLineEdit used
        description = self.description.text()
        #checks if amount/description had valued entered, if NOT warning
        if not amount or not description:
            QMessageBox.warning(self, "Input Error", "Amount and Description can NOT be EMPTY!!")
            return

        if add_expanses(date, category, amount, description): #if expanse was added, the table is reloaded with the new expense
            self.load_table_data()
            #then clear input
            self.clear_inputs()
        else:
            QMessageBox.critical(self, "Error", "Failed to Add Expanse")

    def delete_expense(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Uh oh", "You need to choose a row to delete!!")
            return
        expense_id = int(self.table.item(selected_row, 0).text())
        confirm = QMessageBox.question(self, "Confirm", "Are you sure you want to delete?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes and delete_expenses( expense_id):
            self.load_table_data()