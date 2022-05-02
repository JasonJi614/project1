from TabsWidget import TabsWidget
from PyQt5.QtWidgets import QApplication

import sys

def main():
    app = QApplication(sys.argv)

    tabsWidget = TabsWidget()
    tabsWidget.show()

    exit(app.exec_())

if __name__ == '__main__':
    main()
    