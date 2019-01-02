import MeCab
import codecs
import json
from normalize_neologd import normalize_neologd

# キーがワードでバリューがそのワードが含まれる文章を形態素に分割した配列の辞書を作る
def make_word_to_morpheme_list_dict(mecab, path):
    dic = {}
    with codecs.open(path, 'r', 'utf-8') as f:
        messages = json.loads(f.read())

        for message_dic in messages:
            message = message_dic['message']
            msec = message_dic['offsetMsec']

            # 正規化してからMeCabに渡す
            rows = mecab.parse(normalize_neologd(message))
            # 形態素が行ごとにあるのでそれで分割していく
            words = []
            for row in rows.split('\n'):
                cols = row.split('\t')
                if (len(cols) == 0 or cols[0] == 'EOS'):
                    continue
                word = cols[0]
                if word == '':
                    continue
                words.append(word)

                o = { 'words':words, 'original':message, 'msec': msec }
                if word in dic:
                    dic[word].append(o)
                else:
                    dic[word] = [o]

    return dic

# listの中のstart_index以降に含まれるwordのindexをすべて返す
def get_indexes_all(list, start_index, word):
    return [i for i in range(start_index, len(list)) if list[i] == word]


# 形態素の並びから次に来る可能性のある文字のリストを取得する
# ex) もともとの文章が ["今日", "は", "いい", "天気", ",", "今日", "は", "眠い"]
#     で入力が["今日", "は"]なら出力は["いい", "眠い"]となる
def search_next_words(dic, list):
    word_count = len(list)
    if word_count == 0:
        return {}

    first_word = list[0]
    if first_word not in dic:
        return {}

    cdr = list[1:]

    memo = set()
    next_word_dict = {}
    for o in dic[first_word]:
        if o['original'] in memo:
            continue
        memo.add(o['original'])
        line = o['words']
        indexes = get_indexes_all(line, 0, first_word)

        for w in cdr:
            new_indexes = []
            for index in indexes:
                if index + 1 >= len(line):
                    break
                
                if line[index + 1] == w:
                    new_indexes.append(index + 1)
            
            indexes = new_indexes
            if len(indexes) == 0:
                break
        
        if len(indexes) > 0:
            for index in indexes:
                if index + 1 >= len(line):
                    break
                w = line[index+1]
                if w in next_word_dict:
                    next_word_dict[w] += 1
                else:
                    next_word_dict[w] = 1
    
    return next_word_dict
            



# ワードが含まれる文章のツリーを作る
# "今日はいい天気", "今日は眠い"という二つ文章があったときに
# "今日" を入力にすると今日から始まる単語のツリーが作られる
def make_tree(dic, word, words=[], parent=None):
    children = []
    _self = { 'word': word, 'children': children, 'parent': parent, 'count': 0 }
    concat = words + [word]
    total_count = 0
    for w, count in search_next_words(dic, concat).items():
        child = make_tree(dic, w, concat, _self)
        children.append(child)
        total_count += count
    
    _self['count'] = total_count

    return _self

# ツリーのなかから一番出現回数が多い子供を抜き出す
def select_tree_node(tree):
    node = tree
    max_count = -1

    for child in tree['children']:
        if child['count'] > max_count:
            node = child
            max_count = child['count']
    
    if max_count >= 0:
        node = select_tree_node(node)

    return node

# ルートからそのツリーに至るまでのワードの配列を取得する
def collect_tree_path(tree):
    l = [tree['word']]
    if tree['parent'] is None:
        return l
    
    return collect_tree_path(tree['parent']) + l

# ツリーのノードを親から削除する
def remove_from_parent(tree):
    if tree['parent'] is None:
        return False
    
    parent = tree['parent']

    siblings = parent['children']
    siblings.remove(tree)
    parent['count'] -= tree['count']

    # 親が自分しか子供を持ってない場合は親もその親から削除する
    if len(siblings) == 0:
        return remove_from_parent(parent)
    
    return True

# デバッグ用にツリーの情報を表示する
def print_all(tree, l=[]):
    children = tree['children']
    l = l + ['{}({})'.format(tree['word'], tree['count'])]
    if len(children) == 0:
        print(' '.join(l))
    else:
        for child in children:
            print_all(child, l)


# ワードからそのワードから始まる文章を指定した数だけ取得する
def restore_sentence(dic, word, count = 5):
    tree = make_tree(dic, word)
    # print_all(tree)

    result = []

    while True:
        selected = select_tree_node(tree)
        path = collect_tree_path(selected)
        result.append(path)

        if len(result) >= count or not remove_from_parent(selected):
            break

    return result
