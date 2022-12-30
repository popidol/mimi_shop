import sys
from PyQt5.QtWidgets import QTableWidgetItem
import input_menu
import body_menu_clerk
import body_menu_manager
import psycopg2
from PyQt5 import QtCore, QtGui, QtWidgets
import registration_menu


def input_bd(user, password):
    global con
    global cur
    con = psycopg2.connect(
        database="mini_shop",
        user=f"{user}",
        password=f"{password}",
        host="127.0.0.1",
        port="5432"
    )
    cur = con.cursor()

class OneWindow(QtWidgets.QMainWindow, input_menu.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.twoWindow = None
        self.threeWindow = None
        self.pushButton.clicked.connect(self.check)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)

    def check(self):
        input_bd('postgres', 'pass')
        cur.execute("SELECT login_staff FROM staff")
        rows = cur.fetchall()
        for row in rows:
            if self.lineEdit.text() == row[0]:
                cur.execute(f"SELECT password_staff FROM staff WHERE login_staff = '{row[0]}';")
                password_bd = cur.fetchall()[0][0]
                cur.execute(f"SELECT to_md5('{self.lineEdit_2.text()}');")
                password_me = cur.fetchall()[0][0]

                if password_me == password_bd:

                    cur.execute(f"SELECT first_name_staff FROM staff WHERE login_staff = '{row[0]}';")
                    first_name = cur.fetchall()
                    cur.execute(f"SELECT last_name_staff FROM staff WHERE login_staff = '{row[0]}';")
                    last_name = cur.fetchall()
                    cur.execute(f"SELECT post_staff FROM staff WHERE login_staff = '{row[0]}';")
                    post = cur.fetchall()[0][0]

                    # cur.execute(f"set role \"{row[0]}\";")
                    con.commit()
                    if post == 'manager':
                        self.lineEdit.text()
                        self.close()
                        self.twoWindow = TwoWindow()
                        self.twoWindow.show()
                        self.twoWindow.label.setText(f"Пользователь: {first_name[0][0]} {last_name[0][0]}")
                    elif post == 'clerk':
                        self.lineEdit.text()
                        self.close()
                        self.threeWindow = ThreeWindow()
                        self.threeWindow.show()
                        self.threeWindow.label.setText(f"Пользователь: {first_name[0][0]} {last_name[0][0]}")
class TwoWindow(QtWidgets.QMainWindow, body_menu_manager.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.oneWindow = None
        self.fourWindow = None
        self.pushButton.clicked.connect(self.check)



        lable_up = ('id', 'название товара', 'количесво на складе', 'закупочная цена', 'габариты', 'поставщик')
        self.tableWidget.setColumnCount(len(lable_up))
        self.tableWidget.setHorizontalHeaderLabels(lable_up)

        self.pushButton_8.clicked.connect(self.add_user)
        self.pushButton_9.clicked.connect(self.drop_user)
        self.pushButton_5.clicked.connect(self.search)
        self.pushButton_2.clicked.connect(self.add_assortment)
        self.pushButton_4.clicked.connect(self.drop_assortment)

        # self.label_14.setText('')
        # self.label_15.setText('')
        self.label_7.setText('')

        self.pushButton_2 # добавить
        # self.pushButton_3 # изменить
        self.pushButton_4 # удалить
        self.pushButton_5 # найти
        self.lineEdit_7
        self.lineEdit_6
        self.lineEdit_5
        self.lineEdit
        self.lineEdit_2
        self.lineEdit_3
    def check(self):
        self.close()
        self.oneWindow = OneWindow()
        self.oneWindow.show()
    def drop_user(self):
        if self.lineEdit_4.text() is not None:
            self.pushButton_10.clicked.connect(self.true_drop_user)
    def true_drop_user(self):
        login_staff = self.lineEdit_4.text()
        cur = con.cursor()
        cur.execute(f"call drop_staff('{login_staff}');")
        con.commit()
        self.label_7.setText('Выполненно')
    def open_table(self):
        cur.execute(
            f"select assortment.id_product,assortment.name_product,additional_product_information.quantities_in_stock,"
            f"additional_product_information.purchase_price_product, additional_product_information.dimensions_product,additional_product_information.postavshik "
            f"from (assortment join additional_product_information on assortment.id_product = additional_product_information.id_product);")
        arr = cur.fetchall()
        self.tableWidget.setRowCount(len(arr))
        row = 0
        for a in arr:
            column = 0
            for r in a:
                cellinfo = QtWidgets.QTableWidgetItem(str(r))
                self.tableWidget.setItem(row, column, cellinfo)
                column += 1
            row += 1
    def search(self):
        if (self.lineEdit_6.text() == '') and (self.lineEdit_7.text() == '')and (self.lineEdit_5.text() == '')and (self.lineEdit.text() == '')and (self.lineEdit_2.text() == '')and (self.lineEdit_3.text() == ''):
            self.open_table()
            return
        elif self.lineEdit_7.text() != '':
            cur.execute(
                f"select assortment.id_product,assortment.name_product,additional_product_information.quantities_in_stock,additional_product_information.purchase_price_product, additional_product_information.dimensions_product,additional_product_information.postavshik "
                f"from (assortment join additional_product_information on assortment.id_product = additional_product_information.id_product) where id_product ='{self.lineEdit_7.text()}';")
        elif self.lineEdit_6.text() != '':
            cur.execute(
                f"select assortment.id_product,assortment.name_product,additional_product_information.quantities_in_stock,additional_product_information.purchase_price_product, additional_product_information.dimensions_product,additional_product_information.postavshik "
                f"from (assortment join additional_product_information on assortment.id_product = additional_product_information.id_product) where name_product ='{self.lineEdit_6.text()}';")

        elif self.lineEdit_5.text() != '':
            cur.execute(
                f"select assortment.id_product,assortment.name_product,additional_product_information.quantities_in_stock,additional_product_information.purchase_price_product, additional_product_information.dimensions_product,additional_product_information.postavshik "
                f"from (assortment join additional_product_information on assortment.id_product = additional_product_information.id_product) where quantities_in_stock ='{self.lineEdit_5.text()}';")

        elif self.lineEdit.text() != '':
            cur.execute(
                f"select assortment.id_product,assortment.name_product,additional_product_information.quantities_in_stock,additional_product_information.purchase_price_product, additional_product_information.dimensions_product,additional_product_information.postavshik "
                f"from (assortment join additional_product_information on assortment.id_product = additional_product_information.id_product) where purchase_price_product ='{self.lineEdit.text()}';")

        elif self.lineEdit_2.text() != '':
            cur.execute(
                f"select assortment.id_product,assortment.name_product,additional_product_information.quantities_in_stock,additional_product_information.purchase_price_product, additional_product_information.dimensions_product,additional_product_information.postavshik "
                f"from (assortment join additional_product_information on assortment.id_product = additional_product_information.id_product) where  postavshik ='{self.lineEdit_2.text()}';")

        elif self.lineEdit_3.text() != '':
            cur.execute(
                f"select assortment.id_product,assortment.name_product,additional_product_information.quantities_in_stock,additional_product_information.purchase_price_product, additional_product_information.dimensions_product,additional_product_information.postavshik "
                f"from (assortment join additional_product_information on assortment.id_product = additional_product_information.id_product) where dimensions_product ='{self.lineEdit_3.text()}';")

        arr = cur.fetchall()
        self.tableWidget.setRowCount(len(arr))
        row = 0
        for a in arr:
            column = 0
            for r in a:
                cellinfo = QtWidgets.QTableWidgetItem(str(r))
                self.tableWidget.setItem(row, column, cellinfo)
                column += 1
            row += 1
    def add_user(self):
        self.fourWindow = FourWindow()
        self.fourWindow.show()

    def add_assortment(self):
        id_product = self.lineEdit_7.text()
        name_product = self.lineEdit_6.text()
        quantities_in_stock = self.lineEdit_5.text()
        cost_product = self.lineEdit.text()
        postavshik = self.lineEdit_2.text()
        dimensions_product = self.lineEdit_3.text()
        if (self.lineEdit_7.text() is not None) and (self.lineEdit_6.text() is not None):
            cur.execute(
                f"INSERT INTO assortment (id_product, name_product, cost_product, availability) "
                f"VALUES ({int(id_product)}, '{name_product}', {int(cost_product)}, TRUE);")
            con.commit()
            cur.execute(
                f"INSERT INTO additional_product_information (id_product, quantities_in_stock, dimensions_product, postavshik) "
                f"VALUES ({int(id_product)},{int(quantities_in_stock)},'{dimensions_product}','{postavshik}');")
            con.commit()
        self.open_table()

    def drop_assortment(self):
        id_product = self.lineEdit_7.text()
        if (self.lineEdit_7.text() is not None) :
            cur.execute(f"DELETE from  additional_product_information where id_product = {int(id_product)};")
            con.commit()
            cur.execute(f"DELETE from assortment where id_product = {int(id_product)};")
            con.commit()
        self.open_table()


class ThreeWindow(QtWidgets.QMainWindow, body_menu_clerk.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.oneWindow = None
        self.pushButton.clicked.connect(self.check)


        global count_check
        global id_receipt
        cur.execute(f"SELECT MAX(id_check) FROM purchase;")
        count_check = cur.fetchall()[0][0]+1
        cur.execute(f"SELECT MAX(id_receipt) FROM purchase;")
        id_receipt = cur.fetchall()[0][0]

        self.lineEdit_7 # поле товара
        self.lineEdit_6 # поле кол-ва товара
        self.pushButton_2 # добавить
        self.pushButton_4 # удалить
        self.pushButton_6 # пробить
        self.pushButton_3 # добавить 2
        self.pushButton_5 # найти 2
        self.pushButton_2.clicked.connect(self.add_product)
        self.pushButton_2.clicked.connect(self.open_table)
        self.pushButton_4.clicked.connect(self.drop_product)
        self.pushButton_6.clicked.connect(self.commodity_receipt)
        self.pushButton_3.clicked.connect(self.add_buyer)
        self.pushButton_3.clicked.connect(self.search_buyer)
        self.pushButton_5.clicked.connect(self.search_buyer)


        lable_up = ('товар', 'количество', 'стоимость товара', 'итоговая стоимость')
        self.tableWidget.setColumnCount(len(lable_up))
        self.tableWidget.setHorizontalHeaderLabels(lable_up)
        lable_up_2 = ('номер телефона', 'фамилия', 'имя', 'email')
        self.tableWidget_2.setColumnCount(len(lable_up_2))
        self.tableWidget_2.setHorizontalHeaderLabels(lable_up_2)

    def check(self):
        self.close()
        self.oneWindow = OneWindow()
        self.oneWindow.show()
    def open_table(self):
        cur.execute(f"SELECT MAX(id_receipt) FROM purchase;")
        id_receipt_new = cur.fetchall()[0][0]
        if id_receipt == id_receipt_new:
            self.tableWidget.clear()
            lable_up = ('товар', 'количество', 'стоимость товара', 'итоговая стоимость')
            self.tableWidget.setColumnCount(len(lable_up))
            self.tableWidget.setHorizontalHeaderLabels(lable_up)
            self.tableWidget.setRowCount(0)
        else:
            cur.execute(
                f"select name_product, quantity, cost_product, (cost_product*quantity)  from (select name_product, id_check, quantity, cost_product from assortment inner join purchase on assortment.id_product = purchase.id_product)as food where id_check =  (select MAX(""id_check"") from ""purchase"");")
            arr = cur.fetchall()
            self.tableWidget.setRowCount(len(arr))
            row = 0
            for a in arr:
                column = 0
                for r in a:
                    cellinfo = QtWidgets.QTableWidgetItem(str(r))
                    self.tableWidget.setItem(row, column, cellinfo)

                    column += 1
                row += 1
    def add_product(self):
        if (self.lineEdit_7.text() is not None) and (self.lineEdit_6.text() is not None):
            product = self.lineEdit_7.text()
            count = int(self.lineEdit_6.text())
            cur.execute(f"select add_product('{product}', {count_check}, {count});")
            con.commit()
    def drop_product(self):
        if (self.lineEdit_7.text() != '') and (self.lineEdit_6.text() != ''):
            product = self.lineEdit_7.text()
            count = int(self.lineEdit_6.text())
            cur.execute(f"select drop_product('{product}', {count_check}, {count});")
            con.commit()
        elif (self.lineEdit_7.text() != ''):
            product = self.lineEdit_7.text()
            cur.execute(f"select drop_product('{product}', {count_check});")
            con.commit()
        self.open_table()
    def commodity_receipt(self):
        cur.execute(f"select add_check({count_check});")
        con.commit()
        self.tableWidget.clear()
        lable_up = ('товар', 'количество', 'стоимость товара', 'итоговая стоимость')
        self.tableWidget.setColumnCount(len(lable_up))
        self.tableWidget.setHorizontalHeaderLabels(lable_up)
        self.tableWidget.setRowCount(0)
    def open_table_2(self):
        cur.execute(
            f"select phone_number, last_name_buyer,first_name_buyer, email from buyer;")
        arr = cur.fetchall()
        self.tableWidget_2.setRowCount(len(arr))
        row = 0
        for a in arr:
            column = 0
            for r in a:
                cellinfo = QtWidgets.QTableWidgetItem(str(r))
                self.tableWidget_2.setItem(row, column, cellinfo)

                column += 1
            row += 1
    def search_buyer(self):
        if self.lineEdit.text() == '':
            self.open_table_2()
        elif self.lineEdit.text() != '':
            cur.execute(
                f"select phone_number,last_name_buyer, first_name_buyer, email from buyer where phone_number = '{self.lineEdit.text()}';")
            arr = cur.fetchall()
            self.tableWidget_2.setRowCount(len(arr))
            row = 0
            for a in arr:
                column = 0
                for r in a:
                    cellinfo = QtWidgets.QTableWidgetItem(str(r))
                    self.tableWidget_2.setItem(row, column, cellinfo)

                    column += 1
                row += 1
        if self.lineEdit_2.text() != '':
            cur.execute(
                f"select phone_number,last_name_buyer, first_name_buyer, email from buyer where last_name_buyer = '{self.lineEdit_2.text()}';")
            arr = cur.fetchall()
            self.tableWidget_2.setRowCount(len(arr))
            row = 0
            for a in arr:
                column = 0
                for r in a:
                    cellinfo = QtWidgets.QTableWidgetItem(str(r))
                    self.tableWidget_2.setItem(row, column, cellinfo)

                    column += 1
                row += 1
        if self.lineEdit_3.text() != '':
            cur.execute(
                f"select phone_number,last_name_buyer, first_name_buyer, email from buyer where first_name_buyer = '{self.lineEdit_3.text()}';")
            arr = cur.fetchall()
            self.tableWidget_2.setRowCount(len(arr))
            row = 0
            for a in arr:
                column = 0
                for r in a:
                    cellinfo = QtWidgets.QTableWidgetItem(str(r))
                    self.tableWidget_2.setItem(row, column, cellinfo)

                    column += 1
                row += 1
        if self.lineEdit_4.text() != '':
            cur.execute(
                f"select phone_number,last_name_buyer, first_name_buyer, email from buyer where email = '{self.lineEdit_4.text()}';")
            arr = cur.fetchall()
            self.tableWidget_2.setRowCount(len(arr))
            row = 0
            for a in arr:
                column = 0
                for r in a:
                    cellinfo = QtWidgets.QTableWidgetItem(str(r))
                    self.tableWidget_2.setItem(row, column, cellinfo)

                    column += 1
                row += 1
    def add_buyer(self):

        first_name_buyer = ''
        last_name_buyer= ''
        phone_number= ''
        email= ''
        if self.lineEdit.text() != '':
             phone_number = self.lineEdit.text()
        if self.lineEdit_2.text() != '':
             last_name_buyer = self.lineEdit_2.text()
        if self.lineEdit_3.text() != '':
             first_name_buyer = self.lineEdit_3.text()
        if self.lineEdit_4.text() != '':
             email = self.lineEdit_4.text()
        if (last_name_buyer != '') and (first_name_buyer != '') and (phone_number == '') and (email == ''):
            cur.execute(f"select add_buyer('{first_name_buyer}', '{last_name_buyer}');")
            con.commit()
        elif (last_name_buyer != '') and (first_name_buyer != '') and (phone_number != '') and (email == '') :
            cur.execute(f"select add_buyer('{first_name_buyer}', '{last_name_buyer}','{phone_number}' );")
            con.commit()
        elif (last_name_buyer != '') and (first_name_buyer != '') and (phone_number != '') and (email != ''):
            cur.execute(f"select add_buyer('{first_name_buyer}', '{last_name_buyer}','{phone_number}', '{email}');")
            con.commit()

class FourWindow(QtWidgets.QMainWindow, registration_menu.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.fourWindow = None
        self.pushButton_2.clicked.connect(self.check)
        self.lineEdit_5.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_6.setEchoMode(QtWidgets.QLineEdit.Password)
        self.label_8.setText('')
        self.close()




    def check(self):
        if self.lineEdit_1.text() \
                and self.lineEdit_2.text() \
                and self.lineEdit_3.text() \
                and self.lineEdit_4.text() \
                and self.lineEdit_5.text() \
                and self.lineEdit_6.text() is not None:
            if self.lineEdit_5.text() == self.lineEdit_6.text():
                login_staff = self.lineEdit_4.text()
                password_staff = self.lineEdit_5.text()
                first_name_staff = self.lineEdit_1.text()
                last_name_staff = self.lineEdit_2.text()
                post_staff = self.lineEdit_3.text()
                cur.execute(f"call add_staff('{login_staff}','{password_staff}','{first_name_staff}','{last_name_staff}','{post_staff}');")
                con.commit()
        self.close()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = OneWindow()
    window.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()


