import os,sys,time


# A very basic and simple way to access the gkamus-id,gkamus-en files
# from http://gkamus.sourceforge.net/ which are opensource. Thank you.

# we just open the file and read until we find what we need
# since python is fast this works well.

# usage :  python gkamus.py  setelah
#          python gkamus.py  morning 
#          python gkamus.py

aWord=''
global tc
tc=0
def gkamid(sw):
  global tc
  global linelist
  s=1
  c=0
  with open('gkamus-id.dict','r+') as f:
    while s <> '':
       s= f.readline()
       c+=1
       if s.startswith(sw) :   #for more output we cud do : if sw in s :
          print c,'-id : ',s
          tc+=1
 
 
def gkamen(sw):
  global tc
  s=1
  c=0
  with open('gkamus-en.dict','r+') as f:
    while s <> '':
       s= f.readline()
       c+=1
       if s.startswith(sw) :   #for more output we cud do : if sw in s :
          print c,'-en : ',s
          tc+=1

# main
if len(sys.argv) > 1:
	aWord=sys.argv[1]
while 1:
      start=time.clock()
      if aWord=='':
        tc=0
	linelist=[]
	print '-'*100
	theWord=raw_input('\nWord/Kata :  ')
      else:
        theWord=aWord
        aWord=''  # need this to avoid endless looping
      
      # we just run over both files ,its fast
      
      gkamid(theWord)
      gkamen(theWord)
	
      end=time.clock()
      print '\nDuration : ',end-start,' secs.'
      print 'Finished gkamus Lookup, Search returned :',tc,' lines','            Ctrl-C to Quit'
