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

    def show(self, xlim=None, ylim=None):
        if xlim is not None:
            plt.xlim(xlim)
        if ylim is not None:
            plt.ylim(ylim)
        self.ax.set_aspect('equal', adjustable='box')
        plt.axis('off')
        plt.show()


    def draw_bottom_connections(self, x1, x2, y, length):
        y_bottom = y - 0.75 - length
        plt.plot([x1, x1], [y - 0.75, y_bottom], color='red', linewidth=1)
        plt.plot([x2, x2], [y - 0.75, y_bottom], color='red', linewidth=1)
        plt.plot([x1, x2], [y_bottom, y_bottom], color='red', linewidth=1)

    def draw_current_transformer(self, x, y, radius=0.5):
        circle = plt.Circle((x, y), radius, edgecolor='black', facecolor='none', linewidth=1)
        self.ax.add_artist(circle)

    def draw_top_connections(self, x, y, length):
        y_top = y + 0.75 + length
        plt.plot([x, x], [y + 0.75, y_top], color='black', linewidth=1)

# Exemplo de uso:
desenho = DesenharCapacitoresParalelos()
m = 4
n = 5
d = 2.5
horizontal_spacing = 6

desenho.draw_multiple_parallel_capacitors(0, 0, n, d, m, 4)
desenho.draw_multiple_parallel_capacitors(n * d + horizontal_spacing, 0, n, d, m, 4)

# Adicionar as conexões na parte inferior dos desenhos
x1 = (n - 1) * d / 2
x2 = n * d + horizontal_spacing + (n - 1) * d / 2
desenho.draw_bottom_connections(x1, x2, 0, 2)


# Desenhar o símbolo do transformador de corrente no centro da linha vermelha
transformer_x = (x1 + x2) / 2
transformer_y = -2.75
desenho.draw_current_transformer(transformer_x, transformer_y)

# Adicionar as conexões no topo dos desenhos
y_top = (m - 1) * 4
desenho.draw_top_connections(x1, y_top, 2)
desenho.draw_top_connections(x2, y_top, 2)

desenho.show(xlim=(-2, 2 * n * d + horizontal_spacing + 2), ylim=(-4, m * 4 + 4))
