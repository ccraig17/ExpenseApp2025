# All SQL stuff here
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

def init_db(db_name):
    database = QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName(db_name)
    if not database.open():
        return False
    query = QSqlQuery()
    query.exec("""
    CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        date TEXT,
        category TEXT,
        amount REAL,
        description TEXT
        )
        """)
    return True

#3 Methods: 1.get ALL data from db 2.add data 3.delete data

#gets all the data
def get_expense():
    query = QSqlQuery("SELECT * FROM expenses ORDER BY date DESC")
    expenses = [] #empty list
    while query.next():
        row = [query.value(i) for i in range(5)]
        expenses.append(row)
    return expenses

def add_expanses(date, category, amount, description):
    query = QSqlQuery()
    query.prepare("""
                    INSERT INTO expenses (date, category, amount, description) 
                    VALUES (?,?,?,?)
                    """)
    #the values/parameters being sent to the db
    query.addBindValue(date)
    query.addBindValue(category)
    query.addBindValue(amount)
    query.addBindValue(description)
    return query.exec()

def delete_expenses(expense_id):
    query = QSqlQuery()
    query.prepare("DELETE FROM expenses WHERE id = ?")
    query.addBindValue(expense_id)
    return query.exec()