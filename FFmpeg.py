import TimeManager

class DeletePart:
    start_time = ''
    end_time = ''
    start_millis = 0
    end_millis = 0

    def __init__(self , start , end ):
        if isinstance(start , str) and isinstance(end , str):
            self.start_millis = TimeManager.time_to_millis(start)
            self.end_millis = TimeManager.time_to_millis(end)
            if  self.start_millis >= self.end_millis:
                raise Exception("Error : start must be smaller than end")
            self.start_time = start
            self.end_time = end
        elif isinstance(start , int) and isinstance(end , int):
            if start >= end:
                raise Exception("Error : start must be smaller than end")
            self.start_time = TimeManager.millis_to_time(start)
            self.end_time = TimeManager.millis_to_time(end)
            self.start_millis = start
            self.end_millis = end
        else:
            raise Exception("Illegal arguments given")



    def __str__(self):
        return "{} --> {}".format(self.start_time , self.end_time)


def bubble_sort(arr):
    not_done = True
    while not_done:
        i = 0
        not_done = False
        while i < len(arr) - 1:
            if arr[i].start_millis > arr[i + 1].start_millis:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                not_done = True
            i += 1
    return arr

def compare_rows(one, two):
    if one.get_delete_part().start_millis < 0 or two.get_delete_part().start_millis < 0:
        return "Error"
    en1 = one.get_delete_part().end_millis
    # en2 = two.get_delete_part().end_millis
    # st1 = one.get_delete_part().start_millis
    st2 = two.get_delete_part().start_millis

    return st2 < en1

def has_conflict(dp1 : DeletePart, dp2 : DeletePart):
    en1 = dp1.end_millis
    en2 = dp2.end_millis
    st1 = dp1.start_millis
    st2 = dp2.start_millis

    one =   st2 <= en1 and en2 >= en1
    two =   st2 >= st1 and en2 <= en1
    three = st2 <= st1 and en2 >= st1

    return True if one or two or three else False


class FFmpegHelper:
    pass

