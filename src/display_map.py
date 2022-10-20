import tkinter as tk
import os
import re
import json
from json.decoder import JSONDecodeError
from datetime import datetime
from PIL import Image, ImageTk

from logger import MapLogger


class MapBuilder:
    """
        Main class to instanciate a map explorer.
        Launches all the subclasses of the GUI components and the controller
        to collate all the elements together
    """
    def __init__(self, root_tk):
        self.root_tk = root_tk
        self.map_name = map_name

        self.controller = MapController(self.root_tk, self)
        # TODO cambiare le classi in sottoclassi di tkinter già configurate (?)
        self.canvas = MapCanvas(self.root_tk, self)
        self.sidebar = MapSidebar(self.root_tk, self)
        self.logger = MapLogger(self.root_tk, self)
        self.logger.grid(column=0, row=1)


class MapDisplayer:
    def __init__(self, root, map_name, canvas_w=1000, canvas_h=800):
        self.root = root
        self.canvas_w = canvas_w
        self.canvas_h = canvas_h
        self.buildings = {}
        self.sidebar_list = {}
        self.image_id = None
        self.saving_clicks = []
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

        # create button to add a new POI
        self.button_add_poi = tk.Button(
                self.buttons_frame,
                text='Nuovo POI',
                command=self.add_poi
            )
        self.button_add_poi.grid(column=0, row=0)

        # create button to remove POI
        self.button_delete_poi = tk.Button(self.buttons_frame, text='Rimuovi POI')
        self.button_delete_poi.grid(column=0, row=1)

        self.setup_new_map(map_name)


    def drop_down_selector(self, event):
        self.setup_new_map(self.variable.get())




if __name__ == '__main__':
    bg_image = 'Rexxentrun'
    main_window = tk.Tk()
    MapDisplayer(main_window, bg_image)
    main_window.mainloop()
