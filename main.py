import matplotlib.patches as patches
import numpy as np
import matplotlib.pyplot as plt

from engineerign_notation_modificada import EngNumber
import base64
import streamlit as st
import openpyxl
import numpy as np
import pandas as pd
from fonte import Fonte_trifasica
from impedancia import MatrizImpedancia
import funcoes_auxiliares as fa
import funcoes_pricipais as fp
from desenho_dos_capacitores_v2 import CapacitoresY





st.set_page_config(page_title='Meu Super App')


st.title("Calculadora de Capacitância")

col1, col2, col3 = st.columns(3)
with col1:
    num_paralelo = st.slider("Número de capacitâncias em paralelo:", min_value=1, max_value=6, step=1, value=4)
    num_serie = st.slider("Número de capacitâncias em série:", min_value=1, max_value=6, step=1, value=4)

with col3:
    tol = st.slider("Tolerância valor:", min_value=0, max_value=20, step=1, value=0)
    tol = tol / 100
    valor_capacitancia = st.slider("Digite o valor da capacitância em uF:", min_value=0.01, max_value=1000., step=0.01, value=10.)

if 'matriz_original_uF1' not in globals():
    np.random.seed(42)
    matriz_original_uF1 = valor_capacitancia * np.random.uniform(1 - tol, 1 + tol, size=(3, num_serie, num_paralelo))
    matriz_original_uF2 = valor_capacitancia * np.random.uniform(1 - tol, 1 + tol, size=(3, num_serie, num_paralelo))

matriz_original_uF1 = fa.preenche_tabs(ramo=1, matriz_original_uF=matriz_original_uF1)
matriz_original_uF2 = fa.preenche_tabs(ramo=2, matriz_original_uF=matriz_original_uF2)

st.write(matriz_original_uF1.shape)

Z_malha, Yabc1, Yabc2, Yabc, Zabc1, Zabc2, Zabc, C1_eqivalente, C2_eqivalente, C_equivalente, matriz_1, matriz_2 = fp.matriz_impedancia_da_malha(1e-6*matriz_original_uF1, 1e-6*matriz_original_uF2)

nr_fases, n, m = matriz_original_uF1.shape


fig = CapacitoresY.generate_and_save_capacitor_plot(m=num_serie, n=num_paralelo, d=2.5, horizontal_spacing=6, filename='capacitores.png')
st.pyplot(fig)


v_ab = 34.5e3 + 1j * 0
config='delta'
Vabc_fonte = Fonte_trifasica(v_ab, config).vetor_tensoes()
I_malha, Iabc1, Iabc2, Iabc, Vabco = fp.correntes(Zabc, Z_malha, Yabc1, Yabc2, Vabc_fonte = Vabc_fonte)

I012_1, I012_2, I012, V012o, V012_fonte = fp.componentes_simetricas(Iabc1, Iabc2, Iabc, Vabco, Vabc_fonte)



cols = st.columns(3)

fp.display_data(cols[0], '1', C1_eqivalente, I012_1, Iabc1, V012o, Vabco)
fp.display_data(cols[1], '2', C2_eqivalente, I012_2, Iabc2, V012o, Vabco)
fp.display_data(cols[2], 'Equivalente', C_equivalente, I012, Iabc, V012o, Vabco)


fasorial, Von = fp.plot_diagrama_fasorial(Vabco, v_ab)

lim = 1.1 * np.max(np.abs(Iabc))
fig_Iabc1, ax, io = fp.plot_diagrama_fasorial_correntes(Iabc1, lim, '1')
fig_Iabc2, ax, io = fp.plot_diagrama_fasorial_correntes(Iabc2, lim, '2')
fig_Iabc, ax, io = fp.plot_diagrama_fasorial_correntes(Iabc, lim, 'Equivalente')


st.pyplot(fig=fasorial)
st.pyplot(fig=fig_Iabc1)
st.pyplot(fig=fig_Iabc2)
st.pyplot(fig=fig_Iabc)



















