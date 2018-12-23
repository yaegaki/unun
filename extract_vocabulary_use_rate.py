
import codecs

import vocabulary

dic = vocabulary.get_vocabulary_dic()
keyword_dict = vocabulary.calc_total_use_rate(dic)

with codecs.open('vocabulary_use_rate.txt', 'w', 'utf-8') as f:
    for keyword, rate in sorted(keyword_dict.items(), key=lambda x: x[1], reverse=True):
        f.write('{}:{}\n'.format(keyword, rate))