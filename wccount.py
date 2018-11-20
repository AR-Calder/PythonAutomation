#!/usr/bin/env python3
import tkinter as tk

window = tk.Tk();
window.withdraw()

# Prints number of chracters and words in current selection
print("characters: %s" % len(window.selection_get()))
print("words: %s" % len(window.selection_get().split()))
