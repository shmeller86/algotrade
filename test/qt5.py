import sys
from PyQt5.QtChart import QCandlestickSeries, QChart, QChartView, QCandlestickSet
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget
from PyQt5.QtCore import Qt, QPointF, QObject, pyqtSignal, QTimer, QRect
from PyQt5 import QtChart as qc
from PyQt5 import QtGui

import random


class MainWindow(QMainWindow):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(QRect(0, 0, 261, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setObjectName("label")



        self.series = QCandlestickSeries()
        self.series.setDecreasingColor(Qt.red)
        self.series.setIncreasingColor(Qt.green)

        self.ma5 = qc.QLineSeries()
        self.tm = []

        self.chart = QChart()

        self.chart.addSeries(self.series)  # candle
        self.chart.addSeries(self.ma5)  # ma5 line

        self.chart.createDefaultAxes()
        self.chart.legend().hide()

        self.chart.axisX(self.series).setCategories(self.tm)
        self.chart.axisX(self.ma5).setVisible(False)

        self.chartview = QChartView(self.chart)
        self.setGeometry(50, 50, 500, 300)
        self.setCentralWidget(self.chartview)

    def append_data_and_plot(self, d):
        """Append and update the plot"""
        num, o, h, l, c, m = d

        ax1 = self.chart.axisX(self.ma5)
        ay1 = self.chart.axisY(self.ma5)

        xmin = xmax = num
        ymin = ymax = m

        step = 10
        offset = 100

        for p in self.ma5.pointsVector()[-step:]:
            xmin = min(p.x(), xmin)
            xmax = max(p.x(), xmax)

            ymin = min(p.y(), ymin) - offset
            ymax = max(p.y(), ymax) + offset

        xmin = max(0, xmax - step)

        ax1.setMin(xmin)
        ax1.setMax(xmax)
        ay1.setMin(ymin)
        ay1.setMax(ymax)

        self.ma5.append(QPointF(num, m))
        self.tm.append(str(num))

        self.series.append(QCandlestickSet(o, h, l, c))
        ax2 = self.chart.axisX(self.series)
        ax2.setCategories(self.tm)
        ax2.setMin(str(xmin))
        ax2.setMax(str(xmax))

        ay2 = self.chart.axisY(self.series)
        ay2.setMin(ymin)
        ay2.setMax(ymax)


def create_data():


    i = 1
    while True:
        i += 1
        yield (
            i,
            random.randint(7000, 8000),
            random.randint(7000, 8000),
            random.randint(7000, 8000),
            random.randint(7000, 8000),
            random.randint(7000, 8000),
        )


class Producer(QObject):
    dataChanged = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.iter = create_data()
        QTimer.singleShot(random.randint(0, 1500), self.send_data)

    def send_data(self):
        d = list(next(self.iter))
        self.dataChanged.emit(d)
        QTimer.singleShot(random.randint(0, 1500), self.send_data)


def main():
    app = QApplication(sys.argv)

    data = ((1, 7380, 7520, 7380, 7510, 7324),)
    w = MainWindow(data)
    w.resize(800, 600)
    w.show()

    p = Producer()
    p.dataChanged.connect(w.append_data_and_plot)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()