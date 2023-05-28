
from engineering_notation import EngNumber
import numpy as np
import base64
import pandas as pd
import streamlit as st
import funcoes_auxiliares as fa
from impedancia import MatrizImpedancia
from fonte import Fonte_trifasica
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.pyplot as mpl




def matriz_impedancia_da_malha(matriz_original_1, matriz_original_2):
    matriz_original_1, matriz_1, paralelos_1, series_1 = fa.matriz_capacitancias_das_tres_fases(matriz_original_1)
    matriz_original_2, matriz_2, paralelos_2, series_2 = fa.matriz_capacitancias_das_tres_fases(matriz_original_2)
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
    return [Z_malha, Yabc1, Yabc2, Yabc, Zabc1, Zabc2, Zabc, C1_eqivalente, C2_eqivalente, C_equivalente, matriz_1, matriz_2]



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






def avoid_tiny_numbers(arr):
    arr[np.abs(arr < 1e-15)] = 0
    return arr

def display_data(col, branch, C_eqivalente, I012, Iabc, V012o, Vabco):
    with col:
        st.markdown(f'### Ramo {branch}', unsafe_allow_html=True)
        st.markdown('<u>Capacitâncias</u>', unsafe_allow_html=True)
        st.write(f'$\; \; \; C_{{a}} = $ {EngNumber(C_eqivalente[0, 0])}F')
        st.write(f'$\; \; \; C_{{b}} = $ {EngNumber(C_eqivalente[1, 1])}F')
        st.write(f'$\; \; \; C_{{c}} = $ {EngNumber(C_eqivalente[2, 2])}F')

        st.markdown('<u>Correntes de Sequência</u>', unsafe_allow_html=True)
        # I012 = avoid_tiny_numbers(I012)
        st.write(f'$\; \; \; I_{{0}} = $ {fa.eng_complex_polar(I012[0, 0])}A')
        st.write(f'$\; \; \; I_{{1}} = $ {fa.eng_complex_polar(I012[1, 0])}A')
        st.write(f'$\; \; \; I_{{2}} = $ {fa.eng_complex_polar(I012[2, 0])}A')

        st.markdown('<u>Correntes de fase</u>', unsafe_allow_html=True)
        # Iabc = avoid_tiny_numbers(Iabc)
        st.write(f'$\; \; \; I_{{a}} = $ {fa.eng_complex_polar(Iabc[0, 0])}A')
        st.write(f'$\; \; \; I_{{b}} = $ {fa.eng_complex_polar(Iabc[1, 0])}A')
        st.write(f'$\; \; \; I_{{c}} = $ {fa.eng_complex_polar(Iabc[2, 0])}A')

        st.markdown('<u>Tensões de Sequência</u>', unsafe_allow_html=True)
        # V012o = avoid_tiny_numbers(V012o)
        st.write(f'$\; \; \; V_{{0}} = $ {fa.eng_complex_polar(V012o[0, 0])}V')
        st.write(f'$\; \; \; V_{{1}} = $ {fa.eng_complex_polar(V012o[1, 0])}V')
        st.write(f'$\; \; \; V_{{2}} = $ {fa.eng_complex_polar(V012o[2, 0])}V')

        st.markdown('<u>Tensões de fase</u>', unsafe_allow_html=True)
        st.write(f'$\; \; \; V_{{ao}} = $ {fa.eng_complex_polar(Vabco[0, 0])}V')
        st.write(f'$\; \; \; V_{{bo}} = $ {fa.eng_complex_polar(Vabco[1, 0])}V')
        st.write(f'$\; \; \; V_{{co}} = $ {fa.eng_complex_polar(Vabco[2, 0])}V')


# ===================================================================
def plot_diagrama_fasorial(Vabco, v_ab):
    mpl.rcParams['font.size'] = 8
    # limite de escala do gráfico
    lim = np.abs(v_ab/np.sqrt(3))

    Vao = Vabco[0]
    Vbo = Vabco[1]
    Vco = Vabco[2]

    a = np.exp(-2j*np.pi/3)
    v_bc = v_ab * a
    v_ca = v_ab * a**2

    b = np.exp(-1j*np.pi/6)
    Van = v_ab * b / np.sqrt(3)
    Vbn = Van * a
    Vcn = Van * a **2

    # Vabco = np.array([[Vao], [Vbo], [Vco]])
    Vabcn = np.array([[Van], [Vbn], [Vcn]])
    Von = Vabcn - Vabco
    Vonx, Vony = np.real(Von[0]), np.imag(Von[0])

    Vanx, Vany = np.real(Van), np.imag(Van)
    Vbnx, Vbny = np.real(Vbn), np.imag(Vbn)
    Vcnx, Vcny = np.real(Vcn), np.imag(Vcn)


    Vabx, Vaby = np.real(v_ab), np.imag(v_ab)
    Vbcx, Vbcy = np.real(v_bc), np.imag(v_bc)
    Vcax, Vcay = np.real(v_ca), np.imag(v_ca)

    Vaox, Vaoy = np.real(Vao), np.imag(Vao)
    Vbox, Vboy = np.real(Vbo), np.imag(Vbo)
    Vcox, Vcoy = np.real(Vco), np.imag(Vco)

    fasorial, ax = plt.subplots()
    x0 = -Vanx
    y0 = -Vany
    ww = 0.002
    ax.quiver(x0, y0, Vaox, Vaoy, color='r', angles='xy', scale_units='xy', scale=1,  width=2*ww, label="$V_{ao}=$"+str(fa.eng_complex_polar(Vao)))
    ax.plot([x0, x0 + Vanx], [y0, y0 + Vany], color='r',  ls='--', alpha=0.5)
    ax.quiver(x0, y0, Vabx, Vaby, color='r', angles='xy', scale_units='xy', scale=1,  width=2*ww, label="$V_{ab}=$"+str(fa.eng_complex_polar(v_ab)))
    x0 = -Vbnx
    y0 = -Vbny
    ax.quiver(x0, y0, Vbox, Vboy, color='g', angles='xy', scale_units='xy', scale=1,  width=2*ww, label="$V_{bo}=$"+str(fa.eng_complex_polar(Vbo)))
    ax.plot([x0, x0 + Vbnx], [y0, y0 + Vbny], color='g',  ls='--', alpha=0.5)
    ax.quiver(x0, y0, Vbcx, Vbcy, color='g', angles='xy', scale_units='xy', scale=1, width=2*ww, label="$V_{bc}=$"+str(fa.eng_complex_polar(v_bc)))
    x0 = -Vcnx
    y0 = -Vcny
    ax.quiver(x0, y0, Vcox, Vcoy, color='b', angles='xy', scale_units='xy', scale=1,  width=2*ww, label="$V_{co}=$"+str(fa.eng_complex_polar(Vco)))
    ax.plot([x0, x0 + Vcnx], [y0, y0 + Vcny], color='b',  ls='--', alpha=0.5)
    ax.quiver(x0, y0, Vcax, Vcay, color='g', angles='xy', scale_units='xy', scale=1, width=2*ww, label="$V_{ca}=$"+str(fa.eng_complex_polar(v_ca)))
    x0 = -Vonx
    y0 = -Vony
    ax.quiver(x0, y0, Vonx, Vony, color='k', angles='xy', scale_units='xy', scale=1, width=2*ww)

    rho = np.linspace(0, 1.2*lim, 100)
    phi = np.linspace(0, 2*np.pi, 100)
    RHO, PHI = np.meshgrid(rho, phi)
    XXX = RHO * np.cos(PHI)
    YYY = RHO * np.sin(PHI)
    ZZZ = RHO
    CS = ax.contour(XXX, YYY, ZZZ, colors='gray', linewidths=0.5, linestyles='dotted', alpha=0.5)
    ax.clabel(CS, inline=1, fontsize=6)

    plt.legend(loc='best')
    formatter_y = ticker.EngFormatter(unit='V')
    ax.yaxis.set_major_formatter(formatter_y)

    formatter_x = ticker.EngFormatter(unit='V')
    ax.xaxis.set_major_formatter(formatter_x)
    ax.set_aspect('equal')
    ax.set_xlabel('Real')
    ax.set_ylabel('Imaginário')
    ax.grid(ls= ":")
    ax.set_title('Diagrama Fasorial das Tensões de Fase')

    return [fasorial, Von]

# ===================================================================
def plot_diagrama_fasorial_correntes(Iabc, lim, ramo):
    ww = 0.002
    ramo = ramo
    mpl.rcParams['font.size'] = 6
    ia = Iabc[0]
    ib = Iabc[1]
    ic = Iabc[2]
    io = ia + ib + ic

    Iaox, Iaoy = np.real(ia), np.imag(ia)
    Ibox, Iboy = np.real(ib), np.imag(ib)
    Icox, Icoy = np.real(ic), np.imag(ic)
    Ionx, Iony = np.real(io), np.imag(io)

    fig, ax = plt.subplots()

    x0 = 0
    y0 = 0
    ax.quiver(x0, y0, Iaox, Iaoy, color='r', angles='xy', scale_units='xy', scale=1, linewidths=0.5, label="${I_a}=$"+str(fa.eng_complex_polar(ia)), width=2*ww)
    ax.quiver(x0, y0, Ibox, Iboy, color='g', angles='xy', scale_units='xy', scale=1, linewidths=0.5, label="${I_b}=$"+str(fa.eng_complex_polar(ib)), width=2*ww)
    ax.quiver(x0, y0, Icox, Icoy, color='b', angles='xy', scale_units='xy', scale=1, linewidths=0.5, label="${I_c}=$"+str(fa.eng_complex_polar(ic)), width=2*ww)
    if abs(io) < 1e-6:
        io = 0.

    ax.quiver(x0, y0, Ionx, Iony, color='k', angles='xy', scale_units='xy', scale=1, linewidths=0.5, label="${I_n}=$"+str(fa.eng_complex_polar(io)), width=1*ww)

    rho = np.linspace(0, 1.2*lim, 100)
    phi = np.linspace(0, 2*np.pi, 100)
    RHO, PHI = np.meshgrid(rho, phi)
    XXX = RHO * np.cos(PHI)
    YYY = RHO * np.sin(PHI)
    ZZZ = RHO
    CS = ax.contour(XXX, YYY, ZZZ, colors='gray', linewidths=0.5, linestyles='dotted', alpha=0.5)
    ax.clabel(CS, inline=1, fontsize=6)



    plt.legend(loc='best')

    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect('equal')
    formatter_y = ticker.EngFormatter(unit='A')
    ax.yaxis.set_major_formatter(formatter_y)

    formatter_x = ticker.EngFormatter(unit='A')
    ax.xaxis.set_major_formatter(formatter_x)
    ax.set_xlabel('Real')
    ax.set_ylabel('Imaginário')

    # ax.grid(ls= ":")
    ax.set_title(f'Diagrama Fasorial das Correntes de Fase Ramo {ramo}')

    return [fig, ax, io]


