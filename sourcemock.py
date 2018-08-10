from source import Source


class SourceMock(Source):

    def __init__(self, address: str, idn: str, inst=None):
        super().__init__(address, idn, inst)

    def send(self, command):
        print(f'{self._name} send: {command}')
        return 'success'

    def query(self, question):
        answer = '42'
        print(f'{self._name} query: {question}, answer: {answer}')
        return answer

