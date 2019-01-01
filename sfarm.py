from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
import pyqtgraph as pg
import serial
from sfarm_gui import *
import threading
import random

ser = serial.Serial(port='COM4',
    				baudrate=115200,
        			parity=serial.PARITY_NONE,
        			stopbits=serial.STOPBITS_ONE,
        			bytesize=serial.EIGHTBITS,
    				timeout=1)


def receiveData(self, ui):
	while True:      
		rxdata = ser.readline().decode('utf-8')
		if rxdata :
			print(rxdata)


def signals(self):
    # 페이지 전환 버튼
    self.buttonManage.clicked.connect(self.changetoManagePage)
    self.buttonSettings.clicked.connect(self.changetoSettingsPage)
    # 그래프 요소 선택 체크 박스
    self.checkboxCo2.stateChanged.connect(self.plotting)
    self.checkboxHumid.stateChanged.connect(self.plotting)
    self.checkboxTemp.stateChanged.connect(self.plotting)
    self.checkboxTDS.stateChanged.connect(self.plotting)
    self.checkboxPH.stateChanged.connect(self.plotting)
    self.buttonSave.clicked.connect(self.plotting)
    # 제어 요소 가동 여부 버튼
    self.buttonHumid.clicked.connect(self.buttonHumidClicked)
    self.buttonCo2.clicked.connect(self.buttonCo2Clicked)
    self.buttonFan.clicked.connect(self.buttonFanClicked)
    self.buttonPump.clicked.connect(self.buttonPumpClicked)
    self.buttonLED.clicked.connect(self.buttonLEDClicked)
    # 설정값 적용 버튼
    self.buttonApply.clicked.connect(self.apply)
    # 설정값 적용 취소 버튼
    self.buttonRevert.clicked.connect(self.revert)

# 페이지 전환 버튼
def changetoSettingsPage(self):
    self.stackedWidget.setCurrentIndex(1)

def changetoManagePage(self):
    self.stackedWidget.setCurrentIndex(0)
    
# 제어 요소 가동 start <-> stop 전환 버튼
def buttonHumidClicked(self):
    s=self.buttonHumid.text()
    self.buttonHumid.setText('start') if s=='stop' else self.buttonHumid.setText('stop')

def buttonCo2Clicked(self):
    s=self.buttonCo2.text()
    self.buttonCo2.setText('start') if s=='stop' else self.buttonCo2.setText('stop')

def buttonFanClicked(self):
    s=self.buttonFan.text()
    self.buttonFan.setText('start') if s=='stop' else self.buttonFan.setText('stop')

def buttonPumpClicked(self):
    s=self.buttonPump.text()
    self.buttonPump.setText('start') if s=='stop' else self.buttonPump.setText('stop')

def buttonLEDClicked(self):
    s=self.buttonLED.text()
    self.buttonLED.setText('start') if s=='stop' else self.buttonLED.setText('stop')


# 시리얼 통신을 통한 LED 디밍
def LEDControl(self,string):
    print(string)
    if string=='stop' :
        message = '\x02L01B000R000W000B000\x03\x0a'
        ser.write(bytes(message.encode()))
        print(message)
    elif string=='start':
        R=self.labelR_2.text()
        if int(R) < 10 :
            R = '00'+R
        elif int(R) < 100 :
            R = '0' + R
        W=self.labelW_2.text()
        if int(W) < 10 :
            W = '00'+W
        elif int(W) < 100 :
            W = '0' + W
        B=self.labelB_2.text()
        if int(B) < 10 :
            B = '00'+B
        elif int(B) < 100 :
            B = '0' + B
        message = ''.join(['\x02L01B000','R',R,'W',W,'B',B,'\x03\x0a'])
        ser.write(bytes(message.encode()))
        print(message)

# 설정값 적용 버튼
def apply(self):
    self.LEDControl(string=self.buttonLED.text())
    self.saveSettings()

# 설정값 적용 취소 버튼
def revert(self):
    self.setSettings()

# 설정 파일 읽어 저장된 설정값 적용
def setSettings(self):
    #In append mode, Python will create the file if it does not exist.
    f = open("settings.txt", 'r' )
    settings_list = f.readlines()
    self.spinBoxCo2.setValue(int(settings_list[0].strip()))
    self.spinBoxHumid.setValue(int(settings_list[1].strip()))
    self.spinBoxTemp.setValue(float(settings_list[2].strip()))
    self.spinBoxFan.setValue(int(settings_list[3].strip()))
    self.sliderTDS.setValue(int(settings_list[4].strip()))
    self.sliderPH.setValue(int(settings_list[5].strip()))
    self.spinBoxPump.setValue(int(settings_list[6].strip()))
    self.sliderR.setValue(int(settings_list[7].strip()))
    self.sliderG.setValue(int(settings_list[8].strip()))
    self.sliderB.setValue(int(settings_list[9].strip()))
    self.sliderW.setValue(int(settings_list[10].strip()))

# 설정 파일에 설정값 저장
def saveSettings(self):
    settings_list =[str(self.spinBoxCo2.text()),str(self.spinBoxHumid.text()),str(self.spinBoxTemp.text())
    ,str(self.spinBoxFan.text()),str(self.sliderTDS.value()),str(self.sliderPH.value()),str(self.spinBoxPump.text())
    ,str(self.sliderR.value()),str(self.sliderG.value()),str(self.sliderB.value()),str(self.sliderW.value())]
    print(settings_list)
    f = open("settings.txt", 'w' )
    f.write('\n'.join(settings_list))
    f.close()


# 데이터
Co2_list = [random.randrange(600,800) for i in range(30)]
Humid_list = [random.randrange(50,75) for i in range(30)]
# 청경채의 싹트는 온도 : 15~20℃
# 청경재 재배 적정 온도 : 낮 20∼25℃
Temp_list = [random.uniform(20.0,25.0) for i in range(30)]
TDS_list = [random.randrange(900,1000) for i in range(30)]
# 청경채 재배 산성도 : pH 6.5∼7.0
PH_list = [random.uniform(6.5,7.0) for i in range(30)]
# 청경채 상태 데이터
Condition_list = [random.randrange(1,6) for i in range(30)]
# 청경채의 설정값과 센서값 편차 데이터
Deviation_list = [random.randrange(1,11) for i in range(30)]

# 그래프 그리기
def plotting(self):
    # 새로운 데이터 추가 및 기존 데이터 삭제
    # 센서값 보여주기
    Co2_list.append(random.randrange(600,800))
    value = Co2_list[-1]
    if abs(self.spinBoxCo2.value() - value) < 50:
        self.Co2Display.display(Co2_list[-1])
    elif abs(self.spinBoxCo2.value() - value) < 100:
        self.Co2Display.display(Co2_list[-1])
    else :
        self.Co2Display.display(Co2_list[-1])
    Co2_list.pop(0)
    Humid_list.append(random.randrange(50,75))
    self.HumidDisplay.display(Humid_list[-1])
    Humid_list.pop(0)
    Temp_list.append(random.uniform(20.0,25.0))
    self.TempDisplay.display(Temp_list[-1])
    Temp_list.pop(0)
    TDS_list.append(random.randrange(900,1000))
    self.TDSDisplay.display(TDS_list[-1])
    TDS_list.pop(0)
    PH_list.append(random.uniform(6.5,7.0))
    self.PHDisplay.display(PH_list[-1])
    PH_list.pop(0)
    Condition_list.append(random.randrange(1,6))
    Condition_list.pop(0)
    Deviation_list.append(random.randrange(1,11))
    Deviation_list.pop(0)
    # 그래프 요소 초기화
    # 그래프 배경값 설정
    self.viewAir.clear()
    self.viewAir.setBackground('#fafafa')
    self.viewWater.clear()
    self.viewWater.setBackground('#fafafa')
    self.viewCondition.clear()
    self.viewCondition.setBackground('#fafafa')

    # 체크된 요소의 그래프 그리기
    if self.checkboxCo2.isChecked() :
        self.viewAir.plot(Co2_list, pen=pg.mkPen(color=(85,85,119), width=3,style=QtCore.Qt.DotLine),
        antialias = True)#, symbol=('o'), symbolSize=7,symbolBrush=(85,85,119),antialias=True)
    if self.checkboxHumid.isChecked() :
        self.viewAir.plot(Humid_list, pen=pg.mkPen(color=(68,102,153), width=3,style=QtCore.Qt.DotLine), antialias = True)
        #symbol=('o'), symbolSize=5,symbolBrush=(68,102,153),antialias=True) 
    if self.checkboxTemp.isChecked() :
        self.viewAir.plot(Temp_list, pen=pg.mkPen(color=(100,176,188), width=3,style=QtCore.Qt.DashLine), antialias = True)
        #symbol=('o'), symbolSize=7,symbolBrush=(100,176,188),antialias=True) 
    if self.checkboxTDS.isChecked() :
        self.viewWater.plot(TDS_list, pen=pg.mkPen(color=(251,192,99), width=3,style=QtCore.Qt.SolidLine),
        symbol=('o'), symbolSize=7,symbolBrush=(251,192,99),antialias=True)
    if self.checkboxPH.isChecked() :
        self.viewWater.plot(PH_list, pen=pg.mkPen(color=(234,87,61) , width=3, style=QtCore.Qt.SolidLine),
        symbol=('o'), symbolSize=7,symbolBrush=(234,87,61),antialias=True) 

    self.viewCondition.plot(Condition_list,pen=pg.mkPen(color=(250,10,10) , width=3),
    style=QtCore.Qt.DashLine, symbol=('o'), symbolSize=7,symbolBrush=(250,10,10),antialias=True) 
    self.viewCondition.plot(Deviation_list,pen=pg.mkPen(color=(140,25,15) , width=3),
    style=QtCore.Qt.DashLine, symbol=('o'), symbolSize=7,symbolBrush=(140,25,15),antialias=True) 
    

"""Ui_Dialog.signals = signals
Ui_Dialog.ledOn = ledOn
Ui_Dialog.ledOff = ledOff"""
Ui_MainWindow.signals = signals
Ui_MainWindow.apply = apply
Ui_MainWindow.revert = revert
Ui_MainWindow.saveSettings = saveSettings
Ui_MainWindow.setSettings = setSettings
Ui_MainWindow.LEDControl=LEDControl
Ui_MainWindow.plotting=plotting
Ui_MainWindow.changetoSettingsPage = changetoSettingsPage
Ui_MainWindow.changetoManagePage = changetoManagePage
Ui_MainWindow.ReceiveData = receiveData
Ui_MainWindow.buttonHumidClicked = buttonHumidClicked
Ui_MainWindow.buttonCo2Clicked = buttonCo2Clicked
Ui_MainWindow.buttonFanClicked = buttonFanClicked
Ui_MainWindow.buttonPumpClicked = buttonPumpClicked
Ui_MainWindow.buttonLEDClicked = buttonLEDClicked

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.signals()
    ui.setSettings()
    ui.plotting()
    thread = threading.Thread(target=receiveData, args=(ser,ui))
    thread.daemon = True
    thread.start()
    MainWindow.show()
    sys.exit(app.exec_())
    