from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import rest_api
import re
from bardapi import Bard
''' 
    ##이 스크립트를 구현하기 위해서는 다음 pip install 이 작동되어야 합니다.
    pip install bardapi
    pip install pyqt5
    ##
'''
#Copyright Junsu Lee
# Program Name : EveryWhereNote
# Value : 서버에 메모를 할 수 있어서 작업하는 컴퓨터가 달라도 사용 가능합니다!

#  https://bard.google.com/chat?hl=ko
#  위 사이트에서 F12 -> 쿠키값 중 밑에 해당하는 값을 가져와서 업데이트 할 수 있습니다.
#  (ps. 로그인해서 크롤링하는 기능을 넣으려 했으나, 구글에서 봇감지를 잘하여, 보류하였습니다.)
# 바드 API 사용을 위하여, __Secure-1PSID 쿠키값을 가져와야 합니다.
api_key = 'dwh_9Kbhzg2Ep-9xU4ycGThzS98YYYMl7J9AbabzI8c4BgS2fa7WVn8NNby5MNWl8tDd0Q.'
llm = Bard(token = api_key)

#PyQt5로 GUI 구현을 위한 MainWindow 클래스를 만듭니다.
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        #MainWindow의 UI를 초기화합니다.
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 700)
        #윈도우 창 이름 설정
        MainWindow.setWindowTitle("Untitle.txt")
        #툴버튼 스타일 변경
        MainWindow.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        #버튼, 리스트 등 Widget의 디자인을 정의합니다.
        self.btnSummary = QPushButton(self.centralwidget)
        self.btnSummary.setObjectName(u"btnSummary")
        self.btnSummary.setGeometry(QRect(160, 3, 100, 30))
        self.btnSummary.setFont(QFont("맑은 고딕"))

        self.textSummary = QLineEdit(self.centralwidget)
        self.textSummary.setObjectName(u"textSummary")
        self.textSummary.setGeometry(QRect(265, 3, 550, 30))
        self.textSummary.setFont(QFont("맑은 고딕"))

        self.fileList = QListWidget(self.centralwidget)
        self.fileList.setObjectName(u"fileList")
        self.fileList.setGeometry(QRect(3, 90, 150, 480))
        self.fileList.setFont(QFont("맑은 고딕"))

        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(160, 0, 640, 600))
        self.textEdit.setFont(QFont("맑은 고딕"))

        self.saveFile = QPushButton(self.centralwidget)
        self.saveFile.setObjectName(u"saveFile")
        self.saveFile.setGeometry(QRect(3, 0, 150, 30))
        self.saveFile.setFont(QFont("맑은 고딕"))

        self.openFile = QPushButton(self.centralwidget)
        self.openFile.setObjectName(u"openFile")
        self.openFile.setGeometry(QRect(3, 30, 150, 30))
        self.openFile.setFont(QFont("맑은 고딕"))

        self.textFileName = QLineEdit(self.centralwidget)
        self.textFileName.setObjectName(u"textFileName")
        self.textFileName.setGeometry(QRect(3, 90, 150, 30))
        self.textFileName.setFont(QFont("맑은 고딕"))

        self.deleteFile = QPushButton(self.centralwidget)
        self.deleteFile.setObjectName(u"deleteFile")
        self.deleteFile.setGeometry(QRect(3, 570, 150, 30))
        self.deleteFile.setFont(QFont("맑은 고딕"))

        self.newFile = QPushButton(self.centralwidget)
        self.newFile.setObjectName(u"newFile")
        self.newFile.setGeometry(QRect(3, 60, 150, 30))
        self.newFile.setFont(QFont("맑은 고딕"))

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

        # MainWindow와 resizeEvent 연결
        MainWindow.resizeEvent = self.on_window_resized
        
        #아래 코드들은 버튼을 눌렀을 때 이벤트와 함수(Slot)를 연결시키는 구문입니다.
        self.saveFile.clicked.connect(self.saveFile_clicked)
        self.deleteFile.clicked.connect(self.deleteFile_clicked)
        self.newFile.clicked.connect(self.newFile_clicked)
        self.btnSummary.clicked.connect(self.btnSummary_clicked)

        #아래 코드는 리스트 인덱스가 변화할 때 이벤트와 함수를 연결시키는 구문입니다.
        self.fileList.itemSelectionChanged.connect(self.chkCurrentItmChanged)


    #서버에 저장된 파일리스트를 불러오고 리스트에 업데이트합니다.
    #업데이트 후에는 리스트의 첫번째를 선택하도록 설계하여,
    #리스트 인덱스가 줄었을 때 혹은 파일리스트 개수가 급격히 변화하였을 때 오류를 방지합니다.
    def updateFileList(self):
        #rest_api에 구현된 메서드로 리스트를 가져옵니다.
        _list = rest_api.getFileList()

        #파일 목록을 초기화합니다.
        self.fileList.clear()
        #텍스트로 전달된 목록을 개행문자로 구분짓고, 공백은 처리하지 않습니다.
        for i in _list.split("\n"):
            if i == "":
                continue
            self.fileList.addItem(i)
        #0번째 행을 지정하고 아이템을 사전 순으로 정렬합니다.
        self.fileList.setCurrentRow(0)
        self.fileList.sortItems()

    #리스트에서 선택된 파일을 서버에서 제거합니다.
    def deleteFile_clicked(self):
        #rest_api에 구현된 파일 삭제 메서드로 파일을 제거합니다.
        if rest_api.deleteFile(self.textFileName.text()) == "OK":
            #제거가 성공적으로 이루어지면 파일 목록을 업데이트 합니다.
            self.updateFileList()
            self.chkCurrentItmChanged()
        else:
            QMessageBox.critical(MainWindow, "실패", "파일 제거에 실패하였습니다.")

    #현재 메모를 서버에 저장합니다.
    def saveFile_clicked(self):
        #rest_api에 구현된 메서드로 파일을 저장합니다.
        if rest_api.saveFile(self.textFileName.text(), self.textEdit.toPlainText()) == "OK":
            #저장이 성공적으로 이루어지면 파일 목록을 다시 업데이트 합니다.
            self.updateFileList()
            self.chkCurrentItmChanged()
            QMessageBox.information(MainWindow, "성공", "성공적으로 저장되었습니다.")
        else:
            QMessageBox.critical(MainWindow, "저장에 실패하였습니다.", "저장 실패")
    
    #선택된 아이템이 변화하였을 때 처리를 담당하는 함수입니다.
    def chkCurrentItmChanged(self):
        #파일 목록의 아이템 개수가 0보다 클때
        if self.fileList.count() > 0:
            #rest_api에 구현된 파일 내용 가져오기 메서드로 현재 선택된 파일의 내용을 가져옵니다.
            res = rest_api.getFile(self.fileList.currentItem().text())
            print(res)
            
            #창 제목과 파일 내용 에디트, 파일이름 에디트를 변경합니다.
            self.textEdit.setText(res)
            self.textFileName.setText(self.fileList.currentItem().text())
            MainWindow.setWindowTitle(self.fileList.currentItem().text())

    #메모 내용을 요약하는 버튼을 눌렀을 때 처리 함수입니다.
    # Bard를 기반으로 요약 처리가 이루어집니다.
    def btnSummary_clicked(self):
        res =llm.get_answer("다음 글을 한국어로 간단하게 요약해줘. :\n" + self.textEdit.toPlainText())
        self.textSummary.setText(res['content'])

    #새파일을 생성하는 버튼을 눌렀을 때 처리 함수입니다.
    #클릭과 동시에 서버에 새파일 생성되고,
    #정규식을 활용해서 untitle[숫자..].txt가 중복해서 있는지 검사합니다.
    #만약 있다면 그 중에서 가장 큰 숫자 + 1 해서 순서를 정합니다.
    def newFile_clicked(self):
        self.textEdit.setText("")
        cnt = 0
        p = re.compile("untitle[0-9]*.txt")
        for i in range(0, self.fileList.count()):
            s = self.fileList.item(i).text()
            if p.match(s) != None:
                print(s)
                cnt = max(cnt, int(s[7:s.find('.')]))
        cnt = cnt + 1
        print(cnt)
        
        self.textFileName.setText("untitle" +str(cnt) + ".txt")
        MainWindow.setWindowTitle("untitle" +str(cnt) + ".txt")
        rest_api.saveFile(self.textFileName.text(), self.textEdit.toPlainText())
        self.updateFileList()
        self.chkCurrentItmChanged()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "untitle.txt", None))
        self.saveFile.setText(QCoreApplication.translate("MainWindow", "파일 저장", None))
        self.openFile.setText(QCoreApplication.translate("MainWindow", "파일 열기", None))
        self.textFileName.setText(QCoreApplication.translate("MainWindow", "untitle.txt", None))
        self.deleteFile.setText(QCoreApplication.translate("MainWindow", "저장된 파일 삭제", None))
        self.newFile.setText(QCoreApplication.translate("MainWindow", "새 파일", None))
        self.btnSummary.setText(QCoreApplication.translate("MainWindow", "요약", None))

    def on_window_resized(self, event):
        # MainWindow의 사이즈를 저장
        new_size = event.size()

        # 텍스트 에디트와 리스트 사이즈 조정
        text_edit_width = new_size.width() - 160 - 3  # 텍스트 에디트 길이 조정 변수
        text_summary_width = new_size.width() - 180 - 100  # 텍스트 에디트 길이 조정 변수
        file_list_height = new_size.height() - (30* 5+ 3) # 파일리스트 길이 조정 변수

        self.textEdit.setGeometry(160, 40, text_edit_width, new_size.height() - 3)
        self.fileList.setGeometry(3, 125, 150, file_list_height -5)
        self.deleteFile.setGeometry(3, 120 + file_list_height, 150, 30)
        self.textSummary.setGeometry(265, 3, text_summary_width, 30)
       
# 만약, 현재 모듈이 직접적으로 실행됐을 때만 작동
if __name__ == "__main__":
    #GUI 어플리케이션 생성을 위한 변수
    app = QApplication(sys.argv)

    #메인 창 정의
    MainWindow = QMainWindow()
    #사용자가 정의한한 메인 창
    window = Ui_MainWindow()
    window.setupUi(MainWindow)

    #메인 창 표시
    MainWindow.show()

    #서버에서 리스트를 업데이트한다. (초기화 작업)
    window.updateFileList()
    window.chkCurrentItmChanged()
    sys.exit(app.exec_())