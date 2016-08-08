import pytronlinks as pytron
import time


def main():

    try:
        
        cur_time = time.localtime()
        hour = cur_time.tm_hour
        min = cur_time.tm_min
        sec = cur_time.tm_sec

        if hour > 12:
            hour -= 12
            chime = "{}:{}am".format(hour, min)
        else:
            hour = hour
            chime = "{}:{}pm".format(hour, min)
            
        return chime

        # AI.talk(chime)

    except Exception as e:
        pass

if __name__ == '__main__':
    AI = pytron.Client()
    main()
