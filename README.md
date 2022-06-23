### Каков шанс, что Вы бы выжили на титанике?

#### При помощи телеграмм бота можно узнать!   
> (сейчас бот не активен. Включается по запросу.)
> 
> ![alt text](https://github.com/RPavelD/titanic_classifier/blob/master/info/dialog1.png)
> ![alt text](https://github.com/RPavelD/titanic_classifier/blob/master/info/dialog2.png)

### Проект:
- Обучена модель градиентного бустинга над решающими деревьями для бинарной классификации признака "Survived".
- Использование модели реализовано при помощи телеграм бота.
    
### Модель:
- Делает одно предсказание за примерно 0.015 секунды.
-  Имеет точность на данных, которые она не видела ~80%
    > Результат на kaggle: https://www.kaggle.com/competitions/titanic/leaderboard#
        
    > ![alt text](https://github.com/RPavelD/titanic_classifier/blob/master/info/score.png)
    
### Особенности:
- Реализован подпроект, создающий машину состояний для последователности вопросов-ответов.
    > ./use_model/machine_state.py
    
- Возможно возвращаться на предыдущий вопрос
    > ![alt text](https://github.com/RPavelD/titanic_classifier/blob/master/info/last_state.png)
    
- Продуман отлов ошибок
    > ![alt text](https://github.com/RPavelD/titanic_classifier/blob/master/info/error_filter.png)


### Недостатки:
1. Не объясняется или плохо объясняется при использовании модели, какой ожидается ввод.
