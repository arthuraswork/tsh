tsh - Terminal decoration shell

- Грамматика
- Оформление
- Интеракция
- Анимации
- Модули

## Основы
Одна команда - одна строка, нет АСТ и все парсится и исполняется на лету 

## Грамматика
**Объявление переменных**
?set:X Y
```
?set:name John
?set:text Hello world
```
**Условия**
?(X operation Y) -> THEN || ELSE

```
?(var operation yes) -> yes
?(var operation yes) -> yes || no
```
==
!=
in
starts 
ends

Также есть проверка переменных 
exists?

**Комментарии**
```
//комментарий
текст //комментарий
текст //комментарий --nocomment #обработает как обычный текст
```
**Интерполяция**
```
?set:name Вася
Hello, name
```

**Вызов функций**
fork(PATH) NONE/-i NONE/{args}
```
fork(./hello)
fork(./hello) -i # Выводит путь до файла перед вызовом
fork(./hello) {a,b,c} # Передает аргументы в формате bash, но индексация с 0 ($0,$1,$2)
fork(./hello) {a,b,c} -i
```
Можно также вызывать баш код
```
#!/bin/bash sudo rm -rf /

и исполнять пайтон код

#!/python-unsafe subprocess.run("sudo rm -rf /", shell=True)
```

## Оформление
**Цвета**
[color:red]Hello

**Стили**
[style:bold]Hello

**Фон**
[bg:red]Hello

**Сброс**
[style:reset]Hello
```
[style:bold]Hello[style:reset]
[color:red][bg:red][style:bold]Hello[style:reset]
```

Подробнее в в src/consts.py

## Анимации

?draw{[Этапы через ',']}([Длительность])[Модификаток или ничего]

```
?draw{. ,..,.:,.}(1) #лоадер в одну секунду
?draw{#,##,###,####}(0.5).each #прогрессбар в 2 секунды
?draw{#,##,###,####}(1).div #прогрессбар в 1 секунду
```

## Интерация

?:[ТИП](Сообщение){[Варианты | Ничего]} >> [Переменная]

**Типы интеракций**

```
?:Select(){} #Выбор варианта
?:Confirm() #Y/n
?:Complete(){} #Автодополнение
```

подробнее в src/consts.py

## Модули
Импорт через #include <[Модуль]::[Функция]>
Использование через
[Название]([Аргумент])!
доступно с ?set:VAR
```
#include <objects::time>
?set:time time()!
Сейчас time 
```

Чтобы добавить модуль, нужно в папку stdlib и добавить свои файлы или функции с помощью класса define.module, подключая через src/modules с помощью импорта файла и modules.add()
