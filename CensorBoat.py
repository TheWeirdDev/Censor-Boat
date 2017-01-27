import os , gi

gi.require_version('Gtk' , '3.0')
from gi.repository import  Gtk , Gdk
import TimeManager
import vlc
from FFmpeg import *


class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data : DeletePart):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.label = Gtk.Label(data.__str__())
        self.label.set_alignment(0,0.5)
        self.label.set_size_request(25,25)
        self.add(self.label)

    def get_delete_part(self):
        return self.data


class Main:

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('main.glade')
        self.window = self.get_object('window')
        self.play_area = self.get_object('play_area')
        self.time = self.get_object('time')
        self.seekbar = self.get_object('seekbar')
        self.play_button = self.get_object('play')
        self.set_from = self.get_object('set_from')
        self.set_to = self.get_object('set_to')
        self.from_time = self.get_object('from')
        self.to_time = self.get_object('to')
        self.volume = self.get_object('volume')
        self.volume.set_range(0,150)
        self.volume.set_value(70)
        self.remove = self.get_object('remove')
        self.input_choose = self.get_object('input_btn')
        self.output_choose = self.get_object('output_btn')
        self.input = self.get_object('input')
        self.output = self.get_object('output')
        self.add = self.get_object('add')
        self.list = self.get_object('list')
        self.list.set_sort_func(compare_rows)

        self.output_file = ''

        self.enable_controlls(False)

        self.setup_connectors()
        self.window.show_all()

    def setup_connectors(self):
        self.window.connect("destroy",self.quit)
        self.play_area.connect("realize",self._realized)
        self.play_area.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(0,0,0))

        self.play_button.connect('clicked' , self.play_toggle)
        self.seekbar.connect('change-value' , self.seekbar_change)
        self.seekbar.connect('button-release-event', self.seekbar_change)

        self.set_from.connect('clicked' , self.btn_from)
        self.set_to.connect('clicked' , self.btn_to)
        self.add.connect('clicked', self.add_item)
        self.remove.connect('clicked', self.remove_item)

        self.volume.connect('value-changed', self.volume_changed)

        self.input_choose.connect('clicked' , self.in_choose)
        self.output_choose.connect('clicked' , self.out_choose)

    #    def show(self):
#        pass

    def get_object(self , id):
        return self.builder.get_object(id)


    def play_toggle(self , *args):
        if self.player.is_playing():
            self.player.pause()
            self.play_button.set_image(Gtk.Image(stock=Gtk.STOCK_MEDIA_PLAY))
            self.play_button.set_label("Play")
        else:
            self.player.play()
            self.play_button.set_image(Gtk.Image(stock=Gtk.STOCK_MEDIA_PAUSE))
            self.play_button.set_label("Pause")

    def _realized(self, widget, data=None):
        self.vlcInstance = vlc.Instance("--no-xlib")
        self.player = self.vlcInstance.media_player_new()
        win_id = widget.get_window().get_xid()
        self.player.set_xwindow(win_id)
        #self.player.play()
        event = self.player.event_manager()
        event.event_attach(vlc.EventType.MediaPlayerTimeChanged , self.time_changed)
        event.event_attach(vlc.EventType.MediaFreed, self.media_freed)
        event.event_attach(vlc.EventType.MediaPlayerPlaying, self.playing)


    def get_time(self):
        return TimeManager.millis_to_time(self.player.get_time())

    def time_changed(self , *args):
        self.time.set_text(self.get_time())
        self.seekbar.set_value(self.player.get_position() * 100)

    def seekbar_change(self , *args):
        self.player.set_position(self.seekbar.get_value() / 100)
        self.time.set_text(self.get_time())

    def btn_to(self, *args):
        self.to_time.set_text(self.get_time())

    def btn_from(self, *args):
        self.from_time.set_text(self.get_time())

    def in_choose(self, *args):
        file_chooser = Gtk.FileChooserDialog("Pick a file", self.window,
                                            Gtk.FileChooserAction.OPEN,
                                           (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                            Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT))
        file_chooser.set_modal(True)
        file_chooser.connect("response", self.in_response)
        file_chooser.show()

    def in_response(self , dialog , id):
        if id == Gtk.ResponseType.ACCEPT:
            input_file = dialog.get_filename()
            self.input.set_text(input_file)
            self.player.stop()
            self.player.set_mrl(input_file)
            self.enable_controlls(True)
            self.seekbar.set_value(0)
            self.play_button.set_image(Gtk.Image(stock=Gtk.STOCK_MEDIA_PLAY))
            self.play_button.set_label("Play")
            childs = self.list.get_children()
            for i in childs:
                self.list.remove(i)

            print("opened: " + dialog.get_filename())
        elif id == Gtk.ResponseType.CANCEL:
            print("cancelled: FileChooserAction.OPEN")
        dialog.destroy()


    def out_choose(self, *args):
        save_dialog = Gtk.FileChooserDialog("Pick a file", self.window,
                                            Gtk.FileChooserAction.SAVE,
                                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                             Gtk.STOCK_SAVE, Gtk.ResponseType.ACCEPT))

        save_dialog.set_do_overwrite_confirmation(True)
        save_dialog.set_modal(True)
        save_dialog.connect("response", self.out_response)
        save_dialog.show()

    def out_response(self , dialog , id):
        save_dialog = dialog
        if id == Gtk.ResponseType.ACCEPT:
            self.output_file = save_dialog.get_filename()
            self.output.set_text(self.output_file)
        elif id == Gtk.ResponseType.CANCEL:
            print("cancelled: FileChooserAction.SAVE")
        dialog.destroy()

    def volume_changed(self , *args):
        self.player.audio_set_volume(int(self.volume.get_value()))
        print(self.volume.get_value())

    def media_freed(self , args):
        print('freed')

    def playing(self, args):
        print('playing')

    def enable_controlls(self , enable):
        for i in self.seekbar , self.play_button , self.set_to , self.set_from , self.to_time , self.from_time , self.add , self.volume:
            i.set_sensitive(enable)
        # self.seekbar.set_sensitive(enable)
        # self.play_button.set_sensitive(enable)
        # self.set_to

    def add_item(self , args):
        st = self.from_time.get_text()
        en = self.to_time.get_text()
        data = DeletePart(st, en)

        childs = self.list.get_children()
        for i in childs:
            if has_conflict(i.get_delete_part(),data):
                print("Error !!! {} & {}".format(i.get_delete_part() , data))
                return

        self.list.add(ListBoxRowWithData(data))
        self.list.show_all()

    def remove_item(self , args):
        self.list.remove(self.list.get_selected_row())

    def quit(self, *args):
        self.player.stop()
        Gtk.main_quit()


Main()
Gtk.main()

#print(TimeManager.millis_to_time(6784545))
#print(TimeManager.time_to_millis('15:45:34.93'))


# ff = FFmpegHelper()
# one = DeletePart(6784545 , 7784545)
# two = DeletePart(8784545 , 9784545)
# x = [two , one]
# s  = bubble_sort(x)
# for i in s:
#     print(i)
#     if has_conflict(DeletePart(5784545 , 5784547) , i):
#         print("error")

#print(ff.has_conflict(one , two))