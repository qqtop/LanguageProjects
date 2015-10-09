# -*- coding: utf-8 -*-


# #####################################################################################
# Program     : indoG6.py 
# Status      : Useable
# License     : MIT opensource  
# Version     : 1.0
# Compiler    : python 2.7.8
# Description : Simple Terminal based Indonesian/English Translator
#               wrapped around trans ex http://www.soimort.org/translate-shell/
#               
# Notes       :  awk or gawk needs to be installed
#                using following word prefix switches:
# 
#                -e  for english:indonesian look up 
#                -v  full
#                -b  brief  
#                -a  automatic language detection to english
#                -o  same as trans accepts all arguments as per trans incl -p but no -I
#                -clearhist     will clear the buffer
#
#                words and sentences are automatically wrapped into 'my look up word'
#                for improved translation , automatically we first try id:en ,
#                if nothing found we try en:id
#                
# Issues      :  Occasionally the line is not cleared to the beginning on screen               
# 
# Usage       :  kata: -e what a nice day
#                kata: -v saya suka tidur 
#                kata: -o -b en:ja "I like to have a beer"
#                kata: -a wo ist der Bahnhof
# Tested on   :  Linux            
# ProjectStart:  2015-01-10
# Todo        : 
# Last        :  2015-03-03   
# 
# Programming :  Eternal Tester
# 
# #####################################################################################
# #####################################################################################

import os
import sys
import codecs
import subprocess
import time,readline,thread
import struct,fcntl,termios
import atexit
import shutil
import socket
import sh
from termcolor import colored, cprint

# open a file to keep last few results
# change path filenames as required
afile    = '/dev/shm/indoG6.txt'  # .. on ubuntu maybe /dev/run 
savefile = '/home/lxuser/Dropbox/indoG6.txt'


#  some info
PROG    = "indoG6.py      : Indonesian/English Translator using trans [soimort]"
VERSION = " - 2015/03/03"
STATUS  = "Status         : Production"
PROD    = "Programming by : Eternal Tester"

tc = 0
i  = 0
theWord = ''
aWord   = ''
aline = 20*"-"

print ""
print colored(PROG, 'green')
print colored(STATUS + VERSION, 'green')
print colored(PROD, 'yellow', attrs=['reverse'])
print '\n'


# buffer for raw_input  code from stackoverflow
def blank_current_readline():
    # Next line said to be reasonably portable for various Unixes
    (rows,cols) = struct.unpack('hh', fcntl.ioctl(sys.stdout, termios.TIOCGWINSZ,'1234'))

    text_len = len(readline.get_line_buffer())+2

    # ANSI escape sequences (All VT100 except ESC[0G)
    sys.stdout.write('\x1b[2K')                         # Clear current line
    sys.stdout.write('\x1b[1A\x1b[2K'*(text_len/cols))  # Move cursor up and clear line
    sys.stdout.write('\x1b[0G')                         # Move to start of line


# terminal size code is from here:
# http://blog.taz.net.au/2012/04/09/getting-the-terminal-size-in-python/
def get_terminal_size(fd=1):

    try:
        hw = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
    except:
        try:
            hw = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            hw = (25, 80)

    return hw


def get_terminal_height(fd=1):

    if os.isatty(fd):
        height = get_terminal_size(fd)[0]
    else:
        height = 999

    return height


def get_terminal_width(fd=1):

    if os.isatty(fd):
        width = get_terminal_size(fd)[1]
    else:
        width = 999

    return width


def doGoog(sw):
                
        okres=""
        if len(sw) > 0:
                   
                    
          bflag=False
          eflag=False
          vflag=False
          aflag=False
          oflag=False
          
          # original trans needs usual trans arguments
          if "-o" in sw:
            oflag=True
            sw=sw.replace("-o","")
          
          if oflag == False:
          
                  if "-b" in sw:
                          bflag=True
                          sw=sw.replace("-b","")
                  if "-v" in sw:
                          vflag=True
                          sw=sw.replace("-v","")  
                  if "-e" in sw:
                          eflag=True
                          sw=sw.replace("-e","")
                          
                  if "-a" in sw:
                          aflag=True
                          eflag=False
                          sw=sw.replace("-a","")
                  
                  # for better translation and less typing
                  sw="'"+sw+"'"
                               
                  if eflag==False and aflag==False:
                        # assume id:en first                                      
                        if vflag==True :
                                  s = 'trans -v id:en %s' % sw
                                  p = subprocess.Popen(s, stdout=subprocess.PIPE, shell=True)
                                  output, err = p.communicate()
                                  okres=output
                                
                              
                        else: 
                                s = 'trans -b id:en %s' % sw   
                                p = subprocess.Popen(s, stdout=subprocess.PIPE, shell=True)
                                output, err = p.communicate()
                                okres=output.replace('\n',' ')
                                
                                        
                        # now if nothing returned maybe its english
                        # we change to capitals in case of any camels...
                              
                        if "'"+okres.upper().rstrip(" ")+"'" == sw.upper():
                                          
                        
                            if vflag==True :
                                s = "trans -v en:id %s" % sw
                                p = subprocess.Popen(s, stdout=subprocess.PIPE, shell=True)
                                output, err = p.communicate()
                                okres=output
                                                          
                            else: 
                                s = 'trans -b en:id id %s' % sw   
                                p = subprocess.Popen(s, stdout=subprocess.PIPE, shell=True)
                                output, err = p.communicate()
                                okres=output.replace('\n',' ')
                                
                                  
                  elif eflag==True or okres.upper().startswith(sw.upper()):
                  
                            
                            if vflag==True:
                              s = 'trans -v en:id %s' % sw
                                                      
                            else:  
                              s = 'trans -b en:id %s' % sw   
                                                    
                            p = subprocess.Popen(s, stdout=subprocess.PIPE, shell=True)
                            output, err = p.communicate()
                            okres=output.replace('\n',' ')
                      
                              
                  elif aflag==True:
                            # automatic language finder  
                            if vflag==True:
                              s = 'trans -v  %s' % sw
                                                      
                            else:  
                              s = 'trans -b  %s' % sw   
                                                    
                            p = subprocess.Popen(s, stdout=subprocess.PIPE, shell=True)
                            output, err = p.communicate()
                            okres=output.replace('\n',' ')
                            
                            
          else:
                 # we try to pipe original trans
                  s = 'trans %s' % sw   
                                                  
                  p = subprocess.Popen(s, stdout=subprocess.PIPE, shell=True)
                  output, err = p.communicate()
                  okres=output.replace('\n',' ')
                      
                 
          
          
          okres=okres.replace('[1m','')
          okres=okres.replace('[21m','') 
          return okres   

    
def closer():
    # this runs upon ctrl-c to exit shell
    f.close()
    shutil.copy2(afile,savefile)
    
    print '\nindoG6.txt copied to Dropbox!'
    # also clear the /dev/shm
    os.remove(afile)
    print 'Sampai Jumpa\n'

def checkInternet():
  
      REMOTE_SERVER = "www.google.com"
    
      try:
        # see if we can resolve the host name -- tells us if there is a DNS listening
        host = socket.gethostbyname(REMOTE_SERVER)
        # connect to the host -- tells us if the host is actually reachable
        s = socket.create_connection((host, 80), 2)
        return True
      except:
        pass
      return False
      
      
#### main ####

os.system('clear')
atexit.register(closer)

if len(sys.argv) > 1:
    aWord = sys.argv[1]


# if a savefile exists but no afile than we load it as afile so to have some continuity
if not os.path.exists(afile):
  if os.path.exists(savefile):
    # we read line by line and write each line imm. this may save memory for long files here 
    with open(savefile,'r') as infile:
      with open(afile,'a') as outfile:
        for line in infile:
            outfile.write(line)

# if file does not exist create it
with open(afile,'a') as f:
    
 while True:
       
    if aWord == '':
        tc = 0
        blank_current_readline() # this does the magic
        theWord = raw_input(colored('\nKata: ', 'yellow'))
        
    else:
        theWord = aWord
        aWord = ''  # need this to avoid endless looping

    os.system('clear')
    theWord=theWord.rstrip(" ")
    cI=checkInternet()
    
    if theWord== "-clearhist":
       os.remove(savefile)
       # we also clear the open afile
       f.seek(0)
       f.truncate()
             
       print colored("History cleared ok","cyan")
    
    elif cI == True:
          if len(theWord) > 0:  
                
                resgoog=doGoog(theWord)
                #we try to read and print the prev data using sh
                for line in sh.tr(sh.tail("-n 30", afile , _piped=True), "[:upper:]", "[:lower:]", _iter=True):
                    print(line.strip('\n'))
                
                # print a line the length of the reply    
                ll=len(resgoog)+len(theWord)+7
                if ll > get_terminal_width():
                   ll = get_terminal_width()
                  
                print colored("-"*ll,"green")
                rgs=resgoog.split("     ")
                
                
                # clean the word of prefixes
                if "-b" in theWord: theWord=theWord.replace("-b","")
                if "-v" in theWord: theWord=theWord.replace("-v","")
                if "-e" in theWord: theWord=theWord.replace("-e","")
                if "-a" in theWord: theWord=theWord.replace("-a","")
                
                print colored(theWord.strip(),"green")
                rgs=resgoog.split("   ")
                if len(rgs) < 3:
                      print colored(resgoog,"white")
                
                else:
                    for rgx in range(0,len(rgs)):
                       if rgs[rgx] <> "":
                          print colored(rgs[rgx],"white")
                
                # we also add it to an in memory buffer which on atexit
                # will be copied to dropbox
                try:
                    aggline=theWord+' - '+resgoog+'\n'
                    f.write(aggline)
                    f.flush()
                    print
                except:
                  # we may get here if enter is pressed without a word 
                  # which wud make resgoog a non object
                  print
                  
                # print some centered text
                ll=get_terminal_width()
                mmsg=" Finished / Selesai "
                
                sll = (ll - len(mmsg))/2
                sll = sll -1
                sl  = "-" * sll
                
                print colored(sl,"green"),colored(mmsg,"magenta"),colored(sl,"green")
                
          else:
                  print colored("indoG6.py Indonesian/English/Indonesian Translator (trans)","green")
                  print ""
                  print colored("Usage : word in english or indonesian","green")
                  print "        prefix word with -e to force english"
                  print "        prefix word with -v more output"
                  print "        prefix word with -b less output  default"
                  print "        prefix word with -a any language to english"
                  print "        if -v and -b selected then default will be -v"
                  print "        input -clearhist only to clear all history"
                  print "        Press : Ctrl-C to Exit"
                  print colored("\nProgrammed by : Alien2 ","green")

    else:
           print colored("-"*get_terminal_width(),"red")
           print colored('\n没有互联网连接 - Currently no network connection - Saat ini tidak ada koneksi jaringan')
           print colored("-"*get_terminal_width(),"red")


##################################################################################################
# copy of trans options most can be used with -o 
#Usage: trans [options] [source]:[target] [text] ...
       #trans [options] [source]:[target1]+[target2]+... [text] ...

#Options:
  #-V, -version
    #Print version and exit.
  #-H, -h, -help
    #Show this manual, or print this help message and exit.
  #-r, -reference
    #Print a list of languages (displayed in endonyms) and their ISO 639 codes for reference, and exit.
  #-R, -reference-english
    #Print a list of languages (displayed in English names) and their ISO 639 codes for reference, and exit.
  #-v, -verbose
    #Verbose mode. (default)
  #-b, -brief
    #Brief mode.
  #-w [num], -width [num]
    #Specify the screen width for padding when displaying right-to-left languages.
  #-browser [program]
    #Specify the web browser to use.
  #-p, -play
    #Listen to the translation.
  #-player [program]
    #Specify the command-line audio player to use, and listen to the translation.
  #-x [proxy], -proxy [proxy]
    #Use proxy on given port.
  #-I, -interactive
    #Start an interactive shell, invoking `rlwrap` whenever possible (unless `-no-rlwrap` is specified).
  #-no-rlwrap
    #Don't invoke `rlwrap` when starting an interactive shell with `-I`.
  #-E, -emacs
    #Start an interactive shell within GNU Emacs, invoking `emacs`.
  #-prompt [prompt_string]
    #Customize your prompt string in the interactive shell.
  #-prompt-color [color_code]
    #Customize your prompt color in the interactive shell.
  #-i [file], -input [file]
    #Specify the input file name.
  #-o [file], -output [file]
    #Specify the output file name.
  #-l [code], -lang [code]
    #Specify your own, native language ("home/host language").
  #-s [code], -source [code]
    #Specify the source language (language of the original text).
  #-t [codes], -target [codes]
    #Specify the target language(s) (language(s) of the translated text).