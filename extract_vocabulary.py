import codecs

import vocabulary

dic = vocabulary.get_vocabulary_dic()
v = vocabulary.flatten_vocabulary_dic(dic)

with codecs.open('vocabulary.txt', 'w', 'utf-8') as f:
    for keyword in v:
        f.write(keyword)
        f.write('\n')