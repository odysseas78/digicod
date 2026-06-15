


def jaccard_similarity(str1, str2):
    set1, set2 = set(str1.replace(' ','').replace('-','').lower()), set(str2.replace(' ','').replace('-','').lower())
    similarity = len(set1 & set2) / len(set1 | set2)
    return similarity


def arraycompare(list1, list2, threshold=0.8):
    similarity = 0
    for word1 in list1:
        for word2 in list2:
            similarity = jaccard_similarity(word1, word2)
            print(f'{word1} - {word2} {similarity}')
            print(similarity >= threshold)
            if similarity >= threshold:
                print(similarity)
                break
            return similarity
    return similarity


def random_code(length=16, low=True, up=True, num=True, spchr=True):
    import secrets
    lower = "abcdefghijklnopqrstuvwxyz"
    uper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    number = "1234567890"
    spchar = "+-/*!&$#?=@<>"
    chars = ""
    if low == True:
        chars += lower
    if up == True:
        chars += uper
    if num == True:
        chars += number
    if spchr == True:
        chars += spchar
    return ''.join([secrets.choice(chars) for i in range(length)])

    