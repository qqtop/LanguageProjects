#! /usr/bin/python
# -*- coding: utf-8 -*-
import sys
import requests,json
from pprint import pprint
import time

# glosbe.py
# version 0.6
# using glosbe api
# this version will do translation of a word and try to get some
# example sentences , phrases and meanings if avaialable from glosbe
# Note : changed argument order to better handle multiple words input
#        future version will check for correct language code

# usage :   python glosbe.py en  jpn   sleeping bag    <--- fromlang  tolang  words

#http://pastebin.com/VvnamFPg
#http://pastebin.com/mb19CVHJ

def aline():
    # just print a seperator line
    print '-'*100


def getData(theWord,orglang,destlang):
       
    r= requests.get('http://glosbe.com/gapi/translate?from=%s&dest=%s&format=json&phrase=%s&pretty=true' % (orglang,destlang,theWord))
    try:
        
        jdata = json.loads(r.text)
        return jdata
      
    except:
            return -1
	   
	      
try:
  print '\n\n'
  print 'Translation from : ', sys.argv[1], ' to: ',sys.argv[2]
  theWord=''
  for xx in sys.argv[3:]:
     theWord=theWord+' '+xx
  theWord=str(theWord).strip(' ')
  print 'Results for word : ', theWord
  aline()
  orglang=str(sys.argv[1])
  destlang=str(sys.argv[2])
except:
   
  orglang = 'ind'
  destlang= 'eng'
  theWord = 'pantai'  # a default word  
  print '\n\n'
  print 'ATTENTION : Default setting used , as data not correctly specified on command line\n'
  print 'Usage: python glosbe.py  ind de   YOURWORDS '
  print '\n\nExample Output   : \n'
  print 'Translation from : ', orglang, ' to: ',destlang
  print 'Results for word : ', theWord
  aline()


### Main

start=time.clock()
data=getData(theWord,orglang,destlang)
if data== -1:
       print '\nHello : ',theWord,'  maybe mispelled or not the correct root word for dicitionary lookup or wrong language code'
       print 'Correct and try again'
else:	 
       
	  print 'From   :  ',data['from']
	  print 'Dest   :  ',data['dest']
	  print 'Result :  ',data['result']
	  print 'Phrases:  ',data['phrase']
	  print '\n'
	  print 'Translations : ',
	  # translation results
	  phr = data['tuc']
	  for item in range(0,len(phr)):
	     try:
	        print data['tuc'][item]['phrase']['text'],' , ',
             except:
	        pass
	  

print '\n\n\n Translation + Sample Sentence\n\n'
r2=requests.get('http://glosbe.com/gapi/translate?from=%s&dest=%s&format=json&tm=true&phrase=%s&pretty=true' % (orglang,destlang,theWord))
try:  
      data=json.loads(r2.text)
      # translation results
      phr = data['tuc']
      #pprint(phr)
      if len(phr)==0:
	      print '      Nothing returned from Glosbe'
      else:
	      # for formatting precalc maxl
	      maxl=0
	      ll=0
	      for item in range(0,len(phr)):
		try:
		  ll=len(str(phr[item]['phrase']['text']).encode('UTF-8').rstrip(' '))
		  if ll > maxl:
		    maxl=ll
		except:
		    ll=10
		    pass

		  
	      try:
		    print '\nPhrase/Meanings :\n'
		    if len(phr)==0:
		      print '      Nothing returned from Glosbe'
		    else:
		      for item in range(0,len(phr)):
			  try:
			      if phr[item]['phrase']['text'].encode('UTF-8') <> '':
				print 'Phrase   : ',phr[item]['phrase']['text'].encode('UTF-8').replace('&#39;',"'").replace('&rsquo;',"'").replace('&eacute;','`')
			  
				for itx in range(0,len(phr[item])):
				    try:
				      if phr[item]['meanings'][itx]['text'].encode('UTF-8') <> '':
					  print 'Meaning  : ',phr[item]['meanings'][itx]['text'].encode('UTF-8').replace('&#39;',"'").replace('&rsquo;',"'").replace('&eacute;','`')
				    except:
				      pass
			      aline()
			  except:
			    pass
				
	      except:
		#print 'Error in Phrase/Meanings'
		#raise
		pass	      
	      
	      try:
			    print '\n'
			    if data['tuc'][item]['phrase']['text']  <> ' ':
					  
				for ite in range(0,len(data['examples'])):
							      
				      ss= data['examples'][ite]['second'].encode('UTF-8').replace('<strong class="keyword">','')
				      ss=ss.replace('</strong>','').replace('#','').replace('|','')
						
				      sf= data['examples'][ite]['first'].replace('<strong class="keyword">','')
				      sf=sf.replace('</strong>','').replace('#','').replace('|','')
				      if sf.encode('utf-8') <> '':
					    print '\nExamples for : ',data['tuc'][item]['phrase']['text'] 
					    print sf.encode('utf-8')
					    print ss
				
	      except:
			      #raise
			      pass

except:
  
   #raise
   print 'JSon Error, maybe no data retrieved'
   print 'Re-try'


end=time.clock()
print '\n\nBye Bye and Thank You Glosbe\n\n'
print 'Duration : ',end-start,' secs'
print 'Tested on openSuse 13.1 , Ubuntu 14.04 and Mint 16 Debian\n'

