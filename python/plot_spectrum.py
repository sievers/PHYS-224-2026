#!/usr/bin/env python3
"""Plot the live microphone signal(s) with matplotlib.

Matplotlib and NumPy have to be installed.

"""
import argparse
import queue
import sys

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd

osamp=64
fs=[0]

def get_shifted(ts,thresh=0,rising=True):    
    n=len(ts)//2
    if rising:
        m1=ts[1:]>=thresh
        m2=ts[:-1]<thresh
    else:
        m1=ts[1:]<=thresh
        m2=ts[:-1]>thresh
    mask=m1&m2
    if np.sum(mask):
        ind=np.min(np.where(mask>0)[0])
        if ind<n:
            return ts[ind:ind+n]
    else:
        return ts[:n]

        
def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    'channels', type=int, default=[1], nargs='*', metavar='CHANNEL',
    help='input channels to plot (default: the first)')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-w', '--window', type=float, default=200, metavar='DURATION',
    help='visible time slot (default: %(default)s ms)')
parser.add_argument(
    '-i', '--interval', type=float, default=30,
    help='minimum time between plot updates (default: %(default)s ms)')
parser.add_argument(
    '-b', '--blocksize', type=int, help='block size (in samples)')
parser.add_argument(
    '-r', '--samplerate', type=float, help='sampling rate of audio device')
parser.add_argument(
    '-n', '--downsample', type=int, default=1, metavar='N',
    help='display every Nth sample (default: %(default)s)')
args = parser.parse_args(remaining)
if any(c < 1 for c in args.channels):
    parser.error('argument CHANNEL: must be >= 1')
mapping = [c - 1 for c in args.channels]  # Channel numbers start with 1
q = queue.Queue()


def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    #print('indata is ',indata.shape,args.downsample)
    # Fancy indexing with mapping creates a (necessary!) copy:
    q.put(indata[::args.downsample, mapping])


def get_spec(dat,osamp=2):
    n=len(dat)
    dd=np.zeros(osamp*n)
    x=np.linspace(-np.pi,np.pi,n)
    win=np.cos(x)/2+0.5
    dd[:n]=(win*(dat-dat.mean()))
    return np.abs(np.fft.rfft(dd))
    
def update_plot(frame):
    """This is called by matplotlib for each plot update.

    Typically, audio callbacks happen more frequently than plot updates,
    therefore the queue tends to contain multiple blocks of audio data.

    """
    global plotdata
    global pd
    while True:
        try:
            data = q.get_nowait()
        except queue.Empty:
            break
        shift = len(data)
        plotdata = np.roll(plotdata, -shift, axis=0)
        #print('plotdata shape is ',plotdata.shape)
        plotdata[-shift:, :] = data
        pd[:]=get_shifted(plotdata[:2*len(pd),0],thresh=0.01)
        #tmp=np.abs(np.fft.rfft(pd))

        tmp=np.abs(get_spec(pd,osamp))
        #nsamp original = len(pd), so # of samples = len(pd)*osamp
        #and time = len(pd)*osamp/fs, dnu=fs[0]/(len(pd)*osamp)
        dnu=fs[0]/(len(pd)*osamp)
        #print('dnu is ',dnu)
        nskip=int(np.ceil(20/dnu))
        ind=np.argmax(tmp[nskip:])+nskip
        print('peak freq: ',ind*dnu)
        
        if len(tmp)>len(pd):
            pd[:]=tmp[:len(pd)]/np.sqrt(len(tmp))
        else:
            pd[:len(tmp)]=tmp
            pd[len(tmp):]=0
    for column, line in enumerate(lines):
        #line.set_ydata(plotdata[:, column])
        line.set_ydata(pd)
    return lines


try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        args.samplerate = device_info['default_samplerate']
    fs[0]=args.samplerate
    length = int(args.window * args.samplerate / (1000 * args.downsample))
    #print('downsample is ',1000*args.downsample)
    print('length is ',length,args.window,args.samplerate,args.downsample)
    dnu=args.samplerate/length/args.downsample/osamp
    print('length is ',length, ' and dnu is ',dnu)
    plotdata = np.zeros((length, len(args.channels)))
    pd=np.zeros(length//2)

    fig, ax = plt.subplots()
    #lines = ax.plot(plotdata)
    xx=np.arange(len(pd))*dnu*2 #2 I think is from half-length rfft
    #lines = ax.plot(xx,pd)
    lines = ax.semilogx(xx,pd)
    if len(args.channels) > 1:
        ax.legend([f'channel {c}' for c in args.channels],
                  loc='lower left', ncol=len(args.channels))
    #ax.axis((0, len(plotdata), -1, 1))
    #ax.axis((0, len(pd)*dnu, -0.1, 1))
    ax.axis((20, len(pd)*dnu*10, -0.1, 1))
    ax.set_yticks([0])
    ax.yaxis.grid(True)
    ax.set_xlabel('Freq (Hz)')
    ax.tick_params(bottom=True, top=False, labelbottom=True,
                   right=False, left=False, labelleft=False)
    fig.tight_layout(pad=0)

    stream = sd.InputStream(
        device=args.device, channels=max(args.channels),
        samplerate=args.samplerate, callback=audio_callback)
    ani = FuncAnimation(fig, update_plot, interval=args.interval, blit=True)
    with stream:
        plt.show()
except Exception as e:
    parser.exit(1, type(e).__name__ + ': ' + str(e))
