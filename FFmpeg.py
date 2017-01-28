import subprocess, os , time

class FFmpegHelper:
    def censor(self, array, input, output, progress):
        i = 0
        while i < len(array):
            number = '{0:03d}.mkv'.format(i)
            if(i==0):
                subprocess.Popen(['ffmpeg' , '-i' , input , '-to' , array[i].start_time , '-c:a' , 'copy' , '-c:v' , 'copy' , output+number])
                i+=1
                #progress.set_value(len(array)/i *100)
                continue

            subprocess.Popen(['ffmpeg', '-i', input, '-ss' , array[i-1].end_time,'-to', array[i].start_time, '-c:a' , 'copy' , '-c:v' , 'copy' , output+number])
            i+=1
            #progress.set_value(len(array) / i * 100)

        subprocess.Popen(['ffmpeg', '-i', input, '-ss', array[len(array)-1].end_time, '-c:a', 'copy', '-c:v', 'copy', output + "end.mkv"])
        progress.set_value(50)
        listtxt = output + "CONCATLIST.TXT"
        with open(listtxt, 'w') as lt:
            j = 0
            while j < i:
                lt.write("file '"+output+ "{0:03d}.mkv'\n".format(j))
                j += 1
            lt.write("file '" +output + "end.mkv'")
        time.sleep(5)
        subprocess.Popen(['ffmpeg' ,'-f' ,'concat' ,'-safe' ,'0' ,'-i' ,listtxt ,'-c' ,'copy' ,output])
        time.sleep(5)
        j = 0
        while j < i:
            os.remove(output+ "{0:03d}.mkv".format(j))
            j+=1
        os.remove(output + "end.mkv")
        os.remove(listtxt)
        progress.set_value(100)


        #subprocess.Popen([])

