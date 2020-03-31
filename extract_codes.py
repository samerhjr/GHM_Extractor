from sys import argv, exit
from pandas import DataFrame, read_csv 
from re import search, match
from os import path
from subprocess import check_output
from datetime import datetime
from PyQt5 import  QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt, QRect, QMetaObject, QCoreApplication
from threading import Thread

class Ui_MainWindow(QtWidgets.QMainWindow):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Extractor of French Medical Codes")
        MainWindow.resize(758, 270)
        MainWindow.setWindowTitle("Extractor of French Medical Codes")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QRect(610, 10, 131, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openfile)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QRect(610, 70, 131, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.multithread)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QRect(30, 10, 551, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QRect(30, 70, 551, 31))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar1 = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar1.setGeometry(QRect(30, 130, 551, 31))
        self.progressBar1.setProperty("value", 0)
        self.progressBar1.setObjectName("progressBar")
        self.progressBar1.setAlignment(Qt.AlignCenter)
        self.progressBar2 = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar2.setGeometry(QRect(30, 190, 551, 31))
        self.progressBar2.setProperty("value", 0)
        self.progressBar2.setObjectName("progressBar")
        self.progressBar2.setAlignment(Qt.AlignCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 758, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Extractor of French Medical Codes"))
        self.pushButton.setText(_translate("MainWindow", "choose pdf file"))
        self.pushButton_2.setText(_translate("MainWindow", "Extract"))

    def openfile(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Choose Volume 2", "",
                                                      "PDF Files (*.pdf)", options=options)
        if fileName:
            self.lineEdit.setText(fileName)
            self.lineEdit.setDisabled(True)

    def diagnotcis_extract(self):
        df2 = DataFrame()
        j = 0
        i = 0
        t = None
        l = 0
        categ = ""
        categn = ""
        df = read_csv(path.dirname(path.realpath(__file__)) + "\\cmds.txt", sep="\n", header=None)
        while i < df.shape[0] - 4:
            i += 1
            if match("CATÉGORIE MAJEURE", df.loc[i, 0]):
                t = None
                self.progressBar.setValue( round(((i + 1) / df.shape[0])*100))
                self.progressBar.setFormat("extracting List of Diagnostics... " + str(self.progressBar.value()) + "%")
                categ = df.loc[i, 0]
                categn = df.loc[i + 1, 0]
                list = ""

            str1 = df.loc[i, 0]
            liste = match("Liste D-+[0-9]{3}", str1)
            if liste:
                t = True
                list = df.loc[i, 0]
                listarray = list.split()
                listcode = listarray[1]

            if t == True:
                m = match("[A-Z]{1,}[0-9]{2}", str1)
                d = df.loc[i + 2, 0]
                v = match("[A-Z]{1,}[0-9]{2}", d)
                cklist = match("Liste D-+[0-9]{3}", d)
                ckcat = match("Catégorie majeure", d)
                ckman = match("Manuel", d)
                if m:
                    if v or cklist or ckcat or ckman:
                        df2.loc[j, 0] = categ
                        df2.loc[j, 1] = categn
                        df2.loc[j, 3] = list
                        df2.loc[j, 2] = listcode
                        df2.loc[j, 4] = df.loc[i, 0]
                        df2.loc[j, 5] = df.loc[i + 1, 0]
                        j += 1
                    else:
                        df2.loc[j, 0] = categ
                        df2.loc[j, 1] = categn
                        df2.loc[j, 3] = list
                        df2.loc[j, 2] = listcode
                        df2.loc[j, 4] = df.loc[i, 0]
                        df2.loc[j, 5] = df.loc[i + 1, 0] + " " + df.loc[i + 2, 0]
                        j += 1
        now = datetime.now()
        df2.to_excel("Diagnostics_list" + now.strftime("%m_%d_%Y_%H_%M_%S") + ".xlsx")
        return None

    def acts_extract(self):
        l_a = DataFrame()
        df2 = DataFrame()
        j = 0
        i = 0
        t = None
        l = 0
        categ = ""
        categn = ""
        df = read_csv(path.dirname(path.realpath(__file__))+"\\cmds.txt", sep="\n", header = None)
        while i < df.shape[0] -4:
            i += 1

            if match("CATÉGORIE MAJEURE", df.loc[i,0]):
                t = None
                self.progressBar1.setValue(round(((i + 1) / df.shape[0]) * 100))
                self.progressBar1.setFormat("extracting List of Acts... " + str(self.progressBar1.value()) + "%")
                list = ""
                categ = df.loc[i,0]
                categn = df.loc[i+1,0]


            str1 = df.loc[i , 0]
            liste = match("Liste A-+[0-9]{3}",str1)
            if liste:
                t = True
                list = df.loc[i,0]
                listarray = list.split()
                listcode = listarray[1]

            if t == True:
                m = match("[A-Z]{4,}[0-9]{3,}", str1)
                if i >= df.shape[0] - 3 :
                    break
                d = df.loc[i+3 , 0]
                v1 = match("[A-Z]{4,}[0-9]{3,}", d)
                cklist = match("Liste A-+[0-9]{3}", d)
                ckcat  = match("Catégorie majeure", d)
                ckman  = match("Manuel", d)
                d2 = df.loc[i+2 , 0]
                v12 = match("[A-Z]{4,}[0-9]{3,}", d2)
                cklist2 = match("Liste A-+[0-9]{3}", d2)
                ckcat2  = match("Catégorie majeure", d2)
                ckman2  = match("Manuel", d2)
                if m:
                    s = search("/0", str1)
                    if s:

                        if v12 or cklist2 or ckcat2 or ckman2:
                            l_a.loc[j, 0] =  categ
                            l_a.loc[j, 1] = categn
                            l_a.loc[j, 2] =  listcode
                            l_a.loc[j, 3] = list
                            code = df.loc[i,0]
                            l_a.loc[j, 4] = code[0:7]
                            l_a.loc[j, 5] = df.loc[i+1,0]
                            j += 1
                        else:
                            l_a.loc[j, 0] =  categ
                            l_a.loc[j, 1] = categn
                            l_a.loc[j, 2] = listcode
                            l_a.loc[j, 3] = list
                            code = df.loc[i,0]
                            l_a.loc[j, 4] = code[0:7]
                            l_a.loc[j, 5] = df.loc[i+1,0]+ " "+ df.loc[i+2,0]
                            j += 1
                    else:

                        if v1 or cklist or ckcat or ckman:
                            l_a.loc[j, 0] =  categ
                            l_a.loc[j, 1] = categn
                            l_a.loc[j, 2] =  listcode
                            l_a.loc[j, 3] = list
                            l_a.loc[j, 4] = df.loc[i,0]
                            l_a.loc[j, 5] = df.loc[i+2,0]
                            j += 1
                        else:
                            l_a.loc[j, 0] =  categ
                            l_a.loc[j, 1] = categn
                            l_a.loc[j, 2] = listcode
                            l_a.loc[j, 3] = list
                            l_a.loc[j, 4] = df.loc[i,0]
                            l_a.loc[j, 5] = df.loc[i+2,0]+ " "+ df.loc[i+3,0]
                            j += 1

        now = datetime.now()
        l_a.to_excel("list_of_acts"+ now.strftime("%m_%d_%Y_%H_%M_%S") +".xlsx")
        return None
    def extract_ghm(self):
        l_ghm = DataFrame()
        ghmdesc = ""
        ghmcode = ""
        j = 0
        i = 0

        df = read_csv(path.dirname(path.realpath(__file__))+"\\cmds.txt", sep="\n", header = None)
        while i < df.shape[0] -4:
            i += 1
            if match("CATÉGORIE MAJEURE", df.loc[i,0]):
                t = None
                self.progressBar2.setValue(round(((i + 1) / df.shape[0]) * 100))
                self.progressBar2.setFormat("extracting GHMs... " + str(self.progressBar2.value())+"%")
                categ = df.loc[i,0]
                categn = df.loc[i+1,0]
            str1 = df.loc[i , 0]
            ghmlist = match("[0-9]{2,}[A-Z]{1,}[0-9]{2,} ",str1)
            ghmlower1 = match("[0-9]{2,}[A-Z]{1,}[0-9]{3,}",str1)
            ghmlower2 = match("[0-9]{2,}[A-Z]{1,}[0-9]{2,}[A-Z]{1,}",str1)
            if ghmlist and not ghmlower1 and not ghmlower2 :
                l_ghm.loc[j, 0] = str1[0:5]
                if not match("[0-9]{2,}[A-Z]{1,}[0-9]{3,}", str(df.loc[i +1 , 0])) and\
                   not match("[0-9]{2,}[A-Z]{1,}[0-9]{2,}[A-Z]{1,}", str(df.loc[i + 1 , 0])) and\
                   not match("[*]",str(df.loc[i + 1 , 0])) and\
                   not match("Voir",str(df.loc[i + 1 , 0])):
                           l_ghm.loc[j, 1] = str1[5:] + " "+df.loc[i + 1, 0]
                           ghmdesc = str1[5:] + " "+df.loc[i + 1, 0]

                else:
                    l_ghm.loc[j, 1] = str1[5:]
                    ghmdesc = str1[5:]
                ghmcode = str1[0:5]
            if ghmlower1 or ghmlower2 :
                l_ghm.loc[j, 2] = str1[0:6]
                if not match("[0-9]{2,}[A-Z]{1,}[0-9]{3,}", str(df.loc[i + 1 , 0])) and\
                   not match("[0-9]{2,}[A-Z]{1,}[0-9]{2,}[A-Z]{1,}", str(df.loc[i + 1 , 0])) and\
                   not match("Voir", str(df.loc[i + 1 , 0])) and\
                   not match("[*]",str(df.loc[i + 1 , 0])):
                        l_ghm.loc[j, 3] = str1[7:]  + " " + df.loc[i + 1, 0]
                        l_ghm.loc[j, 0] = ghmcode
                        l_ghm.loc[j, 1] = ghmdesc
                        j+=1
                else:

                        l_ghm.loc[j, 3] = str1[7:]
                        l_ghm.loc[j, 0] = ghmcode
                        l_ghm.loc[j, 1] = ghmdesc
                        j+=1
        now = datetime.now()
        l_ghm.to_excel("list_GHMs"+ now.strftime("%m_%d_%Y_%H_%M_%S") +".xlsx")
        return None
    def java_line(self, str):
        check_output("java -jar extract_cmds.jar \""+str+"\"", shell=True)

    @pyqtSlot()
    def multithread(self):
        self.pushButton_2.setDisabled(True)
        start = Thread(target=self.extract_code)
        start.start()


    def extract_code(self):

        pdf = Thread(target=self.java_line, args= (str(self.lineEdit.text()),))
        pdf.start()
        pdf.join()
        ghms = Thread(target=self.extract_ghm)
        ghms.start()
        ghms.join()
        acts = Thread(target= self.acts_extract)
        acts.start()
        diag = Thread(target=self.diagnotcis_extract)
        diag.start()
        diag.join()
        self.pushButton_2.setDisabled(False)

if __name__ == "__main__":

    app = QtWidgets.QApplication(argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    exit(app.exec_())