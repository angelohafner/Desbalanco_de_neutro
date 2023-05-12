import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class CapacitoresY:
    def __init__(self, m, n, d, horizontal_spacing, color='black', ax=None):
        self.m = m
        self.n = n
        self.d = d
        self.horizontal_spacing = horizontal_spacing
        self.color = color
        if ax is None:
            self.fig, self.ax = plt.subplots()
        else:
            self.ax = ax
            self.fig = ax.figure

    def draw_capacitor(self, x, y, color=None):
        color = color or self.color
        ax = self.ax

        plate_width = 1.5
        plate_height = 0.1
        spacing = 0.2

        top_plate = patches.Rectangle((x - plate_width / 2, y + spacing / 2), plate_width, plate_height,
                                      edgecolor=color, facecolor=color)
        bottom_plate = patches.Rectangle((x - plate_width / 2, y - plate_height - spacing / 2), plate_width,
                                         plate_height, edgecolor=color, facecolor=color)

        ax.add_patch(top_plate)
        ax.add_patch(bottom_plate)

        plt.plot([x, x], [y - plate_height - spacing / 2, y - plate_height - spacing / 2 - 0.5], color=color,
                 linewidth=1)
        plt.plot([x, x], [y + plate_height + spacing / 2, y + plate_height + spacing / 2 + 0.5], color=color,
                 linewidth=1)



# Exemplo de uso da função






