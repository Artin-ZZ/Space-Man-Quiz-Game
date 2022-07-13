##############################
#  Importing Dependencies    #
##############################
import sys,sqlite3,time,os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtPrintSupport import *





########################
#  Mainwindow Class    #
########################
class MainWindowC(QMainWindow):
    # Constractor Method
    def __init__(self, *args, **kwargs):
        super(MainWindowC, self).__init__(*args, **kwargs)

        self.conn = sqlite3.connect('questions.db')
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS Cinema(
            question VARCHAR(800) NOT NULL UNIQUE,
            one VARCHAR(255) NOT NULL,
            two VARCHAR(255) NOT NULL,
            three VARCHAR(255) NOT NULL,
            four VARCHAR(255) NOT NULL,
            answer INTEGER NOT NULL,
            id INTEGER NOT NULL UNIQUE
        );""")
        self.c.close()
        
        file_menu = self.menuBar().addMenu("&File")

        self.setWindowTitle("Cinema Managment")

        self.setMinimumSize(800, 600)

        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(("Questions", "One", "Two", "Three", "Four","Answer", "ID"))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        btn_ac_adduser = QAction(QIcon("Pics/add_qu.png"), "Add Question", self)
        btn_ac_adduser.triggered.connect(self.insert)
        btn_ac_adduser.setStatusTip("Add Question")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresh = QAction(QIcon("Pics/refresh.png"),"Refresh",self)
        btn_ac_refresh.triggered.connect(self.loaddata)
        btn_ac_refresh.setStatusTip("Refresh Table")
        toolbar.addAction(btn_ac_refresh)

        adduser_action = QAction(QIcon("Pics/add.png"),"Insert Question", self)
        adduser_action.triggered.connect(self.insert)
        file_menu.addAction(adduser_action)

        btn_ac_delete = QAction(QIcon("Pics/trash.png"), "Delete", self)
        btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Delete Question")
        toolbar.addAction(btn_ac_delete)

        deluser_action = QAction(QIcon("Pics/trash.png"), "Delete", self)
        deluser_action.triggered.connect(self.delete)
        file_menu.addAction(deluser_action)
    
    ########################
    #  LoadData Function   #
    ########################
    def loaddata(self):
        self.connection = sqlite3.connect("questions.db")
        query = "SELECT * FROM Cinema"
        result = self.connection.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number,QTableWidgetItem(str(data)))
        self.connection.close()
    
    ########################
    #  handle ER Function  #
    ########################
    def handlePaintRequest(self, printer):
        document = QTextDocument()
        cursor = QTextCursor(document)
        model = self.table.model()
        table = cursor.insertTable(model.rowCount(), model.columnCount())
        for row in range(table.rows()):
            for column in range(table.columns()):
                cursor.insertText(model.item(row, column).text())
                cursor.movePosition(QTextCursor.NextCell)
        document.print_(printer)


    def insert(self):
        dlg = InsertDialog()
        dlg.exec_()

    def delete(self):
        dlg = DeleteDialog()
        dlg.exec_()


########################
#  DeletDialog Class   #
########################
class DeleteDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(DeleteDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Delete")

        self.setWindowTitle("Delete Question")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.deletestudent)
        layout = QVBoxLayout()

        self.deleteinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.deleteinput.setValidator(self.onlyInt)
        self.deleteinput.setPlaceholderText("Question Id.")
        self.deleteinput.setInputMask("9999999999999")
        layout.addWidget(self.deleteinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def deletestudent(self):

        delrol = ""
        delrol = self.deleteinput.text()
        try:
            self.conn = sqlite3.connect("questions.db")
            self.c = self.conn.cursor()
            self.c.execute("DELETE from Cinema WHERE id="+str(delrol))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(),'Successful','Question Deleted From Database Successful')
            self.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not Delete Question from the database.')


########################
#  InsertDLG  Class    #
########################
class InsertDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(InsertDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Add Question")

        self.setWindowTitle("Add Questions")
        self.setFixedWidth(300)
        self.setFixedHeight(250)

        self.QBtn.clicked.connect(self.add_qu)

        layout = QVBoxLayout()

        self.qu_input = QLineEdit()
        self.qu_input.setPlaceholderText("Type The Question Here!")
        layout.addWidget(self.qu_input)

        self.opt_one = QLineEdit()
        self.opt_one.setPlaceholderText("Type In Option 1")
        layout.addWidget(self.opt_one)

        self.opt_two = QLineEdit()
        self.opt_two.setPlaceholderText("Type In Option 2")
        layout.addWidget(self.opt_two)

        self.opt_three = QLineEdit()
        self.opt_three.setPlaceholderText("Type In Option 3")
        layout.addWidget(self.opt_three)

        self.opt_four = QLineEdit()
        self.opt_four.setPlaceholderText("Type In Option 4")
        layout.addWidget(self.opt_four)

        self.right_answer = QComboBox()
        self.right_answer.addItem("1")
        self.right_answer.addItem("2")
        self.right_answer.addItem("3")
        self.right_answer.addItem("4")
        layout.addWidget(self.right_answer)

        self.rand_id = QLineEdit(f'{round(time.time() * 1000)}')
        self.rand_id.setReadOnly(True)
        layout.addWidget(self.rand_id)


        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def add_qu(self):

        qu_inp = ""
        one = ""
        two = ""
        three = ""
        four = ""
        answer = -1
        ra_id = ""

        qu_inp = self.qu_input.text()
        one = self.opt_one.text()
        two = self.opt_two.text()
        three = self.opt_three.text()
        four = self.opt_four.text()
        answer = self.right_answer.itemText(self.right_answer.currentIndex())
        ra_id = self.rand_id.text()

        while True:
            if self.qu_input.text() == "":
                self.conn = sqlite3.connect('questions.db')
                self.c = self.conn.cursor()
                QMessageBox.warning(QMessageBox(), 'Warning', 'Question Field Can Not Be Empty!')
                self.c.close()
                self.conn.close()
                break
            
            elif self.opt_one.text() == "":
                self.conn = sqlite3.connect('questions.db')
                self.c = self.conn.cursor()
                QMessageBox.warning(QMessageBox(), 'Warning', 'Option 1 Field Can Not Be Empty!')
                self.c.close()
                self.conn.close()
                break

            elif self.opt_two.text() == "":
                self.conn = sqlite3.connect('questions.db')
                self.c = self.conn.cursor()
                QMessageBox.warning(QMessageBox(), 'Warning', 'Option 2 Can Not Be Empty!')
                self.c.close()
                self.conn.close()
                break

            elif self.opt_three.text() == "":
                self.conn = sqlite3.connect('questions.db')
                self.c = self.conn.cursor()
                QMessageBox.warning(QMessageBox(), 'Warning', 'Option 3 Field Can Not Be Empty!')
                self.c.close()
                self.conn.close()
                break
            elif self.opt_four.text() == "":
                self.conn = sqlite3.connect('questions.db')
                self.c = self.conn.cursor()
                QMessageBox.warning(QMessageBox(), 'Warning', 'Option 4 Field Can Not Be Empty!')
                self.c.close()
                self.conn.close()
                break
            try:
                self.conn = sqlite3.connect("questions.db")
                self.c = self.conn.cursor()
                self.c.execute("INSERT INTO Cinema (question,one,two,three,four,answer,id) VALUES (?,?,?,?,?,?,?)",(qu_inp,one,two,three,four,answer,ra_id))
                self.conn.commit()
                self.c.close()
                self.conn.close()
                QMessageBox.information(QMessageBox(),'Successful','Question is added successfully to the database.')
                self.close()
                break
            except Exception:
                QMessageBox.warning(QMessageBox(), 'Error', 'Could not add Question to the database.')
                break




app = QApplication(sys.argv)
if __name__ == "__main__":
    window = MainWindowC()
    window.loaddata()
    window.show()
    # Set Window size
    window.setMinimumSize(800, 600)
    window.setMaximumSize(1920, 1080)