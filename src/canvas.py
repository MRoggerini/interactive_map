import tkinter as tk


class MapCanvas(tk.Canvas):
    def __init__(self, root_tk, builder):
        super(self).__init__(root_tk)
        self.root_tk = root_tk
        self.builder = builder

        # tells the canvas if a new poi is being added
        self.new_poi = False

        # image currently shown
        self.image_id = None

        # polygon currently under the cursor
        self.current_poly = None

        # bind click event and hover event
        self.bind('<Button-1>', self.canvas_click)
        self.bind('<Motion>', self.poly_enter_event)


    def toggle_new_poi(self):
        self.is_new_poi = not self.is_new_poi


    def set_new_bg(self, image):
        self.delete(self.image_id)
        self.image_id = self.create_image(
                0, 0, anchor='nw', image=image
            )


    def canvas_click(self, event):
        self.builder.log(f'Clicked canvas: {event.x}, {event.y}')
        self.builder.saving_clicks.append([event.x, event.y])
        # TODO add line that connects the two points to give visual feedback


    def poly_enter_event(self, event):
        self.builder.log(f'{event.x}, {event.y}')
        # get the polygons under the cursor
        elem = self.find_overlapping(event.x, event.y, event.x+1, event.y+1)

        # unset color if moved in another region
        if self.current_poly and self.current_poly not in elem:
            self.builder.buildings[self.current_poly].configure(fg='black')
            self.current_poly = None

        # color the polygon under the region and the associated label
        for i in elem:
            try:
                self.builder.buildings[i].configure(fg='red')
            except KeyError:
                continue
            self.current_poly = i
            break
