from time import sleep

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDialog, QAction
from PyQt5.QtCore import Qt, QStateMachine, QState, pyqtSignal

from instrumentmanager import InstrumentManager
from measuremodel import MeasureModel


class MainWindow(QMainWindow):

    instrumentsFound = pyqtSignal()
    sampleFound = pyqtSignal()
    measurementFinished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        self._ui = uic.loadUi('mainwindow.ui', self)

        # create models
        self.measureModels = {
            1: MeasureModel(self),
            2: MeasureModel(self),
        }
        self._instrumentManager = InstrumentManager(self, self.measureModels)

        self.machine = QStateMachine()
        self.stateInitial = QState()
        self.stateReadyToCheck = QState()
        self.stateReadyToMeasure = QState()
        self.stateAfterMeasure = QState()

        self.initDialog()

    def setupStateMachine(self):
        self.machine.addState(self.stateInitial)
        self.machine.addState(self.stateReadyToCheck)
        self.machine.addState(self.stateReadyToMeasure)
        self.machine.addState(self.stateAfterMeasure)

        self.stateInitial.addTransition(self.instrumentsFound, self.stateReadyToCheck)
        self.stateInitial.assignProperty(self._ui.btnSearchInstruments, 'enabled', 'True')
        self.stateInitial.assignProperty(self._ui.btnCheckSample, 'enabled', 'False')
        self.stateInitial.assignProperty(self._ui.btnMeasureStart, 'visible', 'True')
        self.stateInitial.assignProperty(self._ui.btnMeasureStart, 'enabled', 'False')
        self.stateInitial.assignProperty(self._ui.btnMeasureStop, 'visible', 'False')
        self.stateInitial.assignProperty(self._ui.btnMeasureStop, 'enabled', 'False')
        self.stateInitial.assignProperty(self._ui.radioLetter1, 'checked', 'True')
        self.stateInitial.assignProperty(self._ui.radioLetter1, 'enabled', 'True')
        self.stateInitial.assignProperty(self._ui.radioLetter2, 'enabled', 'True')

        self.stateReadyToCheck.addTransition(self.sampleFound, self.stateReadyToMeasure)
        self.stateReadyToCheck.assignProperty(self._ui.btnSearchInstruments, 'enabled', 'True')
        self.stateReadyToCheck.assignProperty(self._ui.btnCheckSample, 'enabled', 'True')
        self.stateReadyToCheck.assignProperty(self._ui.btnMeasureStart, 'visible', 'True')
        self.stateReadyToCheck.assignProperty(self._ui.btnMeasureStart, 'enabled', 'False')
        self.stateReadyToCheck.assignProperty(self._ui.btnMeasureStop, 'visible', 'False')
        self.stateReadyToCheck.assignProperty(self._ui.btnMeasureStop, 'enabled', 'False')
        self.stateReadyToCheck.assignProperty(self._ui.radioLetter1, 'enabled', 'True')
        self.stateReadyToCheck.assignProperty(self._ui.radioLetter2, 'enabled', 'True')

        self.stateReadyToMeasure.addTransition(self.measurementFinished, self.stateAfterMeasure)
        self.stateReadyToMeasure.addTransition(self.instrumentsFound, self.stateReadyToCheck)
        self.stateReadyToMeasure.assignProperty(self._ui.btnSearchInstruments, 'enabled', 'True')
        self.stateReadyToMeasure.assignProperty(self._ui.btnCheckSample, 'enabled', 'False')
        self.stateReadyToMeasure.assignProperty(self._ui.btnMeasureStart, 'visible', 'True')
        self.stateReadyToMeasure.assignProperty(self._ui.btnMeasureStart, 'enabled', 'True')
        self.stateReadyToMeasure.assignProperty(self._ui.btnMeasureStop, 'visible', 'False')
        self.stateReadyToMeasure.assignProperty(self._ui.btnMeasureStop, 'enabled', 'False')
        self.stateReadyToMeasure.assignProperty(self._ui.radioLetter1, 'enabled', 'False')
        self.stateReadyToMeasure.assignProperty(self._ui.radioLetter2, 'enabled', 'False')

        self.stateAfterMeasure.addTransition(self._ui.btnMeasureStop.clicked, self.stateReadyToCheck)
        self.stateAfterMeasure.addTransition(self.instrumentsFound, self.stateReadyToCheck)
        self.stateAfterMeasure.assignProperty(self._ui.btnSearchInstruments, 'enabled', 'True')
        self.stateAfterMeasure.assignProperty(self._ui.btnCheckSample, 'enabled', 'False')
        self.stateAfterMeasure.assignProperty(self._ui.btnMeasureStart, 'visible', 'False')
        self.stateAfterMeasure.assignProperty(self._ui.btnMeasureStart, 'enabled', 'False')
        self.stateAfterMeasure.assignProperty(self._ui.btnMeasureStop, 'visible', 'True')
        self.stateAfterMeasure.assignProperty(self._ui.btnMeasureStop, 'enabled', 'True')
        self.stateAfterMeasure.assignProperty(self._ui.radioLetter1, 'enabled', 'False')
        self.stateAfterMeasure.assignProperty(self._ui.radioLetter2, 'enabled', 'False')

        self.machine.setInitialState(self.stateInitial)
        self.machine.start()

    def setupUiSignals(self):
        self._ui.btnSearchInstruments.clicked.connect(self.onBtnSearchInstrumentsClicked)
        self._ui.btnCheckSample.clicked.connect(self.onBtnCheckSample)
        self._ui.btnMeasureStart.clicked.connect(self.onBtnMeasureStart)
        self._ui.btnMeasureStop.clicked.connect(self.onBtnMeasureStop)

        self._ui.radioLetter1.toggled.connect(self.onRadioToggled)
        self._ui.radioLetter2.toggled.connect(self.onRadioToggled)

    def initDialog(self):
        self.setupStateMachine()

        self.setupUiSignals()

        self._ui.bgrpLetter.setId(self._ui.radioLetter1, 1)
        self._ui.bgrpLetter.setId(self._ui.radioLetter2, 2)

        self._ui.textLog.hide()

        self.refreshView()

    # UI utility methods
    def refreshView(self):
        self.resizeTable()
        # twidth = self.ui.tableSuggestions.frameGeometry().width() - 30
        # self.ui.tableSuggestions.setColumnWidth(0, twidth * 0.05)
        # self.ui.tableSuggestions.setColumnWidth(1, twidth * 0.10)
        # self.ui.tableSuggestions.setColumnWidth(2, twidth * 0.55)
        # self.ui.tableSuggestions.setColumnWidth(3, twidth * 0.10)
        # self.ui.tableSuggestions.setColumnWidth(4, twidth * 0.15)
        # self.ui.tableSuggestions.setColumnWidth(5, twidth * 0.05)

    def resizeTable(self):
        self._ui.tableMeasure.resizeRowsToContents()
        self._ui.tableMeasure.resizeColumnsToContents()

    def search(self):
        if not self._instrumentManager.findInstruments():
            QMessageBox.information(self, "Ошибка",
                                    "Не удалось найти инструменты, проверьте подключение.\nПодробности в логах.")
            return False

        print('found all instruments, enabling sample test')
        return True

    # event handlers
    def resizeEvent(self, event):
        self.refreshView()

    # TODO: extract to a measurement manager class
    def onBtnSearchInstrumentsClicked(self):
        if not self.search():
            return
        self.stateReadyToCheck.assignProperty(self._ui.editSource, 'text', str(self._instrumentManager._source))
        self.stateReadyToCheck.assignProperty(self._ui.editGen1, 'text', str(self._instrumentManager._generator1))
        self.stateReadyToCheck.assignProperty(self._ui.editGen2, 'text', str(self._instrumentManager._generator2))
        self.stateReadyToCheck.assignProperty(self._ui.editAnalyzer, 'text', str(self._instrumentManager._analyzer))
        self.instrumentsFound.emit()

    def failWith(self, message):
        QMessageBox.information(self, "Ошибка", message)
        self.instrumentsFound.emit()

    def onBtnCheckSample(self):

        if not self._instrumentManager.checkSample():
            self.failWith("Не удалось найти образец, проверьте подключение.\nПодробности в логах.")
            print('sample not detected')
            return

        if not self._instrumentManager.checkTaskTable():
            self.failWith("Ошибка при чтении таблицы с заданием на измерение.\nПодробности в логах.")
            print('error opening table')
            return

        self.sampleFound.emit()
        self.refreshView()

    def onBtnMeasureStart(self):
        print('start measurement task')

        if not self._instrumentManager.checkSample():
            self.failWith("Не удалось найти образец, проверьте подключение.\nПодробности в логах.")
            print('sample not detected')
            return

        self._instrumentManager.measure(self._ui.bgrpLetter.checkedId())
        self.measurementFinished.emit()
        self.refreshView()

    def onBtnMeasureStop(self):
        # TODO implement
        print('abort measurement task')

    def onRadioToggled(self, checked):
        if not checked:
            return

        letter = self._ui.bgrpLetter.checkedId()
        print('switching to letter', letter)

        self._ui.tableMeasure.setModel(self.measureModels[letter])
        self.refreshView()

