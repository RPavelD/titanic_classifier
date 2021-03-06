# Классификация пассажиров Титаника
____
### __Цель проекта__: по ряду признаков определить - выжил бы человек на Титанике.


### Инструменты решения:
| Действие | Инструмент |
| ------ | ------ |
| Визуализация | missingno, matplotlib, seaborn |
| Статистические тесты | scipy |
| Работа с данными | numpy, pandas |
| Импутация пропущенных данных | fancyimpute |
| Деление данных и оценка модели | sklearn |
| Создание и обучение модели | catboost |


## Что сделано:
1. Выводы сводного анализа:
    - Чем выше класс обслуживания, тем большая часть его спаслась. Однако, это может быть объясняться тем, что первый и второй классы располагались ближе к спасательным шлюпкам, чем третий.
    - 74% женщин и девушек выжило, в то время как только 18% мужчин смогли остаться в живых.
    - Было замечено, что в каждом классе предпочтительно выживали более молодые.
        > Были проведены тесты и получены статистически значимые результаты.
2. Предобработка данных:
    - Был создан признак, показывающий расстояние от этажа пассажира до палубы, на которой находились спасательные шлюпки.
        > Были сгенерированы и другие признаки.
    - Пропущенные данные заполнялись алгоритмом k ближайших соседей.
    - Почищены и кодированы текстовые и категориальные признаки.
3. Выбор модели:
    - В ходе проверки различных алгоритмов машинного обучения для бинарной классификации: logistic regression, bayesian, SVM, CatboostClassifier - была выбрана модель градиентного бустинга над решающими деревьями CatboostClassifier, дающая наилучший результат.
        > После отбора модели, код предобработки был оптимизирован, поскольку библиотека catboost умеет самостоятельно кодировать текстовые и категориальные признаки. 
4. Оценка модели:
    - Одно предсказание за примерно 15 милисекунд.
    - Имеет точность на данных, которые она не видела ~80%
        > Результат на kaggle: https://www.kaggle.com/competitions/titanic/leaderboard#     
        > ![alt text](https://github.com/RPavelD/titanic_classifier/blob/master/info/score.png)
        >> Модель оценивалась метрикой accuracy. Однако автор проекта по причине дисбаланса целевого признака (68%/32%) предпочел бы использовать метрику полноты precision.


## Итог:
_По итогам анализа и построения модели можно сделать вывод, что определенные группы: женщины, 1,2 классы, более молодые в каждом классе - имели больший шанс спастись._

##  Пример использования  модели:
Был реализован телеграм бот, с помощью которого, ответив на ряд вопросов, можно узнать свой шанс выжить на борту Титаника.
>   ![alt text](https://github.com/RPavelD/titanic_classifier/blob/master/info/dialog.gif)

### Подпроекты:
1. Телеграм бот 
    > use_model/telegrambot_use_model.ipynb
2. Машина состояний для телеграм бота
    > use_model/machine_state.py
