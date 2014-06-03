#! /usr/bin/python
# -*- coding: utf-8 -*-
import sys
import requests,json,subprocess
from pprint import pprint

# initial version
# accessing Indonesian - English Dictionary at kateglo
# http://pastebin.com/AFY0DFGZ

# this is now an improved version
# which also inludes translation for all_relation phrases
# but it hits google hard
# 
# also we cud try to parse some stuff from the kateglo proverb site
# and translate it , but this is currently not required..

# functionality here used now in qtJJ2.py ! ID button

# now moved google trans to doTranslate and added translation to def_text,sample,proverbs
#http://pastebin.com/xaBP4Uep
# latest 2014-05-27



def aline():
    # just print a seperator line
    print '-'*100


def getData(theWord):
    r= requests.get('http://kateglo.com/api.php?format=json&phrase=%s' % theWord)
    try:
        
        jdata = json.loads(r.text)
        return jdata
      
    except:
            return -1
	   
def doTranslate(zx):
    
    tm=''
    if len(zx)> 1:
	s = 'awk -f /data4/PythonStuff/Python/QtPython/qtJapan/translate.awk {=en} %s' % '"' + zx + '"'  # yeah escape like this so we get rid of errors for high comma words like : I'm nice
	p = subprocess.Popen(s, stdout=subprocess.PIPE, shell=True)
	output, err = p.communicate()
	tm = output.rstrip()
	tm = tm.replace('\n', ' ').replace('\r', '')  # \r also catches carriage returns
	tm = tm + '  [G]'  # mark it as google translation
    return tm



def translator(data):
    
      
        trResult=[]
        c=0
        for x in range(len(data['kateglo']['translations'])):
	      # we only want 1 result usually first is from ebsoft
	      # if not the other result would be from gkamus
	      c+=1
	      if c==2: # in case you want both just change this top c>0 or c==2 for gkamus only
	        trResult.append(data['kateglo']['translations'][x]['ref_source'])  
	        trResult.append(data['kateglo']['translations'][x]['translation'])
	  
               
	#print '\nInformation for Phrase : ',data['kateglo']['phrase']
	#pprint(data)  # uncomment this for all stuff
	
	if c==0:
	  trResult.append('None found . Check correct, spelling and root word')

        return trResult 

   
def definitor(data):
        # for a nicer output we precalc the max length of the keys
        # print data['kateglo']['definition']
	kmax=0
	dfResult=[]
	for zd in data['kateglo']['definition']:
	      for k in zd:
		if len(k) > kmax:
		  kmax=len(k)

	for zd in data['kateglo']['definition']:
	      for k in zd:
		  #print k,' '*(kmax-len(k)),'  :  ',zd[k] # we show only 2 interesting rows from thsi data block
		  if k=="def_text":
                     try:		    
		       dfT=k.capitalize()+' '*(kmax-len(k))+'  :  \n\n'+zd[k]
		       dfResult.append(dfT)
		       dfResult.append(doTranslate(zd[k]))
		     except:
		        pass
		  if k=='sample':
		     try:
		       dfS='\n'+ k.capitalize()+' '*(kmax-len(k))+'  :  \n\n'+zd[k]
		       dfResult.append(dfS)
		       dfResult.append(doTranslate(zd[k]))
		     except:
		         pass
	      dfResult.append('-'*100)
	      
        return dfResult
	


def proverbor(data):
       prResult=[]
       for x in range(len(data['kateglo']['proverbs'])):
	      prResult.append(data['kateglo']['proverbs'][x]['meaning'])
	      prResult.append(doTranslate(data['kateglo']['proverbs'][x]['meaning']))
	      
	      
       if len(prResult)<1:
	   prResult.append('None')
       prResult.append('-'*100)
       
       return prResult
     
     
def proverbMaster(theWord):
    # we try to access http://kateglo.com/?phrase=ikan&mod=proverb
    #r= requests.get('http://kateglo.com/?phrase=%s&mod=proverb' % theWord)
    try:
        # this wud return the first page of possibly many
        # but in html which we wud need to parse with beautifulsoup
        # something for a rainy day.
        # start with <ul><p>
        #print(r.text)
        pass
      
    except:
            return -1


def relator(data):
       #print data['kateglo']['all_relation']

       # for a nicer output we precalc the max length of k
       kmax=0
       rlResult=[]
       try:
         for zd in data['kateglo']['all_relation']:
           for k in zd:
		if len(k) > kmax:
		  kmax=len(k)
       except:
	 pass
       
       
       rlmax=0
       try:
         for zd in data['kateglo']['all_relation']:
	    for k in zd:
		  if k=="related_phrase": # comment this out to get the whole data block and prappend k, to below statement
		    if len(zd[k]) > rlmax:
	                rlmax=len(zd[k])
       except:
	 pass
                              
       
       
       
       try:
         for zd in data['kateglo']['all_relation']:
	    for k in zd:
		  if k=="related_phrase": # comment this out to get the whole data block and prappend k, to below statement
		    try:
		      #rlResult.append(' '*(kmax-len(k))+' '+zd[k]) 
		      # we also try to get the translations for the relations so
		      # while this works for single words it does not for two words yet
		      # like ikan asin tried this..
		      #datarel=getData(zd[k])
		      #reltr=translator(datarel)
		      #for relx in reltr:
		          #rlResult.append(relx)
		    		      
		      tm = doTranslate(zd[k])
		      
		      
		      rlResult.append(zd[k]+' '*(rlmax-len(zd[k]))+'  -  '+tm.decode('utf8'))
		         

                      # however we are hitting google a lot , it wud be better to
                      # have this in one call , however this means packing unpacking 
                      # tried but if we do not one by one we might not be able
                      # to align correctly if google returns more than one result
                      # so above is still the best if we want a translation for all_relations
                           
		      
		    except:
		        raise
		      
		      
	 

       except:
	  rlResult.append('None')
	  
       rlResult.append('-'*100)

       return rlResult


	      

try:
  print '\n\nResults for : \n\n'
  print sys.argv[1]
  theWord=sys.argv[1]   # the word must be a valid indonesian word obviously
except:
  theWord= 'doyan'  # a default word  



data=getData(theWord)
if data== -1:
       print '\nHello : ',theWord,'  maybe mispelled or not Indonesian or not the correct root'
       print 'Correct and try again'
else:	    
       tr=translator(data)
       aline()
       print '\nPhrase : ',theWord
       rxc=0
       for rx in tr:
	    if rxc==0:
		print 'Source : ',rx
	    else:
		print rx
	    rxc+=1   
	    aline()

       df=definitor(data)
       
       print "\nDefinitions\n"
       for rx in df:
	   print rx

       pr=proverbor(data)
             
       print "\nProverbs\n"
       for rx in pr:
	   print rx
      
      
       rl=relator(data)
      
       print "\nRelations\n"
       for rx in rl:
	   print rx

# experimental  see above
#print 'Test for proverbMaster'
#pm=proverbMaster(theWord)

  

print '\nBye Bye and Thank You Kateglo\n\n'
