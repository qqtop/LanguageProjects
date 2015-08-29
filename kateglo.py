#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import requests
import json
import subprocess
import time
from pprint import pprint


# Accessing Indonesian - English Dictionary at kateglo
# latest 2015-08-29


def aline():
    # just print a seperator line
    print '-' * 80


def getData(theWord):
    r = requests.get(
        'http://kateglo.com/api.php?format=json&phrase=%s' % theWord)

    try:

        jdata = json.loads(r.text)
        return jdata

    except:
        return -1


def doTranslate(zx):

    tm = ''

    if os.path.isfile('translate.awk'):

        if len(zx) > 1:

            # yeah escape like this so we get rid of errors for high comma
            # words like : I'm nice
            s = 'awk -f translate.awk {=en} %s' % '"' + zx + '"'
            p = subprocess.Popen(s, stdout=subprocess.PIPE, shell=True)
            output, err = p.communicate()
            tm = output.rstrip()
            # \r also catches carriage returns
            tm = tm.replace('\n', ' ').replace('\r', '')
            tm = tm + '  [G]'  # mark it as google translation

    return tm


def translator(data):

    trResult = []
    c = 0
    for x in range(len(data['kateglo']['translations'])):
        # we only want 1 result usually first is from ebsoft
        # if not the other result would be from gkamus
        c += 1
        # in case you want both just change this top c>0 or c==2 for gkamus
        # only
        if c == 2:
            trResult.append(data['kateglo']['translations'][x]['ref_source'])
            trResult.append(data['kateglo']['translations'][x]['translation'])

    # print '\nInformation for Phrase : ',data['kateglo']['phrase']
    # pprint(data)  # uncomment this for all stuff

    if c == 0:
        trResult.append('None found . Check correct, spelling and root word')

    return trResult


def definitor(data):
    # for a nicer output we precalc the max length of the keys
    # print data['kateglo']['definition']
    kmax = 0
    dfResult = []
    for zd in data['kateglo']['definition']:
        for k in zd:
            if len(k) > kmax:
                kmax = len(k)

    for zd in data['kateglo']['definition']:
        for k in zd:
                # print k,' '*(kmax-len(k)),'  :  ',zd[k] # we show only 2
                # interesting rows from thsi data block
            if k == "def_text":
                try:
                    dfT = k.capitalize() + ' ' * (kmax - len(k)) + \
                        '  :  \n\n' + zd[k]
                    dfResult.append(dfT)
                    dfResult.append(doTranslate(zd[k]))
                except:
                    pass
            if k == 'sample':
                try:
                    dfS = '\n' + k.capitalize() + ' ' * (kmax - len(k)) + \
                        '  :  \n\n' + zd[k]
                    dfResult.append(dfS)
                    dfResult.append(doTranslate(zd[k]))
                except:
                    pass
        dfResult.append('-' * 100)

    return dfResult


def proverbor(data):
    prResult = []
    for x in range(len(data['kateglo']['proverbs'])):
        prResult.append(data['kateglo']['proverbs'][x]['meaning'])
        prResult.append(doTranslate(data['kateglo']['proverbs'][x]['meaning']))

    if len(prResult) < 1:
        prResult.append('None')
    prResult.append('-' * 100)

    return prResult


def proverbMaster(theWord):
    # we try to access http://kateglo.com/?phrase=ikan&mod=proverb
    #r= requests.get('http://kateglo.com/?phrase=%s&mod=proverb' % theWord)
    try:
        # this wud return the first page of possibly many
        # but in html which we wud need to parse with beautifulsoup
        # something for a rainy day.
        # start with <ul><p>
        # print(r.text)
        pass

    except:
        return -1


def relator(data):
    # print data['kateglo']['all_relation']
    # for a nicer output we precalc the max length of k
    kmax = 0
    rlResult = []
    try:
        for zd in data['kateglo']['all_relation']:
            for k in zd:
                if len(k) > kmax:
                    kmax = len(k)
    except:
        pass

    rlmax = 0
    try:
        for zd in data['kateglo']['all_relation']:
            for k in zd:
                # comment this out to get the whole data block and prappend k,
                # to below statement
                if k == "related_phrase":
                    if len(zd[k]) > rlmax:
                        rlmax = len(zd[k])
    except:
        pass

    try:
        for zd in data['kateglo']['all_relation']:
            for k in zd:
                # comment this out to get the whole data block and prappend k,
                # to below statement
                if k == "related_phrase":
                    try:

                        tm = doTranslate(zd[k])
                        rlResult.append(
                            zd[k] + ' ' * (rlmax - len(zd[k])) + '  -  ' + tm.decode('utf8'))

                    except:
                        raise

    except:
        rlResult.append('None')

    rlResult.append('-' * 100)

    return rlResult


# Main
start = time.clock()
try:
    print '\n\nResults for : \n\n'
    print sys.argv[1]
    # the word must be a valid indonesian word obviously
    theWord = sys.argv[1]
except:
    theWord = 'doyan'  # a default word


data = getData(theWord)
if data == -1:
    print '\nHello : ', theWord, '  maybe mispelled or not Indonesian or not the correct root'
    print 'Correct and try again'
else:
    tr = translator(data)
    aline()
    print '\nPhrase : ', theWord
    rxc = 0
    for rx in tr:
        if rxc == 0:
            print 'Source : ', rx
        else:
            print rx
        rxc += 1
        aline()

    df = definitor(data)

    print "\nDefinitions\n"
    for rx in df:
        print rx

    pr = proverbor(data)

    print "\nProverbs\n"
    for rx in pr:
        print rx

    rl = relator(data)

    print "\nRelations\n"
    for rx in rl:
        print rx

# experimental  see above
# print 'Test for proverbMaster'
# pm=proverbMaster(theWord)

end = time.clock()
print '\nDuration : ', end - start, ' secs'
print 'Kateglo - Kamus, Tesaurus dan Glosarium bahasa Indonesia.\n\n'
