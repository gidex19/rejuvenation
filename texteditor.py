
import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qrc_rec import *
__version__="1.0.0"

class TextEditor(QMainWindow):
    def __init__(self,parent=None):
        super(TextEditor,self).__init__(parent)
        #settings = QSettings()
        #size = settings.value("TextEditor/Size",QVariant(QSize(600, 500))).toSize()
        #self.resize(size)
        self.UIinit()
        #self.setGeometry(140, 140, 1020, 600)
    def UIinit(self):
        #GUI initialiser
        self.dirty=False
        self.filename=None
        self.answered=False
        self.qwidget=QWidget()
        self.textedit=QTextEdit()
        #self.textedit.setFont(QFont('Arial',12))
        self.textedit.textChanged.connect(self.typed)
        self.textedit.isWindowModified()

        self.vbox=QVBoxLayout()
        self.hbox=QHBoxLayout()
        self.save_btn=QPushButton('Save')
        self.open_btn=QPushButton('Open')
        self.clear_btn=QPushButton('Clear')
        self.hbox.addWidget(self.open_btn)
        self.hbox.addWidget(self.save_btn)
        self.hbox.addWidget(self.clear_btn)
        self.vbox.addWidget(self.textedit)
        self.status=QStatusBar()
        self.status.showMessage('information and tip display')
        self.vbox.addWidget(self.status)

        #self.vbox.addLayout(self.hbox)
        self.qwidget.setLayout(self.vbox)
        self.setCentralWidget(self.qwidget)
        self.setGeometry(140,140,1020,600)
        self.setWindowTitle("Untitled-Geepad")
        self.setWindowIcon(QIcon(':/creep-003.png'))
        #creating and adding menu to the editor
        menu=self.menuBar()

        file=menu.addMenu('&File')
        edit=menu.addMenu('&Edit')
        view=menu.addMenu('&View')
        settings=menu.addMenu('Settings')
        help=menu.addMenu('&Help')
        #creating and adding actions for file menu
        open=QAction('&Open',self)
        open.setIcon(QIcon(':/OK.png'))
        save=QAction('Save',self)
        save.setIcon(QIcon(':/Save.png'))

        #creating and adding actions to the logout
        toolbar=self.addToolBar('file')
        new_bar=QAction(QIcon(':/Text.png'),'New',self)
        new_bar.setShortcut('Ctrl+N')
        open_bar=QAction(QIcon(':/OK.png'),'Open file',self)
        save_bar=QAction(QIcon(':/Save.png'),'Save file',self)
        exit=QAction('Exit',self)
        exit.setIcon(QIcon(':/Close.png'))
        settings_bar=QAction(QIcon(':/Settings.png'),'Settings',self)
        settings_bar.setShortcut("Ctrl+Alt+S")
        #calc_bar=QAction(QIcon('icons/Calculator.png'),'Calculator',self)
        help_bar=QAction(QIcon(':/helpbook.png'),'Help ',self)
        About_bar=QAction(QIcon(':/creep-002.png'),'About Us',self)
        print_bar=self.create_action('Print',self.print_action,'Ctrl+P',':/Print.png','Print text file')

        toolbar.addAction(new_bar)
        toolbar.addAction(open_bar)
        toolbar.addAction(save_bar)
        toolbar.addAction(print_bar)
        toolbar.addAction(settings_bar)
        toolbar.addAction(help_bar)
        toolbar.addAction(About_bar)
        toolbar.addAction(exit)
        #connectcing the toolbar signal to a chosen slot
        toolbar.actionTriggered.connect(self.tb_triggered)

        #Adding slots to the button signals
        self.save_btn.clicked.connect(self.save_action)
        self.open_btn.clicked.connect(self.open_action)
        self.clear_btn.clicked.connect(self.clear_action)

        file.addAction(new_bar)
        file.addAction(save)
        file.addAction(open)
        file.addAction(print_bar)
        file.addAction(exit)
        exit.setShortcut("Ctrl+q")
        new_bar.triggered.connect(self.new_action)
        exit.triggered.connect(self.exit)
        open.triggered.connect(self.open_action)
        save.triggered.connect(self.save_action)
        open.setShortcut("Ctrl+O")
        save.setShortcut("Ctrl+s")

        full=QAction('Fullscreen mode',self)
        mini=QAction('Minimise',self)
        full.setIcon(QIcon(':/fullscreen.png'))
        mini.setIcon(QIcon(':/Remove.png'))
        font_settings=QAction('Font Settings',self)
        font_settings.setIcon(QIcon(':/Font.png'))
        theme_settings=QAction('Theme Settings',self)
        theme_settings.setIcon(QIcon(':/Theme.png'))
        font_settings.triggered.connect(self.my_font)
        theme_settings.triggered.connect(self.theme)
        settings.addAction(font_settings)
        settings.addAction(theme_settings)
        full.triggered.connect(self.fullscreen)
        mini.triggered.connect(self.minimize)
        view.addAction(full)
        view.addAction(mini)


        #adding both buttons to the hbox layout

        #creating my custom functions..oh yeah
        copy_bar=self.create_action('Copy',self.copy_action,'Ctrl+C',':/Copy.png','Copy text data')
        cut_bar=self.create_action('Cut',self.cut_action,'Ctrl+x',':/Cut.png','cut text data')
        paste_bar=self.create_action('Paste',self.paste_action,'Ctrl+V',':/Paste.png','paste text data')
        undo_bar=self.create_action('Undo',self.undo_action,'Ctrl+Z',':/Undo.png','undo recent actions')
        redo_bar=self.create_action('Redo',self.redo_action,'Ctrl+R',':/Redo.png','redo action')
        find_bar=self.create_action('Find',self.find_dlg,'Ctrl+F',':/Find.png','find in document')

        edit.addAction(copy_bar)
        edit.addAction(cut_bar)
        edit.addAction(paste_bar)
        edit.addAction(undo_bar)
        edit.addAction(redo_bar)
        edit.addAction(find_bar)

    def find_action(self):
        print(self.find_word)
        self.con=self.textedit.toPlainText()
        cursor=self.textedit.textCursor()
        #content=self.con
        format=QTextCharFormat()
        format.setBackground(QBrush(QColor('red')))
        pattern=self.find_word
        regex= QRegExp(pattern)
        pos=0
        index= regex.indexIn(self.textedit.toPlainText(),pos)
        while(index != -1):
            cursor.setPosition(index)
            cursor.movePosition(QTextCursor.EndOfWord,1)
            cursor.mergeCharFormat(format)
            pos= index + regex.matchedLength()
            index=regex.indexIn(self.textedit.toPlainText(),pos)


    def find_dlg(self):
        self.f_dlg=QDialog()
        formlayout=QFormLayout()
        self.line=QLineEdit()
        self.line.textChanged.connect(self.line_action)
        hbox=QHBoxLayout()
        vbox=QVBoxLayout(self.f_dlg)
        self.btn_find=QPushButton('Find Next')
        self.btn_find.setEnabled(False)

        btn2=QPushButton('Cancel')
        self.btn_find.clicked.connect(self.find_triggered)
        btn2.clicked.connect(self.find_triggered)
        formlayout.addRow('Find this text',self.line)
        hbox.addWidget(self.btn_find)
        hbox.addWidget(btn2)
        vbox.addLayout(formlayout)
        vbox.addLayout(hbox)
        self.f_dlg.setWindowTitle('Find Text')
        self.f_dlg.setFixedWidth(300)
        self.f_dlg.setFixedHeight(100)
        print('this is the linedit value')
        self.f_dlg.exec_()
    def line_action(self):
        if self.line.text() =='':
            self.btn_find.setEnabled(False)
        else:
            self.btn_find.setEnabled(True)

    def find_triggered(self):
        sender=self.sender()
        self.find_word=self.line.text()
        btn_text=sender.text()
        if btn_text=='Find Next':
            self.find_action()
        elif btn_text=='Cancel':
            self.f_dlg.close()

    def undo_action(self):
        self.textedit.undo()

    def redo_action(self):
        self.textedit.redo()

    def typed(self):
        self.dirty=True

    def new_set(self):
        self.dirty = False
        self.filename = None
        self.setWindowTitle("Untitled-Geepad")
        self.textedit.clear()
        self.dirty=False

    def new_action(self):
        if self.filename is None and self.dirty == False:
            self.new_set()
        elif self.filename is None and self.dirty == True:
            self.confirm_new()
            self.new_dlg.close()
            self.answered=True
        elif self.filename is not None and self.dirty == False:
            self.new_set()
        elif self.filename is not None and self.dirty == True:
            self.answered=True
            self.confirm_new()

    def new_dlg_btn(self):
        sender = self.sender()
        content = sender.text()
        if content == 'Save':
            if self.answered == False:
                self.save_action()

                self.new_dlg.close()
                self.new_set()
            else:
                #save automatically without displaying box
                print('save auto without box')
                self.answered = False
        if content == 'Don\'t Save':
            self.new_set()
            self.new_dlg.close()
        if content == 'Cancel':
            self.new_dlg.close()
    def confirm_new(self):

        self.new_dlg = QDialog()
        vcont = QVBoxLayout(self.new_dlg)
        lbl = QLabel('Do you want to save unsaved changes to this file before opening a new file?')
        vcont.addWidget(lbl)
        hcont = QHBoxLayout()
        btn1 = QPushButton("Save")
        btn1.clicked.connect(self.new_dlg_btn)
        btn2 = QPushButton("Don't Save")
        btn2.clicked.connect(self.new_dlg_btn)
        btn3 = QPushButton("Cancel")
        btn3.clicked.connect(self.new_dlg_btn)
        hcont.addWidget(btn1)
        hcont.addWidget(btn2)
        hcont.addWidget(btn3)
        vcont.addLayout(hcont)
        self.new_dlg.setWindowTitle('New Sheet')
        self.new_dlg.setFixedWidth(400)
        self.new_dlg.setFixedHeight(110)
        self.new_dlg.exec_()

    def save_action(self):

        if self.filename is None and self.dirty == False:
            #no new file opened amd no new text typed
            print('No changes made already')
        if self.filename is None and self.dirty == True:
            #no file opened and new text typed
            self.save_as_action()
            self.fname = os.path.basename(self.dfile)
            self.filename = self.fname
            self.setWindowTitle("%s-Geepad" % self.fname)
        if self.filename is not None and self.dirty == False:
            #already existing file has been opened and no new text typed(un-edited)
            print('no changes made to this already existing file')
        if self.filename is not None and self.dirty == True:
            #already existing file has been opened and new text typed(edited)
            #just save without the save box been displayed
            self.save_existing()

    def save_as_action(self):
        self.dfile = QFileDialog.getSaveFileName(self, 'Save File As', 'C:\\', 'text files(*.txt)')
        with open(self.dfile, 'w') as f:
            content = self.textedit.toPlainText()
            f.write(content)
            self.dirty=False

    def save_existing(self):
        with open(self.dfile, 'w') as f:
            content=self.textedit.toPlainText()
            f.write(content)

    def open_action(self):
        if self.filename is None and self.dirty==False:

            self.dfile = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('C:'), 'text files(*.txt)')
            with open(self.dfile,'r') as f:
                self.content=f.read()
                self.textedit.setText(self.content)
                self.path,self.fname=os.path.split(self.dfile)
                print('self.path:{}'.format(self.path))
                print('self.fname: {}'.format(self.fname))
                self.setWindowTitle("%s-Geepad"%self.fname)
                self.filename=self.fname
                self.dirty=False
        elif self.filename is None and self.dirty==True:
            self.confirm_open()
        elif self.filename is not None and self.dirty==False:
            print('exists and nt edited')
            self.dfile = QFileDialog.getOpenFileName(self, 'Open File', 'C:\\', 'text files(*.txt)')
            with open(self.dfile, 'r') as f:
                self.content = f.read()
                self.textedit.setText(self.content)
                self.fname = os.path.basename(self.dfile)
                self.setWindowTitle("%s-Geepad" % self.fname)
                self.setWindowModified(True)
                self.filename = self.fname
                self.dirty=False
        elif self.filename is not None and self.dirty==True:
            print('exists and edited')
            self.answered=True
            self.confirm_open()
            self.answered=False

    def open_2(self):
        self.dfile = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('C:'), 'text files(*.txt)')
        with open(self.dfile, 'r') as f:
            self.content = f.read()
            self.textedit.setText(self.content)
            self.path, self.fname = os.path.split(self.dfile)
            self.dirty=False
    def confirm_open(self):
        self.open_dlg = QDialog()
        vcont = QVBoxLayout(self.open_dlg)
        lbl = QLabel('Do you want to save unsaved changes to this file before opening a New File?')
        vcont.addWidget(lbl)
        hcont = QHBoxLayout()
        btn_save = QPushButton("Save")
        btn_save.clicked.connect(self.open_btn_triggered)
        btn_dsave = QPushButton("Don't Save")
        btn_dsave.clicked.connect(self.open_btn_triggered)
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.open_btn_triggered)
        hcont.addWidget(btn_save)
        hcont.addWidget(btn_dsave)
        hcont.addWidget(btn_cancel)
        vcont.addLayout(hcont)
        self.open_dlg.setWindowTitle('Save Present file')
        self.open_dlg.setWindowIcon(QIcon('icons/creep-003.png'))
        self.open_dlg.setFixedWidth(400)
        self.open_dlg.setFixedHeight(110)

        self.open_dlg.exec_()
    def open_btn_triggered(self):
        sender=self.sender()
        content=sender.text()
        if content=='Save':
            if self.answered==True:
                self.save_existing()
                self.open_dlg.close()
                self.open_2()
            else:
                self.save_action()
                self.open_2()
        if content=='Don\'t Save':
            self.open_2()
            self.open_dlg.close()
        if content=='Cancel':
            self.open_dlg.close()

    def dlg_exit(self):
        self.exit_dlg.close()
    def btn_triggered(self):
        sender=self.sender()
        content=sender.text()
        if content=='Save':
            self.save_action()
            self.exit_dlg.close()
            qApp.quit()
        if content=='Don\'t Save':
            qApp.quit()
        if content=='Cancel':
            self.exit_dlg.close()
    def exit(self):

        if self.dirty == False:
            qApp.quit()
        if self.dirty == True:
            self.confirm_exit()
    def confirm_exit(self):
        self.exit_dlg=QDialog()
        vcont=QVBoxLayout(self.exit_dlg)
        lbl=QLabel('Do you want to save unsaved changes to this file?')
        vcont.addWidget(lbl)
        hcont=QHBoxLayout()
        btn1=QPushButton("Save")
        btn1.clicked.connect(self.btn_triggered)
        btn2=QPushButton("Don't Save")
        btn2.clicked.connect(self.btn_triggered)
        btn3=QPushButton("Cancel")
        btn3.clicked.connect(self.btn_triggered)
        hcont.addWidget(btn1)
        hcont.addWidget(btn2)
        hcont.addWidget(btn3)
        vcont.addLayout(hcont)
        self.exit_dlg.setWindowTitle('Exit Geepad')
        self.exit_dlg.setFixedWidth(300)
        self.exit_dlg.setFixedHeight(110)

        self.exit_dlg.exec_()
    def theme(self):
        theme_dlg=QDialog()
        lb=QLabel('Select your desired Theme')
        vb=QVBoxLayout(theme_dlg)
        hb=QHBoxLayout()
        apply_btn=QPushButton('Apply')
        close_btn=QPushButton('Close')
        rad=QRadioButton('Green Theme',theme_dlg)
        rad2=QRadioButton('Night Theme',theme_dlg)
        vb.addWidget(lb)
        vb.addWidget(rad)
        vb.addWidget((rad2))
        hb.addWidget(apply_btn)
        hb.addWidget(close_btn)
        vb.addLayout(hb)
        def change_theme():

            if rad2.isChecked():
                app.setStyleSheet(night)
            else:
                app.setStyleSheet(green)
        def close_dlg():
            theme_dlg.close()
        apply_btn.clicked.connect(change_theme)
        close_btn.clicked.connect(close_dlg)
        theme_dlg.setWindowTitle('Theme Selection')
        theme_dlg.setGeometry(200,200,240,120)
        theme_dlg.exec_()

    def create_action(self,text,slot=None,shortcut=None,icon=None,tip=None):
        action=QAction(text,self)
        if slot is not None:
            action.triggered.connect(slot)
        if shortcut is not None:
            action.setShortcut(shortcut)
        if icon is not None:
            action.setIcon(QIcon(icon))
        if tip is not None:
            action.setToolTip(tip)
        return action

    def copy_action(self):
        self.textedit.copy()
    def cut_action(self):
        self.textedit.cut()
    def paste_action(self):
        self.textedit.paste()
    def print_action(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.textedit.print(printer)

    def tb_triggered(self,a):
        content=a.text()
        if content == 'New file':
            self.new_action()
        if content == 'Open file':
            self.open_action()
        if content == 'Save file':
            self.save_action()
        if content == 'Calculator':
            self.calc()
        if content == 'Settings':
            self.font()
        if content == 'About Us':
            self.About_action()
        else:
            pass
    def About_action(self):
        my_about=QMessageBox.information(self,'About Geepad',
                                'Geepad is a high profile notepad for text-editing\n'
                                ' Built by Geedtech Softwares\n'
                                '   Geepad version 2.2.3\n'
                                '       2009\n')

    def fullscreen(self):
        self.showFullScreen()

    def minimize(self):
        self.setGeometry(140,140,700,600)

    def clear_action(self):
        self.textedit.clear()

    def my_font(self):
        font,ok = QFontDialog.getFont()
        if ok:
            self.textedit.setFont(font)

green = """   QMenuBar::item{
                            background-color: transparent;}
            QMenuBar::item:selected{
                            background-color:limegreen; color:white;}
            
            QMenu::item{
                        padding: 2px 28px 2px 24px;}
            QMenu::item{
                        padding: 2px 28px 4px 30px;}
            QMenu::item:selected{
                            background-color:limegreen; color:white;}
            QToolBar::item{
                            background-color:red; color:white; margin:14px;} 
            QPushButton{
                        color:white; background-color:limegreen; border-width:1px;
                         border-style: solid; border-radius:3px; border-color:limegreen;
                        padding-left:4px; padding-right:4px;
                        font-size:12px;}           
            QPushButton:pressed{color:white; background-color:lightseagreen;}
            QTextEdit{ background-color:white; color:black;}
            QDialog{background-color:lightgrey; font-size:12px;}
        """

night = """
            QMainWindow{background-color:Dimgray;}
            QMenuBar::item{
                            background-color: dimgray;}
            QMenuBar::item:selected{
                            background-color:steelblue; color:white;}

            QMenu::item{
                        padding: 2px 28px 2px 24px;}
            QMenu::item{
                        padding: 2px 28px 4px 30px;}
            QMenu::item:selected{
                            background-color:steelblue; color:white;}
            QToolBar::item{
                            background-color:red; color:white; margin:14px;} 
            QPushButton{
                        color:white; background-color:steelblue; border-width:1px;
                         border-style: solid; border-radius:3px; border-color:steelblue;
                        padding-left:4px; padding-right:4px;
                        font-size:12px;}           
            QPushButton:pressed{color:white; background-color:skyblue;}
            QTextEdit{ background-color:black; color:white;}
            QDialog{background-color:lightgrey; font-size:12px;}
        """

app=QApplication(sys.argv)
app.setStyleSheet(green)
app.setApplicationName('Geepad')
app.setWindowIcon(QIcon(':/creep-003.png'))
screen=TextEditor()
screen.show()
app.exec_()
