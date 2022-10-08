import tkinter as tk
import os
from PIL import Image, ImageTk


def map_explorer(root, map_name):
    bg_image_path = os.path.join('data', 'maps', map_name)
    bg_image = Image.open(bg_image_path)
    root.bg = ImageTk.PhotoImage(bg_image)
    bg_width, bg_height = bg_image.size

    root.canvas = tk.Canvas(main_window, width=bg_width, height=bg_height)
    root.canvas.create_image(0, 0, anchor='nw', image=root.bg)
    root.canvas.pack()


if __name__ == '__main__':
    main_window = tk.Tk()
    bg_image = 'Rexxentrun.jpg'
    map_explorer(main_window, bg_image)
    main_window.mainloop()
