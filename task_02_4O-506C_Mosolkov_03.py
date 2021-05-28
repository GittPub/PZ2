import requests
import math
import scipy.special
import numpy as np
from scipy.special import spherical_jn, spherical_yn
import matplotlib.pyplot as plt
import requests as rqst
import xml.etree.ElementTree as ET

# Рассчитать ЭПР
# Построить график
# Сохранить результаты в файл

# Radar cross section
def RCS(lam, r):
    summ = 0
    kr = 2 * math.pi * r / lam
    # Задаем значения функций Бесселя для n = 0 для первой итерации
    J_prev = spherical_jn (0, kr)
    Y_prev = spherical_yn (0, kr)
    H_prev = J_prev + 1j * Y_prev
    for n in range(1, 50):
        # Вычисляем значения функций Бесселя для текущей n
        J_now = spherical_jn (n, kr)
        #J_prev = spherical_jn (n - 1, kr)
        Y_now = spherical_yn (n, kr)
        #Y_prev = spherical_yn (n - 1, kr)
        H_now = J_now + 1j * Y_now
        #H_prev = J_prev + 1j * Y_prev
        # Считаем коэффициенты a и b
        a = J_now / H_now
        b = (kr * J_prev - n * J_now) / (kr * H_prev - n * H_now)
        summ += ((-1) ** n) * (n + 0.5) * (b - a)
        # Переносим значения функций Бесселя на следующий шаг
        J_prev = J_now
        Y_prev = Y_now
        H_prev = H_now
    return lam * lam * np.abs(summ) * np.abs(summ) / math.pi

def graf(lam, p):
  plt.plot(lam, p)
  plt.ylabel('RCS')
  plt.xlabel('lambda')
  plt.grid()
  plt.show()

def graf_freq(f, p):
  plt.plot(f, p)
  plt.ylabel('RCS, [м2]')
  plt.xlabel('f, [Гц]')
  plt.grid()
  plt.show()

# Скачать файл с вариантом задания 

def download(url):
  r=rqst.get(url)
  return r.text

# Разобрать прочитанные данные и найти нужные данные

# Возврат данных по номеру варианта
def var(text,nomervar):
  t=text.splitlines()
  return t[nomervar]

# Проверка возможности преобразования строки в число
def is_digit(string):
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False

# Запись в xml-файл
def xml(ls, lam, s):
    # Формирование файловой структуры
    data = ET.Element('data')
    frequencydata = ET.SubElement(data, 'frequencydata')
    for i in ls:
        frequency1 = ET.SubElement(frequencydata, 'f')
        frequency1.text = str(i)
    lambdadata = ET.SubElement(data, 'lambdadata')
    for i in lam:
        lambda1 = ET.SubElement(lambdadata, 'lambda')
        lambda1.text = str(i)
    rcsdata = ET.SubElement(data, 'rcsdata')
    for i in s:
        rcs1 = ET.SubElement(rcsdata, 'rcs')
        rcs1.text = str(i)
    # Формирование файла XML с результатами 
    with open('task_02_40-506C_Mosolkov_03.xml', 'w') as myfile:
        myfile.write(ET.tostring(data, method='xml').decode(encoding='utf-8'))

  
if __name__ == '__main__':
    txt = download('https://jenyay.net/uploads/Student/Modelling/task_02.xml')
    variant = 3
    line=var(txt, variant + 1)
    print(line)
    L = [float(i) for i in line.split('"') if is_digit(i)]
    D, fmin, fmax = L[1], L[2], L[3]
    s = []
    ls = np.linspace(fmin,fmax,500)
    lam = 3e8 / ls
    for f in ls:
        p = RCS(3e8 / f, D/2)
        s.append(p)
    
    graf_freq(ls,s)
    xml(ls, lam, s)
