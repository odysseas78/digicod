



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