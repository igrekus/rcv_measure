from PyQt5 import uic
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDialog, QAction
from PyQt5.QtCore import Qt

from instrumentmanager import InstrumentManager
from measuremodel import MeasureModel
from uistate import UiState


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        self._ui = uic.loadUi('mainwindow.ui', self)

        self._uiState = UiState()

        # create models
        self.measureModels = {
            1: MeasureModel(self),
            2: MeasureModel(self),
        }
        self._instrumentManager = InstrumentManager(self, self.measureModels)

        self.initDialog()

    def setupUiSignals(self):
        self._ui.btnSearchInstruments.clicked.connect(self.onBtnSearchInstrumentsClicked)
        self._ui.btnCheckSample.clicked.connect(self.onBtnCheckSample)
        self._ui.btnMeasureStart.clicked.connect(self.onBtnMeasureStart)
        self._ui.btnMeasureStop.clicked.connect(self.onBtnMeasureStop)

        self._ui.radioLetter1.toggled.connect(self.onRadioToggled)
        self._ui.radioLetter2.toggled.connect(self.onRadioToggled)

    def initDialog(self):
        self.setupUiSignals()

        self._ui.bgrpLetter.setId(self._ui.radioLetter1, 1)
        self._ui.bgrpLetter.setId(self._ui.radioLetter2, 2)

        self._ui.textLog.hide()

        self.updateUi(state=self._uiState)

        self.refreshView()

    # UI utility methods
    def refreshView(self):
        pass
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

    def updateUi(self, state):
        print('updating ui', state)
        self.blockSignals(True)

        if state._letterActive == UiState.letter1:
            self._ui.radioLetter1.setChecked(True)
        elif state._letterActive == UiState.letter2:
            self._ui.radioLetter2.setChecked(True)

        self._ui.editSource.setText(state._sourceName)
        self._ui.editGen1.setText(state._generator1Name)
        self._ui.editGen2.setText(state._generator2Name)
        self._ui.editAnalyzer.setText(state._analyzerName)

        self._ui.btnCheckSample.setEnabled(state._btnCheckSampleEnabled)
        self._ui.btnMeasureStart.setEnabled(state._btnMeasureStartEnabled)
        self._ui.btnMeasureStart.setVisible(state._btnMeasureStartVisible)
        self._ui.btnMeasureStop.setVisible(state._btnMeasureStopVisible)

        self._ui.radioLetter1.setEnabled(state._bgrpLetterEnabled)
        self._ui.radioLetter2.setEnabled(state._bgrpLetterEnabled)

        self.blockSignals(False)

        self.resizeTable()

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
        self._uiState._btnCheckSampleEnabled = False
        self._uiState._btnMeasureStartEnabled = False
        self._uiState._bgrpLetterEnabled = True

        if not self.search():
            return

        self._uiState._btnCheckSampleEnabled = True
        self._uiState.setInstrumentNames(self._instrumentManager.getInstrumentNames())
        self.updateUi(self._uiState)

    def failWith(self, message):
        QMessageBox.information(self, "Ошибка", message)
        self._uiState._bgrpLetterEnabled = True
        self._uiState._btnMeasureStartEnabled = False
        self.updateUi(self._uiState)

    def onBtnCheckSample(self):

        if not self._instrumentManager.checkSample():
            self.failWith("Не удалось найти образец, проверьте подключение.\nПодробности в логах.")
            print('sample not detected')
            return

        if not self._instrumentManager.checkTaskTable():
            self.failWith("Ошибка при чтении таблицы с заданием на измерение.\nПодробности в логах.")
            print('error opening table')
            return

        self._uiState._bgrpLetterEnabled = False
        self._uiState._btnMeasureStartEnabled = True
        self.updateUi(self._uiState)

    def onBtnMeasureStart(self):
        print('start measurement task')

        if not self._instrumentManager.checkSample():
            self.failWith("Не удалось найти образец, проверьте подключение.\nПодробности в логах.")
            print('sample not detected')
            return

        self._instrumentManager.measure(self._ui.bgrpLetter.checkedId())

        self._uiState._btnMeasureStartVisible = False
        self._uiState._btnMeasureStopVisible = True
        self._uiState._btnCheckSampleEnabled = False
        self.updateUi(self._uiState)

    def onBtnMeasureStop(self):
        print('abort measurement task')
        # TODO: stop measure
        self._uiState._btnMeasureStartVisible = True
        self._uiState._btnMeasureStopVisible = False
        self._uiState._btnMeasureStartEnabled = False
        self._uiState._btnCheckSampleEnabled = True
        self._uiState._bgrpLetterEnabled = True
        self.updateUi(self._uiState)

    def onRadioToggled(self, checked):
        if not checked:
            return

        letter = self._ui.bgrpLetter.checkedId()
        print('switching to letter', letter)
        self._uiState.setActiveLetter(letter)

        self._ui.tableMeasure.setModel(self.measureModels[letter])
        self.resizeTable()
