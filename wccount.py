#!/usr/bin/env python3
import tkinter as tk
import os

window = tk.Tk();
window.withdraw()

# Prints number of chracters and words in current selection
# Only tested in gnome3 environments

characters = len(window.selection_get())
words = len(window.selection_get().split())

print("characters: %s" % characters)
print("words: %s" % words)
os.system("notify-send 'wccount' 'words: %s, Characters %s'" % (words, characters))
