import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class CapacitorConfiguration:
    def __init__(self, m, n, d, horizontal_spacing, color):
        self.m = m
        self.n = n
        self.d = d
        self.horizontal_spacing = horizontal_spacing
        self.color = color

class CapacitoresY:
    def __init__(self, config, ax=None):
        self.config = config
        if ax is None:
            self.fig, self.ax = plt.subplots()
        else:
            self.ax = ax
            self.fig = ax.figure

    def draw_capacitor(self, x, y, color=None):
        color = color or self.config.color
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

    def draw_parallel_capacitors(self, x, y, n, d, color=None):
        color = color or self.config.color
        for i in range(n):
            self.draw_capacitor(x + i * d, y, color)

        # Conectar os pontos superiores
        plt.plot([x, x + (n - 1) * d], [y + 0.75, y + 0.75], color=color, linewidth=1)

        # Conectar os pontos inferiores
        plt.plot([x, x + (n - 1) * d], [y - 0.75, y - 0.75], color=color, linewidth=1)

    def draw_multiple_parallel_capacitors(self, x, y, n, d, m, vertical_spacing, color=None):
        color = color or self.config.color
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
        plt.plot([x1, x1], [y - 0.75, y_bottom], color=self.config.color, linewidth=1)
        plt.plot([x2, x2], [y - 0.75, y_bottom], self.config.color, linewidth=1)
        plt.plot([x1, x2], [y_bottom, y_bottom], self.config.color, linewidth=1)
        self.xmed = x1
        self.ymed = y_bottom

    def draw_top_connections(self, x, y, length, x_offset=0):
        x += x_offset
        y_top = y + 0.75 + length
        plt.plot([x, x], [y + 0.75, y_top], color=self.config.color, linewidth=1)

    def draw(self, x_offset=0):
        m = self.config.m
        n = self.config.n
        d = self.config.d
        horizontal_spacing = self.config.horizontal_spacing
        color = self.config.color

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

        print(f'xmed: {self.xmed}, ymed: {self.ymed}')  # Imprima os valores antes de retornar
        return self.xmed, self.ymed

    @staticmethod
    def draw_current_transformer(x, y, radius=0.5, color='black'):
        circle = plt.Circle((x, y), radius, edgecolor=color, facecolor='none', linewidth=1)
        plt.gca().add_artist(circle)

        angle = np.linspace(0, 2 * np.pi, 100)
        spiral_x = radius * (1 + 0.1 * angle) * np.cos(angle)
        spiral_y = radius * (1 + 0.1 * angle) * np.sin(angle)
        plt.plot(x + spiral_x, y + spiral_y, color=color, linewidth=1)
        plt.plot(x - spiral_x, y - spiral_y, color=color, linewidth=1)

    @staticmethod
    def draw_vertical_lines_and_connector(x1, y1, x2, y2, color='black'):
        plt.plot([x1, x1], [y1, y1 - 2], color=color, linewidth=1)
        plt.plot([x2, x2], [y2, y2 - 2], color=color, linewidth=1)
        plt.plot([x1, x2], [y1 - 2, y2 - 2], color=color, linewidth=1)

        x_center = (x1 + x2) / 2
        y_center = y1 - 2 - 0.5
        draw_current_transformer(x_center, y_center)

    def save_plot(self, filename):
        plt.axis('off')
        plt.savefig(filename, dpi=600, bbox_inches='tight')


    def generate_and_save_capacitor_plot(self, x_offset, filename='capacitores.png'):
        x, y = self.draw(x_offset)
        return [x, y]

    @staticmethod
    def interconnect_capacitors(cap1, cap2, filename='capacitores.png'):
        x1, y1 = cap1.generate_and_save_capacitor_plot(x_offset=0)
        x2, y2 = cap2.generate_and_save_capacitor_plot(x_offset=3 * cap1.config.n * cap1.config.d + 2 * cap1.config.horizontal_spacing + 5)
        CapacitoresY.draw_vertical_lines_and_connector(x1, y1, x2, y2)
        CapacitoresY.save_plot(filename)


# Exemplo de uso da classe
config1 = CapacitorConfiguration(m=5, n=2, d=2.5, horizontal_spacing=6, color='red')
config2 = CapacitorConfiguration(m=5, n=2, d=2.5, horizontal_spacing=6, color='green')
capacitores1 = CapacitoresY(config1)
capacitores2 = CapacitoresY(config2)

CapacitoresY.interconnect_capacitors(capacitores1, capacitores2, filename='capacitores.png')

