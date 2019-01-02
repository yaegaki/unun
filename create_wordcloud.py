import os
import codecs
import random
import numpy as np

from PIL import Image
from wordcloud import WordCloud


mask = np.array(Image.open('./mokotaiori_mask.png'))

def get_keywords_text(keywords):
    # ランダムにしておかないとなぜか同じ単語が近い位置に出てきてしまうことがあるのでその対策
    random.shuffle(keywords)

    # WordCloud用に空白区切りの文字列にする
    return ' '.join(keywords)

def create_wordcloud(font, vocabulary, vocabulary_use_rate, output_path):
    print('create wordcloud for {}.'.format(output_path))
    background_color = 'white'
    contour_color = 'hsl(193, 96%, 82%)'

    keywords = []
    for keyword, count in vocabulary.items():
        keywords.extend([keyword] * count)

    keywords_text = get_keywords_text(keywords)

    sw = set()
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

    wordcloud.to_file(output_path)