#! Python3
# -*- coding: utf-8 -*-

import pandas  as pd

#1. dataファイルを開く
df = pd.read_csv('Publications.csv', header = 10)

#2. Author ID を抽出(重複あり)
aIds = []
for i, row in kudf.iterrows():
    author = [row['Scopus Author Ids']]
    author = author[0].split(', ')
    aIds.extend(author)

aIdsdf = pd.DataFrame(aIds, columns=['Author ID'])

#3. Unique Author ID listを作る
uniqueaIds = aIdsdf.drop_duplicates()
print('Unique Author IDs: ' + str(len(uniqueaIds)))

uniqueaIds.to_csv('UniqueAuthorIdsList.csv', index=False)





