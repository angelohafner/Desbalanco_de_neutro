import numpy as np
import funcoes_auxiliares as fa
import streamlit as st
class Fonte_trifasica:
    def __init__(self, v_ab, config):
        self.v_ab = a = v_ab
        self.config = config

    def vetor_tensoes(self):
        a = np.exp(1j * 2 * np.pi / 3)
        if self.config=='delta':
            Vabc = np.array([[self.v_ab], [self.v_ab * a ** 2], [self.v_ab * a]])
            return Vabc
        else:
            Vabc = np.array([[self.v_ab], [self.v_ab * a ** 2], [self.v_ab * a]])
            return Vabc*0
