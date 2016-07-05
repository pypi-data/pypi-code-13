import string

def rotate_letter(letter, n):
    """
        Rotate a letter by n places
    """
    if letter.isupper():
        start = ord('A')
    elif letter.islower():
        start = ord('a')
    else:
        return letter

    c = ord(letter) - start
    i = (c + n) % 26 + start
    return chr(i)


def rotate_word(word, n,encode_bool=True):
    """
        Rotate a word by n places.

        encode_bool = True =>encode
        else decode
    """

    out_str = ''
    if encode_bool==False:
        n = -1*n

    for letter in word:
        out_str += rotate_letter(letter, n)
    return out_str


if __name__ == '__main__':

    while True:
        inp_str = raw_input("enter string to encode/decode,enter 0 to stop: ")
        if inp_str=='0':
            break

        rot_id = raw_input("enter id of rotation : ")
        opt = raw_input("enter e to encode , other to decode : ")

        encode_bool = False
        if opt=='e':
            encode_bool = True
            print '\nEncoded string : ',rotate_word(inp_str,int(rot_id),encode_bool)
        else:
            print '\nDecoded string : ',rotate_word(inp_str,int(rot_id),encode_bool)


    print 'id = 13 , decode this one ;)'
    print 'yngre ubzvr'