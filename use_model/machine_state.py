import re 

class Test:
    def __init__(
            self,
            int_test=False,
            numeric_test=False,
            boundaries_test=False,
            sequence_boundaries: tuple =None,
            entering_test=False,
            entering_set: tuple =None,
            valid_text_test=False,
            regex_for_valid_text: str =None
        ):
        
        self.__tests = []
        
        if int_test:
            self.__tests.append(self.__int_test)
            
        if numeric_test:
            self.__tests.append(self.__numeric_test)
            
        if boundaries_test:
            if not sequence_boundaries:
                raise ValueError('Не заданы границы (sequence_boundaries=(min, max) ) для теста на границы (boundaries_test)')
                
            self.__sequence_boundaries = sequence_boundaries
            self.__tests.append(self.__boundaries_test)
            
        if entering_test:
            if not entering_set:
                raise ValueError('Не задано множество (entering_set) для теста на вхождение (entering_test)')
                
            self.__entering_set = entering_set
            self.__tests.append(self.__entering_test)

            
        if valid_text_test:
            if not regex_for_valid_text:
                raise ValueError('Не задано регулярная строка (regex_for_valid_text) для теста на соответствие (entervalid_text_testing_test)')
            
            self.__regex_for_valid_text = regex_for_valid_text
            self.__tests.append(self.__valid_text_test)
            
            
    def __call__(self, x):        
        for test in self.__tests:
            msg_check, x_is_nice = test(x)
            
            # Если x не прошел проверку, возвращаем информацию об ошибке и сигнал о не пройденной проверке
            if not x_is_nice:
                return msg_check, False
            
        return None, True


    def __int_test(self, x):
        try:
            int(x)
            return None, True
        except:
            return 'Принимается одно целое целое число. Ни строка, ни дробное число не подойдут в качестве ответа!', False
        
        
    def __numeric_test(self, x):
        try:
            float(x)
            return None, True
        except:
            return 'Принимается только одно ЧИСЛО.', False
        
        
    def __boundaries_test(self, x):
        # проверка на число
        temp_check = self.__numeric_test(x)
        if not temp_check[1]:
            return temp_check
        
        x_min, x_max = self.__sequence_boundaries
        if x_min <= float(x) <= x_max:
            return None, True
        else:
            return f'Число должно быть от {x_min} до {x_max}', False
        
        
    def __entering_test(self, x):
        if x.strip() in self.__entering_set: 
            return None, True
        else:
            entering_set = '\n'.join(self.__entering_set)
            return f"Ответом может быть одно из:\n{entering_set}", False
        
    def __valid_text_test(self, x):
        re_find = re.findall(self.__regex_for_valid_text , x)
        if re_find and (len(re_find) == 1):
            return None, True
        else:
            return 'Неподходящий тип строки', False
    

class State:
    """
    Класс реализует текущее состояние
     
    Необходимо устанавливать 
        предыдущее состояние
        следующее состояние
        текст, который будет отправляться для отображения текущего состояния
        функцию проверки ответа 
    """
    def __init__(self, text, last_state=None, next_state=None, check_answer=None):
        self.__text = text
        
        if last_state:
            self.set_last_state(last_state)
        else:
            self.__last_state = None
            
            
        if next_state:
            self.set_next_state( next_state)
        else:
            self.__next_state = None
            
            
        if check_answer:
            self.set_check_answer_function(check_answer)
            
        else:
            self.__check_answer = None
    
    
    # Вызов состояния
    def __call__(self, answer=None, get_last=False):
        #  если указано, что надо вернуть предыдущий шаг, то нужно его выслать
        if get_last:
            return self.__last_state
        
        # если ответа нет, тогда вернуть текст состояния
        if not answer:
            return self.__text
                
        # если ответ правильный, то вернут следующий шаг
        temp_check = self.__check_answer(answer)
        if temp_check[1]:
            return self.__next_state        
        # иначе вернуть информацию об ощибке и текст текущего состояния
        else:
            return f'{temp_check[0]}\n\n{self.__text}' 
        
    
    # установка следующего шага
    def set_next_state(self, next_state):
        if isinstance(next_state, State):
            self.__next_state = next_state
        else:
            raise TypeError('следующий состояние должно быть такого же класса')
    
    # установка предыдущего шага
    def set_last_state(self, last_state):
        if isinstance(last_state, State):
            self.__last_state = last_state
        else:
            raise TypeError('предыдущее состояние должно быть такого же класса')

    # установка проверяющей функции
    def set_check_answer_function(self, foo):
        if isinstance(foo, Test):
            self.__check_answer = foo
        else:
            raise TypeError('объект проверки не является проверяющим классом')
    
    

class MachineStates:
    """ Класс реализует машину состояний"""
    
    def __init__(self, ways:tuple ):
        """
        ways: tuple(
            ('текст состояния', check_answer)
            ...
        )
        """
        # тут будут храниться ответы
        self.__answers = ['']*(len(ways)-1)

        # устанавливаю корневое состояние
        self.__ways = [State(ways[0][0], check_answer=ways[0][1])]
        # предыдущее состояние корневого узла = корневой узел
        self.__ways[0].set_last_state(self.__ways[0])
        
        for way in ways[1:]: 
            # добавляем в конец еще одно состояние
            self.__ways.append(State(way[0], last_state=self.__ways[-1], check_answer=way[1]))
            # для предыдущего состояния дать ссылку на последнее
            self.__ways[-2].set_next_state(self.__ways[-1])            
                
        # устанавливаю текущим состоянием корневое
        self.__now_state = self.__ways[0]
                        
        
    # машина состояния работает как функтр
    def __call__(self, answer=None, get_last=False)->(str, bool):
        
        reaction = self.__now_state(answer=answer, get_last=get_last)        
        # если передано состояние, тогда надо переходить на него. (Передается следующее состояние)
        if isinstance(reaction, State):
            # записываем ответ для текущего состояния
            self.__answers[ self.__ways.index(self.__now_state) ] = answer
            
            # меняем состояние
            self.__now_state = reaction          
            
            # если достигнут последний вопрос, тогда сигнализируем об этом
            if self.__now_state is self.__ways[-1]:
                return self.__now_state(), True
            
            # возвращаем текст текущего состояния
            return self.__now_state(), False
        
        else:
            return reaction, False
        
        
    def get_answer(self):
        return self.__answers

