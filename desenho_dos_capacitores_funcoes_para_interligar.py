import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from desenho_dos_capacitores as dc
    def draw_parallel_capacitors(self, x, y, n, d, color=None):
        color = color or self.color
        for i in range(n):
            self.dc.draw_capacitor(x + i * d, y, color)

        # Conectar os pontos superiores
        plt.plot([x, x + (n - 1) * d], [y + 0.75, y + 0.75], color=color, linewidth=1)

        # Conectar os pontos inferiores
        plt.plot([x, x + (n - 1) * d], [y - 0.75, y - 0.75], color=color, linewidth=1)

    def draw_multiple_parallel_capacitors(self, x, y, n, d, m, vertical_spacing, color=None):
        color = color or self.color
        for i in range(m):
            self.draw_parallel_capacitors(x, y + i * vertical_spacing, n, d, color)
            if i > 0:
                # Conectar os conjuntos de capacitores com uma linha vertical
                plt.plot([x + (n - 1) * d / 2, x + (n - 1) * d / 2],
                         [y + (i - 1) * vertical_spacing + 0.75, y + i * vertical_spacing - 0.75], color=color,
                         linewidth=1)



    def show(self, xlim=None, ylim=None):
        if xlim is not None:
            plt.xlim(xlim)
        if ylim is not None:
            plt.ylim(ylim)
        self.ax.set_aspect('equal', adjustable='box')
        plt.axis('off')
        plt.show()


    def draw_bottom_connections(self, x1, x2, y, length, x_offset=0):
        x1 += x_offset
        x2 += x_offset
        y_bottom = y - 0.75 - length
        plt.plot([x1, x1], [y - 0.75, y_bottom], color=self.color, linewidth=1)
        plt.plot([x2, x2], [y - 0.75, y_bottom], color=self.color, linewidth=1)
        plt.plot([x1, x2], [y_bottom, y_bottom], color=self.color, linewidth=1)
        self.xmed = x1
        self.ymed = y_bottom

    def draw_top_connections(self, x, y, length, x_offset=0):
        x += x_offset
        y_top = y + 0.75 + length
        plt.plot([x, x], [y + 0.75, y_top], color=self.color, linewidth=1)

    def draw(self, x_offset=0):
        m = self.m
        n = self.n
        d = self.d
        horizontal_spacing = self.horizontal_spacing
        color = self.color

        self.draw_multiple_parallel_capacitors(x_offset + 0, 0, n, d, m, 4)
        self.draw_multiple_parallel_capacitors(x_offset + n * d + horizontal_spacing, 0, n, d, m, 4)
        self.draw_multiple_parallel_capacitors(x_offset + 2 * (n * d + horizontal_spacing), 0, n, d, m, 4)

        x1 = (n - 1) * d / 2
        x2 = n * d + horizontal_spacing + (n - 1) * d / 2
        x3 = 2 * (n * d + horizontal_spacing) + (n - 1) * d / 2
        self.draw_bottom_connections(x1, x2, 0, 2, x_offset)
        self.draw_bottom_connections(x2, x3, 0, 2, x_offset)

        y_top = (m - 1) * 4
        self.draw_top_connections(x1, y_top, 2, x_offset)
        self.draw_top_connections(x2, y_top, 2, x_offset)
        self.draw_top_connections(x3, y_top, 2, x_offset)

        return [self.xmed, self.ymed]



def show_plot(xlim=None, ylim=None):
    plt.gca()
    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)
    plt.axis('off')
    plt.show()


def draw_current_transformer(x, y, radius=0.5, color='black'):
    circle = plt.Circle((x, y), radius, edgecolor=color, facecolor='none', linewidth=1)
    plt.gca().add_artist(circle)

    angle = np.linspace(0, 2 * np.pi, 100)
    spiral_x = radius * (1 + 0.1 * angle) * np.cos(angle)
    spiral_y = radius * (1 + 0.1 * angle) * np.sin(angle)
    plt.plot(x + spiral_x, y + spiral_y, color=color, linewidth=1)
    plt.plot(x - spiral_x, y - spiral_y, color=color, linewidth=1)

def draw_vertical_lines_and_connector(x1, y1, x2, y2, color='black'):
    plt.plot([x1, x1], [y1, y1 - 2], color=color, linewidth=1)
    plt.plot([x2, x2], [y2, y2 - 2], color=color, linewidth=1)
    plt.plot([x1, x2], [y1 - 2, y2 - 2], color=color, linewidth=1)

    x_center = (x1 + x2) / 2
    y_center = y1 - 2 - 0.5
    draw_current_transformer(x_center, y_center)

def save_plot(filename):
    plt.axis('off')
    plt.savefig(filename, dpi=600, bbox_inches='tight')

#from capacitores_y import CapacitoresY  # Certifique-se de que a classe CapacitoresY está no arquivo capacitores_y.py

def generate_and_save_capacitor_plot(m=4, n=5, d=2.5, horizontal_spacing=6, filename='capacitores.png'):
    fig, ax = plt.subplots()

    capacitores1 = CapacitoresY(m=m, n=n, d=d, horizontal_spacing=horizontal_spacing, color='red', ax=ax)
    x1, y1 = capacitores1.draw()

    capacitores2 = CapacitoresY(m=m, n=n, d=d, horizontal_spacing=horizontal_spacing, color='green', ax=ax)
    x_offset = 3 * n * d + 2 * horizontal_spacing + 5
    x2, y2 = capacitores2.draw(x_offset)

    draw_vertical_lines_and_connector(x1, y1, x2, y2)
    save_plot(filename)

    return fig

fig = generate_and_save_capacitor_plot(m=5, n=2, d=2.5, horizontal_spacing=6, filename='capacitores.png')