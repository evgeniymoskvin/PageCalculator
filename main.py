import PyPDF2
import math

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

pdf_size_file = {}
a4_count = 0
normal_pages = 0
path = str(input("Введите путь к файлу: "))
list_pages = []
with open(path, 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    i = 0
    num_pages = len(pdf_reader.pages)
    for i in range(num_pages):
        box = pdf_reader.pages[i]
        width = math.ceil(float(box.mediabox.width) * 0.35273159)
        height = math.ceil(float(box.mediabox.height) * 0.35273159)
        list_pages.append([height, width])
        if width < height:
            small = width
            long = height
        else:
            small = height
            long = width
        for key, value in page_size_standard.items():
            if value[0] == small and value[1] == long:
                normal_pages += 1
                a4_count += value[2]
                try:
                    pdf_size_file[key] += 1
                except:
                    pdf_size_file[key] = 1

print(pdf_size_file)
print(f'Всего форматов а4: {a4_count}')
print(f'Всего страниц: {num_pages}')
print(f'Всего распознано страниц: {normal_pages}')
# C:\Users\E.I.Moskvin\Downloads\sp_131.13330.2020_stroitelnaya_klimatologiya(1).pdf
#  C:\Users\E.I.Moskvin\Downloads\4293851086.pdf

# pyside2-uic "you_file.ui" -o "your_file.py"