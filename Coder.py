import os
import struct
import sys
import BinaryTree
import pickle


class Coder:
    def __init__(self):
        self.__freq = []  # частоты символов
        self.__tree = BinaryTree.BinaryTree()  # дерево с кодами
        self.__codes = dict()  # словарь с кодами
        # self.__result = []
        self.__codeToWrite = []

    # функция кодирования (построение дерева и кодирование входного потока)
    def encode(self, origin_filename, result_filename):
        """
        Функция побайтово считывает исходный файл, строит словарь частот. Внутри вызывается приватная функция
        __encode(freqs, code), которая на основе словаря частот формирует словарь и дерево кодов. Затем открывается
        результирующий файл, куда записывается сериализованный словарь частот со сдвигом 8 от начала файла. Исходя из
        текущего положения курсора вычисляется размер записанного словаря частот, и это значение записывается в начало
        результирующего файла. Затем снова открывается и считывается побайтово исходный файл. Каждый байт кодируется
        значеним из словаря __codes. Финальный байт, если такой существует, дополняется необходимым количеством нулей.
        Формирующийся код записывается в результирующий файл побайтово с помощью функции __write_code(code, file).
        Параллельно с этим подсчитывается длина формирующегося кода (количество бит). Итоговая длина кода записывается в
        результирующий файл со сдвигом 4 от начала.
        :param origin_filename: путь к исходному файлу
        :param result_filename: путь к результирующему файлу
        :return: True - успех, False - ошибка
        """
        if os.path.exists(result_filename):
            os.remove(result_filename)
        # сортировка пар "символ - частота" по убыванию частоты
        dictionary = dict()
        with open(origin_filename, "rb") as origin:  # считывание байтов из исходного файла для построения статистики
            while True:
                byte = origin.read(1)
                if not byte:
                    break
                if byte in dictionary.keys():
                    dictionary[byte] += 1
                else:
                    dictionary[byte] = 1
        sorted_dictionary = sorted(dictionary.items(), key=lambda item: item[1], reverse=True)  # сортировка словаря
        self.__freq = sorted_dictionary  # сохранение словаря частот
        # вызов рекурсивной функции построения дерева
        self.__encode(self.__freq)
        # сохранение результатат кодирования
        self.__tree.back_to_root()
        with open(result_filename,
                  "wb+") as result_file:
            result_file.seek(8, 0)
            serialized_freq = pickle.dumps(self.__freq)
            result_file.write(serialized_freq)
            freq_size = result_file.tell() - 8
            result_file.seek(0, 0)
            packed_size = struct.pack('i', freq_size)
            result_file.write(packed_size)
        # region Кодирование входного потока на основе словаря "символ - код"
        bits_to_read = 0
        with open(origin_filename, "rb") as origin, open(result_filename, "ab+") as result_file:
            while True:
                byte = origin.read(1)
                if not byte:
                    return False
                try:
                    current_code = self.__codes[byte]
                    bits_to_read += len(current_code)
                except KeyError:
                    break
                current_code = list(current_code)
                self.__write_code(current_code, result_file)

            # region Добавление в конец закодированного потока символа конца файла (~)
            if len(self.__codeToWrite) != 0:
                while len(self.__codeToWrite) < 8:
                    self.__codeToWrite.append('0')
                byte = ""
                for item in self.__codeToWrite:
                    byte += item

                byte = struct.pack('B', int(byte, 2))
                result_file.write(byte)

        with open(result_filename, "r+b") as file:
            file.seek(4, 0)
            packed_bits = struct.pack('i', bits_to_read)
            file.write(packed_bits)
            file.seek(0, 0)
        return True
        # endregion
        # endregion

    # рекурсивная функция построения дерева на основе входного потока
    def __encode(self, freqs=None, code=""):
        # разбиение частот на два списка и вычисление наименьшей разницы в суммах
        difference = sys.maxsize
        middle_index = 0
        left_sum = 0
        for i in range(0, len(freqs) - 1):
            left_sum += freqs[i][1]
            right_sum = 0
            for j in range(i + 1, len(freqs)):
                right_sum += freqs[j][1]
            if abs(left_sum - right_sum) <= difference:
                difference = abs(left_sum - right_sum)
                middle_index = i
        # рекурсивные вызовы функции
        if len(freqs) == 1:  # добавление символа к дереву и результирующей строке
            self.__tree.insert_data([freqs[0][0], code])
            self.__codes[freqs[0][0]] = code
        else:
            self.__tree.add_left()
            temp = code
            temp += "0"
            self.__encode(freqs[:middle_index + 1], temp)
            self.__tree.add_right()
            temp = code
            temp += "1"
            self.__encode(freqs[middle_index + 1:], temp)
        self.__tree.back_to_parent()

    def get_codes(self):  # получение списка пар "символ-частота" из поля __codes
        return self.__codes

    def get_code(self):  # получение списка пар "символ-частота" из листьев дерева
        return self.__tree.get_leaf_values()

    def decode(self, origin_filename, result_filename):
        """
        Функция декодирования в начале работы считывает два числа типа integer из начала файла. Первое число --
        размер словаря частот, второе число -- длина закодированной последовательности в битах. Затем считывается и
        десериализуется словарь частот. Создаются экземпляры словаря кодов и дерева кодов. С помощью функции
        __encode(freqs) строится дерево кодов на основе словаря частот. В цикле while исходный файл считывается
        побайтово. Каждый байт преобразуется в строку вида "01010101". Эта строка перебирается, и осуществляется
        проход по дереву на основе считанных битов. При считывании очередного бита к переменной read_bit_count
        прибавляется единица, а их переменной bits_to_read вычитается единицы.Если байт полностью перебран, то
        считывается следующий байт. Это отслеживает переменная read_bit_count. Окончание закодированный
        последовательности наступает тогда, когда переменная bits_to_read становится равной 0.
        :param origin_filename: путь к исходному файлу
        :param result_filename: путь к результирующему файлу
        :return: True
        """
        if os.path.exists(result_filename):
            os.remove(result_filename)
        self.__tree.back_to_root()
        with open(origin_filename, "rb") as file, open(result_filename, "ab+") as result_filename:
            bytes_of_dictionary = struct.unpack("i", file.read(4))[0]
            bits_to_read = struct.unpack("i", file.read(4))[0]
            self.__freq = pickle.loads(file.read(bytes_of_dictionary))
            self.__tree = BinaryTree.BinaryTree()  # дерево с кодами
            self.__codes = dict()  # словарь с кодами
            self.__encode(self.__freq)
            read_bit_count = 8
            byte = ""
            while bits_to_read > 0:  # перебор строки нулей и единиц с проходом по дереву до листьев
                if read_bit_count == 8:
                    byte = file.read(1)
                    if not byte:
                        break
                    byte = struct.unpack('B', byte)[0]
                    byte = bin(byte)[2:].zfill(8)
                    read_bit_count = 0
                for item in byte:
                    read_bit_count += 1
                    bits_to_read -= 1
                    if item == "0" and self.__tree.get_left() is not None:
                        self.__tree.set_current(self.__tree.get_left())
                        if self.__tree.get_current().get_right() is None and self.__tree.get_current().get_left() is None:
                            result = self.__tree.get_current().get_data()[0]
                            self.__tree.back_to_root()
                            result = struct.pack('B', ord(result))
                            result_filename.write(result)
                            if bits_to_read == 0:
                                break
                    elif item == "1" and self.__tree.get_right() is not None:
                        self.__tree.set_current(self.__tree.get_right())
                        if self.__tree.get_current().get_right() is None and self.__tree.get_current().get_left() is None:
                            result = self.__tree.get_current().get_data()[0]
                            self.__tree.back_to_root()
                            self.__tree.back_to_root()
                            result = struct.pack('B', ord(result))
                            result_filename.write(result)
                            if bits_to_read == 0:
                                break
        return True

    def __write_code(self, code, file):
        """
        На вход подается строка из случайного количества 0 и 1. Элементы строки добавляются в список codeToWrite
        Если в codeToWrite больше 8 элементо (8 бит), то открывается файл для записи и в него записываются все
        байты из начала списка codeToWrite. Допустим в codeToWrite 20 элементов. В файл будут записаны 16 элементов
        (2 байта), в codeToWrite останется 4 элемента
        :param code: код символа для записи
        :param file: поток
        """
        for item in code:
            self.__codeToWrite.append(item)
        if len(self.__codeToWrite) > 8:
            len_to_write = len(self.__codeToWrite)
            eight_number = len_to_write // 8
            for i in range(eight_number):
                byte = ""
                for j in range(0, 8):
                    byte += self.__codeToWrite[j]
                del self.__codeToWrite[0:8]
                byte = struct.pack('B', int(byte, 2))
                file.write(byte)
