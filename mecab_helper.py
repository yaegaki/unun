def parse_mecab_result(str):
    result = []
    # 形態素が行ごとにあるのでそれで分割していく
    for row in str.split('\n'):
        cols = row.split('\t')
        if (len(cols) == 0):
            continue

        word = cols[0]
        if word == 'EOS' or len(cols) < 2:
            continue

        part = cols[1].split(',')[0]
        result.append({'word':word, 'part':part})

    return result