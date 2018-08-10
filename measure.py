import sys

from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow


def main(args):
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    # import smtplib
    #
    # server = smtplib.SMTP('mail.pulsarnpp.ru', 587)
    #
    # # Next, log in to the server
    # server.login("kuznetsov_sa", "xc74RmbY")
    #
    # # Send the mail
    # msg = "\nHello!"
    #
    # server.sendmail("kuznetsov_sa@pulsarnpp.ru", "upload234@mail.ru", msg)

    main(sys.argv)
