import codecs
import json
from normalize_neologd import normalize_neologd

def check_accept(word, cols, accept_part):
    if (word == 'EOS' or len(cols) < 2):
        return False

    # 品詞
    part = cols[1].split(',')[0]


    return part in accept_part

def get_keywords(mecab, path, accept_part=['名詞', '形容詞']):
    with codecs.open(path, encoding='utf-8') as f:
        messages = json.loads(f.read())
        keywords = []
        for message_dic in messages:
            if 'message' not in message_dic:
                print('{}:{}'.format(path,message_dic))
                continue
            message = message_dic['message']
            # 正規化してからMeCabに渡す
            rows = mecab.parse(normalize_neologd(message))
            # 形態素が行ごとにあるのでそれで分割していく
            for row in rows.split('\n'):
                cols = row.split('\t')
                if (len(cols) == 0):
                    continue

                word = cols[0]
                if check_accept(word, cols, accept_part):
                    keywords.append(word)
                
        return keywords