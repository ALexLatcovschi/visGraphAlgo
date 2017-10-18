import gobject
import gtk

class Bar(object):
    def __init__(self,widget):
        self.val=0
        self.scale = gtk.HScale()
        self.scale.set_range(0, 100)
        self.scale.set_update_policy(gtk.UPDATE_CONTINUOUS)
        self.scale.set_value(self.val)
        widget.add(self.scale)
        gobject.timeout_add(100, self.timeout)
    def timeout(self):
        self.val +=1
        self.scale.set_value(self.val)
        return True

if __name__=='__main__':
    win = gtk.Window()
    win.set_default_size(300,50)
    win.connect("destroy", gtk.main_quit)
    bar=Bar(win)
    win.show_all()
    gtk.main()