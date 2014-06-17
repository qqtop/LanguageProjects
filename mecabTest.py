# coding:utf-8
import MeCab

# worked ok 2014-05-24

test = "授業で日本語文書を単語に切り分けて，索引語リストを作りtf-idfを求めよという課題が出たので"


def pyMecab(s):

    print 'Test Ochasen\n'
    tagger = MeCab.Tagger('-Ochasen')
    result = tagger.parse(s)
    print(result)

    print '\nTest onyomi\n'
    tagger = MeCab.Tagger('-onyomi')
    result = tagger.parse(s)
    print(result)

    print '\nTest Owakati\n'
    tagger = MeCab.Tagger('-Owakati')
    result = tagger.parse(s)
    print(result)

pyMecab(test)


# example from stackoverflow for issues with raw text and maybe others
#rawtext = open("UTF.file", "rb").read()
#tagger = MeCab.Tagger()
#encoded_text = rawtext.encode('shift-jis', errors='ignore')
# print tagger.parse(encoded_text).decode('shift-jis', errors='ignore')
