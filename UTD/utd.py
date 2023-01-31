__title__ = 'utd'
__version__ = '0.0.1'
__author__ = 'suchoi'
__license__ = ''
__copyright__ = 'Niccompany'

import os
import pickle
import numpy as np
from UTD.ats_module.TextPreprocessing import *
from UTD.ats_module.TextTagging import NicWordTagging
import datetime
installpath = os.path.dirname(os.path.realpath(__file__))

tests_dict = {"개인거래":0,
              "입금이체":1,
              "금융":2,
              "기타":3,
              "소득":4,
              "서비스이용":5,
              "주거/생활":6,
              "교육":7,
              "금융수익":8,
              "여가":9,
              "자동차":10,}

age_dict = {"10":0,
           "20_24":1,
           "25_29":2,
           "30_34":3,
           "35_39":4,
           "40_44":5,
           "45_49":6,
           "50_54":7,
           "55_59":8,
           "60":9,}

md_dict = {"지급": 1,
           "입금": 2}


def ats_kdcd_dtl(string):
    if "보증료" in string:
        return 15 # 보증료
    elif any(i in string for i in ["외화", "해외"]):
        return 14 # 해외
    elif "연금" in string:
        return 13 # 연금
    elif "수익증권" in string:
        return 12 # 증권
    elif any(i in string for i in ["어음", "역환처리"]):
        return 11 # 어음
    elif "재정자금" in string:
        return 10 # 재정자금
    elif "이자" in string:
        return 9 # 이자
    elif any(i in string for i in ["타행자동이체", "요구불간", "납부자자동", "스쿨뱅킹", "일반대출"]):
        return 7 # 자동이체
    elif "예약" in string:
        return 8 # 예약이체
    elif any(i in string for i in ["급여", "상여금", "지로대량급여"]):
        return 5 # 급여
    elif any(i in string for i in ["지로", "아파트관리비", "한전"]):
        return 6 # 요금납부
    elif any(i in string for i in ["적립식", "예금"]):
        return 4 # 예금
    elif "대량" in string:
        return 3 # 대량이체
    elif any(i in string for i in ["CMS공동망", "전자금융", "대금", "PG", "AMA"]):
        return 2 # 전자결제
    elif "펌뱅킹" in string:
        return 1 # 펌뱅킹
    else:
        return 0 # 그외

def weekday(ym, day):
    week = datetime.datetime(int(str(ym)[:4]), int(str(ym)[-2:]), day).weekday()
    if week < 5:
        return 0
    else:
        return 1

class UniqueTransactionDetect():
    def __init__(self):
        with open('%s/model/k_20230127_13.pickle' % installpath, 'rb') as handle:
            self.model = pickle.load(handle)
        # self.categorical = [0, 1, 2, 3, 4, 5, 6]
        self.nk = Nickonlpy()
        self.nwt = NicWordTagging()

    def predict_result(self, x):

        age_dc = age_dict[x['age_dc']]
        gender = x['gender']
        bas_mon = int(str(x['bas_ym'])[-2:])
        tran_md = md_dict[x['tran_md']]
        akd_pro = ats_kdcd_dtl(x['ats_kdcd_dtl'])
        am_pro = np.digitize(x['dps_trn_am'], bins=[0, 9, 49, 99, 499, 999, 4999, 9999, 49900])

        def text1_preprocessing(trans_md, text):
            text = find_null(text)
            text = ascii_check(text)
            text = change_upper(text)
            text = space_delete(text)
            text = remove_bank(text)
            text = corporatebody(text)
            text = numbers_to_zero(text)
            text = remove_specialchar(text)
            text = space_delete(text)
            text = find_null(text)
            if (text != "공백") or (len(text) >= 1):
                # tagging
                text = self.nk.predict_tokennize(text)
                result = self.nwt.text_tagging(text, trans_md)
                # text = nk.name_check(text)
            return tests_dict[result[0]]  # 대분류만
        text_2 = text1_preprocessing(x['tran_md'], x['text_1'])
        week = weekday(x['bas_ym'], x['bas_dt'])

        x_array = np.array([age_dc, gender, bas_mon, tran_md, akd_pro, am_pro, text_2, week]).reshape(8, 1).T
        result = str(self.model.predict(x_array)[0])
        return 'c' + result



