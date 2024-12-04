Разработать инструмент командной строки для учебного конфигурационного
языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из
входного формата в выходной. Синтаксические ошибки выявляются с выдачей
сообщений.


Входной текст на языке json принимается из стандартного ввода. Выходной
текст на учебном конфигурационном языке попадает в стандартный вывод.


Словари:


$[

 имя : значение,
 
 имя : значение,
 
 имя : значение,
 
 ...
 
]


Имена:

[A-Z]+

Значения:


• Числа.
• Строки.
• Словари.


Строки:


"Это строка"


Объявление константы на этапе трансляции:

var имя = значение


Вычисление константы на этапе трансляции:

^{имя}


Результатом вычисления константного выражения является значение.
Все конструкции учебного конфигурационного языка (с учетом их
возможной вложенности) должны быть покрыты тестами. Необходимо показать 3
примера описания конфигураций из разных предметных областей.


Структура файлов в проекте:


main.py - Главный файл программы, в котором мы преобразуем JSON файл в выдуманный конфигурационный файл

tests.py - Файл программы, который тестирует работоспособность всей программы.

sample1.json - JSON файл для проверки работоспособности программы

sample2.json - JSON файл для проверки выполнения ошибки


Пример скрипта для запуска программы: python main.py sample1.json


Содержимое файла sample1.json:

![Image alt1](https://github.com/BEZBIG/Configuration-Management.Homework-3/blob/master/pic/1.png)

Работа с инструментом командной строки для преобразования текста из JSON файла, используя sample1.json:

![Image alt2](https://github.com/BEZBIG/Configuration-Management.Homework-3/blob/master/pic/2.png)

Содержимое файла sample2.json:

![Image alt3](https://github.com/BEZBIG/Configuration-Management.Homework-3/blob/master/pic/3.png)

Работа с инструментом командной строки для преобразования текста из JSON файла, используя sample2.json (Вывод ошибки из-за отсутствия способа преобразования массива по заданию:

![Image alt4](https://github.com/BEZBIG/Configuration-Management.Homework-3/blob/master/pic/4.png)

Тесты программы: 

![Image alt5](https://github.com/BEZBIG/Configuration-Management.Homework-3/blob/master/pic/5.png)

![Image alt6](https://github.com/BEZBIG/Configuration-Management.Homework-3/blob/master/pic/6.png)

![Image alt7](https://github.com/BEZBIG/Configuration-Management.Homework-3/blob/master/pic/7.png)

![Image alt8](https://github.com/BEZBIG/Configuration-Management.Homework-3/blob/master/pic/8.png)

![Image alt9](https://github.com/BEZBIG/Configuration-Management.Homework-3/blob/master/pic/9.png)

Оперируем с тестовым файлом и проводим проверку:

![Image alt10](https://github.com/BEZBIG/Configuration-Management.Homework-3/blob/master/pic/10.png)
