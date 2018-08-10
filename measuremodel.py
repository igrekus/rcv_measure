import random

from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, QDate, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QFont


class MeasureModel(QAbstractTableModel):
    _default_column_count = 1

    _default_headers = ['№'] * _default_column_count

    # TODO: read params from .xlsx
    def __init__(self, parent=None):
        super().__init__(parent)

        self._data = list()
        self._headers = self._default_headers
        self._columnCount = self._default_column_count

    def clear(self):
        self.beginRemoveRows(QModelIndex(), 0, len(self._data))
        self._data.clear()
        self.endRemoveRows()

    def initModel(self, params: dict=None):

        def generateValue(data):

            if not data or '-' in data or chr(0x2212) in data or not all(data):
                return '-'

            span, step, mean = data
            start = mean - span
            stop = mean + span
            return random.randint(0, int((stop - start) / step)) * step + start

        self.beginResetModel()

        if params:
            # TODO: rewrite gen
            print('init model')

            self._data = [1] + [generateValue(v) for v in params]

            print(self._data)

        self.endResetModel()

    def initHeader(self, headers):
        self.beginResetModel()
        self._headers = headers
        self._columnCount = len(headers)
        self.endResetModel()

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                if section < len(self._headers):
                    return QVariant(self._headers[section])
        return QVariant()

    def rowCount(self, parent=None, *args, **kwargs):
        if parent.isValid():
            return 0
        # FIXME: row counter
        return 1

    def columnCount(self, parent=None, *args, **kwargs):
        return self._columnCount

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()

        col = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            if not self._data:
                return QVariant()

            return QVariant(self._data[col])
            # if col == self.ColumnRowNumber:
            #     return QVariant(self._data[0])
            # elif col == self.ColumnFreqLow:
            #     return QVariant(self._data[1])
            # elif col == self.ColumnFreqHigh:
            #     return QVariant(self._data[2])
            # elif col == self.ColumnAlphaPr:
            #     return QVariant(self._data[3])
            # elif col == self.ColumnAlphaOff:
            #     return QVariant(self._data[4])
            # elif col == self.ColumnCurrent:
            #     return QVariant(self._data[5])
            # elif col == self.ColumnPow:
            #     return QVariant(self._data[6])
            # elif col == self.ColumnTime:
            #     return QVariant(self._data[7])
            # elif col == self.ColumnCoeff:
            #     return QVariant(self._data[8])
            # elif col == self.ColumnIIP3:
            #     return QVariant(self._data[9])
            # elif col == self.ColumnDelta:
            #     return QVariant(self._data[10])

        # elif role == Qt.EditRole:
        #     if col == self.ColumnDoc:
        #         return QVariant(item.item_doc)

        return QVariant()

    # def flags(self, index):
    #     f = super(BillTableModel, self).flags(index)
    #     if index.column() == self.ColumnActive or index.column() == self.ColumnStatus:
    #         f = f | Qt.ItemIsUserCheckable
    #     return f

    @pyqtSlot(int, int)
    def itemsInserted(self, first: int, last: int):
        self.beginInsertRows(QModelIndex(), first, last)
        # print('table model slot:', first, last)
        self.endInsertRows()

    @pyqtSlot(int, int)
    def itemsRemoved(self, first: int, last: int):
        self.beginRemoveRows(QModelIndex(), first, last)
        # print('table model slot:', first, last)
        self.endRemoveRows()

    @pyqtSlot()
    def beginClearModel(self):
        self.beginResetModel()

    @pyqtSlot()
    def endClearModel(self):
        self.endResetModel()

