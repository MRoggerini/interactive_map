import tkinter as tk


class NamePoiPopup(tk.Toplevel):
    def __init__(self, root_tk, builder):
        super(self).__init__(root_tk)
        self.root_tk = root_tk
        self.builder = builder

        self.title('Dai un nome a questo POI')

        self.ask_name_label = tk.Label(
                self,
                text='Dai un nome a questo POI:'
            )
        self.ask_name_label.grid(column=0, row=0)

        self.ask_name_textbox = tk.Text(self)
        self.ask_name_textbox.grid(column=0, row=1)

        self.ask_name_button = tk.Button(
                self,
                text='Conferma',
                command=self.ask_name_collect
            )
        self.ask_name_button.grid(column=0, row=2)


    def ask_name_collect(self):
        # collect the name from the textbox
        poi_name = self.ask_name_textbox.get(1.0, 1000.0)
        # destroy everything in the window
        self.ask_name_button.destroy()
        self.ask_name_textbox.destroy()
        self.ask_name_label.destroy()
        # call parent routine to save POI
        self.builder.controller.ask_name_collect(poi_name)
