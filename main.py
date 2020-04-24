#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import gui
from tcpgecko import TCPGecko
import sys
from binascii import hexlify

TID_EUR = 0x0005000010176a00
TID_USA = 0x0005000010176900
TID_JAP = 0x0005000010162b00

class MyWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = gui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_3.clicked.connect(self.connection)
        self.ui.pushButton_2.clicked.connect(self.disconnection)
        self.ui.pushButton_6.clicked.connect(self.getStats)
        self.ui.pushButton_5.clicked.connect(self.applyStats)

    def getStats(self):
        try:
            # Level
            self.ui.spinBox.setValue(self.gecko.readkern(0x12CDC1A8) + 1)
            # XP
            self.ui.spinBox_2.setValue(self.gecko.readkern(0x12CDC1A4))
            # Rank
            rank = self.gecko.readkern(0x12CDC1AC)
            if rank == 0:
                self.ui.comboBox.setCurrentIndex(0)
            elif rank == 1:
                self.ui.comboBox.setCurrentIndex(1)
            elif rank == 2:
                self.ui.comboBox.setCurrentIndex(2)
            elif rank == 3:
                self.ui.comboBox.setCurrentIndex(3)
            elif rank == 4:
                self.ui.comboBox.setCurrentIndex(4)
            elif rank == 5:
                self.ui.comboBox.setCurrentIndex(5)
            elif rank == 6:
                self.ui.comboBox.setCurrentIndex(6)
            elif rank == 7:
                self.ui.comboBox.setCurrentIndex(7)
            elif rank == 8:
                self.ui.comboBox.setCurrentIndex(8)
            elif rank == 9:
                self.ui.comboBox.setCurrentIndex(9)
            elif rank == 10:
                self.ui.comboBox.setCurrentIndex(10)
            # Rank Points
            self.ui.spinBox_3.setValue(self.gecko.readkern(0x12CDC1B0))
            # Gold
            self.ui.spinBox_4.setValue(self.gecko.readkern(0x12CDC1A0))
            # Sea Snails
            self.ui.spinBox_5.setValue(self.gecko.readkern(0x12CDC1B4))
            # Gender
            gender = self.gecko.readkern(0x12CD1D90)
            if gender == 0:
                self.ui.comboBox_2.setCurrentIndex(0)
            elif gender == 1:
                self.ui.comboBox_2.setCurrentIndex(1)
            elif gender == 2:
                self.ui.comboBox_2.setCurrentIndex(2)
            # Eyes
            eyes = self.gecko.readkern(0x12CD1D98)
            if eyes == 0:
                self.ui.comboBox_3.setCurrentIndex(0)
            elif eyes == 1:
                self.ui.comboBox_3.setCurrentIndex(1)
            elif eyes == 2:
                self.ui.comboBox_3.setCurrentIndex(2)
            elif eyes == 3:
                self.ui.comboBox_3.setCurrentIndex(3)
            elif eyes == 4:
                self.ui.comboBox_3.setCurrentIndex(4)
            elif eyes == 5:
                self.ui.comboBox_3.setCurrentIndex(5)
            elif eyes == 6:
                self.ui.comboBox_3.setCurrentIndex(6)
            # Skin
            skin = self.gecko.readkern(0x12CD1D94)
            if skin == 0:
                self.ui.comboBox_4.setCurrentIndex(0)
            elif skin == 1:
                self.ui.comboBox_4.setCurrentIndex(1)
            elif skin == 2:
                self.ui.comboBox_4.setCurrentIndex(2)
            elif skin == 3:
                self.ui.comboBox_4.setCurrentIndex(3)
            elif skin == 4:
                self.ui.comboBox_4.setCurrentIndex(4)
            elif skin == 5:
                self.ui.comboBox_4.setCurrentIndex(5)
            elif skin == 6:
                self.ui.comboBox_4.setCurrentIndex(6)
            self.ui.comboBox.setEnabled(True)
            self.ui.comboBox_2.setEnabled(True)
            self.ui.comboBox_3.setEnabled(True)
            self.ui.comboBox_4.setEnabled(True)
            self.ui.spinBox.setEnabled(True)
            self.ui.spinBox_2.setEnabled(True)
            self.ui.spinBox_3.setEnabled(True)
            self.ui.spinBox_4.setEnabled(True)
            self.ui.spinBox_5.setEnabled(True)
            self.ui.pushButton_5.setEnabled(True)
            QMessageBox.information(self, 'SplatStats', "The statistics have been updated!")
        except:
            QMessageBox.critical(self, 'SplatStats', "Reading console data failed!")

    def disconnection(self):
        try:
            self.gecko.s.close()
            self.ui.lineEdit.setEnabled(True)
            self.ui.pushButton_3.setEnabled(True)
            self.ui.pushButton_2.setEnabled(False)
            self.ui.pushButton_5.setEnabled(False)
            self.ui.pushButton_6.setEnabled(False)
            self.ui.comboBox.setEnabled(False)
            self.ui.comboBox_2.setEnabled(False)
            self.ui.comboBox_3.setEnabled(False)
            self.ui.comboBox_4.setEnabled(False)
            self.ui.spinBox.setEnabled(False)
            self.ui.spinBox_2.setEnabled(False)
            self.ui.spinBox_3.setEnabled(False)
            self.ui.spinBox_4.setEnabled(False)
            self.ui.spinBox_5.setEnabled(False)
            QMessageBox.information(self, 'SplatStats', "Disconnection of the console was successful!")
        except:
            QMessageBox.critical(self, 'SplatStats', "An error occurred when disconnecting the console!")

    def connection(self):
        try:
            ip = self.ui.lineEdit.text()
            self.gecko = TCPGecko(ip)
        except:
            QMessageBox.critical(self, 'SplatStats', "The connection to the console failed!")
            return
        
        firmVer = self.gecko.getversion()
        if firmVer == 550:
            loc = 0x10013C10
        elif firmVer < 550 and firmVer >= 532:
            loc = 0x100136D0
        elif firmVer < 532 and firmVer >= 500:
            loc = 0x10013010
        elif firmVer == 410:
            loc = 0x1000ECB0
        else:
            QMessageBox.critical(self, 'SplatStats', "The version of your wiiu is not compatible with the software. Please update it!")
            return
        
        titleID = int(hexlify(self.gecko.readmem(loc, 8)), 16)
        if titleID == TID_EUR or titleID == TID_USA or titleID == TID_JAP:
            self.ui.lineEdit.setEnabled(False)
            self.ui.pushButton_3.setEnabled(False)
            self.ui.pushButton_2.setEnabled(True)
            self.ui.pushButton_6.setEnabled(True)
            QMessageBox.information(self, 'SplatStats', "The connection to " + ip + " was successful!")
        else:
            self.gecko.s.close()
            QMessageBox.critical(self, 'SplatStats', "The connection to the console was successful, but was cut because Splatoon was not launched!")
            
    def applyStats(self):
        try:
            # Level
            self.gecko.pokemem(0x12CDC1A8, self.ui.spinBox.value() - 1)
            # XP
            self.gecko.pokemem(0x12CDC1A4, self.ui.spinBox_2.value())
            # Rank
            self.gecko.pokemem(0x12CDC1AC, self.ui.comboBox.currentIndex())
            # Rank Points
            self.gecko.pokemem(0x12CDC1B0, self.ui.spinBox_3.value())
            # Money
            self.gecko.pokemem(0x12CDC1A0, self.ui.spinBox_4.value())
            # Sea Snails
            self.gecko.pokemem(0x12CDC1B4, self.ui.spinBox_5.value())
            # Gender
            self.gecko.pokemem(0x12CD1D90, self.ui.comboBox_2.currentIndex())
            # Eyes
            self.gecko.pokemem(0x12CD1D98, self.ui.comboBox_3.currentIndex())
            # Skin
            self.gecko.pokemem(0x12CD1D94, self.ui.comboBox_4.currentIndex())
            QMessageBox.information(self, 'SplatStats', "The statistics have been changed successfully!")
        except:
            QMessageBox.critical(self, 'SplatStats', "An error occurred when changing the values!")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
