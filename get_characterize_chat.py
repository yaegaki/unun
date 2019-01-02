# 配信を特徴となるようなチャットを抜き出す
import os
import restore_sentence

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

        # 復元したチャットには時間の情報がないのでそこも復元する
        for sentence in sentences:
            # sentenceは単語ごとの配列になっているので結合して文字列にする
            sentence_str = ''.join(sentence)

            # sentence_strが完全に含まれているチャットを探す
            for obj in objs:
                original_chat = obj['original']
                if original_chat.find(sentence_str) >= 0:
                    if not original_chat in memo:
                        memo.add(original_chat)
                        chats.append({'msec': obj['msec'], 'sentence': sentence_str})
                    break

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