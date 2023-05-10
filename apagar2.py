import matplotlib.pyplot as plt
import matplotlib.patches as patches

class DesenharCapacitoresParalelos:
    def __init__(self):
        self.fig, self.ax = plt.subplots()

    def draw_capacitor(self, x, y):
        ax = self.ax

        plate_width = 1.0
        plate_height = 0.15
        spacing = 0.2

        top_plate = patches.Rectangle((x - plate_width/2, y + spacing/2), plate_width, plate_height, edgecolor='black', facecolor='none')
        bottom_plate = patches.Rectangle((x - plate_width/2, y - plate_height - spacing/2), plate_width, plate_height, edgecolor='black', facecolor='none')

        ax.add_patch(top_plate)
        ax.add_patch(bottom_plate)

        plt.plot([x, x], [y - plate_height - spacing/2, y - plate_height - spacing/2 - 0.5], color='black', linewidth=1)
        plt.plot([x, x], [y + plate_height + spacing/2, y + plate_height + spacing/2 + 0.5], color='black', linewidth=1)

    def draw_parallel_capacitors(self, x, y, n, d):
        for i in range(n):
            self.draw_capacitor(x + i * d, y)

        # Conectar os pontos superiores
        plt.plot([x, x + (n - 1) * d], [y + 0.75, y + 0.75], color='black', linewidth=1)

        # Conectar os pontos inferiores
        plt.plot([x, x + (n - 1) * d], [y - 0.75, y - 0.75], color='black', linewidth=1)

    def draw_multiple_parallel_capacitors(self, x, y, n, d, m, vertical_spacing):
        for i in range(m):
            self.draw_parallel_capacitors(x, y + i * vertical_spacing, n, d)
            if i > 0:
                # Conectar os conjuntos de capacitores com uma linha vertical
                plt.plot([x + (n - 1) * d / 2, x + (n - 1) * d / 2], [y + (i - 1) * vertical_spacing + 0.75, y + i * vertical_spacing - 0.75], color='black', linewidth=1)

    def draw_multiple_sets(self, x, y, n, d, m, vertical_spacing, num_sets, horizontal_spacing):
        for i in range(num_sets):
            self.draw_multiple_parallel_capacitors(x + i * (n * d + horizontal_spacing), y, n, d, m, vertical_spacing)

    def show(self, xlim=None, ylim=None):
        if xlim is not None:
            plt.xlim(xlim)
        if ylim is not None:
            plt.ylim(ylim)
        self.ax.set_aspect('equal', adjustable='box')
        plt.show()

# Exemplo de uso:
desenho = DesenharCapacitoresParalelos()
m = 4
n = 5
desenho.draw_multiple_parallel_capacitors(0, 0, n, 2.5, m, 4) # 2 conjuntos de capacitores paralelos com um espaçamento vertical de 4
desenho.draw_multiple_sets(0, 0, 3, 2.5, 2, 4, 2, 6)
desenho.show()
