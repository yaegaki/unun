# 配信を特徴となるようなチャットを抜き出す
import os
import restore_sentence
from normalize_neologd import normalize_neologd

def restore_chat(mecab, id, keywords):
    livechat_json_path = './livechat/{}.json'.format(id)
    morpheme_dic = restore_sentence.make_word_to_morpheme_list_dict(mecab, livechat_json_path)

    chats = []
    memo = set()
    count = 0
    for keyword in keywords:
        if keyword not in morpheme_dic:
            continue
        
        # キーワードを含むチャットについての情報
        # [{'msec': 0, 'original': '', 'words': ['', ...]}]
        objs = morpheme_dic[keyword]

        # キーワードから復元したチャット
        sentences = restore_sentence.restore_sentence(morpheme_dic, keyword)

        # 登録されたかどうかチェック用
        appended = False

        # 復元したチャットには時間の情報がないのでそこも復元する
        for sentence in sentences:
            # sentenceは単語ごとの配列になっているので結合して文字列にする
            sentence_str = ''.join(sentence)
            # mecabで'do it'のような単語をパースしたときに固有名詞扱いになって1単語になるものがある
            # チャットを探すときに都合が悪いのでスペースを削除する
            sentence_str_for_search = sentence_str.replace(' ', '')

            # sentence_strが完全に含まれているチャットを探す
            for obj in objs:
                # ノーマライズして空白を削除
                original_chat = normalize_neologd(obj['original']).replace(' ', '')
                if original_chat.find(sentence_str_for_search) >= 0:
                    # keywordによっては既に選ばれたsentence_strが候補になる可能性がある
                    # 例えば'二'というkeywordと'二重'というキーワードがあったとき、同じものが選ばれる可能性がある
                    # それと元々のチャットのなかにほぼ同じ内容があった場合、形態素解析の都合上かぶってしまうことがある
                    # '昨日は十五夜だったね' => ['昨日', 'は', '十', '五', '夜', 'だっ', 'た', 'ね', 'EOS', '']
                    # '十五夜だったね' => ['十五夜', 'だっ', 'た', 'ね', 'EOS', '']
                    # のように十五夜がバラバラにされた場合、別のsentenceとして表れてしまう
                    if not sentence_str in memo:
                        memo.add(sentence_str)
                        chats.append({'msec': obj['msec'], 'sentence': sentence_str})
                        appended = True
        
        if not appended:
            print('warning, not appended - {}'.format(keyword))

        # 500単語分登録する
        count = count + 1
        if count >= 500:
            break
    
    return chats

def get_characterize_chat(mecab, id, vocabulary, vocabulary_use_rate):
    dic = {}

    total_count = 0
    for count in vocabulary.values():
        total_count += count

    for keyword, count in vocabulary.items():
        if keyword not in vocabulary_use_rate:
            continue

        rate = count / total_count
        dic[keyword] = rate

    w = sorted(dic.items(), key=lambda x: x[1], reverse=True)

    words = []
    for keyword, rate in w:
        local_per_global = rate / vocabulary_use_rate[keyword]
        if local_per_global > 2:
            words.append(keyword)
    
    return restore_chat(mecab, id, words)