#!/usr/bin/env python3
'''
Procura ocorrências de uma imagem dentro de outra imagem
'''
import cv2 as cv
import numpy as np
import sys
import math

if len(sys.argv) != 3:
    print("""
-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
Use: {} <imagem-pai> <imagem-a-encontrar>

Exemplo:
    {} paisagem.png pessoa.png
-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
""".format(sys.argv[0], sys.argv[0]))
    sys.exit()

IMAGEM_PAI = sys.argv[1]
IMAGEM_FIL = sys.argv[2]

img_rgb = cv.imread(IMAGEM_FIL)
template = cv.imread(IMAGEM_PAI)
w, h = template.shape[:-1]

res = cv.matchTemplate(img_rgb, template, cv.TM_CCOEFF_NORMED)
#  threshold = .8
threshold = .7
loc = np.where(res >= threshold)

print(math.floor(len(loc[0]) / 2))
