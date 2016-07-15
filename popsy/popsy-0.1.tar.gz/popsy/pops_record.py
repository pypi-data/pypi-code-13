from read_stream import POPSStream
from read_config import POPS
import process_stream as process
import Queue
import time

'''
Reads streaming data from a POPS instrument via UDP or serial, calculates
several size distribution parameters, and writes streaming data to a csv file.
'''


def main():
    p = POPS()  # initiate a POPS object containing attributes of the instrument
    POPSQueue = Queue.Queue()

    myThread = POPSStream(0, POPSQueue)  # 0 = UDP; 1 = serial
    myThread.udp_ip = '127.0.0.1'  # change to either POPS or client IP?
    myThread.udp_port = 5050  # POPS sends UDP Status data to port 5200
    myThread.start()

    # --- create output file
    filename = time.strftime("POPS_%Y%m%d_%H%M%S.csv")
    f = open(filename, 'w')
    n = 0
    prev_nbins = None
    diam_label = 'BinLimits_Diameter_nm, '
    UDP_fails = 0

    while UDP_fails < 3:  # -- main loop
        if not POPSQueue.empty():
            line = POPSQueue.get()
            if line == 'UDP timeout':
                UDP_fails += 1
                if UDP_fails == 1:
                    print 'No UDP data received after ' + str(UDP_fails) + ' try.'
                else:
                    print 'No UDP data received after ' + str(UDP_fails) + ' tries.'
                continue
            data = process.parse_incoming(p, line)
            nbins = data['nbins']
            if nbins != prev_nbins:
                print 'change in number of bins'
                f.write(diam_label +
                        str([int(i) for i in data['diam_lim']]).strip('[]') +
                        '\n')
            prev_nbins = nbins
            print data['time'], data['nconc']
            f.write(line)
        time.sleep(0.1)
        n += 1

    myThread.join()  # stops the thread

if __name__ == "__main__":
    main()
