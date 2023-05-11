
from engineering_notation import EngNumber
import numpy as np
import base64
import pandas as pd
import streamlit as st
import funcoes_auxiliares as fa
from impedancia import MatrizImpedancia
from fonte import Fonte_trifasica



def matriz_impedancia_da_malha(num_paralelo, num_serie, tol, valor_capacitancia):
    matriz_original_1, matriz_1, paralelos_1, series_1 = fa.matriz_capacitancias_das_tres_fases(valor_capacitancia = valor_capacitancia, tol = tol, num_paralelo=num_paralelo, num_serie=num_serie)
    matriz_original_2, matriz_2, paralelos_2, series_2 = fa.matriz_capacitancias_das_tres_fases(valor_capacitancia = valor_capacitancia, tol = tol, num_paralelo=num_paralelo, num_serie=num_serie)
    C1_eqivalente = matriz_1
    C2_eqivalente = matriz_2
    C_equivalente = C1_eqivalente + C1_eqivalente

    omega_fundamental = 2*np.pi*60
    Yabc1 = 1j * omega_fundamental * C1_eqivalente
    Yabc2 = 1j * omega_fundamental * C2_eqivalente
    Yabc = Yabc1 + Yabc2

    Zabc1 = np.linalg.inv(Yabc1)
    Zabc2 = np.linalg.inv(Yabc2)
    Zabc = np.linalg.inv(Yabc)

    configuracao = "y_isolado"
    matriz_impedancia = MatrizImpedancia(Zabc, configuracao)
    Z_malha = matriz_impedancia.matriz()
    return [Z_malha, Yabc1, Yabc2, Yabc, Zabc1, Zabc2, Zabc, C1_eqivalente, C2_eqivalente, C_equivalente, matriz_1, matriz_2, matriz_original_1, matriz_original_2]



def correntes(Zabc, Z_malha, Yabc1, Yabc2, Vabc_fonte):
    V_malha = Vabc_fonte[0:2]
    I_malha = np.linalg.inv(Z_malha) @ V_malha

    Iabc = [[I_malha[0, 0]],
             [I_malha[1, 0] - I_malha[0, 0]],
             [-I_malha[1, 0]]]
    Iabc = np.array(Iabc)

    Vabco = Zabc  @ Iabc
    Iabc1 = Yabc1 @ Vabco
    Iabc2 = Yabc2 @ Vabco

    return [I_malha, Iabc1, Iabc2, Iabc, Vabco]



def componentes_simetricas(Iabc1, Iabc2, Iabc, Vabco, Vabc_fonte):
    I012_1 = fa.transformada_Fortescue(Iabc1)
    I012_2 = fa.transformada_Fortescue(Iabc2)
    I012 = fa.transformada_Fortescue(Iabc)
    V012o = fa.transformada_Fortescue(Vabco)
    V012_fonte = fa.transformada_Fortescue(Vabc_fonte)
    return [I012_1, I012_2, I012, V012o, V012_fonte]
