def __init__(self, parent, option, **kwargs):
    ttk.Frame.__init__(self, parent, **kwargs)
    self.parent = parent
    self.option = option

    # TODO: Add more options.

    ttk.Checkbutton(self, text="Debugging Mode", variable=self.option.variable_debug).grid(row=0, column=0, sticky="we")
    ttk.Checkbutton(self, text="Scrollbars", variable=self.option.variable_scrollbars).grid(row=1, column=0,
                                                                                            sticky="we")
    ttk.Checkbutton(self, text="Grid", variable=self.option.variable_grid).grid(row=2, column=0, sticky="we")
    ttk.Checkbutton(self, text="Grid Highlight", variable=self.option.variable_grid_highlight).grid(row=3, column=0,
                                                                                                    sticky="we")

    frame_colour = ttk.Frame(self)
    ttk.Label(frame_colour, text="Highlight Colour").grid(row=0, column=0)
    ttk.Combobox(frame_colour, textvariable=self.option.variable_highlight_colour,
                 values=["white", "red", "blue", "yellow", "green", "purple", "orange", "pink"], state="readonly",
                 width=7).grid(row=0, column=1)
    frame_colour.grid(row=4, column=0, sticky="we")

    ttk.Checkbutton(self, text="Extra Speed Arrows", variable=self.option.variable_extra_speed_arrows).grid(row=5,
                                                                                                            column=0,
                                                                                                            sticky="we") 