##Icon image from freepik
from sys import argv
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QFileDialog, QApplication, QLineEdit
from PyQt5.QtGui import QIcon
from os import path
from subprocess import call

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(500, 400, 620, 190)
        self.setWindowTitle("making Dyna input files with a minimum timestep")
        self.setWindowIcon(QIcon('pp.ico'))
        isfile = path.isfile('post_directory.1')
        if isfile:
            ddd = open('post_directory.1').readlines()    
            self.lspost_full = ddd[0]
            self.lspost_dir = path.dirname(self.lspost_full)
            self.lspost_fname = path.basename(self.lspost_full)
            self.post_exe = 1
        else:
            self.lspost_full = 'C:\Program Files\LSTC\LS-PrePost 4.6\lsprepost4.6_x64.exe'
            self.lspost_dir = 'C:\Program Files\LSTC\LS-PrePost 4.6'
            self.lspost_fname = 'lsprepost4.6_x64.exe'
            self.post_exe = 0
        self.input = 0
        self.input_dir = ''
        self.input_full = ''
        self.input_fname = ''
        self.input_fname_woext = ''
        self.min_timestep = '0'
        self.new_dt2ms = '-1.000E-07'

        self.label1 = QLabel('minimum timestep:            new dt2ms value: ', self)
        self.label1.move(30, 90)
        self.label1.resize(400, 80)
        self.label2 = QLabel('status: ', self)
        self.label2.move(30, 120)
        self.label2.resize(400, 80)

        btn1 = QPushButton("Input open", self)
        btn1.move(510, 20)
        btn2 = QPushButton("exe Select", self)
        btn2.move(510, 50)
        btn3 = QPushButton("Make inputs", self)
        btn3.move(31, 85)
        btn1.clicked.connect(self.pushButtonClicked)
        btn2.clicked.connect(self.pushButtonClicked2)
        btn3.clicked.connect(self.pushButtonClicked3)
        self.lineEdit1 = QLineEdit('Select a Dyna key file', self)
        self.lineEdit1.move(30, 20)
        self.lineEdit1.resize(470,25)
        self.lineEdit2 = QLineEdit(self.lspost_full, self)
        self.lineEdit2.move(30, 50)
        self.lineEdit2.resize(470,25)
        self.lineEdit2.returnPressed.connect(self.linedEditEntered2)

    def linedEditEntered2(self):
        self.lspost_full = self.lineEdit2.text()
        self.label2.setText('Status: lspost directory entered')
        self.lspost_dir = path.dirname(self.lspost_full)
        self.lspost_fname = path.basename(self.lspost_full)
        f = open('post_directory.1', 'w', encoding='utf-8')
        f.write(self.lspost_full)
        f.close()
        self.post_exe = 1

    def pushButtonClicked(self):
        try:
            file = QFileDialog.getOpenFileName(self, 'Select Dyna input files', filter='Dyna file(*.k *.key *.dyn)')
            self.input_full = file[0]
            self.input_dir = path.dirname(self.input_full)
            self.input_fname = path.basename(self.input_full)
            self.input_fname_woext = self.input_fname.split('.')[0]
            self.lineEdit1.setText(self.input_full)
            self.label2.setText('Status: Dyna input file selected')
            self.input = 1

        except:
            window.show()

    def pushButtonClicked2(self):
        try:
            file = QFileDialog.getOpenFileName(self, 'Select lspost exe', filter='exe file(*.exe)')
            self.lspost_full = file[0]
            self.lspost_dir = path.dirname(self.lspost_full)
            self.lspost_fname = path.basename(self.lspost_full)
            self.lineEdit2.setText(self.lspost_full)
            self.label2.setText('Status: lspost file selected')
            f = open('post_directory.1', 'w', encoding='utf-8')
            f.write(self.lspost_full)
            f.close()
            self.post_exe = 1

        except:
            window.show()

    def pushButtonClicked3(self):
        try:
            self.file_exist_check()
            if self.input == 1 and self.post_exe == 1:
                self.cfile_making()
                self.bat_making()
                self.excute_batch()
                self.get_mintimestep()
                self.get_tssfac()

            else:
                window.show()
        except:
            self.label2.setText('Status: internal process error')
            return

    def file_exist_check(self):
        isfile = path.isfile(self.lspost_full)
        if isfile:
            self.label2.setText('Status: lspost exe file check complete')
            self.post_exe = 1
        else:
            self.label2.setText('Status: lspost exe file Not exist')
            self.post_exe = 0

    def cfile_making(self):
        input_full = self.input_full.replace('/', '\\', 100)
        input_dir = self.input_dir.replace('/', '\\', 100)
        msg = 'open keyword "' + input_full + '"\n' + 'elemcheck shell timestep 1e-06\n' + 'elemcheck shellreport "' + input_dir + '\\timestep_check"' + '\nexit'
        f = open(self.input_dir + '/timestep_check.cfile', 'w', encoding='utf-8')
        f.write(msg)
        f.close()

    def bat_making(self):
        lspost_dir = self.lspost_dir.replace('/', '\\', 100)
        msgg = 'cd /d ' + lspost_dir + '\n' + self.lspost_fname + ' c="' + self.input_dir + '/timestep_check.cfile' + '" -nographics'
        f = open(self.input_dir + '/timestep_check.bat', 'w', encoding='utf-8')
        f.write(msgg)
        f.close()

    def excute_batch(self):
        call(self.input_dir + '/timestep_check.bat')

    def get_mintimestep(self):
        data = open(self.input_dir + '/timestep_check').readlines()
        start = 0

        for i, line in enumerate(data):
            if 'TimeStep' in line:
                start = i

        self.min_timestep = float(data[start][20:35].replace(" ", ""))

    def get_tssfac(self):
        data = open(self.input_full).readlines() 
        start = 0

        for i, line in enumerate(data):
            line = line.lower()
            if '*control_timestep' in line:
                start = i
                break
        while '$' in data[start+1]:
            start += 1
        start += 1
        tssfac = float(data[start][10:20].replace(" ", ""))
        old_dt2ms = (data[start][40:50])
        self.new_dt2ms = format(self.min_timestep/tssfac*-1, '.3E')

        fw = open(self.input_dir + '/' + self.input_fname_woext + '_1.k', 'w')
        for line in data:
            fw.write(line.replace(old_dt2ms, self.new_dt2ms))
        fw.close()
        self.label1.setText('minimum timestep: ' + str(self.min_timestep) + ' new dt2ms value: ' + self.new_dt2ms)
        self.label2.setText('Status: Dyna input created')

if __name__ == "__main__":
    app = QApplication(argv)
    window = MyWindow()
    window.show()
    app.exec_()
