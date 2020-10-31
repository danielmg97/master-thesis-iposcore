# -*- coding: utf-8 -*-

import math
import numpy as np
import pandas as pd
import global_variables
import data_processing

from sklearn.feature_selection import chi2, f_classif, mutual_info_regression, f_regression

def f_select_numeric(output, p_value=0.05, k=None):
    dataset,X,y = data_processing.load_data(output, global_variables.numericas)
    if(output=="dias na UCI"):
        lista_index_remover = []
        for col in range(0,len(X[0])):
            if(np.var(list(X[:,col]))==0):
                lista_index_remover.append(col)
        X = np.delete(X, lista_index_remover, 1)
        dataset.drop(dataset.columns[lista_index_remover], axis=1, inplace=True)
        rank = f_regression(X, y)
    else:
        rank = f_classif(X, y)
    lista = [(dataset.columns[i],rank[0][i],rank[1][i]) for i in range(0,len(X[0]))]
    lista = sorted(lista, key=lambda par: par[1])
    lista.reverse()
    lista = list(filter(lambda x: x[2] <= p_value, lista))
    if(k==None):
        k=len(lista)
    result = []
    for i in range(0,k):
        result.append((lista[i][0],lista[i][1]))
    return result

def f_select_categoric(output, p_value=0.05, k=None):
    dataset,X,y = data_processing.load_data(output, global_variables.categoricas)
    if(output=="dias na UCI"):
        lista_index_remover = []
        for col in range(0,len(X[0])):
            if(np.var(list(X[:,col]))==0):
                lista_index_remover.append(col)
        X = np.delete(X, lista_index_remover, 1)
        dataset.drop(dataset.columns[lista_index_remover], axis=1, inplace=True)
        rank = f_regression(X, y)
    else:
        rank = chi2(X, y)
    lista = [(dataset.columns[i],rank[0][i],rank[1][i]) for i in range(0,len(X[0]))]
    lista = sorted(lista, key=lambda par: par[1])
    lista.reverse()
    lista = list(filter(lambda x: x[2] <= p_value, lista))
    if(k==None):
        k=len(lista)
    result = []
    for i in range(0,k):
        result.append((lista[i][0],lista[i][1]))
    return result

def f_select_binary(output, p_value=0.05, k=None):
    dataset,X,y = data_processing.load_data(output, global_variables.binarias)
    if(output=="dias na UCI"):
        lista_index_remover = []
        for col in range(0,len(X[0])):
            if(np.var(list(X[:,col]))==0):
                lista_index_remover.append(col)
        X = np.delete(X, lista_index_remover, 1)
        dataset.drop(dataset.columns[lista_index_remover], axis=1, inplace=True)
        rank = f_regression(X, y)
    else:
        rank = chi2(X, y)
    lista = [(dataset.columns[i],rank[0][i],rank[1][i]) for i in range(0,len(X[0]))]
    lista = sorted(lista, key=lambda par: par[1])
    lista.reverse()
    lista = list(filter(lambda x: x[2] <= p_value, lista))
    if(k==None):
        k=len(lista)
    result = []
    for i in range(0,k):
        result.append((lista[i][0],lista[i][1]))
    return result

def f_select_codigo(output, p_value=0.05, k=None):
    dataset,X,y = data_processing.load_data(output, global_variables.codigos)
    if(output=="dias na UCI"):
        lista_index_remover = []
        for col in range(0,len(X[0])):
            if(np.var(list(X[:,col]))==0):
                lista_index_remover.append(col)
        X = np.delete(X, lista_index_remover, 1)
        dataset.drop(dataset.columns[lista_index_remover], axis=1, inplace=True)
        rank = f_regression(X, y)
    else:
        rank = chi2(X, y)
    lista = [(dataset.columns[i],rank[0][i],rank[1][i]) for i in range(0,len(X[0]))]
    lista = sorted(lista, key=lambda par: par[1])
    lista.reverse()
    lista = list(filter(lambda x: x[2] <= p_value, lista))
    if(k==None):
        k=len(lista)
    result = []
    for i in range(0,k):
        result.append((lista[i][0],lista[i][1]))
    return result

for output in global_variables.outputs:
    print("ALL:",len(global_variables.numericas+global_variables.binarias+global_variables.categoricas))
    print("#### Feature ranking for the output: ####", output)
    selected_features = []
    p=0.0001
    selected_features+=f_select_numeric(output,p_value=p)
    selected_features+=f_select_categoric(output,p_value=p)
    selected_features+=f_select_binary(output,p_value=p)

    selected_features = sorted(selected_features, key=lambda par: par[1])
    selected_features.reverse()
    print([x[0] for x in selected_features])
    print("\n")