import base64
from engineering_notation import EngNumber
import numpy as np
import pandas as pd
import streamlit as st

def eng_complex_polar(c):
    magnitude = EngNumber(abs(c))
    angle = EngNumber(np.angle(c, deg=True))
    return f"{magnitude} ∠ {angle}°"

def eng_complex(c):
    real = EngNumber(c.real)
    imag = EngNumber(abs(c.imag))
    sign = '+' if c.imag >= 0 else '-'

    if c.real == 0 and c.imag != 0:
        return f"{sign} j{imag}"
    elif c.imag == 0 or (c.real == 0 and c.imag == 0):
        return f"{real}"
    else:
        return f"{real} {sign} j{imag}"


def eng_complex_polar(c):
    magnitude = EngNumber(abs(c))
    angle = EngNumber(np.angle(c, deg=True))
    return f"{magnitude} ∠ {angle}°"
import numpy as np
import cmath

def eng_complex_polar(complex_number):
    r, theta = cmath.polar(complex_number)
    if np.round(r, 10) == 0:
        r = 0
        theta = 0
    else:
        r = EngNumber(np.round(r, 10))
        theta = int(np.round(np.degrees(theta), 0))
    return '{} ∠ {}°'.format(r, theta)

def eng_complex_matrix(matrix, format='rectangular'):
    shape = matrix.shape
    formatted_matrix = np.empty(shape, dtype=object)
    for i in range(shape[0]):
        for j in range(shape[1]):
            if format == 'rectangular':
                formatted_matrix[i, j] = eng_complex(matrix[i, j])
            elif format == 'polar':
                formatted_matrix[i, j] = eng_complex_polar(matrix[i, j])
            else:
                raise ValueError("Invalid format. Choose 'rectangular' or 'polar'.")

    return formatted_matrix



def matriz_capacitancias_das_tres_fases(valor_capacitancia = 2, tol = 0.01, num_paralelo=3, num_serie=2):
    aleatorios = np.random.uniform(1-tol, 1+tol, size=(3, num_serie, num_paralelo))
    matriz_original = valor_capacitancia * aleatorios
    paralelos = np.sum(matriz_original, axis=1)
    series = 1/np.sum(np.reciprocal(paralelos), axis=1)
    matriz = np.diag(series)
    return [matriz_original, matriz, paralelos, series]


def converter_matriz_em_data_frame(matriz):
    df = pd.DataFrame(matriz)
    st.write(df.to_html(index=False, header=False), unsafe_allow_html=True)


def transformada_Fortescue(Iabc):
    a = np.exp(1j*2*np.pi/3)
    F = 1/3 * np.array([[1, 1, 1], [1, a, a**2], [1, a**2, a]])
    I012 = F @ Iabc
    return I012


import base64
import pandas as pd
import streamlit as st

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index = False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Download csv file</a>' # decode b'abc' => abc

def preenche_tab(indice, matriz, key, n, m):
    cols = st.columns(m)
    for ii in range(n):
        for jj in range(m):
            with cols[jj]:
                matriz[indice, ii, jj] = st.number_input(label='C', min_value=0.01, max_value=1000., step=0.01, value=matriz[indice, ii, jj], key=str(key)+str(indice) + str(ii) + str(jj), label_visibility="collapsed")

    return matriz

def preenche_tabs(ramo, matriz_original, key, n, m):
    st.markdown(f"### Ramo {ramo}")
    tab1, tab2, tab3 = st.tabs(["Fase A", "Fase B", "Fase C"])
    with tab1:
        preenche_tab(0, matriz_original, key, n, m)
    with tab2:
        preenche_tab(1, matriz_original, key, n, m)
    with tab3:
        preenche_tab(2, matriz_original, key, n, m)