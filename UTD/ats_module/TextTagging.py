__title__ = 'TextTagging'
__version__ = '0.0.5'
__author__ = 'suchoi'
__license__ = ''
__copyright__ = 'Niccompany'


# from jamo import h2j, j2hcj
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import models
import os
import json
import numpy as np
import pickle

installpath = os.path.dirname(os.path.realpath(__file__))


# class NicJamoTagging():
    # def __init__(self, max_len=21, base_path='./models/L3'):
        # self.max_len = max_len
        # self.base_path = base_path
        # with open('%s/info/적요_카테고리_정리_v0.31.json' % installpath, 'r', encoding="utf-8-sig") as fp: 
            # self.info = json.load(fp)        


    #### 자모단위로 나누고 유니코드 번호로 치환하여 max_len 만큼 뒤에서 자르고 0으로 채워서 반환
    # def text_to_sequences(self, string):
        # string_check(string)
        # sequences_array = [np.array([ord(i) for i in j2hcj(h2j(string))])]
        # return pad_sequences(sequences_array, maxlen=self.max_len)


    # def text_tagging(self, lists, code):
        # numpy_check(lists)
        # if code == '지급': model_name='ex_v0.33'
        # elif code == '입금': model_name='de_v0.33'
        # assert code in ['지급','입금'], 'code 변수는 지급 또는 입금이 들어가야 합니다. 확인해주세요. error-%s' % code

        # model_path = os.path.join(self.base_path,'일단계분류',model_name+'.h5')
        # model = models.load_model(model_path)
        # first_result = str(np.argmax(model.predict(lists),axis=1)[0])
        # first_result = self.info[code]['1단계분류'][first_result]

        # model_path = os.path.join(self.base_path,'이단계분류',first_result,model_name+'.h5')
        # model = models.load_model(model_path)
        # second_result = str(np.argmax(model.predict(lists),axis=1)[0])
        # second_result = self.info[code]['2단계분류'][first_result][second_result]
        # return (first_result, second_result)



class NicWordTagging():
    def __init__(self):
        with open('%s/info/categorical_name_v0.78.json' % installpath, 'r', encoding="utf-8-sig") as fp:
            self.info = json.load(fp)
        with open('%s/models/input_length_v0.78.json' % installpath, 'rb') as fp:
            self.inputlength = json.load(fp)

        with open('%s/models/tokenizer/tokenizer_v0.78.pkl' % installpath, 'rb') as handle:
            self.tokenizer = pickle.load(handle)

        self.model_ex = models.load_model('%s/models/L3/ex_v0.78_9.h5' % installpath)
        self.model_de = models.load_model('%s/models/L3/de_v0.78_14.h5' % installpath)


    def text_tagging(self, string, code):
    
        string_check(string)
        
        if code == '1':
            code = '지급'
        elif code == '2':
            code = '입금'

        sequences_array = self.tokenizer.texts_to_sequences([string.split()])
        lists = pad_sequences(sequences_array, maxlen=self.inputlength[code])
        
        if code == '지급':
            result = str(np.argmax(self.model_ex.predict(lists, verbose=0),axis=1)[0])
            result = [k for k, v in self.info[code].items() if v == result][0]
        elif code == '입금':
            result = str(np.argmax(self.model_de.predict(lists, verbose=0),axis=1)[0])
            result = [k for k, v in self.info[code].items() if v == result][0]
            
        return (result.split("_")[0], result.split("_")[1])
        


#### input 타입체크 
def string_check(x):
    assert type(x) is str, "문자열 형식이 아닙니다. 적요 텍스트의 타입을 확인해주세요. {}".format(x)

#### input 타입체크 
def list_check(x):
    assert type(x) is list, "리스트 형식이 아닙니다. 적요 텍스트의 타입을 확인해주세요. {}".format(x)
    
#### input 타입체크 
def numpy_check(x):
    assert type(x).__module__ == np.__name__, "array 형식이 아닙니다. 적요 텍스트의 타입을 확인해주세요. {}".format(x)
