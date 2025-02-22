# Скриншоты
![image](https://github.com/user-attachments/assets/90b29d4e-5662-44fe-a1b1-687465dc7a10)
![image](https://github.com/user-attachments/assets/82111df6-89ad-4b4b-960d-054babee22dd)
# Описание метода сжатия
Алгоритм Шеннона-Фано — это один из первых алгоритмов сжатия, который был
сформулирован американскими учёными Клодом Шенноном и Робертом Фано. Этот метод
сжатия использует коды переменной длины, где часто встречающиеся символы кодируются
короткими двоичными последовательностями, а редко встречающиеся — более длинными.
Для того, чтобы выяснить частоту появления каждого символа, необходимо построить
частотную таблицу алфавита.
Модель кодирования строится в формате дерева префиксных кодов – бинарного
дерева, листьям которого сопоставлены символы входного потока кодера, а дуги размечены
0 и 1. Путь от вершины дерева до листа можно считать кодом символа, который хранится в
этом листе. Для построения этого дерева заранее составленную таблицу частот необходимо
отсортировать по убыванию частот. Затем нужно разбить эту таблицу на две части с
наиболее близкими суммами частот. Полученные две части таким же образом разбиваются.
В основе этого принципа лежит рекурсия. Таблицы будут разбиваться до тех пор, пока не
достигнут размера в 1 символ. Этот символ будет сопоставлен листу дерева.
# Исследование эффективности
Для исследования эффективности алгоритма сжатия были сгенерированы файлы
размером от 200 килобайт до 1000 килобайт с шагом 200 килобайт с мощностью алфавита
4, 16, 64, 128, 256 символов. Основным критерием эффективности сжатия является степень
сжатия. Ниже представлены графики зависимости степени сжатия от размера файла для каждой мощности алфавита.

![image](https://github.com/user-attachments/assets/8fe88f77-820e-4d4c-9927-02604c4ce68a)

Для исследования эффективности алгоритма распаковки были использованы сжатые
файлы из предыдущего эксперимента. Основным критерием эффективности распаковки
является время распаковки.

![image](https://github.com/user-attachments/assets/89872782-09d7-471f-a634-f434caae1929)
