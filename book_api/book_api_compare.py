import pandas as pd
import numpy as np
import requests
import xml.etree.ElementTree as ET
from time import sleep

#book_data = pd.read_csv('book_history_2018_09_16.csv')
#test_data = book_data.sample(n=300)
#test_data.to_csv('testdata.csv')
test_data = pd.read_csv('testdata.csv')

def transform_isbn(isbn):
    '''
    10桁のISBNコードを13桁に変換する．
    Parameters
    __________
    isbn:10桁のisbnコードのうち1の位以外の9桁,str
    Returns
    _______
    isbn:13桁のisbnコード
    '''
    each_digit = list(isbn)
    check_digit_sum = 9*1+7*3+8*1
    for i in range(len(each_digit)):
        if i%2==0:
            check_digit_sum += 3*int(each_digit[i])
        if i%2==1:
            check_digit_sum += 1*int(each_digit[i])
    q,mod = divmod(check_digit_sum,10)#余りが0のときはcheck_digit=0
    if mod !=0:
        check_digit = 10-mod
    elif mod ==0:
        check_digit = 0
    return 978*10**10 + int(isbn)*10+check_digit


class Book_api(object):
    def __init__(self, isbn):

        isbn_nine = ''.join(list(isbn)[:-1])#isbnコードのうち1の位以外の9桁
        self.isbn_ten = isbn#ISBNコード(10桁.末尾がXだったりして面倒)
        self.isbn_thir=transform_isbn(isbn_nine)#13桁のISBNコード



class Rakuten_api(Book_api):
    def __init__(self,isbn):
        super().__init__(isbn)
        self.request_url = 'https://app.rakuten.co.jp/services/api/BooksTotal/Search/20170404?format=json&isbnjan={}&applicationId=1028077349819132154'.format(self.isbn_thir)

    def request_by_isbn(self):
        '''
        APIにリクエストを送る．ヒットした件数を返す
        '''
        result_of_api = requests.get(self.request_url)
        result = result_of_api.json()
        return result['count']

class Googlebooks_api(Book_api):
    def __init__(self,isbn):
        super().__init__(isbn)
        self.request_url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:{}'.format(self.isbn_thir)

    def request_by_isbn(self):
        '''
        APIにリクエストを送る．ヒットした件数を返す
        '''
        result_of_api = requests.get(self.request_url)
        result = result_of_api.json()
        return result['totalItems']

class NationalLibrary_api(Book_api):
    def __init__(self,isbn):
        super().__init__(isbn)
        self.request_url = 'http://iss.ndl.go.jp/api/opensearch?isbn={}'.format(self.isbn_thir)

    def request_by_isbn(self):
        '''
        APIにリクエストを送る．ヒットした件数を返す
        '''
        result_of_api = requests.get(self.request_url)
        result = ET.fromstring(result_of_api.text)
        return result[0][4].text

test_num = len(test_data)
isbn_title = test_data[['isbn','title']]
hit_count = pd.DataFrame({'rakuten':np.zeros(test_num),
                            'Google':np.zeros(test_num),
                            'NationalLibrary':np.zeros(test_num)})
result_dataframe = pd.concat([isbn_title,hit_count],axis=1)


for i in range(test_num):
    isbn = test_data.loc[i,'isbn']
    print(isbn)
    rakuten = Rakuten_api(isbn)
    google  = Googlebooks_api(isbn)
    national= NationalLibrary_api(isbn)
    print('Rakuten')
    result_dataframe.loc[i,'rakuten'] = rakuten.request_by_isbn()
    sleep(1.5)
    print('Google')
    result_dataframe.loc[i,'Google'] = google.request_by_isbn()
    sleep(1.5)
    print('NationalLibrary')
    result_dataframe.loc[i,'NationalLibrary'] = national.request_by_isbn()
    sleep(1.5)
result_dataframe.to_csv('api_compare_result.csv')
