import os
import sys
import re
from datetime import date
import sqlite3
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from myresources import *

class Origin(QWidget):
    def __init__(self, parent = None):
        super(Origin, self).__init__(parent)

        self.main_func()

    def main_func(self):

        self.session = QComboBox()
        self.session.addItem('2018/2019')
        self.session.addItem('2019/2020')
        self.session.addItem('2020/2021')
        self.session.addItem('2021/2022')
        self.session.addItem('2022/2023')

        self.vbox = QVBoxLayout()
        self.vbox_btn = QVBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.notice_area = QGridLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()
        self.textedit = QTextEdit()
        self.btn_add = QPushButton('Add Member')
        #self.btn_add.setIcon(QIcon('/:man.png'))
        self.btn_add.clicked.connect(self.add_dlg)
        self.btn_edit = QPushButton('Edit Member')
        self.btn_view = QPushButton('View students')
        self.btn_view.clicked.connect(self.view_action)
        self.btn_mod_dept = QPushButton(' Modify Deparments')
        self.btn_mod_dept.clicked.connect(self.mod_dept_action)
        self.btn_search = QPushButton('Search Member')
        self.btn_mod_unit = QPushButton('Modify Units')
        self.btn_mod_unit.clicked.connect(self.mod_unit_action)
        self.btn_remove = QPushButton('Remove Member')
        self.btn_message = QPushButton('Text message')
        self.lb_notice = QLabel('Birthday Notifications')
        self.notice_area.addWidget(self.lb_notice,1,0)
        self.hbox1.addLayout(self.notice_area)
        self.hbox1.addLayout(self.vbox_btn)
        self.hbox2.addWidget(self.btn_add)
        self.hbox2.addWidget(self.btn_edit)
        self.hbox2.addWidget(self.btn_view)
        self.hbox2.addWidget(self.btn_remove)
        self.vbox_btn.addLayout(self.hbox3)
        self.vbox_btn.addLayout(self.hbox2)
        self.btn_remove.setObjectName('first')
        firstbuttons = [self.btn_add,self.btn_edit,self.btn_view,self.btn_search,self.btn_remove,self.btn_message,self.btn_mod_unit,self.btn_mod_dept]
        for i in firstbuttons:
            i.setObjectName('megabutton')
        #self.btn_add.setObjectName('megabutton')
        ##################################################################################
        # creating and poditioning widgets for the notification sidebar layout ###########
        ##################################################################################
        bmonth_listwidget = QListWidget()
        bmonth_listwidget.setAlternatingRowColors(True)
        bweek_listwidget = QListWidget()
        bweek_listwidget.setAlternatingRowColors(True)

        this_month = QLabel(" This Month ")
        this_week = QLabel("In Seven Days ")
        self.notice_area.addWidget(this_month, 2, 0 )
        self.notice_area.addWidget(bmonth_listwidget, 3, 0 )
        self.notice_area.addWidget(this_week, 4, 0 )
        self.notice_area.addWidget(bweek_listwidget, 5, 0)
        today = date.today()
        today_str = today.strftime("%Y/%m/%d")
        current_year     = (today_str[0:4])
        current_month = (today_str[5:7])
        current_day = (today_str[8:10])
        fulltoday_str = today.strftime("%Y/%B/%d")
        fulltoday_str = fulltoday_str.split('/')
        full_month = fulltoday_str[1]
        month_text = ('Birthdays This {}'.format(full_month))
        this_month.setText(month_text)
        int_cday = int(current_day)
        int_cmonth = int(current_month)
        conn = sqlite3.connect('reminders.db')
        cursor = conn.cursor()
        cursor.execute(""" SELECT dateofbirth, matno FROM PERSONS  """)
        data = cursor.fetchall()
        for datez, matnoz in data:
            splitdate = datez.split('/')
            year = splitdate[0]
            month = splitdate[1]
            day = splitdate[2]
            intmonth = int(month)
            if intmonth == int_cmonth:
                cursor.execute(""" SELECT lastname,firstname,middlename,department,unit FROM PERSONS where matno = (?)""",(matnoz,))
                bdata  = cursor.fetchall()
                for i in bdata:

                    text = ('{} {} {} \n Dept: {}\n Date of Birth: {} \n Unit(s): {} '.format(i[0],i[1],i[2],i[3],datez,i[4]))
                    #print(text)
                    bmonth_listwidget.addItem(text)

                for i in bdata:
                    int_day = int(day)
                    if (int_day - int_cday) >=0 and (int_day - int_cday) <= 7:
                        #print('{}-------------{})'.format(matnoz, datez))
                        text2 = ('{} {} {} \n Dept: {}\n Date of Birth: {} \n Unit(s): {} '.format(i[0], i[1], i[2], i[3],datez, i[4]))
                        bweek_listwidget.addItem(text2)
                    else:
                        pass

            else:
                pass

        conn.close()

        ##################################################################################
        self.hbox3.addWidget(self.btn_mod_dept)
        self.hbox3.addWidget(self.btn_search)
        self.hbox3.addWidget(self.btn_mod_unit)
        self.hbox3.addWidget(self.btn_message)
        self.vbox.addWidget(self.session)
        self.vbox.addLayout(self.hbox1)
        #self.vbox.addLayout(self.hbox2)
        #self.vbox.addLayout(self.hbox3)
        self.setLayout(self.vbox)
        '''qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())'''
        #self.setGeometry(400, 300, 700, 500)
        self.showMaximized()
        self.setMinimumHeight(600)
        self.setMinimumWidth(850)

    def mod_unit_action(self):
        conn = sqlite3.connect('reminders.db')
        cursor = conn.cursor()
        mod_unit_dlg = QDialog(self, )
        mod_unit_dlg.setWindowIcon(QIcon(':/compass.png'))
        grid = QGridLayout(mod_unit_dlg)
        listwidget = QListWidget()
        lb_unit = QLabel(' Unit: ')
        le_unit = QLineEdit()
        le_regex = QRegExp(r"[a-z\s]*")
        le_unit.setValidator(QRegExpValidator(le_regex, self))

           btn_add = QPushButton('Add Department')
        btn_cancel = QPushButton('Cancel')
        btn_add = QPushButton('Add Department')
        btn_cancel = QPushButton('Cancel')
        def fill_unit():
            cursor.execute(''' SELECT unit FROM ALL_UNITS ''')
            data = cursor.fetchall()
            unit_tuple = []
            for i in data:
                unit_tuple.append(i)
            self.unit_list = []
            for i in unit_tuple:
                i = i[0]
                self.unit_list.append(i)
                # print(dept_list)
            for unit in self.unit_list:
                listwidget.addItem(unit)
        fill_unit()

        def remove_unit():
            item = listwidget.currentItem()
            item = item.text()
            text = ('Are you sure you want to Permanently Delete \n {} from the units database ? \n This action cannot be undone. '.format(item))
            def msg_action(i):
                msgbtn_text = i.text()
                if msgbtn_text == 'OK':
                    conn = sqlite3.connect('reminders.db')
                    cursor = conn.cursor()
                    cursor.execute(''' DELETE FROM ALL_UNITS WHERE unit = (?)''',(item,))
                    text2 = (' {} has been successfully deleted from the department'.format(item))
                    conn.commit()
                    del_msg_box =QMessageBox( self, )
                    del_msg_box.setText(text2)
                    del_msg_box.setWindowTitle('Delete Unit')
                    del_msg_box.setWindowIcon(QIcon(':/database.png'))
                    del_msg_box.exec_()
                    listwidget.clear()
                    fill_unit()
                    conn.close()
                elif msgbtn_text == 'Cancel':
                    msgbox.close()
                else:
                    print('the qmessage button does not exist')
            msgbox = QMessageBox(self, )
            msgbox.setText(text)
            msgbox.setWindowTitle(' Confirm Delete ')
            msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msgbox.buttonClicked.connect(msg_action)
            msgbox.setWindowIcon(QIcon(':/warning.png'))
            msgbox.exec_()
        listwidget.doubleClicked.connect(remove_unit)
        def mod_unit_cancel():
            mod_unit_dlg.close()
        def mod_unit_add():
            unit = le_unit.text()
            unit = unit.capitalize()
            if unit not in self.unit_list :
                cursor.execute(''' INSERT INTO  ALL_UNITS (unit) values (?) ''', (unit,))
                conn.commit()
                text = ('{} \n has just been successfully added to the database'.format(unit))
                add_unit_box = QMessageBox(self,)
                add_unit_box.setWindowTitle('Add Successfully')
                add_unit_box.setText(text)
                add_unit_box.setWindowIcon(QIcon(':/database.png'))
                add_unit_box.exec_()
                le_unit.clear()
                listwidget.clear()
                fill_unit()

            else:
                text = ('{} already exists in the database'.format(unit))
                warning_box = QMessageBox(self,)
                warning_box.setText(text)
                warning_box.setWindowTitle('Already Exists')
                warning_box.setWindowIcon(QIcon(':/warning.png'))
                warning_box.exec_()
                le_unit.clear()

        btn_cancel.clicked.connect(mod_unit_cancel)
        btn_add.clicked.connect(mod_unit_add)
        grid.addWidget(lb_unit, 1, 0)
        grid.addWidget(le_unit, 1, 1)
        grid.addWidget(btn_cancel, 2, 0)
        grid.addWidget(btn_add, 2, 1)
        grid.addWidget(listwidget, 3, 1)
        mod_unit_dlg.setWindowTitle('Modify Units')
        mod_unit_dlg.exec_()

    def mod_dept_action(self):
        conn = sqlite3.connect('reminders.db')
        cursor = conn.cursor()
        mod_dlg = QDialog(self, )
        mod_dlg.setWindowIcon(QIcon(':/graduation.png'))
        grid = QGridLayout(mod_dlg)
        listwidget = QListWidget()
        lb_dept = QLabel(' Department: ')
        le_dept = QLineEdit()
        le_regex = QRegExp(r"[a-z\s]*")
        le_dept.setValidator(QRegExpValidator(le_regex, self))

        btn_add = QPushButton('Add Department')
        btn_cancel = QPushButton('Cancel')

        def fill_dept():
            cursor.execute(''' SELECT department FROM DEPARTMENTS ''')
            data = cursor.fetchall()
            dept_tuple = []
            for i in data:
                dept_tuple.append(i)
            self.dept_list = []
            for i in dept_tuple:
                i = i[0]
                self.dept_list.append(i)
                #print(dept_list)
            for dept in self.dept_list:
                listwidget.addItem(dept)
        fill_dept()
        def remove_dept():
            item = listwidget.currentItem()
            item = item.text()
            text = ('Are you sure you want to Permanently Delete \n {} from the database ? \n This action cannot be undone. '.format(item))
            def msg_action(i):
                msgbtn_text = i.text()
                if msgbtn_text == 'OK':
                    conn = sqlite3.connect('reminders.db')
                    cursor = conn.cursor()
                    cursor.execute(''' DELETE FROM DEPARTMENTS WHERE department = (?)''',(item,))
                    conn.commit()
                    text2 = (' {} has been successfully deleted from the department'.format(item))
                    warning_box = QMessageBox(self, )
                    warning_box.setText(text2)
                    warning_box.setWindowTitle('Successfully Deleted')
                    warning_box.setWindowIcon(QIcon(':/database.png'))
                    warning_box.exec_()
                    conn.close()
                    listwidget.clear()
                    fill_dept()
                elif msgbtn_text == 'Cancel':
                    msgbox.close()
                else:
                    print('the button does not exist')
            msgbox = QMessageBox(self,)
            msgbox.setText(text)
            msgbox.setWindowTitle('Confirm Delete')
            msgbox.setWindowIcon(QIcon(':/warning.png'))
            msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msgbox.buttonClicked.connect(msg_action)
            msgbox.exec_()
        listwidget.doubleClicked.connect(remove_dept)

        def mod_cancel():
            mod_dlg.close()

        def mod_add():
            department = le_dept.text()
            department = department.capitalize()
            if department not in self.dept_list:
                cursor.execute(''' INSERT INTO  DEPARTMENTS (department) values (?) ''', (department,))
                conn.commit()
                text = ('{} \n has just been successfully added to the database'.format(department))
                add_box = QMessageBox(self,)
                add_box.setText(text)
                add_box.setWindowTitle('Added Succesfully')
                add_box.setWindowIcon(QIcon(':/database.png'))
                add_box.exec_()
                le_dept.clear()
                listwidget.clear()
                fill_dept()

            else:
                text = ('{} already exists in the database'.format(department))
                warning_box= QMessageBox(self,)
                warning_box.setText(text)
                warning_box.setWindowTitle('Already Exists')
                warning_box.setWindowIcon(QIcon(':/warning.png'))
                warning_box.exec()
                le_dept.clear()

        btn_cancel.clicked.connect(mod_cancel)
        btn_add.clicked.connect(mod_add)
        grid.addWidget(lb_dept, 1, 0)
        grid.addWidget(le_dept, 1, 1)
        grid.addWidget(btn_cancel, 2, 0)
        grid.addWidget(btn_add, 2, 1)
        grid.addWidget(listwidget, 3, 1)
        mod_dlg.setWindowTitle('Modify Department')
        mod_dlg.exec_()

    def add_dlg(self):
        conn = sqlite3.connect('reminders.db')
        cursor = conn.cursor()
        dlg = QDialog(self,)
        dlg.setWindowIcon(QIcon(':/man.png'))
        grid = QGridLayout(dlg)
        self.lb_lastname = QLabel('Last Name:')
        self.lb_firstname = QLabel('First Name:')
        self.lb_middle = QLabel('Middle Name:')

        self.lb_dept = QLabel('Department:')
        self.lb_address = QLabel('Address:')
        self.le_address = QLineEdit()
        self.le_lname = QLineEdit()
        self.le_fname = QLineEdit()
        self.le_mname = QLineEdit()
        # adding regex to the lastname, firstname, and middlename lineedits
        name_regex = QRegExp(r"[\w]*")
        self.le_lname.setValidator(QRegExpValidator(name_regex,self))
        self.le_fname.setValidator(QRegExpValidator(name_regex, self))
        self.le_mname.setValidator(QRegExpValidator(name_regex, self))
        self.lb_gender = QLabel('Gender: ')
        matno_regex = QRegExp(r"\d{4}[/]\d[/]\d{5}[A-Z]{2}")
        self.lb_matno = QLabel('Matric Number: ')
        self.lb_date = QLabel('Date Of Birth: ')
        self.lb_level = QLabel('Level: ')
        self.lb_phone = QLabel('Phone Number: ')
        self.lb_units = QLabel('Units: ')
        self.le_matno = QLineEdit()
        self.le_matno.setValidator(QRegExpValidator(matno_regex, self))
        self.gender = QComboBox()
        self.gender.insertSeparator(0)
        self.gender.addItem('Male')
        self.gender.addItem('Female')
        self.level = QComboBox()
        self.level.insertSeparator(0)

        self.phonenumber = QLineEdit()
        #self.phonenumber.setPlaceholderText(' example: 08123456789')
        self.phonenumber.setMaxLength(11)
        # adding regex to the 'self.phonenumber' lineedit
        phone_regex = QRegExp(r"\d{11}")
        self.phonenumber.setValidator(QRegExpValidator(phone_regex,self))

        self.units = QListWidget()
        self.lb_multi = QLabel('Multiple selection of Units is allowed....')
        '''all_units = ['Prayer unit ','Bible Study', 'Organising and Decoration Unit','Evangelism Unit','Counselling and Follow up',
                 'Choir Unit','Transportation Unit', 'Drama Unit','Ushering Unit', 'Academic Unit', 'Technical Unit',
                 'Welfare Unit','Commercial Unit', 'Media Department']'''
        #units = units.sort()
        '''all_units = [QListWidgetItem('Prayer unit '), QListWidgetItem('Bible Study'),
                     QListWidgetItem('Organising and Decoration Unit'),
                     QListWidgetItem('Evangelism Unit'), QListWidgetItem('Counselling and Follow up'),
                     QListWidgetItem('Choir Unit'), QListWidgetItem('Transportation Unit'),
                     QListWidgetItem('Drama Unit'),
                     QListWidgetItem('Ushering Unit'), QListWidgetItem('Academic Unit'),
                     QListWidgetItem('Technical Unit'),
                     QListWidgetItem('Welfare Unit'), QListWidgetItem('Commercial Unit'),
                     QListWidgetItem('Media Department')]'''
        all_units = []
        cursor.execute(''' SELECT unit FROM ALL_UNITS ''')
        units_tuple = cursor.fetchall()

        units_list = []
        for i in units_tuple:
            i = i[0]
            units_list.append(i)
        #print(units_list)
        for i in units_list:
            i = QListWidgetItem(i)
            all_units.append(i)
        for unit in all_units:
            self.units.addItem(unit)
        #enabling multiselection in the listwidget in order to ensure selection of multiple units
        self.units.setSelectionMode(QAbstractItemView.MultiSelection)

        levels = [ '100', '200', '300', '400', '500' ]
        for level in levels:
            self.level.addItem(level)
        '''index = self.level.findText('200')
        self.level.setCurrentIndex(index)
        print(index)'''
        cursor.execute(''' SELECT department FROM DEPARTMENTS ''')
        data = cursor.fetchall()
        dept_tuple = []
        for i in data:
            dept_tuple.append(i)
        dept_list = []
        for i in dept_tuple:
            i = i[0]
            dept_list.append(i)
        conn.close()
        self.dept_combo = QComboBox()
        self.dept_combo.insertSeparator(0)
        for dept in dept_list:
            dept = dept.capitalize()
            self.dept_combo.addItem(dept)

        self.calendar = QCalendarWidget()
        #self.calendar.setSelectedDate()
        self.submit = QPushButton('Submit')
        self.cancel = QPushButton('Cancel')
        def prime_mover():

            #connecting to the already created database
            conn = sqlite3.connect('reminders.db')
            cursor = conn.cursor()


            #obtaining my values from the various data widgets in order to store into the application's database
            lastname = self.le_lname.text()
            firstname = self.le_fname.text()
            middlename = self.le_mname.text()
            address = self.le_address.text()
            gender = self.gender.currentText()
            department = self.dept_combo.currentText()
            matno = self.le_matno.text()
            phonenumber = self.phonenumber.text()
            level = self.level.currentText()

            #obtaining the value of the units via the listwidget "self.units"



            dob = self.calendar.selectedDate()

            #converting Qdate type into string

            year = dob.year()
            month = dob.month()
            day = dob.day()
            dateofbirth = ('{}/{}/{}'.format(year,month,day))
            # inserting all the items from the GUI widgets into the database
            selected = self.units.selectedItems()
            selected_unit = ''
            for i in selected:
                if i == selected[-1]:
                    selected_unit = selected_unit + i.text()
                else:
                    selected_unit = selected_unit + i.text() + ','
            unit = selected_unit
            item_list = [lastname,firstname,middlename,department,gender,address,unit]
            all_matno = [ ]
            cursor.execute(''' SELECT matno FROM PERSONS ''')
            data = cursor.fetchall()
            for i in data:
                all_matno.append(i)
            if (matno,) not in all_matno:
                cursor.execute(''' INSERT into PERSONS(lastname, firstname, middlename, department, matno, gender, address, dateofbirth,
                                phonenumber, unit, level) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',(lastname, firstname, middlename, department,
                                matno, gender, address, dateofbirth, phonenumber, unit, level))

                conn.commit()
                text = ('{} {} {} has just been successfully added to the database'.format(lastname, firstname, middlename))
                add_box=QMessageBox(self,)
                add_box.setText(text)
                add_box.setWindowTitle('Added Successfully')
                add_box.setWindowIcon(QIcon(':/disk.png'))
                add_box.exec_()
                cursor.close()
                conn.close()
                dlg.close()
            else:
                text = ('SORRY !!!!! \n A student with the matric number already exits in the database \n please try again')
                warning_box = QMessageBox(self, )
                warning_box.setText(text)
                warning_box.setWindowTitle('Already Exists')
                warning_box.setWindowIcon(QIcon(':/security.png'))
                warning_box.exec_()
                self.le_matno.clear()



        def cancel_add():
            dlg.close()

        self.submit.clicked.connect(prime_mover)
        self.cancel.clicked.connect(cancel_add)
        grid.addWidget(self.lb_lastname, 1, 0)
        grid.addWidget(self.le_lname, 1, 1)
        grid.addWidget(self.lb_firstname, 2, 0)
        grid.addWidget(self.le_fname, 2, 1)
        grid.addWidget(self.lb_middle, 3, 0)
        grid.addWidget(self.le_mname, 3, 1)
        grid.addWidget(self.lb_address, 4, 0)
        grid.addWidget(self.le_address, 4, 1)
        grid.addWidget(self.lb_gender, 5, 0)
        grid.addWidget(self.gender, 5, 1)
        grid.addWidget(self.lb_dept, 6, 0)
        grid.addWidget(self.dept_combo, 6, 1)
        grid.addWidget(self.lb_matno,7, 0)
        grid.addWidget(self.le_matno,7, 1)
        grid.addWidget(self.lb_level,8, 0)
        grid.addWidget(self.level, 8, 1)
        grid.addWidget(self.lb_phone, 9, 0)
        grid.addWidget(self.phonenumber, 9, 1)
        grid.addWidget(self.lb_date,11, 0)
        grid.addWidget(self.calendar, 11, 1)
        grid.addWidget(self.lb_multi, 12, 1)
        grid.addWidget(self.lb_units, 13, 0)
        grid.addWidget(self.units, 13, 1)
        grid.addWidget(self.cancel, 14, 0)
        grid.addWidget(self.submit, 14, 1)
        dlg.setWindowTitle(' Add New Member  ')
        dlg.exec_()

    def the_edit(self,matric):
        conn =sqlite3.connect('reminders.db')
        cursor = conn.cursor()
        edit_dlg = QDialog(self,)
        edit_dlg.setWindowIcon(QIcon(':/write.png'))
        grid = QGridLayout(edit_dlg)
        self.elb_lastname = QLabel('Last Name:')
        self.elb_firstname = QLabel('First Name:')
        self.elb_middle = QLabel('Middle Name:')

        self.elb_dept = QLabel('Department:')
        self.elb_address = QLabel('Address:')
        self.ele_address = QLineEdit()
        self.ele_lname = QLineEdit()
        self.ele_fname = QLineEdit()
        self.ele_mname = QLineEdit()
        # adding regex to the lastname, firstname, and middlename lineedits
        name_regex = QRegExp(r"[\w]*")
        self.ele_lname.setValidator(QRegExpValidator(name_regex,self))
        self.ele_fname.setValidator(QRegExpValidator(name_regex, self))
        self.ele_mname.setValidator(QRegExpValidator(name_regex, self))
        self.elb_gender = QLabel('Gender: ')
        matno_regex = QRegExp(r"\d{4}[/]\d[/]\d{5}[A-Z]{2}")
        self.elb_matno = QLabel('Matric Number: ')
        self.elb_date = QLabel('Date Of Birth: ')
        self.elb_level = QLabel('Level: ')
        self.elb_phone = QLabel('Phone Number: ')
        self.elb_units = QLabel('Units: ')
        self.ele_matno = QLineEdit()
        self.ele_matno.setValidator(QRegExpValidator(matno_regex, self))
        self.egender = QComboBox()
        self.egender.insertSeparator(0)
        self.egender.addItem('Male')
        self.egender.addItem('Female')
        self.elevel = QComboBox()
        self.elevel.insertSeparator(0)

        self.ephonenumber = QLineEdit()
        self.ephonenumber.setPlaceholderText(' example: 08123456789')
        self.ephonenumber.setMaxLength(11)
        # adding regex to the 'self.phonenumber' lineedit
        phone_regex = QRegExp(r"\d{11}")
        self.ephonenumber.setValidator(QRegExpValidator(phone_regex,self))

        self.eunits = QListWidget()
        self.elb_multi = QLabel('Multiple selection of Units is allowed....')

        all_units = []
        cursor.execute(""" SELECT unit FROM ALL_UNITS """ )
        units_tuple = cursor.fetchall()

        units_list = []
        for i in units_tuple:
            i = i[0]
            units_list.append(i)
        for i in units_list:
            i = QListWidgetItem(i)
            all_units.append(i)
        for unit in all_units:
            self.eunits.addItem(unit)

        #enabling multiselection in the listwidget in order to ensure selection of multiple units
        self.eunits.setSelectionMode(QAbstractItemView.MultiSelection)

        levels = [ '100', '200', '300', '400', '500' ]
        for level in levels:
            self.elevel.addItem(level)

        cursor.execute(''' SELECT department FROM DEPARTMENTS ''')
        data = cursor.fetchall()
        dept_tuple = []
        for i in data:
            dept_tuple.append(i)
        dept_list = []
        for i in dept_tuple:
            i = i[0]
            dept_list.append(i)
        self.edept_combo = QComboBox()
        self.edept_combo.insertSeparator(0)
        for dept in dept_list:
            dept = dept.capitalize()
            self.edept_combo.addItem(dept)

        self.ecalendar = QCalendarWidget()
        self.esubmit = QPushButton('Save Changes')
        self.ecancel = QPushButton('Cancel')
        conn = sqlite3.connect('reminders.db')
        cursor = conn.cursor()
        cursor.execute(""" SELECT lastname, firstname, middlename, department,matno,gender,address,dateofbirth,
         phonenumber,unit,level FROM PERSONS WHERE matno = (?) """, (matric,))
        item = cursor.fetchall()
        #item_list = []
        for i in item:
            #i = (i[0])
            #item_list.append(i)
            self.ele_lname.setText(i[0])
            self.ele_fname.setText(i[1])
            self.ele_mname.setText(i[2])
            index = self.edept_combo.findText(i[3])
            self.edept_combo.setCurrentIndex(index)
            self.ele_matno.setText(i[4])
            index = self.egender.findText(i[5])
            self.egender.setCurrentIndex(index)
            self.ele_address.setText(i[6])
            string_date = i[7]
            splitted= string_date.split('/')
            self.ecalendar.setSelectedDate(QDate(int(splitted[0]), int(splitted[1]), int(splitted[2])))
            self.ephonenumber.setText(i[8])
            index = self.elevel.findText(str(i[10]))
            self.elevel.setCurrentIndex(index)
            unitz = i[9]
            splitted_unit = unitz.split(',')
            #print(splitted_unit)
            cursor.execute(''' SELECT unit FROM ALL_UNITS ''')
            data = cursor.fetchall()
            unit_tuple = []
            for i in data:
                unit_tuple.append(i)
            self.unit_list = []
            for i in unit_tuple:
                i = i[0]
                self.unit_list.append(i)
            for i in splitted_unit:
                pos = self.unit_list.index(i)
                #print(pos)
                self.eunits.setItemSelected(all_units[pos], True)
            #sel = self.eunits.selectedItems()
        conn.close()
        def confirm_save():
            text = ('Are you sure you want to save changes \n to the student with the matric number : {} \n This Action cannot be undone'.format(self.dmat))

            def msg_save_action(i):
                msgbtn_text = i.text()
                if msgbtn_text == 'OK':
                    edit_prime_mover()
                elif msgbtn_text == 'Cancel':
                    msgbox.close()
                else:
                    print('the button does not exist')

            msgbox = QMessageBox()
            msgbox.setText(text)
            msgbox.setWindowTitle(' Confirm Update ')
            msgbox.setWindowIcon(QIcon(':/disk.png'))
            msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msgbox.buttonClicked.connect(msg_save_action)
            msgbox.exec_()
        def edit_prime_mover():

            conn = sqlite3.connect('reminders.db')
            cursor = conn.cursor()

            #obtaining my values from the various data widgets in order to store into the application's database
            lastname = self.ele_lname.text()
            firstname = self.ele_fname.text()
            middlename = self.ele_mname.text()
            address = self.ele_address.text()
            gender = self.egender.currentText()
            department = self.edept_combo.currentText()
            matno = self.ele_matno.text()
            phonenumber = self.ephonenumber.text()
            level = self.elevel.currentText()

            #obtaining the value of the units via the listwidget "self.units"
            dob = self.ecalendar.selectedDate()
            #converting Qdate type into string

            year = dob.year()
            month = dob.month()
            day = dob.day()
            dateofbirth = ('{}/{}/{}'.format(year,month,day))
            # inserting all the items from the GUI widgets into the database
            selected = self.eunits.selectedItems()
            selected_unit = ''
            for i in selected:
                if i == selected[-1]:
                    selected_unit = selected_unit + i.text()
                else:
                    selected_unit = selected_unit + i.text() + ','

            unit = selected_unit
            item_list = [lastname,firstname,middlename,department,gender,address,unit]
            all_matno = [ ]
            cursor.execute(''' SELECT matno FROM PERSONS ''')
            data = cursor.fetchall()
            #print(matno)
            #print(dateofbirth)
            for i in data:
                all_matno.append(i)
            if (matno,) not in all_matno or matric == matno:
                cursor.execute(''' UPDATE PERSONS SET lastname = (?), firstname = (?),middlename = (?), department = (?), matno =  (?),
                            gender = (?), address = (?), dateofbirth = (?), phonenumber = (?), unit = (?), level = (?)
                             WHERE matno = (?)''',(lastname, firstname, middlename, department, matno, gender, address, dateofbirth,
                                                   phonenumber, unit, level, matric))

                conn.commit()
                text = ('{} {} {} \n has just been successfully Updated'.format(lastname, firstname, middlename))
                update_box = QMessageBox(self, )
                update_box.setText(text)
                update_box.setWindowIcon(QIcon(':/database.png'))
                update_box.setWindowTitle('Successfully Updated')
                update_box.exec_()
                cursor.close()
                conn.close()
                #print('new values-------------------------------------')
                #print(matno)
                #print(dateofbirth)

            else:
                text = ('SORRY !!!!! \n A student with the matric number already exits in the database \n please try again')
                else_box = QMessageBox(self,  )
                else_box.setWindowTitle('Already Exists')
                else_box.setText(text)
                else_box.setWindowIcon(QIcon(':/warning.png'))
                else_box.exec_()
            edit_dlg.close()


        def edit_cancel():
            edit_dlg.close()

        self.esubmit.clicked.connect(confirm_save)
        self.ecancel.clicked.connect(edit_cancel)
        grid.addWidget(self.elb_lastname, 1, 0)
        grid.addWidget(self.ele_lname, 1, 1)
        grid.addWidget(self.elb_firstname, 2, 0)
        grid.addWidget(self.ele_fname, 2, 1)
        grid.addWidget(self.elb_middle, 3, 0)
        grid.addWidget(self.ele_mname, 3, 1)
        grid.addWidget(self.elb_address, 4, 0)
        grid.addWidget(self.ele_address, 4, 1)
        grid.addWidget(self.elb_gender, 5, 0)
        grid.addWidget(self.egender, 5, 1)
        grid.addWidget(self.elb_dept, 6, 0)
        grid.addWidget(self.edept_combo, 6, 1)
        grid.addWidget(self.elb_matno,7, 0)
        grid.addWidget(self.ele_matno,7, 1)
        grid.addWidget(self.elb_level,8, 0)
        grid.addWidget(self.elevel, 8, 1)
        grid.addWidget(self.elb_phone, 9, 0)
        grid.addWidget(self.ephonenumber, 9, 1)
        grid.addWidget(self.elb_date,11, 0)
        grid.addWidget(self.ecalendar, 11, 1)
        grid.addWidget(self.elb_multi, 12, 1)
        grid.addWidget(self.elb_units, 13, 0)
        grid.addWidget(self.eunits, 13, 1)
        grid.addWidget(self.ecancel, 14, 0)
        grid.addWidget(self.esubmit, 14, 1)
        edit_dlg.setWindowTitle(' Edit Existing Member  ')
        edit_dlg.exec_()

    def view_action(self):

        dlg = QDialog(self,)
        dlg.setWindowIcon(QIcon(':/man.png'))
        vbox_main = QVBoxLayout(dlg)
        tabwidget = QTabWidget()
        self.present_tab = (tabwidget.currentIndex())
        levelwidget = QWidget()
        levellayout = QVBoxLayout()
        hbox_btn = QHBoxLayout()
        test_btn = QPushButton('test btn')
        btn_all = QPushButton('All Members')
        btn_100 = QPushButton('100 level')
        btn_200 = QPushButton('200 level')
        btn_300 = QPushButton('300 level')
        btn_400 = QPushButton('400 level')
        btn_500 = QPushButton('500 level')

        def create_unit_btns(text, holder):
            btn = QPushButton(text)
            holder.addWidget(btn)
            btn.setCheckable(True)
        def  test_action():
            opt_dlg = QDialog(self,)
            opt_dlg.setWindowIcon(QIcon(':/compass.png'))
            opt_grid = QGridLayout(opt_dlg)
            geom = self.frameGeometry()
            geom.moveCenter(QCursor.pos())
            opt_dlg.setGeometry(geom)
            opt_listwidget = QListWidget()
            opt_cancel = QPushButton('Cancel ')
            opt_listwidget.addItem('Edit Student')
            opt_listwidget.addItem('Delete Student')
            opt_grid.addWidget(opt_listwidget,1,1)
            opt_grid.addWidget(opt_cancel, 2, 1)
            opt_dlg.setFixedHeight(100)
            opt_dlg.setFixedWidth(100)
            opt_dlg.setModal(True)
            self.present_tab = (tabwidget.currentIndex())
            self.table_locator()

            def edit_and_delete_action():
                item = opt_listwidget.currentItem()
                senderz = item.text()

                if senderz == 'Edit Student':
                    opt_dlg.close()
                    self.the_edit(self.dmat)
                elif senderz == 'Delete Student':
                    #self.table_locator()
                    text = ('Are you sure you want to delete the student \n with the matricnumber {}'.format(self.dmat))
                    def msg_del_action(i):
                        msgbtn_text = i.text()
                        if msgbtn_text == 'OK':
                            conn = sqlite3.connect('reminders.db')
                            cursor = conn.cursor()
                            cursor.execute(""" DELETE FROM PERSONS WHERE matno = (?) """,(self.dmat,))
                            conn.commit()
                            text2 = ('The Student has been deleted from the database')
                            del_box = QMessageBox(self,)
                            del_box.setWindowTitle('Successful')
                            del_box.setText(text2)
                            del_box.setWindowIcon(QIcon(':/database.png'))
                            del_box.exec_()
                            conn.close()
                            opt_dlg.close()
                        elif msgbtn_text == 'Cancel':
                            opt_dlg.close()
                        else:
                            print('the button does not exist')

                    msgbox = QMessageBox(self,)
                    msgbox.setText(text)
                    msgbox.setWindowTitle(' Confirm Delete ')
                    msgbox.setWindowIcon(QIcon(':/warning.png'))
                    msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    msgbox.buttonClicked.connect(msg_del_action)
                    msgbox.exec_()

                else:
                    print('this item seems not to be in the listwidget')
            def opt_close():
                opt_dlg.close()
            opt_cancel.clicked.connect(opt_close)
            opt_listwidget.clicked.connect(edit_and_delete_action)
            opt_dlg.exec_()

        test_btn.clicked.connect(test_action)
        btn_list = [btn_all, btn_100,btn_200,btn_300,btn_400,btn_500]
        conn = sqlite3.connect('reminders.db')
        cursor = conn.cursor()
        self.table_level = QTableWidget()
        self.table_level.cellDoubleClicked.connect(test_action)
        self.table_level.setColumnCount(11)
        self.table_level.setHorizontalHeaderLabels(
            ['Lastname', 'Firstname', 'Middlename', 'Department','Matric no', 'Gender', 'Address', 'Date Of Birth', 'Phone Number',
             'Unit', 'Level'])
        self.table_level.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_level.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_level.setSelectionMode(QTableWidget.SingleSelection)
        def dlg_exit():
            dlg.close()


        for button in btn_list:
            button.clicked.connect(self.level_btn_action)
            button.setCheckable(True)
            hbox_btn.addWidget(button)
        #table_level.setRowCount(10)
        # populating the table on first opening of the dialog

        cursor.execute("SELECT * FROM PERSONS ORDER BY lastname asc")
        all = cursor.fetchall()
        for row_number, row_data in enumerate(all):
            self.table_level.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.table_level.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))
        conn.close()

        levellayout.addLayout(hbox_btn)
        levellayout.addWidget(self.table_level)
        levelwidget.setLayout(levellayout)
        tabwidget.addTab(levelwidget, "By Level")
        cancel_btn = QPushButton(" Cancel ")
        cancel_btn.clicked.connect(dlg_exit)
        grid = QGridLayout()
        grid.addWidget(cancel_btn, 1, 1)
        vbox_main.addWidget(tabwidget)
        vbox_main.addLayout(grid)

        #########################################################################################
        ## creating the second tab of the tabwidget ....this covers the unit for table display ##
        #########################################################################################
        """unitwidget = QWidget()
        unitlayout = QVBoxLayout()
        table_unit = QTableWidget()
        table_unit.cellClicked.connect(test_action)
        table_unit.setColumnCount(11)
        table_unit.setHorizontalHeaderLabels(
            ['Lastname', 'Firstname', 'Middlename', 'Department', 'Matric no', 'Gender', 'Address', 'Date Of Birth', 'Phone Number',
             'Unit', 'Level'])
        # table_unit.setEditTriggers(QTableWidget.NoEditTriggers)
        # table_unit.setSelectionBehavior(QTableWidget.SelectRows)
        table_unit.setSelectionMode(QTableWidget.SingleSelection)
        hbox_btn2 = QHBoxLayout()
        '''for unit in all_units:
            create_unit_btns(unit, hbox_btn2)'''
        unitlayout.addLayout(hbox_btn2)
        unitlayout.addWidget(table_unit)
        unitwidget.setLayout(unitlayout)
        tabwidget.addTab(unitwidget, " By Units ")"""
        #########################################################################################
        ## creating the third tab of the tabwidget ...this covers the gender for table display ##
        #########################################################################################

        genderwidget = QWidget()
        genderlayout = QVBoxLayout()
        self.table_gender = QTableWidget()
        self.table_gender.setColumnCount(11)
        self.table_gender.cellClicked.connect(test_action)
        self.table_gender.setHorizontalHeaderLabels(
            ['Lastname', 'Firstname', 'Middlename', 'Department', 'Matric no', 'Gender', 'Address', 'Date Of Birth', 'Phone Number',
             'Unit', 'Level'])
        self.table_gender.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_gender.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_gender.setSelectionMode(QTableWidget.SingleSelection)
        hbox_btn3 = QHBoxLayout()
        male_btn = QPushButton('Male')
        female_btn = QPushButton('Female')
        hbox_btn3.addWidget(male_btn)
        hbox_btn3.addWidget(female_btn)
        male_btn.clicked.connect(self.gender_btn_action)
        female_btn.clicked.connect(self.gender_btn_action)
        genderlayout.addLayout(hbox_btn3)
        genderlayout.addWidget(self.table_gender)
        genderwidget.setLayout(genderlayout)
        tabwidget.addTab(genderwidget, " By Gender ")


        dlg.setMinimumHeight(600)
        dlg.setMinimumWidth(1200)
        dlg.showMaximized()
        qr = dlg.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        dlg.move(qr.topLeft())
        #dlg.setModal(True)
        dlg.exec_()
    def gender_btn_action(self):
        self.table_gender.clear()
        the_sender = self.sender()
        btn_text = the_sender.text()
        # self.table_level = QTableWidget()
        self.table_gender.setColumnCount(11)
        self.table_gender.setHorizontalHeaderLabels(
            ['Lastname', 'Firstname', 'Middlename', 'Department', 'Matric no', 'Gender', 'Address', 'Date Of Birth', 'Phone Number',
             'Unit', 'Level'])
        self.table_level.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_level.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_gender.setSelectionMode(QTableWidget.SingleSelection)
        conn = sqlite3.connect('reminders.db')
        cursor = conn.cursor()
        if btn_text == 'Male':
            cursor.execute("SELECT * FROM PERSONS WHERE gender = 'Male' ORDER BY lastname ASC")
        elif btn_text == 'Female':
            cursor.execute("SELECT * FROM PERSONS WHERE gender = 'Female' ORDER BY lastname ASC")
        else:
            pass
        all = cursor.fetchall()
        for row_number, row_data in enumerate(all):
            self.table_gender.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.table_gender.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))
        conn.close()

    def level_btn_action(self):
        ''' the function for populating the tablewidget based on the selected level by the user '''
        self.table_level.clear()
        the_sender = self.sender()
        btn_text = the_sender.text()
        #self.table_level = QTableWidget()
        self.table_level.setColumnCount(11)
        self.table_level.setHorizontalHeaderLabels(
            ['Lastname', 'Firstname', 'Middlename', 'Department','Matric no', 'Gender', 'Address', 'Date Of Birth', 'Phone Number',
             'Unit', 'Level'])
        self.table_level.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_level.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_level.setSelectionMode(QTableWidget.SingleSelection)
        conn = sqlite3.connect('reminders.db')
        cursor = conn.cursor()
        if btn_text == 'All Members':
            cursor.execute(" SELECT * FROM PERSONS ORDER BY lastname ASC")
        elif btn_text == '100 level':
            cursor.execute("SELECT * FROM PERSONS WHERE level = '100' ORDER BY lastname ASC ")
        elif btn_text == '200 level':
            cursor.execute("SELECT * FROM PERSONS WHERE level = '200' ORDER BY lastname ASC")
        elif btn_text == '300 level':
            cursor.execute("SELECT * FROM PERSONS WHERE level = '300' ORDER BY lastname ASC")
        elif btn_text == '400 level':
            cursor.execute("SELECT * FROM PERSONS WHERE level = '400' ORDER BY lastname ASC")
        elif btn_text == '500 level':
            cursor.execute("SELECT * FROM PERSONS WHERE level = '500' ORDER BY lastname ASC")
        else:
            pass
        all = cursor.fetchall()
        for row_number, row_data in enumerate(all):
            self.table_level.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.table_level.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))
        conn.close()

    def table_locator(self):
        if self.present_tab ==0:
            data = self.table_level.currentItem()
            data = data.text()
            rowz = self.table_level.currentRow()
            col = self.table_level.currentColumn()
            #self.data = data.text()
            dmat = self.table_level.item(rowz, 4)
            self.dmat = dmat.text()
            #print('{} at row: {} and column: {}'.format(data, rowz, col))
            #print(' mat no is {}'.format(self.dmat))

        elif self.present_tab == 1:
            pass

        elif self.present_tab == 2:
            data = self.table_gender.currentItem()
            rowz = self.table_gender.currentRow()
            col = self.table_gender.currentColumn()
            self.data = data.text()
            dmat = self.table_gender.item(rowz, 4)
            self.dmat = dmat.text()
            #print('{} at row: {} and column: {}'.format(data, rowz, col))
            #print(' mat no is {}'.format(dmat))

            data = data.text()
            print(data)

        else:
            print(' the app is confused')

all_units = [QListWidgetItem('Prayer unit '),QListWidgetItem('Bible Study'), QListWidgetItem('Organising and Decoration Unit'),
             QListWidgetItem('Evangelism Unit'),QListWidgetItem('Counselling and Follow up'),
             QListWidgetItem('Choir Unit'),QListWidgetItem('Transportation Unit'),QListWidgetItem('Drama Unit'),
             QListWidgetItem('Ushering Unit'),QListWidgetItem('Academic Unit'),QListWidgetItem('Technical Unit'),
             QListWidgetItem('Welfare Unit'),QListWidgetItem('Commercial Unit'),QListWidgetItem('Media Department')]
all_units_text = []
for i in all_units:
    i = i.text()
    all_units_text.append(i)
style = """
        QPushButton{ color:white; background-color:steelblue; min-height:30px; min-width:80px; max-width:100px; border-radius:4px;}
        QPushButton:pressed{color:white; background-color:lightseagreen;}
        QPushButton#megabutton{
                        color:white; background-color:steelblue; border-width:1px;
                         border-style: solid; border-radius:8px; border-color:steelblue;
                        padding-left:4px; padding-right:4px;
                        font-size:12px; min-height:80px; min-width: 120px;}
        QPushButton#megabutton:hover{color:white; background-color: grey;  }
        QPushButton:hover{color:white; background-color: grey;  }
        QComboBox {border: 1px solid gray; background-color:lightgrey; border-radius: 4px; padding: 1px 18px 1px 3px; min-width: 25px;}
        QLineEdit {border:1px solid lightgrey; border-radius:4px; padding: 0 8px; min-width:15px; min-height:25px; font-size:11px;}
        QTabWidget::pane { border-top: 2px solid #C2C7CB;}
        QTabWidget::tab-bar {left: 5px;}
        QTableWidget {selection-background-color: lightsteelblue; }
        QListWidget:selected{color:black; background-color:lightsteelblue; selection-background-color:steelblue;}
        
        
        """
#bigsized->setStyleSheet("background-color: yellow");
app = QApplication(sys.argv)
app.setStyleSheet(style)
window = Origin()
window.show()
sys.exit(app.exec_())
