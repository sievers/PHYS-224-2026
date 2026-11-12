import numpy as np
import audioread
import sounddevice as sd
import subprocess
try:
    import aifc
except:
    print('aifc not available (probably deprecated).  aiff files not readable.')


def get_key(mystr,key):
    i1=mystr.find(key)
    if i1<0:
        return 'Not found'
    i2=mystr.find('\n',i1+2)
    return mystr[i1+len(key):i2].strip()


    
def read_aac(fname,dtype='int16'):
    faad='faad'
    to_exec=faad + ' -i '+ fname  #first, read header so we can report song info
    aa=subprocess.check_output(to_exec,stderr=subprocess.STDOUT,shell=True)
    aa=aa.decode('ascii',errors='ignore')    #python3 requires explicitly converting to a string
    #print('aa is ',aa)
    nn=get_key(aa,'\nTitle        :')#we'll get name of song #NB - for old faad, it's Tille, not Title
    writer=get_key(aa,'\nComposer     :')  #and composer
    album=get_key(aa,'\nAlbum        :')
    myinfo=get_key(aa,'LC AAC') #we'll get some info about the file    
    tags=myinfo.split()
    rate=tags[-2]
    nchan=tags[-4]
    length=tags[0]
    if tags[1][-1]==',':
        tags[1]=tags[1][:-1]
    
    mystr=('playing ' + nn + ' from ' + album + ' by ' + writer + ' for ' + length + ' ' + tags[1])
    print("aa is: ",aa)
    print(mystr)
    #to_exec=faad+ ' -f2 -w -b4 ' + fname  #this magic command will have faad read data into float arrays
    to_exec=faad+ ' -f2 -w -b1 ' + fname  #b1 says read as int16
    ff=open('/dev/null','w')
    dd=subprocess.check_output(to_exec,stderr=ff,shell=True) #this calls faad to do the heavy lifting 
    ff.close()
    #dat=np.frombuffer(dd,dtype='float32') #convert string output from faad into numpy array
    dat=np.frombuffer(dd,dtype='int16') #convert string output from faad into numpy array
    nchan=int(nchan)
    dat=np.reshape(dat,[len(dat)//nchan,nchan])
    fs=int(rate) #get the sample rate the speakers are expecting
    #sd.play(dat,fs,blocking=False) #play through speakers using sounddevice
    #return float(length),mystr #return length of song.
    return dat,fs

def read_mp3(fname,dtype='int16'):
    #f=audioread.audio_open('Gt_OpenDiapSmall8_arp.mp3')
    f=audioread.audio_open(fname)
    buffs=[]
    for buff in f:
        buffs.append(buff)
    arrs=[]
    for buff in buffs:
        arrs.append(np.frombuffer(buff,dtype))
    vec=np.hstack(arrs)
    nchan=f.channels    
    if nchan>1:
        vec=np.reshape(vec,[len(vec)//nchan,nchan])
    return vec,f.samplerate


def read_aiff(fname):
    stuff=aifc.Aifc_read(fname)
    nchan=stuff.getnchannels()
    nframe=stuff.getnframes()
    fs=stuff.getframerate()
    dat=stuff.readframes(nframe)
    arr=np.frombuffer(dat,dtype='>i2')
    if nchan>1:
        arr=np.reshape(arr,[len(arr)//nchan,nchan])
    return arr,fs
def read_song(fname):
    tags=fname.strip().split('.')
    if len(tags)>1:
        extension=tags[-1]
        if extension in ['mp3']:
            return read_mp3(fname)
        if extension in ['aac','m4a','mp4']:
            return read_aac(fname)
        if extension in ['aiff']:
            return read_aiff(fname)
    print('did not recognize file type on ',fname)
