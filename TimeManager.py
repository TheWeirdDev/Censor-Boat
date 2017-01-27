from click.termui import secho


class Time:
    time_str = '00:00:00'
    time_sec = 0
    time_min = 0
    time_hour = 0

def millis_to_time(millis):
    millis = millis/1000
    sec = millis % 60
    min = (millis - sec) / 60 % 60
    hour = (millis / 60 - min) /60
    return '{0:02d}:{1:02d}:{2:02d}.{3:02d}'.format(int(hour) , int(min) , int(sec) , int(millis%1*100))

def time_to_millis(time):
    times = time.split(':')
    hour = int(times[0])
    min = int(times[1])

    s = times[2].split('.')
    sec = int(s[0])
    mil = int(s[1])

    return (hour*3600*1000) + (min *60*1000) + (sec*1000) + mil *10
