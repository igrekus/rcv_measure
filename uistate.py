class UiState:

    letter1 = 1
    letter2 = 2

    def __init__(self):
        self._letterActive = self.letter1
        self._sourceName = ''
        self._generator1Name = ''
        self._generator2Name = ''
        self._analyzerName = ''
        self._btnCheckSampleEnabled = False
        self._btnMeasureStartEnabled = False
        self._btnMeasureStartVisible = True
        self._btnMeasureStopVisible = False
        self._bgrpLetterEnabled = True

    def __str__(self):
        return f'{self.__class__.__name__}(letter={self._letterActive} source={self._sourceName} ' \
               f'gen1={self._generator1Name} gen2={self._generator2Name} ' \
               f'an={self._analyzerName} check={self._btnCheckSampleEnabled} start={self._btnMeasureStartEnabled} ' \
               f'stop={self._btnMeasureStopVisible})'

    def setActiveLetter(self, letter):
        self._letterActive = letter

    def setInstrumentNames(self, args):
        self._sourceName, self._generator1Name, self._generator2Name, self._analyzerName = args

