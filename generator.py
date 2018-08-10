class Generator:

    def __init__(self, address: str, idn: str, inst):
        self._address = address
        self._idn = idn
        self._name = idn.split(',')[1].strip()
        self._inst = inst

        print(f'{idn} found at {address}')

    def __str__(self):
        return f'{self.__class__}(idn={self._idn})'

    def send(self, command):
        print(f'{self._name}', self._inst.write(command))

    def query(self, question):
        answer = self._inst.query(question)
        print(f'{self._name} {answer}')
        return answer

    def ping(self):
        print(self.query('*IDN?'))

    def set_modulation(self, state):
        self.send(f':OUTP:MOD:STAT {state}')

    def set_freq(self, value, unit):
        # TODO: convert to Hz
        self.send(f'SOUR:FREQ {str(value)}{unit}')

    def set_pow(self, value, unit):
        self.send(f'SOUR:POW {str(value)}{unit}')

    def set_output(self, status):
        self.send(f'OUTP:STAT {status}')

    @property
    def name(self):
        return self._name

