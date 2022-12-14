import tkinter as tk
import os
import re
import json
from datetime import datetime
from PIL import Image, ImageTk


class MapDisplayer:
    def __init__(self, root, map_name, canvas_w=1000, canvas_h=800):
        self.root = root
        self.canvas_w = canvas_w
        self.canvas_h = canvas_h
        self.buildings = {}
        self.sidebar_list = {}
        self.image_id = None
        self.ps1 = '$: '

        self.operative_pane = tk.Frame(self.root)
        self.operative_pane.grid(column=0, row=0)

        self.logging_label = tk.Label(
                self.root,
                anchor='w',
                bg='black',
                fg='white',
                text=self.ps1
            )
        self.logging_label.grid(column=0, row=1)

        # create the map space
        self.canvas = tk.Canvas(
                self.operative_pane,
                width=self.canvas_w,
                height=self.canvas_h
            )
        self.canvas.grid(column=0, row=0)

        # create the sidebar with the list of places
        self.sidebar = tk.Frame(self.operative_pane)
        self.sidebar.grid(column=1, row=0)

        # Get the list of all possible maps
        map_list = os.listdir(os.path.join('data', 'maps'))
        # create a dict to map the name to the filename
        self.map_dict = {re.sub(r'\..*', '', i): i for i in map_list}

        self.variable = tk.StringVar(self.sidebar)
        self.variable.set(re.sub(r'\..*', '', map_name))

        # create the drop-down menu to select maps
        self.drop_down_maps = tk.OptionMenu(
                self.sidebar,
                self.variable,
                *self.map_dict.keys(),
                command=self.drop_down_selector
            )
        self.drop_down_maps.grid(column=0, row=0)

        # create the space to put all labels
        self.places_list = tk.Frame(self.sidebar)
        self.places_list.grid(column=0, row=1)

        # create the buttons frame
        self.buttons_frame = tk.Frame(self.sidebar)
        self.buttons_frame.grid(column=0, row=2)

        self.setup_new_map(map_name)


    def drop_down_selector(self, event):
        self.setup_new_map(self.variable.get())


    def log(self, input_text):
        self.logging_label.config(text=f'[{datetime.now()}] {self.ps1}{input_text}')


    def setup_new_map(self, map_name):
        # last hovered polygon in map. Initialized to be None at startup
        self.current_poly = None
        self.log(f'sto caricando la mappa di {map_name}...')

        # get the filename for the map
        map_filename = self.map_dict[map_name]

        # create canvas
        self.set_new_image(map_filename)

        # setup points of interest in both map and sidebar
        self.setup_poi(map_name)


    def set_new_image(self, map_name):
        # add the image to the canvas
        self.bg = self.import_image(map_name)
        self.canvas.delete(self.image_id)
        self.image_id = self.canvas.create_image(0, 0, anchor='nw', image=self.bg)

        # bind click event and hover event
        self.canvas.bind('<Button-1>', self.canvas_click_event)
        self.canvas.bind('<Motion>', self.poly_enter_event)


    def import_image(self, map_name):
        # load the image of the selected map
        map_image_path = os.path.join('data', 'maps', map_name)
        bg_image = Image.open(map_image_path)

        # resize the image
        self.bg_w, self.bg_h = bg_image.size
        self.resize_rate = min(self.canvas_w / self.bg_w, self.canvas_h / self.bg_h)
        bg_image = bg_image.resize(
                (
                    int(self.bg_w * self.resize_rate),
                    int(self.bg_h * self.resize_rate)
                )
            )

        # pad the image
        self.wpad = int(self.canvas_w - self.bg_w*self.resize_rate) // 2
        self.hpad = int(self.canvas_h - self.bg_h*self.resize_rate) // 2
        final_image = Image.new(
                bg_image.mode,
                (self.canvas_w, self.canvas_h),
                'black'
            )
        final_image.paste(bg_image, (self.wpad, self.hpad))

        # return the final image
        return ImageTk.PhotoImage(final_image)


    def setup_poi(self, map_name):
        self.map_details = os.path.join('data', 'poi', f'{map_name}.json')

        # load details about the selected map
        try:
            with open(self.map_details) as f:
                self.map_details = json.load(f)
        except FileNotFoundError:
            self.map_details = []

        # delete old labels
        for k, v in self.buildings.items():
            v.destroy()

        # delete old polygons
        for k, v in self.sidebar_list.items():
            self.canvas.delete(v)

        self.buildings = {}
        self.sidebar_list = {}

        # create a polygon for each area of interest and add label in sidebar
        for i, value in enumerate(self.map_details):
            # adapt the coordinates to the resized image
            curr_coordinates = value['coordinates']
            for j in curr_coordinates:
                j[0] = int(j[0] * self.resize_rate + self.wpad)
                j[1] = int(j[1] * self.resize_rate + self.hpad)

            # create polygon and label
            poly = self.canvas.create_polygon(curr_coordinates, fill='', activefill='red')
            label = tk.Label(self.places_list, text=value['name'], anchor='n')
            label.grid(column=0, row=i)
            self.buildings[poly] = label
            self.sidebar_list[label] = poly



    def canvas_click_event(self, event):
        # aggiungere il click a una lista sulla root che poi viene usata per
        # creare nuovi punti di interesse da aggiungere alla mappa
        print(f'Clicked canvas: {event.x}, {event.y}')


    def poly_enter_event(self, event):
        pass
        self.log(f'{event.x}, {event.y}')
        # get the polygons under the cursor
        elem = self.canvas.find_overlapping(event.x, event.y, event.x+1, event.y+1)
        self.log(elem)

        # unset color if moved in another region
        if self.current_poly and self.current_poly not in elem:
            self.buildings[self.current_poly].configure(fg='black')
            self.current_poly = None

        # color the polygon under the region
        for i in elem:
            try:
                self.buildings[i].configure(fg='red')
            except KeyError:
                continue
            self.current_poly = i
            break

if __name__ == '__main__':
    bg_image = 'Rexxentrun'
    main_window = tk.Tk()
    MapDisplayer(main_window, bg_image)
    main_window.mainloop()
