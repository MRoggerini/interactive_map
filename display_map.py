import tkinter as tk
import os
import re
import json
from PIL import Image, ImageTk


class MapDisplayer:
    def __init__(self, root, map_name):
        self.current_poly = None
        self.root = root
        self.map_image_path = os.path.join('data', 'maps', map_name)
        self.map_details = os.path.join('data', 'poi', re.sub(r'\..*', '.json', map_name))

        # load the image of the selected map
        bg_image = Image.open(self.map_image_path)
        self.bg = ImageTk.PhotoImage(bg_image)
        bg_width, bg_height = bg_image.size

        # create a canvas
        self.canvas = tk.Canvas(self.root, width=bg_width, height=bg_height)
        self.canvas.grid(column=0, row=0)

        # add the image to the canvas
        self.canvas.create_image(0, 0, anchor='nw', image=self.bg)

        # create the sidebar with the list of places
        self.sidebar = tk.Frame(self.root)
        self.sidebar.grid(column=1, row=0)

        # bind click event and hover event
        self.canvas.bind('<Button-1>', self.canvas_click_event)
        self.canvas.bind('<Motion>', self.poly_enter_event)

        # load details about the selected map
        with open(self.map_details) as f:
            self.map_details = json.load(f)

        # create a polygon for each area of interest and add label in sidebar
        self.buildings = {}
        self.sidebar_list = {}

        for i, value in enumerate(self.map_details):
            poly = self.canvas.create_polygon(value['coordinates'], fill='', activefill='red')
            label = tk.Label(self.sidebar, text=value['name'], anchor='n')
            label.grid(column=0, row=i)
            self.buildings[poly] = label
            self.sidebar_list[label] = poly


    def canvas_click_event(self, event):
        # aggiungere il click a una lista sulla root che poi viene usata per
        # creare nuovi punti di interesse da aggiungere alla mappa
        print(f'Clicked canvas: {event.x}, {event.y}')


    def poly_enter_event(self, event, num=1):
        # get the polygons under the cursor
        elem = self.canvas.find_overlapping(event.x, event.y, event.x+1, event.y+1)

        # unset color if moved in another region
        if self.current_poly and self.current_poly not in elem:
            self.buildings[self.current_poly].configure(fg='black')

        # color the polygon under the region
        for i in elem:
            try:
                self.buildings[i].configure(fg='red')
            except KeyError:
                continue
            self.current_poly = i
            break

if __name__ == '__main__':
    main_window = tk.Tk()
    bg_image = 'Rexxentrun.jpg'
    MapDisplayer(main_window, bg_image)
    main_window.mainloop()
