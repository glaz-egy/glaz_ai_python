import MeCab
import twitterbot
from random import choice
import datetime
import time

def DataCreate(text, mecab, num=3):
    text = text.strip()
    if text == '\n': return
    raw = mecab.parse(text)
    raw = raw.strip().split('\n')
    datalist = []
    for data in raw:
        datalist.append(data.split('\t')[0])
    datalist.remove('EOS')
    returnlist = []
    for i in range(len(datalist)+ (0 if num == 3 else 1)):
        if num == 2:
            returnlist.append(['BOS' if i == 0 else datalist[i-1], datalist[i] if i < len(datalist) else 'EOS'])
        elif num == 3:
            returnlist.append(['BOS' if i == 0 else datalist[i-1], datalist[i], datalist[i+1] if i+1 < len(datalist) else 'EOS'])
    return returnlist

def Markov(datalist, num=3):
    nextstring = next(datalist, ['BOS'], Start=True, num=num)
    out = nextstring[0] if nextstring[0] != 'BOS' else ''
    while True:
        if nextstring[1] == 'EOS': return out
        out += nextstring[1]
        nextstring = next(datalist, nextstring, num=num)
        if len(out) > 140:
            nextstring = next(datalist, ['BOS'], Start=True, num=num)
            out = nextstring[0] if nextstring[0] != 'BOS' else ''

def next(datalist, s, Start=False, num=3):
    if num == 2:
        if Start: nextlist = [data for data in datalist if data[0] == s[0]]
        else: nextlist = [data for data in datalist if data[0] == s[1]]
    else: nextlist = [data for data in datalist if data[0] == s[0] and (Start or data[1] == s[1])]
    ch = choice(nextlist)
    print(ch)
    return (ch if num == 2 else ch[1:])

def main():
    #twitterbot.get_tweet()
    num=2
    with open('textdata.txt', 'r', encoding='utf-8') as f:
        textdata = f.readlines()
    datalist = []
    mecab = MeCab.Tagger()
    for text in textdata:
        datalist.extend(DataCreate(text, mecab, num=num))
    tweettext = Markov(datalist, num=num)
    print(tweettext)
    twitterbot.post_tweet(tweettext)
    twitterbot.auto_follow()
    twitterbot.check_limit()

if __name__=='__main__':
    while True:
        print(datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S]'))
        main()
        time.sleep(600)
    