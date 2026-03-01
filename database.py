import sqlite3
import sys
import os
from pathlib import Path
import csv
import time
DB_PATH = os.path.join(os.path.dirname(__file__), 'vocabulary_bot.db')
COMMON_WORDS_CSV = "common_words.csv"


#Инициализация всех таблиц базы данных
def init_common_words():
    if not Path(COMMON_WORDS_CSV).exists():
        common_words = {
            'A1': [
                ('hello', 'привет'), ('book', 'книга'), ('cat', 'кот'), ('dog', 'собака'), ('apple', 'яблоко'),
                ('car', 'машина'), ('house', 'дом'), ('water', 'вода'), ('food', 'еда'), ('friend', 'друг'),
                ('school', 'школа'), ('family', 'семья'), ('day', 'день'), ('night', 'ночь'), ('sun', 'солнце'),
                ('moon', 'луна'), ('tree', 'дерево'), ('flower', 'цветок'), ('bird', 'птица'), ('fish', 'рыба'),
                ('milk', 'молоко'), ('bread', 'хлеб'), ('chair', 'стул'), ('table', 'стол'), ('pen', 'ручка'),
                ('phone', 'телефон'), ('computer', 'компьютер'), ('window', 'окно'), ('door', 'дверь'), ('street', 'улица'),
                ('city', 'город'), ('country', 'страна'), ('money', 'деньги'), ('time', 'время'), ('year', 'год'),
                ('week', 'неделя'), ('month', 'месяц'), ('morning', 'утро'), ('evening', 'вечер'), ('cold', 'холодный'),
                ('hot', 'горячий'), ('big', 'большой'), ('small', 'маленький'), ('happy', 'счастливый'), ('sad', 'грустный'),
                ('fast', 'быстрый'), ('slow', 'медленный'), ('new', 'новый'), ('old', 'старый'), ('good', 'хороший'),
                ('bad', 'плохой'), ('yes', 'да'), ('no', 'нет'), ('please', 'пожалуйста'), ('thank you', 'спасибо'),
                ('sorry', 'извините'), ('help', 'помощь'), ('stop', 'стоп'), ('go', 'идти'), ('come', 'приходить'),
                ('see', 'видеть'), ('hear', 'слышать'), ('eat', 'есть'), ('drink', 'пить'), ('sleep', 'спать'),
                ('read', 'читать'), ('write', 'писать'), ('run', 'бежать'), ('walk', 'ходить'), ('play', 'играть'),
                ('work', 'работать'), ('love', 'любить'), ('like', 'нравиться'), ('want', 'хотеть'), ('need', 'нуждаться'),
                ('think', 'думать'), ('know', 'знать'), ('understand', 'понимать'), ('learn', 'учить'), ('teach', 'учить'),
                ('open', 'открывать'), ('close', 'закрывать'), ('buy', 'покупать'), ('sell', 'продавать'), ('wait', 'ждать'),
                ('call', 'звонить'), ('answer', 'отвечать'), ('ask', 'спрашивать'), ('tell', 'рассказывать'), ('show', 'показывать'),
                ('clean', 'чистить'), ('wash', 'мыть'), ('drive', 'водить'), ('fly', 'летать'), ('swim', 'плавать'),
                ('jump', 'прыгать'), ('sit', 'сидеть'), ('stand', 'стоять'), ('turn', 'поворачивать'), ('help', 'помогать')

            ],
            "A2": [
                ('always', 'всегда'), ('because', 'потому что'), ('before', 'до'), ('between', 'между'),
                ('breakfast', 'завтрак'),
                ('busy', 'занятой'), ('clean', 'чистый'), ('clothes', 'одежда'), ('cold', 'холодный'),
                ('dance', 'танцевать'),
                ('different', 'разный'), ('dinner', 'ужин'), ('early', 'рано'), ('easy', 'легкий'),
                ('enjoy', 'наслаждаться'),
                ('family', 'семья'), ('fast', 'быстрый'), ('find', 'находить'), ('finish', 'заканчивать'),
                ('friend', 'друг'),
                ('fun', 'веселье'), ('game', 'игра'), ('garden', 'сад'), ('get', 'получать'), ('give', 'давать'),
                ('go', 'идти'), ('good', 'хороший'), ('happy', 'счастливый'), ('have', 'иметь'), ('help', 'помогать'),
                ('home', 'дом'), ('house', 'дом'), ('interesting', 'интересный'), ('job', 'работа'), ('know', 'знать'),
                ('learn', 'учить'), ('like', 'нравиться'), ('listen', 'слушать'), ('live', 'жить'), ('long', 'длинный'),
                ('love', 'любить'), ('make', 'делать'), ('meet', 'встречать'), ('morning', 'утро'), ('music', 'музыка'),
                ('need', 'нуждаться'), ('new', 'новый'), ('night', 'ночь'), ('often', 'часто'), ('open', 'открывать'),
                ('party', 'вечеринка'), ('play', 'играть'), ('quiet', 'тихий'), ('read', 'читать'), ('ride', 'ездить'),
                ('run', 'бегать'), ('say', 'говорить'), ('school', 'школа'), ('see', 'видеть'), ('sell', 'продавать'),
                ('send', 'отправлять'), ('shop', 'магазин'), ('sit', 'сидеть'), ('sleep', 'спать'),
                ('small', 'маленький'),
                ('start', 'начинать'), ('stop', 'останавливаться'), ('study', 'учиться'), ('take', 'брать'),
                ('talk', 'говорить'),
                ('teach', 'учить'), ('tell', 'рассказывать'), ('think', 'думать'), ('travel', 'путешествовать'),
                ('try', 'пытаться'),
                ('use', 'использовать'), ('wait', 'ждать'), ('walk', 'ходить'), ('want', 'хотеть'),
                ('watch', 'смотреть'),
                ('work', 'работать'), ('write', 'писать'), ('young', 'молодой'), ('always', 'всегда'),
                ('because', 'потому что'),
                ('before', 'до'), ('between', 'между'), ('breakfast', 'завтрак'), ('busy', 'занятой'),
                ('clean', 'чистый'),
                ('clothes', 'одежда'), ('cold', 'холодный'), ('dance', 'танцевать'), ('different', 'разный'),
                ('dinner', 'ужин'),
                ('early', 'рано'), ('easy', 'легкий'), ('enjoy', 'наслаждаться'), ('family', 'семья'),
                ('fast', 'быстрый')
            ],

            "B1": [
                ('ability', 'способность'), ('accident', 'авария'), ('advice', 'совет'), ('afraid', 'испуганный'),
                ('agree', 'соглашаться'),
                ('allow', 'позволять'), ('angry', 'злой'), ('arrive', 'прибывать'), ('attention', 'внимание'),
                ('avoid', 'избегать'),
                ('beautiful', 'красивый'), ('believe', 'верить'), ('borrow', 'занимать'), ('break', 'ломать'),
                ('bring', 'приносить'),
                ('build', 'строить'), ('busy', 'занятый'), ('call', 'звонить'), ('careful', 'осторожный'),
                ('change', 'менять'),
                ('choose', 'выбирать'), ('clean', 'чистый'), ('close', 'закрывать'), ('collect', 'собирать'),
                ('continue', 'продолжать'),
                ('correct', 'правильный'), ('cost', 'стоимость'), ('count', 'считать'), ('decide', 'решать'),
                ('describe', 'описывать'),
                ('develop', 'развивать'), ('different', 'разный'), ('difficult', 'трудный'),
                ('discover', 'обнаруживать'), ('divide', 'делить'),
                ('drive', 'водить'), ('drop', 'падать'), ('early', 'рано'), ('easy', 'легкий'),
                ('enjoy', 'наслаждаться'),
                ('enough', 'достаточно'), ('explain', 'объяснять'), ('fail', 'терпеть неудачу'), ('fall', 'падать'),
                ('feel', 'чувствовать'),
                ('fill', 'заполнять'), ('find', 'находить'), ('finish', 'заканчивать'), ('follow', 'следовать'),
                ('forget', 'забывать'),
                ('form', 'форма'), ('free', 'свободный'), ('friend', 'друг'), ('fun', 'веселье'), ('game', 'игра'),
                ('get', 'получать'), ('give', 'давать'), ('go', 'идти'), ('good', 'хороший'), ('great', 'великий'),
                ('guess', 'угадывать'), ('happy', 'счастливый'), ('hate', 'ненавидеть'), ('have', 'иметь'),
                ('hear', 'слышать'),
                ('help', 'помогать'), ('hope', 'надеяться'), ('hurt', 'ранить'), ('important', 'важный'),
                ('increase', 'увеличивать'),
                ('interest', 'интерес'), ('invite', 'приглашать'), ('join', 'присоединяться'), ('jump', 'прыгать'),
                ('keep', 'держать'),
                ('kind', 'добрый'), ('know', 'знать'), ('laugh', 'смеяться'), ('learn', 'учить'), ('leave', 'покидать'),
                ('like', 'нравиться'), ('listen', 'слушать'), ('live', 'жить'), ('look', 'смотреть'),
                ('lose', 'терять'),
                ('love', 'любить'), ('make', 'делать'), ('mean', 'значить'), ('meet', 'встречать'), ('miss', 'скучать'),
                ('move', 'двигаться'), ('need', 'нуждаться'), ('open', 'открывать'), ('order', 'заказывать'),
                ('pay', 'платить'),
                ('play', 'играть'), ('prefer', 'предпочитать'), ('prepare', 'готовить'), ('put', 'класть'),
                ('read', 'читать'),
                ('receive', 'получать'), ('remember', 'запоминать'), ('run', 'бегать'), ('say', 'говорить'),
                ('see', 'видеть'),
                ('sell', 'продавать'), ('send', 'отправлять'), ('show', 'показывать'), ('sit', 'сидеть'),
                ('sleep', 'спать'),
                ('smile', 'улыбаться'), ('start', 'начинать'), ('stay', 'оставаться'), ('stop', 'останавливаться'),
                ('study', 'учиться'),
                ('take', 'брать'), ('talk', 'говорить'), ('teach', 'учить'), ('tell', 'рассказывать'),
                ('think', 'думать'),
                ('try', 'пытаться'), ('turn', 'поворачивать'), ('understand', 'понимать'), ('use', 'использовать'),
                ('wait', 'ждать'),
                ('walk', 'ходить'), ('want', 'хотеть'), ('watch', 'смотреть'), ('work', 'работать'), ('write', 'писать')
            ],

            "B2": [
                ('abstract', 'абстрактный'), ('acquire', 'приобретать'), ('adapt', 'адаптировать'),
                ('adequate', 'адекватный'),
                ('adjust', 'регулировать'), ('advocate', 'защищать'), ('allocate', 'распределять'),
                ('ambiguous', 'двусмысленный'),
                ('analyse', 'анализировать'), ('anticipate', 'предвидеть'), ('apparent', 'очевидный'),
                ('appreciate', 'ценить'),
                ('approach', 'подход'), ('appropriate', 'соответствующий'), ('approximate', 'приблизительный'),
                ('arbitrary', 'произвольный'),
                ('assess', 'оценивать'), ('assign', 'назначать'), ('assume', 'предполагать'), ('attach', 'прикреплять'),
                ('attain', 'достигать'), ('attribute', 'приписывать'), ('aware', 'осведомленный'),
                ('benefit', 'выгода'),
                ('bias', 'предвзятость'), ('brief', 'краткий'), ('capable', 'способный'), ('capacity', 'вместимость'),
                ('cease', 'прекращать'), ('challenge', 'вызов'), ('circumstance', 'обстоятельство'),
                ('coherent', 'связный'),
                ('coincide', 'совпадать'), ('collapse', 'крах'), ('colleague', 'коллега'), ('commence', 'начинать'),
                ('commit', 'совершать'), ('compatible', 'совместимый'), ('compile', 'составлять'),
                ('complement', 'дополнять'),
                ('comprehensive', 'всесторонний'), ('conceive', 'задумывать'), ('conclude', 'заключать'),
                ('concurrent', 'одновременный'),
                ('confine', 'ограничивать'), ('confirm', 'подтверждать'), ('conform', 'соответствовать'),
                ('confront', 'сталкиваться'),
                ('consequent', 'следующий'), ('considerable', 'значительный'), ('consistent', 'последовательный'),
                ('constitute', 'составлять'),
                ('constrain', 'ограничивать'), ('construct', 'строить'), ('consult', 'консультироваться'),
                ('consume', 'потреблять'),
                ('contemporary', 'современный'), ('contradict', 'противоречить'), ('contribute', 'вносить вклад'),
                ('controversy', 'спор'),
                ('convene', 'созывать'), ('converse', 'разговаривать'), ('convert', 'преобразовывать'),
                ('convince', 'убеждать'),
                ('cope', 'справляться'), ('corporate', 'корпоративный'), ('correspond', 'соответствовать'),
                ('criteria', 'критерии'),
                ('crucial', 'ключевой'), ('cumulative', 'накопительный'), ('deduce', 'делать вывод'),
                ('definite', 'определенный'),
                ('demonstrate', 'демонстрировать'), ('denote', 'обозначать'), ('derive', 'происходить'),
                ('designate', 'назначать'),
                ('despite', 'несмотря на'), ('detect', 'обнаруживать'), ('deviate', 'отклоняться'),
                ('devote', 'посвящать'),
                ('diminish', 'уменьшать'), ('discrete', 'отдельный'), ('displace', 'замещать'),
                ('display', 'показывать'),
                ('dispose', 'распоряжаться'), ('distinct', 'отличительный'), ('distort', 'искажать'),
                ('diverse', 'разнообразный'),
                ('document', 'документировать'), ('dominate', 'доминировать'), ('draft', 'черновик'),
                ('drastic', 'радикальный'),
                ('elaborate', 'разрабатывать'), ('element', 'элемент'), ('eliminate', 'устранять'),
                ('emerge', 'появляться'),
                ('emphasize', 'подчеркивать'), ('enable', 'позволять'), ('encounter', 'сталкиваться'),
                ('enhance', 'улучшать'),
                ('enormous', 'огромный'), ('ensure', 'обеспечивать'), ('entity', 'сущность'),
                ('equate', 'приравнивать'),
                ('equivalent', 'эквивалентный'), ('eradicate', 'искоренять'), ('establish', 'устанавливать'),
                ('estimate', 'оценивать'),
                ('evaluate', 'оценивать'), ('evident', 'очевидный'), ('exclude', 'исключать'),
                ('exhibit', 'выставлять'),
                ('expand', 'расширять'), ('expose', 'подвергать'), ('external', 'внешний'), ('extract', 'извлекать'),
                ('facilitate', 'облегчать'), ('factor', 'фактор'), ('feature', 'особенность'),
                ('federal', 'федеральный'),
                ('fluctuate', 'колебаться'), ('focus', 'сосредоточиться'), ('format', 'формат'),
                ('found', 'основывать'),
                ('framework', 'структура'), ('fundamental', 'фундаментальный'), ('generate', 'производить'),
                ('grade', 'оценка'),
                ('grant', 'предоставлять'), ('guarantee', 'гарантировать'), ('highlight', 'выделять'),
                ('hypothesis', 'гипотеза'),
                ('identical', 'идентичный'), ('identify', 'опознавать'), ('ignore', 'игнорировать'),
                ('illustrate', 'иллюстрировать'),
                ('impact', 'влияние'), ('implement', 'осуществлять'), ('imply', 'подразумевать'),
                ('incentive', 'стимул'),
                ('incidence', 'частота'), ('incline', 'склоняться'), ('include', 'включать'), ('income', 'доход'),
                ('incorporate', 'включать'), ('indicate', 'указывать'), ('induce', 'вызывать'),
                ('inevitable', 'неизбежный'),
                ('infer', 'делать вывод'), ('inhibit', 'подавлять'), ('initial', 'первоначальный'),
                ('initiate', 'начинать'),
                ('innovate', 'внедрять новшества'), ('input', 'ввод'), ('insert', 'вставлять'),
                ('inspect', 'осматривать'),
                ('instance', 'пример'), ('institute', 'учреждение'), ('instruct', 'инструктировать'),
                ('integrate', 'интегрировать'),
                ('intend', 'намереваться'), ('interact', 'взаимодействовать'), ('interfere', 'мешать'),
                ('interpret', 'интерпретировать'),
                ('interval', 'интервал'), ('intervene', 'вмешиваться'), ('intrinsic', 'внутренний'),
                ('investigate', 'исследовать'),
                ('involve', 'вовлекать'), ('isolate', 'изолировать'), ('issue', 'вопрос'), ('item', 'предмет'),
                ('journal', 'журнал'), ('justify', 'оправдывать'), ('label', 'этикетка'), ('labour', 'труд'),
                ('layer', 'слой'),
                ('legal', 'законный'), ('legislate', 'законодательствовать'), ('levy', 'налог'),
                ('liberal', 'либеральный'),
                ('license', 'лицензия'), ('link', 'связь'), ('locate', 'располагать'), ('logic', 'логика'),
                ('maintain', 'поддерживать'),
                ('major', 'главный'), ('manipulate', 'манипулировать'), ('manual', 'руководство'), ('margin', 'маржа'),
                ('mediate', 'посредничать'), ('medical', 'медицинский'), ('military', 'военный'),
                ('minimal', 'минимальный'),
                ('minimize', 'минимизировать'), ('minor', 'незначительный'), ('mode', 'режим'), ('modify', 'изменять'),
                ('monitor', 'контролировать'), ('motivate', 'мотивировать'), ('neutral', 'нейтральный'),
                ('notion', 'понятие'),
                ('objective', 'цель'), ('oblige', 'обязывать'), ('obtain', 'получать'), ('occupy', 'занимать'),
                ('occur', 'происходить'),
                ('offset', 'компенсировать'), ('ongoing', 'текущий'), ('option', 'вариант'), ('output', 'выход'),
                ('overall', 'в целом'),
                ('overlap', 'перекрывать'), ('panel', 'комиссия'), ('paradox', 'парадокс'), ('parameter', 'параметр'),
                ('participate', 'участвовать'), ('partner', 'партнер'), ('passive', 'пассивный'),
                ('perceive', 'воспринимать'),
                ('persist', 'упорствовать'), ('persuade', 'убеждать'), ('phase', 'фаза'), ('phenomenon', 'явление'),
                ('policy', 'политика'), ('portion', 'часть'), ('pose', 'ставить'), ('positive', 'положительный'),
                ('potential', 'потенциальный'), ('precede', 'предшествовать'), ('precise', 'точный'),
                ('predict', 'предсказывать'),
                ('preliminary', 'предварительный'), ('presume', 'предполагать'), ('previous', 'предыдущий'),
                ('primary', 'первичный'),
                ('prior', 'предшествующий'), ('priority', 'приоритет'), ('proceed', 'продолжать'),
                ('process', 'процесс'),
                ('professional', 'профессиональный'), ('profit', 'прибыль'), ('project', 'проект'),
                ('promote', 'продвигать'),
                ('prompt', 'побуждать'), ('proportion', 'пропорция'), ('prospect', 'перспектива'),
                ('protocol', 'протокол'),
                ('publish', 'публиковать'), ('purchase', 'покупать'), ('pursue', 'преследовать'),
                ('qualify', 'квалифицировать'),
                ('radical', 'радикальный'), ('random', 'случайный'), ('range', 'диапазон'), ('ratio', 'соотношение'),
                ('rational', 'рациональный'), ('react', 'реагировать'), ('recover', 'восстанавливаться'),
                ('refine', 'усовершенствовать'),
                ('reflect', 'отражать'), ('reform', 'реформа'), ('regime', 'режим'), ('register', 'регистрировать'),
                ('regulate', 'регулировать'), ('reinforce', 'усиливать'), ('reject', 'отклонять'),
                ('relate', 'относиться'),
                ('relevant', 'соответствующий'), ('rely', 'полагаться'), ('remove', 'удалять'), ('replace', 'заменять'),
                ('represent', 'представлять'), ('reproduce', 'воспроизводить'), ('require', 'требовать'),
                ('reside', 'проживать'),
                ('resolve', 'решать'), ('resource', 'ресурс'), ('respond', 'отвечать'), ('restore', 'восстанавливать'),
                ('restrict', 'ограничивать'), ('retain', 'сохранять'), ('reveal', 'раскрывать'),
                ('reverse', 'обращать'),
                ('review', 'обзор'), ('revise', 'пересматривать'), ('revolution', 'революция'), ('role', 'роль'),
                ('route', 'маршрут'), ('scheme', 'схема'), ('scope', 'область'), ('sector', 'сектор'),
                ('secure', 'обеспечивать'), ('select', 'выбирать'), ('sequence', 'последовательность'),
                ('shift', 'сдвиг'),
                ('significant', 'значительный'), ('similar', 'похожий'), ('simulate', 'имитировать'),
                ('sophisticated', 'сложный'),
                ('specify', 'уточнять'), ('spectrum', 'спектр'), ('stable', 'стабильный'), ('status', 'статус'),
                ('strategy', 'стратегия'), ('stress', 'напряжение'), ('structure', 'структура'),
                ('subsequent', 'последующий'),
                ('substitute', 'заменять'), ('sufficient', 'достаточный'), ('summary', 'резюме'),
                ('supply', 'поставка'),
                ('survey', 'опрос'), ('sustain', 'поддерживать'), ('symbol', 'символ'), ('target', 'цель'),
                ('technical', 'технический'), ('technology', 'технология'), ('temporary', 'временный'),
                ('terminate', 'прекращать'),
                ('theory', 'теория'), ('topic', 'тема'), ('trace', 'след'), ('transmit', 'передавать'),
                ('trend', 'тенденция'), ('ultimate', 'окончательный'), ('undergo', 'претерпевать'),
                ('underlie', 'лежать в основе'),
                ('unique', 'уникальный'), ('valid', 'действительный'), ('variable', 'переменный'),
                ('vehicle', 'транспортное средство'),
                ('version', 'версия'), ('via', 'через'), ('visible', 'видимый'), ('volume', 'объем'),
                ('widespread', 'широко распространенный'), ('withdraw', 'выводить'), ('witness', 'свидетель'),
                ('zone', 'зона')
            ],

            "C1": [
                ('abandon', 'покидать'), ('abstract', 'абстрактный'), ('accommodate', 'вмещать'),
                ('accumulate', 'накоплять'),
                ('acknowledge', 'признавать'), ('acquire', 'приобретать'), ('adapt', 'адаптировать'),
                ('adequate', 'адекватный'),
                ('adjacent', 'прилегающий'), ('advocate', 'защищать'), ('aesthetic', 'эстетический'),
                ('allocate', 'распределять'),
                ('alter', 'изменять'), ('ambiguous', 'двусмысленный'), ('analyse', 'анализировать'),
                ('anticipate', 'ожидать'),
                ('apparent', 'очевидный'), ('appreciate', 'ценить'), ('arbitrary', 'произвольный'),
                ('assert', 'утверждать'),
                ('assess', 'оценивать'), ('assign', 'назначать'), ('assume', 'предполагать'), ('attain', 'достигать'),
                ('attribute', 'приписывать'), ('authorize', 'уполномочивать'), ('beneficial', 'выгодный'),
                ('bias', 'предвзятость'),
                ('brief', 'краткий'), ('capable', 'способный'), ('capacity', 'вместимость'),
                ('catalyst', 'катализатор'),
                ('cease', 'прекращать'), ('chronological', 'хронологический'), ('circumvent', 'обходить'),
                ('coherent', 'связный'),
                ('coincide', 'совпадать'), ('collaborate', 'сотрудничать'), ('commence', 'начинать'),
                ('commit', 'совершать'),
                ('compatible', 'совместимый'), ('compile', 'составлять'), ('complement', 'дополнять'),
                ('comprehensive', 'всесторонний'),
                ('conceive', 'задумывать'), ('concur', 'соглашаться'), ('condone', 'прощать'),
                ('confer', 'присваивать'),
                ('confine', 'ограничивать'), ('conform', 'соответствовать'), ('conjecture', 'догадка'),
                ('consolidate', 'укреплять'),
                ('contemplate', 'созерцать'), ('contend', 'утверждать'), ('contradict', 'противоречить'),
                ('contribute', 'вносить вклад'),
                ('convene', 'созывать'), ('converge', 'сходиться'), ('convey', 'передавать'), ('convince', 'убеждать'),
                ('corroborate', 'подтверждать'), ('criterion', 'критерий'), ('culminate', 'завершаться'),
                ('cumulative', 'накопительный'),
                ('debris', 'обломки'), ('deceive', 'обманывать'), ('deduce', 'делать вывод'),
                ('deficient', 'недостаточный'),
                ('deliberate', 'обдуманный'), ('delineate', 'очерчивать'), ('demise', 'кончина'),
                ('denote', 'обозначать'),
                ('depict', 'изображать'), ('derive', 'происходить'), ('detrimental', 'вредный'),
                ('deviate', 'отклоняться'),
                ('digress', 'отклоняться'), ('diminish', 'уменьшать'), ('discrepancy', 'несоответствие'),
                ('discretion', 'осмотрительность'),
                ('disdain', 'презрение'), ('disparage', 'унижать'), ('dispel', 'рассеивать'),
                ('disseminate', 'распространять'),
                ('dissent', 'разногласие'), ('diverge', 'расходиться'), ('divulge', 'разглашать'),
                ('elaborate', 'разрабатывать'),
                ('elicit', 'вызывать'), ('elude', 'избегать'), ('eminent', 'выдающийся'), ('emulate', 'подражать'),
                ('encompass', 'охватывать'), ('endorse', 'одобрять'), ('engender', 'порождать'),
                ('enhance', 'улучшать'),
                ('enigma', 'загадка'), ('entail', 'влечь за собой'), ('enumerate', 'перечислять'),
                ('epitome', 'воплощение'),
                ('equivocal', 'двусмысленный'), ('eradicate', 'искоренять'), ('esoteric', 'эзотерический'),
                ('evoke', 'вызывать'),
                ('exacerbate', 'усугублять'), ('exemplify', 'иллюстрировать'), ('exhort', 'призывать'),
                ('exonerate', 'оправдывать'),
                ('expedite', 'ускорять'), ('explicit', 'явный'), ('extrapolate', 'экстраполировать'),
                ('facilitate', 'облегчать'),
                ('feasible', 'осуществимый'), ('fervent', 'пламенный'), ('fluctuate', 'колебаться'),
                ('formidable', 'грозный'),
                ('fortuitous', 'случайный'), ('foster', 'поощрять'), ('frivolous', 'легкомысленный'),
                ('futile', 'бесполезный'),
                ('garrulous', 'болтливый'), ('gratuitous', 'беспричинный'), ('gregarious', 'общительный'),
                ('hackneyed', 'избитый'),
                ('harbinger', 'предвестник'), ('heed', 'внимание'), ('heresy', 'ересь'), ('hiatus', 'перерыв'),
                ('homogeneous', 'однородный'), ('hypothetical', 'гипотетический'), ('iconoclast', 'иконоборец'),
                ('idiosyncrasy', 'особенность'),
                ('illicit', 'незаконный'), ('imminent', 'неминуемый'), ('immutable', 'неизменный'),
                ('impede', 'препятствовать'),
                ('implicit', 'косвенный'), ('impromptu', 'экспромтом'), ('inadvertent', 'непреднамеренный'),
                ('incessant', 'непрерывный'),
                ('incipient', 'начинающийся'), ('indigenous', 'коренной'), ('indispensable', 'незаменимый'),
                ('ineffable', 'невыразимый'),
                ('inexorable', 'неумолимый'), ('infamous', 'печально известный'), ('innate', 'врожденный'),
                ('insidious', 'коварный'),
                ('insipid', 'пресный'), ('intrepid', 'бесстрашный'), ('inundate', 'затоплять'),
                ('inveterate', 'закоренелый'),
                ('irrefutable', 'неопровержимый'), ('itinerant', 'путешествующий'), ('juxtapose', 'сопоставлять'),
                ('laconic', 'лаконичный'),
                ('lament', 'оплакивать'), ('latent', 'скрытый'), ('laudable', 'похвальный'), ('lethargic', 'вялый'),
                ('lucid', 'ясный'), ('lucrative', 'прибыльный'), ('magnanimous', 'великодушный'),
                ('malevolent', 'злобный'),
                ('malleable', 'податливый'), ('meticulous', 'тщательный'), ('mitigate', 'смягчать'),
                ('morose', 'угрюмый'),
                ('mundane', 'обыденный'), ('nefarious', 'гнусный'), ('nominal', 'номинальный'),
                ('nonchalant', 'беззаботный'),
                ('obfuscate', 'запутывать'), ('obsequious', 'подхалимский'), ('obstinate', 'упрямый'),
                ('omnipotent', 'всемогущий'),
                ('onerous', 'обременительный'), ('ostentatious', 'показной'), ('panacea', 'панацея'),
                ('paradigm', 'образец'),
                ('pariah', 'изгой'), ('partisan', 'сторонник'), ('paucity', 'недостаток'), ('pecuniary', 'денежный'),
                ('penchant', 'склонность'), ('perfunctory', 'поверхностный'), ('pernicious', 'вредоносный'),
                ('perspicacious', 'проницательный'),
                ('pertinent', 'уместный'), ('petulant', 'раздражительный'), ('phlegmatic', 'флегматичный'),
                ('plethora', 'изобилие'),
                ('precocious', 'рано развитый'), ('predilection', 'предрасположенность'), ('prevaricate', 'увиливать'),
                ('pristine', 'первозданный'),
                ('proclivity', 'склонность'), ('prosaic', 'прозаичный'), ('protean', 'разнообразный'),
                ('prudent', 'благоразумный'),
                ('quixotic', 'идеалистичный'), ('rancor', 'злоба'), ('recalcitrant', 'неподатливый'),
                ('redolent', 'напоминающий'),
                ('relegate', 'переводить'), ('remiss', 'небрежный'), ('replete', 'наполненный'),
                ('rescind', 'отменять'),
                ('reticent', 'сдержанный'), ('sagacious', 'мудрый'), ('salient', 'выдающийся'),
                ('sanguine', 'оптимистичный'),
                ('scintillating', 'блестящий'), ('serendipity', 'счастливая случайность'), ('solicitous', 'заботливый'),
                ('spurious', 'ложный'),
                ('staunch', 'верный'), ('stipulate', 'оговаривать'), ('stringent', 'строгий'),
                ('substantiate', 'подтверждать'),
                ('succinct', 'краткий'), ('superfluous', 'избыточный'), ('surreptitious', 'тайный'),
                ('sycophant', 'подхалим'),
                ('taciturn', 'молчаливый'), ('tantamount', 'равносильный'), ('temerity', 'безрассудство'),
                ('tenacious', 'упорный'),
                ('transient', 'временный'), ('trepidation', 'тревога'), ('truculent', 'злобный'),
                ('ubiquitous', 'вездесущий'),
                ('umbrage', 'обида'), ('unilateral', 'односторонний'), ('vacillate', 'колебаться'),
                ('venerate', 'почитать'),
                ('verbose', 'многословный'), ('vicissitude', 'перемена'), ('vindicate', 'оправдывать'),
                ('virulent', 'злокачественный'),
                ('vociferous', 'шумный'), ('wane', 'ослабевать'), ('wanton', 'беспричинный'), ('zealous', 'рьяный')
            ],

            "C2": [
                ('aberration', 'отклонение'), ('abnegation', 'отречение'), ('abstruse', 'труднопонимаемый'),
                ('acumen', 'проницательность'),
                ('adumbrate', 'очерчивать'), ('anathema', 'проклятие'), ('antediluvian', 'древний'),
                ('apocryphal', 'сомнительный'),
                ('approbation', 'одобрение'), ('arcane', 'тайный'), ('assiduous', 'усердный'),
                ('auspicious', 'благоприятный'),
                ('bucolic', 'пасторальный'), ('cabal', 'тайный заговор'), ('cacophony', 'какофония'),
                ('calumny', 'клевета'),
                ('capitulate', 'капитулировать'), ('castigate', 'наказывать'), ('cavil', 'придираться'),
                ('chicanery', 'хитрость'),
                ('circumlocution', 'круговорот речи'), ('clandestine', 'тайный'), ('cogent', 'убедительный'),
                ('comity', 'взаимность'),
                ('conflagration', 'пожар'), ('contumacious', 'непокорный'), ('corpulent', 'тучный'),
                ('coterie', 'кружок'),
                ('debauchery', 'распутство'), ('demagogue', 'демагог'), ('denouement', 'развязка'),
                ('desuetude', 'забвение'),
                ('diaphanous', 'прозрачный'), ('didactic', 'дидактический'), ('disparate', 'несопоставимый'),
                ('dissonance', 'диссонанс'),
                ('ebullient', 'энергичный'), ('effrontery', 'наглость'), ('egregious', 'вопиющий'),
                ('enervate', 'ослаблять'),
                ('ephemeral', 'мимолетный'), ('equanimity', 'спокойствие'), ('eschew', 'избегать'),
                ('excoriate', 'жестко критиковать'),
                ('execrable', 'отвратительный'), ('exigent', 'неотложный'), ('expurgate', 'редактировать'),
                ('fastidious', 'привередливый'),
                ('feckless', 'беспомощный'), ('fatuous', 'глупый'), ('fecund', 'плодовитый'),
                ('fractious', 'раздражительный'),
                ('garrulous', 'болтливый'), ('grandiloquent', 'высокопарный'), ('hapless', 'несчастный'),
                ('hegemony', 'гегемония'),
                ('iconoclast', 'иконоборец'), ('ignominious', 'позорный'), ('impecunious', 'бедный'),
                ('impetuous', 'порывистый'),
                ('improvident', 'нерассудительный'), ('inchoate', 'незрелый'), ('indefatigable', 'неутомимый'),
                ('indolent', 'ленивый'),
                ('ineffable', 'невыразимый'), ('inimical', 'враждебный'), ('insouciant', 'беззаботный'),
                ('intransigent', 'непримиримый'),
                ('inveterate', 'закоренелый'), ('irascible', 'раздражительный'), ('jejune', 'скучный'),
                ('lachrymose', 'плачущий'),
                ('laconic', 'лаконичный'), ('legerdemain', 'ловкость рук'), ('licentious', 'распутный'),
                ('lugubrious', 'мрачный'),
                ('mendacious', 'лживый'), ('meretricious', 'показной'), ('munificent', 'щедрый'),
                ('nefarious', 'гнусный'),
                ('obdurate', 'упрямый'), ('obfuscate', 'запутывать'), ('obsequious', 'подхалимский'),
                ('onerous', 'трудный'),
                ('opprobrium', 'позор'), ('ossify', 'окостеневать'), ('pellucid', 'прозрачный'),
                ('penurious', 'бедный'),
                ('perfidy', 'вероломство'), ('perfunctory', 'поверхностный'), ('perspicacious', 'проницательный'),
                ('phlegmatic', 'флегматичный'),
                ('pithy', 'лаконичный'), ('platitude', 'банальность'), ('plethora', 'изобилие'),
                ('precocious', 'рано развитый'),
                ('predilection', 'предрасположенность'), ('proclivity', 'склонность'), ('propinquity', 'близость'),
                ('pusillanimous', 'трусливый'),
                ('quixotic', 'идеалистичный'), ('recalcitrant', 'неподатливый'), ('recondite', 'трудный для понимания'),
                ('redolent', 'напоминающий'),
                ('reprobate', 'негодяй'), ('reticent', 'сдержанный'), ('sagacious', 'мудрый'),
                ('salubrious', 'полезный'),
                ('sanguine', 'оптимистичный'), ('sartorial', 'относящийся к одежде'), ('sedulous', 'усердный'),
                ('solipsism', 'солипсизм'),
                ('spurious', 'ложный'), ('stentorian', 'громкий'), ('strident', 'резкий'), ('sublime', 'возвышенный'),
                ('supercilious', 'высокомерный'), ('surreptitious', 'тайный'), ('sycophant', 'подхалим'),
                ('taciturn', 'молчаливый'),
                ('tantamount', 'равносильный'), ('temerity', 'безрассудство'), ('tenebrous', 'мрачный'),
                ('turgid', 'напыщенный'),
                ('ubiquitous', 'вездесущий'), ('unctuous', 'неискренний'), ('usurp', 'узурпировать'),
                ('vacillate', 'колебаться'),
                ('vapid', 'безвкусный'), ('venal', 'коррумпированный'), ('veracity', 'правдивость'),
                ('verdant', 'зеленый'),
                ('vicissitude', 'перемена'), ('vindicate', 'оправдывать'), ('vituperate', 'бранить'),
                ('vociferous', 'шумный'),
                ('voluble', 'говорливый'), ('wanton', 'беспричинный'), ('wizened', 'сморщенный'), ('zealous', 'рьяный')
            ]
        }
        with open(COMMON_WORDS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['level', 'english', 'russian'])
            for level, words in common_words.items():
                for eng, rus in words:
                    writer.writerow([level, eng, rus])

init_common_words()


def ensure_stats_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_stats (
            user_id INTEGER PRIMARY KEY,
            total_correct INTEGER NOT NULL DEFAULT 0,
            total_wrong INTEGER NOT NULL DEFAULT 0,
            learned_words INTEGER NOT NULL DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS word_stats (
            user_id INTEGER NOT NULL,
            aword TEXT NOT NULL,
            correct_count INTEGER NOT NULL DEFAULT 0,
            wrong_count INTEGER NOT NULL DEFAULT 0,
            is_learned INTEGER NOT NULL DEFAULT 0,
            is_hard INTEGER NOT NULL DEFAULT 0,
            hard_correct_count INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (user_id, aword)
        )
    """)

    cursor.execute("PRAGMA table_info(word_stats)")
    word_stats_columns = {row[1] for row in cursor.fetchall()}
    if "is_hard" not in word_stats_columns:
        cursor.execute("ALTER TABLE word_stats ADD COLUMN is_hard INTEGER NOT NULL DEFAULT 0")
    if "hard_correct_count" not in word_stats_columns:
        cursor.execute("ALTER TABLE word_stats ADD COLUMN hard_correct_count INTEGER NOT NULL DEFAULT 0")
    if "srs_stage" not in word_stats_columns:
        cursor.execute("ALTER TABLE word_stats ADD COLUMN srs_stage INTEGER NOT NULL DEFAULT 0")
    if "next_review_at" not in word_stats_columns:
        cursor.execute("ALTER TABLE word_stats ADD COLUMN next_review_at INTEGER NOT NULL DEFAULT 0")
    if "last_review_at" not in word_stats_columns:
        cursor.execute("ALTER TABLE word_stats ADD COLUMN last_review_at INTEGER NOT NULL DEFAULT 0")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS error_history (
            user_id INTEGER NOT NULL,
            aword TEXT NOT NULL,
            error_count INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (user_id, aword)
        )
    """)

    conn.commit()
    conn.close()


ensure_stats_tables()



def init_user_stats(user_id: int):
    ensure_stats_tables()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO user_stats (user_id)
        VALUES (?)
    """, (user_id,))
    conn.commit()
    conn.close()



# обновление статистики словаря пользователя
def update_word_stats(user_id: int, aword: str, correct: bool):
    ensure_stats_tables()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    hard_removed = False

    cursor.execute("""
        INSERT OR IGNORE INTO word_stats (user_id, aword)
        VALUES (?, ?)
    """, (user_id, aword))

    cursor.execute("""
        SELECT srs_stage
        FROM word_stats
        WHERE user_id = ? AND aword = ?
    """, (user_id, aword))
    row = cursor.fetchone()
    srs_stage = int(row[0]) if row else 0
    now_ts = int(time.time())
    # 0:10m, 1:1h, 2:6h, 3:1d, 4:3d, 5:7d, 6:14d
    srs_intervals = [600, 3600, 21600, 86400, 259200, 604800, 1209600]

    if correct:
        cursor.execute("""
            UPDATE word_stats
            SET correct_count = correct_count + 1
            WHERE user_id = ? AND aword = ?
        """, (user_id, aword))

        cursor.execute("""
            UPDATE word_stats
            SET hard_correct_count = hard_correct_count + 1
            WHERE user_id = ? AND aword = ? AND is_hard = 1
        """, (user_id, aword))

        cursor.execute("""
            UPDATE user_stats
            SET total_correct = total_correct + 1
            WHERE user_id = ?
        """, (user_id,))

        cursor.execute("""
            SELECT is_hard, hard_correct_count
            FROM word_stats
            WHERE user_id = ? AND aword = ?
        """, (user_id, aword))
        row = cursor.fetchone()
        if row and row[0] == 1 and row[1] >= 10:
            cursor.execute("""
                UPDATE word_stats
                SET is_hard = 0, hard_correct_count = 0
                WHERE user_id = ? AND aword = ?
            """, (user_id, aword))
            hard_removed = True

        new_stage = min(srs_stage + 1, len(srs_intervals) - 1)
        next_review_at = now_ts + srs_intervals[new_stage]
        cursor.execute("""
            UPDATE word_stats
            SET srs_stage = ?, next_review_at = ?, last_review_at = ?
            WHERE user_id = ? AND aword = ?
        """, (new_stage, next_review_at, now_ts, user_id, aword))
    else:
        cursor.execute("""
            UPDATE word_stats
            SET wrong_count = wrong_count + 1
            WHERE user_id = ? AND aword = ?
        """, (user_id, aword))

        cursor.execute("""
            UPDATE user_stats
            SET total_wrong = total_wrong + 1
            WHERE user_id = ?
        """, (user_id,))

        cursor.execute("""
            INSERT INTO error_history (user_id, aword, error_count)
            VALUES (?, ?, 1)
            ON CONFLICT(user_id, aword)
            DO UPDATE SET error_count = error_count + 1
        """, (user_id, aword))

        cursor.execute("""
            UPDATE word_stats
            SET is_hard = 1
            WHERE user_id = ? AND aword = ?
        """, (user_id, aword))

        new_stage = max(srs_stage - 1, 0)
        # After error, schedule an early review.
        next_review_at = now_ts + 300
        cursor.execute("""
            UPDATE word_stats
            SET srs_stage = ?, next_review_at = ?, last_review_at = ?
            WHERE user_id = ? AND aword = ?
        """, (new_stage, next_review_at, now_ts, user_id, aword))

    cursor.execute("""
        UPDATE word_stats
        SET is_learned = 1
        WHERE user_id = ? AND aword = ? AND correct_count >= 10
    """, (user_id, aword))

    cursor.execute("""
        UPDATE user_stats
        SET learned_words = (
            SELECT COUNT(*) FROM word_stats
            WHERE user_id = ? AND is_learned = 1
        )
        WHERE user_id = ?
    """, (user_id, user_id))

    conn.commit()
    conn.close()
    return {"hard_removed": hard_removed, "word": aword}


def pick_srs_word(user_id: int, candidates: list[str]) -> str | None:
    if not candidates:
        return None

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    placeholders = ",".join("?" for _ in candidates)
    params = [user_id, *candidates]
    cursor.execute(
        f"""
        SELECT aword, next_review_at
        FROM word_stats
        WHERE user_id = ?
          AND aword IN ({placeholders})
        """,
        params,
    )
    rows = cursor.fetchall()
    conn.close()

    next_map = {word: 0 for word in candidates}
    for aword, next_review_at in rows:
        next_map[aword] = int(next_review_at or 0)

    now_ts = int(time.time())
    due = [w for w in candidates if next_map.get(w, 0) <= now_ts]
    pool = due if due else candidates

    min_next = min(next_map.get(w, 0) for w in pool)
    prioritized = [w for w in pool if next_map.get(w, 0) == min_next]
    return sorted(prioritized)[0] if prioritized else None




# сложные слова
def get_hard_words(user_id: int, limit: int = 10):
    ensure_stats_tables()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT aword FROM word_stats
        WHERE user_id = ? AND is_hard = 1
        ORDER BY wrong_count DESC, aword ASC
        LIMIT ?
    """, (user_id, limit))
    words = [row[0] for row in cursor.fetchall()]
    conn.close()
    return words


# уровень пользователя
def get_user_level(user_id: int) -> int:
    ensure_stats_tables()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT learned_words FROM user_stats WHERE user_id = ?
    """, (user_id,))
    row = cursor.fetchone()
    conn.close()
    learned = row[0] if row else 0

    if learned >= 1000: return 5
    if learned >= 500: return 4
    if learned >= 200: return 3
    if learned >= 100: return 2
    return 1

##########

