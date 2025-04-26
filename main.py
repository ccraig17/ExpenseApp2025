# Responsible for running the App.
import sys
from PyQt6.QtWidgets import QApplication, QMessageBox #QApplication creates the App,
from app import ExpenseApp # imports our App from the Python file created
from database import init_db


def main():
    app = QApplication(sys.argv)
    if not init_db("expense.db"):
        #alert user if db does NOT work
        QMessageBox.critical(None, "Error", "Could NOT load database...")
        sys.exit(1)




    window = ExpenseApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()