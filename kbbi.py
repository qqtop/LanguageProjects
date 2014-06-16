 
#! /usr/bin/python
# -*- coding: utf-8 -*-
import sys
import requests
from bs4 import BeautifulSoup
import time  
# kbbi.py
# Access the Kamus Besar Bahasa Indonesia (KBBI) in a terminal
# version 0.85
# Note : improved parsing memuat section for suggestions of root word or others per kbbi


def aline():
    # just print a seperator line
    print '-'*100


  
def getData(theWord):
    r= requests.get('http://kbbi.web.id/%s' % theWord)
    return r.text
	
  
def processData(dx):
    gdx = getData(dx)
    soup = BeautifulSoup(gdx,"lxml")
    sxt = soup.get_text()
    atitle= soup.title.string.split('- definisi kata')
    
    print '\n',atitle[0]
    aline()
    print '\nKata : ',atitle[1]
    
    
    sxts = sxt.split('Pranala (link): http://kbbi.web.id/%s' % dx )
    
    try:
      sxts2=sxts[1]
      sxts2= sxts2.split('Tweet')
      res1 = sxts2[0]
      res1 = res1.split(';')
     
      print res1[0].strip('-1').strip('-2').strip('-3')
      for rx in range(1,len(res1)):
	rc  = res1[rx]
	print rc,'\n'
     
    except:
       	print
	print dx,' ==>  Tidak ditemukan - KBBI\n\n'
	print 'Maybe incorrect root word'
	# we want to get data from the Memuat section , if any
	sxtch= sxt.split('Memuat')
	try:
	  sxtchz= sxtch[1].split('Pranala')
	  print 'Try with these suggestions provided by kbbi (if any)  :'
	  print sxtchz[0].replace('1','\n').replace('2','\n').replace('3','\n') # occasionaly there is are subscripts
	
	except:
	  pass
  
 
## Main
start=time.clock()
try:
  theWord=sys.argv[1]   # the word , preferably is a valid Indonesian word
except:
  print '\n\nAttention : Default word used ! '
  print 'Usage     : python kbbi.py YOURWORD\n'
  theWord= 'doyan'  # a default word  

aline()  
processData(theWord)
  
  
end=time.clock()
aline()
print 'Duration : ',end-start,' secs'
print 'Kamus Besar Bahasa Indonesia (KBBI) \n'
# usage:  python kbbi.py abadi

