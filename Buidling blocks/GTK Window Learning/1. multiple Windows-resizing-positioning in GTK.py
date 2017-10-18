import gi
from gi.repository import Gtk
from pprint import pprint

# see all GTk documentation here http://lazka.github.io/pgi-docs/Gtk-3.0/classes/Window.html


def window_destroyer(theWindow, event):
	print 'in the doestroyer function'
	del theWindow
	window_destroyer.destroy_count += 1
	if window_destroyer.destroy_count == 2:
		print 'Exiting Program'
		Gtk.main_quit()	

# function are really objects. window_destroyer.destroy_count here acts as static variable 
window_destroyer.destroy_count = 0

print gi.__file__
win = Gtk.Window(title="win 1111")
win.connect("delete-event", window_destroyer)


print '{:>50} : {}'.format('get_position()' , win.get_position())
print '{:>50} : {}'.format('get_pointer()' , win.get_pointer())
print '{:>50} : {}'.format('get_size()' , win.get_size())


# get current monitor height and width http://lazka.github.io/pgi-docs/Gdk-3.0/classes/Screen.html#Gdk.Screen
print '{:>50} : {}'.format('get_screen().height()' , win.get_screen().height())
print '{:>50} : {}'.format('get_screen().width()' , win.get_screen().width())

# get_monitor_geometry(monitor_number int ) returns Gdk.Rectangle http://lazka.github.io/pgi-docs/Gdk-3.0/classes/Rectangle.html#Gdk.Rectangle  

print '{:>50} : {}'.format('get_screen().get_monitor_geometry(0).height' , win.get_screen().get_monitor_geometry(0).height)
print '{:>50} : {}'.format('get_screen().get_monitor_geometry(0).width' , win.get_screen().get_monitor_geometry(0).width)
print '{:>50} : {}'.format('get_screen().get_monitor_geometry(0).x' , win.get_screen().get_monitor_geometry(0).x)
print '{:>50} : {}'.format('get_screen().get_monitor_geometry(0).y' , win.get_screen().get_monitor_geometry(0).y)


# let us set the win windows as per logger window requirement
# this function sets the size of window
win.resize(win.get_screen().width() * .3,win.get_screen().height())

# setting window position
# win.set_pointer(0,0) --does not work
win.move(win.get_screen().width() * .7,0)
win.show_all()

win2 = Gtk.Window(title = "win 2222")
win2.connect("delete-event", window_destroyer)
win2.show_all()


Gtk.main()