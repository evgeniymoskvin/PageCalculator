import PyPDF2
import math, sys

from PySide6 import QtCore, QtWidgets, QtGui

from ui.main_window import Ui_MainWindow
from ui.icon import rc_icon


def get_pages(path):
    # Стандартизированные размеры листов по ГОСТ
    page_size_standard = {
        'A0': (841, 1189, 16),
        'A0x2': (1189, 1682, 32),
        'A0x3': (1189, 2523, 48),
        'A1': (594, 841, 8),
        'A1x3': (841, 1783, 24),
        'A1x4': (841, 2378, 32),
        'A2': (420, 594, 4),
        'A2x3': (594, 1261, 12),
        'A2x4': (594, 1682, 16),
        'A2x5': (594, 2102, 20),
        'A3': (297, 420, 2),
        'A3x3': (420, 891, 6),
        'A3x4': (420, 1189, 8),
        'A3x5': (420, 1486, 10),
        'A3x6': (420, 1783, 12),
        'A3x7': (420, 2080, 14),
        'A4': (210, 297, 1),
        'A4x3': (297, 630, 3),
        'A4x4': (297, 841, 4),
        'A4x5': (297, 1051, 5),
        'A4x6': (297, 1261, 6),
        'A4x7': (297, 1471, 7),
        'A4x8': (297, 1682, 8),
        'A4x9': (297, 1892, 9),
    }
    # Пустой словарь для подсчета листов
    pdf_size_file = {
        'A0': 0,
        'A0x2': 0,
        'A0x3': 0,
        'A1': 0,
        'A1x3': 0,
        'A1x4': 0,
        'A2': 0,
        'A2x3': 0,
        'A2x4': 0,
        'A2x5': 0,
        'A3': 0,
        'A3x3': 0,
        'A3x4': 0,
        'A3x5': 0,
        'A3x6': 0,
        'A3x7': 0,
        'A4': 0,
        'A4x3': 0,
        'A4x4': 0,
        'A4x5': 0,
        'A4x6': 0,
        'A4x7': 0,
        'A4x8': 0,
        'A4x9': 0,
    }

    a4_count = 0  # Счетчик форматов А4
    normal_pages = 0  # Счетчик распознанных листов
    list_pages = []  # Список листов
    with open(path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        i = 0
        num_pages = len(pdf_reader.pages)
        for i in range(num_pages):
            checker = 0
            box = pdf_reader.pages[i]
            # Переводим значения в миллиметры
            width = math.ceil(float(box.mediabox.width) * 0.35273159)
            height = math.ceil(float(box.mediabox.height) * 0.35273159)
            list_pages.append([height, width])
            # Приводим к одной ориентации
            if width < height:
                small = width
                long = height
            else:
                small = height
                long = width
            # Проверяем вхождение данных размеров в стандартные, с допуском 15мм
            for key, value in page_size_standard.items():
                if (value[0] >= small - 15) and (value[0] <= small + 15) and (value[1] <= long + 15) and (
                        value[1] >= long - 15):
                    normal_pages += 1
                    a4_count += value[2]
                    pdf_size_file[key] += 1
                    checker = 1
            # Если в стандартные значения не вошли
            if checker == 0:
                size = f'{small}x{long}'
                try:
                    pdf_size_file[size] += 1  # Если такой размер уже есть в словаре
                except:
                    pdf_size_file[size] = 1  # Если такого размера нет в словаре
    # Переносим все пустые значения в список
    temp_list = []
    for key, value in pdf_size_file.items():
        if value == 0:
            temp_list.append(key)
    # Удаляем из словаря все пустые значения
    for i in temp_list:
        del pdf_size_file[i]

    print(pdf_size_file)
    print(f'Всего форматов а4: {a4_count}')
    print(f'Всего страниц: {num_pages}')
    print(f'Всего распознано страниц: {normal_pages}')
    return pdf_size_file, a4_count, num_pages, normal_pages, list_pages

    # pyside2-uic "you_file.ui" -o "your_file.py"


class TableModel(QtCore.QAbstractTableModel):

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...):
        """
        Устновка значений шапки таблицы
        """
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            # return f"Column {section + 1}"
            return self.columns[section]
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return f"{section + 1}"

    def __init__(self, data):
        self.columns = ["Формат", "Количество"]
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        try:
            len_ = len(self._data[0])
        except:
            len_ = 0
        return len_


class TableModel2(TableModel):
    """Вторая таблица"""

    def __init__(self, data):
        self.columns = ["Высота", "Ширина"]
        super(TableModel, self).__init__()
        self._data = data


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        rc_icon.qInitResources()  # Подгружаем файл с иконками
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(":/ico/Calculator_30001.ico")))  # Устанаваливаем иконки
        # resource.qInitResources()
        self.ui = Ui_MainWindow()  # Подключаем Ui
        self.ui.setupUi(self)
        self.file_list = []
        self.data_formats = []
        self.setAcceptDrops(True)  # Подключаем drag and drop

        # Сигналы
        self.ui.open_pdf_button.clicked.connect(self.add_files_to_check)  # Кнопка открытия pdf

    def check_pdf_file(self, fname):
        """
        Функция вызова подсчета листов в файле, get_pages
        :param fname: строка с адресом к файла, str
        """
        self.file_list.append(fname)
        print(fname, type(fname))  # Полный путь к файлу
        try:
            self.file_name = fname.split('/')[-1]
        except:
            self.file_name = fname
        print(self.file_name)  # Наименование файла
        pdf_size_file, a4_count, num_pages, normal_pages, list_pages = get_pages(fname)
        self.ui.a4_count_text.setText(str(a4_count))
        self.ui.num_pages_text.setText(str(num_pages))
        self.ui.normal_text.setText(str(normal_pages))
        self.ui.fileName.setText(str(self.file_name))
        self.data_formats = []
        # Делаем список, для подстановки в таблицу
        for key, value in pdf_size_file.items():
            self.data_formats.append([key, value])
            print(key, value)
        self.model_formats = TableModel(self.data_formats)
        self.data_pages = list_pages
        self.model_pages = TableModel2(self.data_pages)

        self.ui.tableView.setModel(self.model_formats)  # Устанавливаем значения в таблицу левую
        self.ui.tableView_2.setModel(self.model_pages)  # Устанавливаем значения в таблицу правую

    def dragEnterEvent(self, event):
        mime = event.mimeData()
        if mime.hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_name = url.toLocalFile()
            self.check_pdf_file(file_name)
        return super().dropEvent(event)

    def add_files_to_check(self):
        """Функция при нажатии кнопки открыть pdf"""
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', "*.pdf")[0]
        self.check_pdf_file(fname)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    win = MainWindow()
    win.show()

    app.exec_()
