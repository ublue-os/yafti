import inspect

from gi.repository import Gtk, Adw


print("Adw")
print("\n".join([n for n, obj in inspect.getmembers(Adw) if inspect.isclass(obj)]))
print("Gtk")
print("\n".join([n for n, obj in inspect.getmembers(Gtk) if inspect.isclass(obj)]))
