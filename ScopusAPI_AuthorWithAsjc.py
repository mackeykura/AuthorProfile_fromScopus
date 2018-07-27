#! Python3
# -*- coding: utf-8 -*-
# Scopus Retrieval API
# 4. 全著者IDそれぞれに専門分野を割り当てる

import pandas as pd
import requests
import xml.etree.ElementTree as ET
import urllib
from urllib.error import URLError

# API Key   
myAPIkey = 'XXXXXXXXXXXXXXXXXXXXXXXX'

# 調べたい Author ('で囲わないとerrorが出るのでつける)
uniqueaIds = pd.read_csv('UniqueAuthorIdsList.csv', dtype= 'object')
uniqueaIds['ID'] = "'" + uniqueaIds['Author ID'] + "'"

# APIのひな型
api =  'https://api.elsevier.com/content/author/author_id/{sid}?apiKey={key}'

#4-1. 著者IDから分野（ASJC, 27分野） codeを抽出（API）
author_asjc27 = []
for i, number in uniqueaIds.iterrows():
    # 2500人前後でerrorが出る（けどプログラムは回り続ける）ので、2600人で終了させる
    if i > 2600:
        break
    else:
        # APIのURLを得る
        aid = number['Author ID']
        url = api.format(sid=aid, key=myAPIkey)
        print('Scopus Author ID'+ str(i) + ' : ' + str(aid) )

        # 実際にAPIにリクエストを送信して結果を取得する（errorが結構よく出るので、でたIDには99をつけて、止まらないようにする）
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                r = requests.get(url)
        except URLError as e:
            asjc27 = '99'
            author27 = [aid, asjc27]
            print(author27)
            author_asjc27.append(author27) 
            if hasattr(e, 'reason'):
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
        else:
            text = r.text.encode('utf-8')
            data = ET.fromstring(text)
        
            # 結果を出力 (Author id, subject-areas)
            #  Defined Author ID
            author_id = data[0][1].text
            author_id = author_id.replace('AUTHOR_ID:','')
            
            #author-profileの下から、分野のコードcode(4桁のうち上位2桁=asjc27)とその頻度frequencyを全て抽出
            asjc_list = []
            asjc = []
            for et in data.findall('.//author-profile/classificationgroup/classifications[@type="ASJC"]/classification'):
                 code = int(et.text[:2])
                 freqs = int(et.get('frequency'))
                 asjc = [code, freqs]
                 asjc_list.append(asjc)

            #ASJCcodeをソートし、freqの多い順に並べ直す
            asjcdf = pd.DataFrame(asjc_list, columns=['code2', 'freqs'])
            asjcsort = asjcdf.groupby('code2',as_index=False)['freqs'].sum()
            asjcsort.sort_values(by='freqs', ascending=False, inplace = True)
    
            #4-2. 一番多い分野を特定, 著者の分野を決定（分野の数が5個なければ分野なし＝0とする）
            asjc27 = asjcsort.iat[0,0]
            author27 = [author_id, asjc27]
            author_asjc27.append(author27)
    
#4-4. listを作成
author_asjc27_df = pd.DataFrame(author_asjc27, columns=['Scopus Author ID', 'asjc27'])
author_asjc27_df.to_csv('AuthorIDwithasjc27List.csv', index = False)

 
