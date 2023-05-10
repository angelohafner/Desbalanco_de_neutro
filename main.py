from engineering_notation import EngNumber
import streamlit as st
import numpy as np

def eng_complex_polar(c):
    magnitude = EngNumber(abs(c))
    angle = EngNumber(np.angle(c, deg=True))
    return f"{magnitude} ∠ {angle}°"
# ===================================================================
class Fonte_trifasica:
    def __init__(self, v_ab, config):
        self.v_ab = v_ab
        self.v_bc = v_ab * np.exp(-1j * 2 * np.pi / 3)
        self.v_ca = v_ab * np.exp(+1j * 2 * np.pi / 3)
        self.config = config

    def vetor_tensoes(self):
        Vabc = [[self.v_ab], [self.v_bc], [self.v_ca]]
        return np.array(Vabc)




# ===================================================================
# ===================================================================
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

# ===================================================================

def estrela_equivalente(Zabc1, Zabc2):
    Yabc1 = np.linalg.inv(Zabc1)
    Yabc2 = np.linalg.inv(Zabc2)
    Yabc = Yabc1 + Yabc2
    Zabc = np.linalg.inv(Yabc)
    return Zabc

def matriz_capacitancias_das_tres_fases(c = 2, tol = 0.01, num_paralelo=3, num_serie=2):
    aleatorios = np.random.uniform(1-tol, 1+tol, size=(3, num_paralelo, num_serie))
    matriz = valor_capacitancia * aleatorios
    paralelos = np.sum(matriz, axis=1)
    series = 1/np.sum(np.reciprocal(paralelos), axis=1)
    matriz = np.diag(series)
    return [matriz, paralelos, series]


st.title("Calculadora de Capacitância")

col1, col2, col3 = st.columns(3)
with col1:
    num_paralelo = st.slider("Número de capacitâncias em paralelo:", min_value=1, max_value=6, step=1, value=4)
    num_serie = st.slider("Número de capacitâncias em série:", min_value=1, max_value=6, step=1, value=3)

with col3:
    tol = st.slider("Tolerância valor:", min_value=0, max_value=100, step=1, value=10)
    tol = tol / 100
    valor_capacitancia = st.slider("Digite o valor da capacitância em uF:", min_value=0., max_value=1000., step=0.01, value=10.)
    valor_capacitancia = valor_capacitancia * 1e-6

matriz_1, paralelos_1, series_1 = matriz_capacitancias_das_tres_fases(c = valor_capacitancia, tol = tol, num_paralelo=num_paralelo, num_serie=num_serie)
matriz_2, paralelos_2, series_2 = matriz_capacitancias_das_tres_fases(c = valor_capacitancia, tol = tol, num_paralelo=num_paralelo, num_serie=num_serie)
C1_eqivalente = matriz_1
C2_eqivalente = matriz_2
omega_fundamental = 2*np.pi*60
Zabc1 = omega_fundamental * C1_eqivalente
Zabc2 = omega_fundamental * C2_eqivalente
Zabc = estrela_equivalente(Zabc1, Zabc2)

st.write(Zabc1*1e3)
st.write(Zabc2*1e3)
st.write(Zabc*1e3)


configuracao = "y_isolado"
matriz_impedancia = MatrizImpedancia(Zabc, configuracao)
Z_malha = matriz_impedancia.matriz()
st.write(Z_malha*1e6)


# Tensao
v_ab = 34.5e3 + 1j * 0
Vabc_fonte = Fonte_trifasica(v_ab, config='delta').vetor_tensoes()
V_malha = Vabc_fonte[0:2]
I_malha = np.linalg.solve(Z_malha, V_malha)
st.write(V_malha)
st.write(I_malha)

Iabc = [[I_malha[0, 0]],
         [I_malha[1, 0] - I_malha[0, 0]],
         [-I_malha[1, 0]]]
Iabc = np.array(Iabc)

Vabco = Zabc  @ Iabc
Iabc1 = np.linalg.inv(Zabc1) @ Vabco
Iabc2 = np.linalg.inv(Zabc2) @ Vabco

st.write(eng_complex_polar(Iabc1.sum()))
st.write(eng_complex_polar(Iabc2.sum()))










