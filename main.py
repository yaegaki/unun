import os
import sys
import codecs
import random
import numpy as np

import MeCab
from wordcloud import WordCloud
from PIL import Image

from normalize_neologd import normalize_neologd
import vocabulary

font = sys.argv[1]

# 使用されている用語を探し出す
print('get vocabulary from files.')
vocabulary_dic = vocabulary.get_vocabulary_dic()
# 使用されている単語が配信でどれくらいの割合で使用されているのかを計算する
print('calc vocabulary use rate.')
vocabulary_use_rate = vocabulary.calc_total_use_rate(vocabulary_dic)

mask_image_pathes = [
    './iori_mask.png',
    './mokotaiori_mask.png',
]

masks = [np.array(Image.open(f)) for f in mask_image_pathes]


def get_keywords_text(keywords):
    # ランダムにしておかないとなぜか同じ単語が近い位置に出てきてしまうことがあるのでその対策
    random.shuffle(keywords)

    # WordCloud用に空白区切りの文字列にする
    return ' '.join(keywords)

settings = [
    # [enable_filter, mask, output_prefix]
    # [False, masks[0], 'all'],
    [True, masks[1], 'part'],
]


def make_wordcloud(path, vocabulary, font, background_color, contour_color):
    print('start wordcloud for {}.'.format(path))

    keywords = []
    for keyword, count in vocabulary.items():
        keywords.extend([keyword] * count)

    keywords_text = get_keywords_text(keywords)
    file_name_without_ext = os.path.splitext(os.path.basename(path))[0]

    for setting in settings:
        enable_filter = setting[0]
        mask = setting[1]
        desc = setting[2]

        sw = set()
        if enable_filter:
            total_keywords_count = len(keywords)
            for keyword, count in vocabulary.items():
                # 今回の出現率と全体での出現率の比
                local_per_global = (count / total_keywords_count) / vocabulary_use_rate[keyword]
                # 比が二倍より小さい場合は他の放送でもよく出ているものとして扱う
                if local_per_global < 2:
                    sw.add(keyword)

        # マスク画像使うとそのサイズになるのでwidthとheightは指定しない
        wordcloud = WordCloud(
            background_color=background_color,
            contour_width=3,
            contour_color=contour_color,
            font_path=font,
            stopwords=sw,
            mask=mask,
        ).generate(keywords_text)

        wordcloud.to_file('./wc/{}-{}.png'.format(file_name_without_ext, desc))

# 出力先ディレクトリがなければ作る
if not os.path.isdir('./wc'):
    os.makedirs('./wc')

for file, vocabulary in vocabulary_dic.items():
    make_wordcloud(file, vocabulary, font, 'white', 'hsl(193, 96%, 82%)')
