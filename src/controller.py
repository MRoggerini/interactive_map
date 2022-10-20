import tkinter as tk
import os
import json
from json.decoder import JSONDecodeError
from PIL import Image, ImageTk

from popup_poi import NamePoiPopup


class MapController:
    """
        Contains all the commands and functions to make the map displayer work
    """
    def __init__(self, builder):
        self.builder = builder


    def setup_new_map(self, map_name):
        """
            Import a new map given a map name
            Input:
                - map_name: the name of the map to load. Default at startup,
                          at runtime it is provided from the drop down menu
            Action:
                - loads the map from file and imports the associated POIs
        """

        # clears the last hovered poly
        self.builder.current_poly = None
        self.builder.logger.log(f'sto caricando la mappa di {map_name}...')

        # get the filename for the map
        map_filename = self.builder.map_dict[map_name]

        # create canvas
        self.set_new_image(map_filename)

        # setup points of interest in both map and sidebar
        self.setup_poi(map_name)


    def set_new_image(self, map_name):
        """
            change the canvas displayed image and clears all the polygons
            Input:
                - map_name: the name of the map to load. Default at startup,
                          at runtime it is provided from the drop down menu
            Action:
                - change the displayed image
        """
        # add the image to the canvas
        bg = self.import_image(map_name)
        bg = self.resize_image(bg)
        self.builder.canvas.set_new_bg(bg)


    def import_image(self, map_name):
        """
            loads the image and resize it
            Input:
                - map_name: the name of the map to load. Default at startup,
                          at runtime it is provided from the drop down menu
            Action:
                - change the displayed image
        """
        # load the image of the selected map
        map_image_path = os.path.join('data', 'maps', map_name)
        return Image.open(map_image_path)


    def resize_image(self, bg_image)
        # resize the image
        bg_w, bg_h = bg_image.size
        resize_rate = min(
                self.builder.canvas_w / bg_w,
                self.builder.canvas_h / bg_h
            )
        self.builder.resize_rate = resize_rate

        bg_image = bg_image.resize(
                (
                    int(bg_w * self.resize_rate),
                    int(bg_h * self.resize_rate)
                )
            )

        # pad the image
        wpad = int(self.builder.canvas_w - bg_w*resize_rate) // 2
        hpad = int(self.builder.canvas_h - bg_h*resize_rate) // 2
        self.builder.wpad = wpad
        self.builder.hpad = hpad

        final_image = Image.new(
                bg_image.mode,
                (self.builder.canvas_w, self.builder.canvas_h),
                'black'
            )
        final_image.paste(bg_image, (wpad, hpad))

        # return the final image
        return ImageTk.PhotoImage(final_image)


    def import_poi(self, map_name):
        self.builder.map_details_file = os.path.join('data', 'poi', f'{map_name}.json')

        # load details about the selected map
        try:
            with open(self.builder.map_details_file) as f:
                self.builder.map_details = json.load(f)
        except (FileNotFoundError, JSONDecodeError):
            self.builder.map_details = []


    def setup_poi(self, map_name):
        # import the pois from the correct file
        self.import_poi(map_name)

        # delete old labels
        for k, v in self.builder.buildings.items():
            v.destroy()

        # delete old polygons
        for k, v in self.builder.sidebar_list.items():
            self.builder.canvas.delete(v)

        self.builder.buildings = {}
        self.builder.sidebar_list = {}

        # create a polygon for each area of interest and add label in sidebar
        for i, value in enumerate(self.builder.map_details):
            # adapt the coordinates to the resized image
            in_coordinates = value['coordinates']
            curr_coordinates = []
            for w, h in in_coordinates:
                w = int(w * self.builder.resize_rate + self.builder.wpad)
                h = int(h * self.builder.resize_rate + self.builder.hpad)
                curr_coordinates.append([w, h])

            # create polygon and label
            poly = self.builder.canvas.create_polygon(
                    curr_coordinates,
                    fill='', activefill='red'
                )
            label = tk.Label(
                    self.builder.places_list,
                    text=value['name'], anchor='n'
                )
            label.grid(column=0, row=i)
            self.builder.buildings[poly] = label
            self.builder.sidebar_list[label] = poly


    def add_poi(self):
        # change button text to 'Salva POI'
        self.builder.button_add_poi.configure(text='Salva POI')

        # change button callback to save_poi
        self.builder.button_add_poi.configure(command=self.save_poi)

        # change map click callback
        self.builder.canvas.toggle_new_poi()

        # clear currently clicked coordinates
        self.builder.saving_clicks = []


    def save_poi(self):
        # get the name of the POI
        self.builder.popup_poi = NamePoiPopup(self.root, self)


    def ask_name_collect(self, poi_name):
        # close the popup window
        self.builder.popup_poi.destroy()

        # change button text back to 'Nuovo POI'
        self.builder.button_add_poi.configure(text='Nuovo POI' command=self.add_poi)
        self.builder.button_add_poi.begin_add_poi()

        # change map click callback
        self.canvas.toggle_new_poi()

        # collect and remap clicked points
        poi_coordinates = []
        for w, h in self.builder.saving_clicks:
            w = (w - self.builder.wpad) / self.builder.resize_rate
            h = (h - self.builder.hpad) / self.builder.resize_rate
            poi_coordinates.append([w, h])

        # save the new POI in dict
        self.builder.map_details.append(
                {
                    'name': poi_name,
                    'coordinates': poi_coordinates
                }
            )
        self.export_poi()

        # reload map
        self.setup_new_map(self.variable.get())


    def export_poi(self)
        # save dict in file
        with open(self.builder.map_details_file, 'w') as f:
            json.dump(self.builder.map_details, f, indent=4)
