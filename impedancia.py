import numpy as np
class MatrizImpedancia:
    def __init__(self, Zabc, configuracao):
        self.configuracao = configuracao
        zaa = Zabc[0, 0]
        zbb = Zabc[1, 1]
        zcc = Zabc[2, 2]
        zab = Zabc[0, 1]
        zac = Zabc[0, 2]
        zbc = Zabc[1, 2]
        if configuracao == 'y_aterrado':
            self.imp_matrix = Zabc
        if configuracao == 'y_isolado':
            self.imp_matrix = np.array(
                [[zaa + zbb, -zbb],
                 [-zbb, zbb + zcc]])

    def matriz(self):
        return self.imp_matrix