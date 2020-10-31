# -*- coding: utf-8 -*-

import math
import numpy as np
import pandas as pd
import global_variables

from sklearn import preprocessing
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MaxAbsScaler

import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, './../bd.xlsx')

def load_data(output,variables,filepath=filename):
    if(variables==global_variables.numericas):
        data = pd.read_excel(open(filepath, 'rb'), skiprows=1,header=None)
        data.replace('sem dados', float('nan'),inplace=True)
        data.replace('x', float('nan'),inplace=True)
        data.fillna(float('nan'), inplace=True)
        counter = 0
        lista = data.loc[[0]].values[0]
        flag = 0
        for i in range(0,len(data.loc[[0]].values[0])):
            if lista[i] == "risco médio":
                if flag==0:
                    flag+=1
                    counter+=1
                else:
                    lista[i] = "risco médio."+str(counter)
                    flag+=1
                    counter+=1
        lista[-1] = "Comorbilidades pré-operatórias"
        data.columns = lista

        data.drop([0],inplace=True,axis=0)
        
    else:
        data= pd.read_excel(open(filepath, 'rb'), skiprows=1)
        data.replace('sem dados', float('nan'),inplace=True)
        data.replace('x', float('nan'),inplace=True)
        data.fillna(float('nan'), inplace=True)
        data.rename( columns={'Unnamed: 136':'Comorbilidades pré-operatórias'}, inplace=True )

    dataset = pd.concat([data.loc[:,variables],data.loc[:,output]], axis=1)

    
    if(output==global_variables.outputs[-1]):
        dataset.replace({global_variables.outputs[-1]:float('nan')},0,inplace=True)

    # To drop every line that has a NaN value on the TARGET column
    dataset.dropna(how="any",subset=dataset.columns[[-1]],inplace=True)

    y =  dataset.iloc[:,-1]
    if(variables==global_variables.numericas):
        y = y.astype(np.float)

    # Pré-tratamento de algumas variáveis
    if(variables==global_variables.codigos): # são criadas, respectivamente: 238 e 233 +/-
        dictionary = {} #em média vão existir 4.7 representantes para cada código...
        for var in variables:
            distinct = set()
            lines = []
            index = 0
            for l in dataset.loc[:,var]:
                lines.append([])
                for x in str(l).replace('\n',' ').split(' '):
                    part = x.strip()
                    if part.isnumeric():
                        if sum(c.isdigit() for c in part) > 2: #os códigos são todos de pelo menos 3 digitos (evitar números da descrição)
                            distinct.add(x.strip())
                            lines[index].append(x.strip())
                index+=1
            for x in distinct:
                dictionary[var+"|"+str(x)]=[]
            for x in lines:
                for key in dictionary.keys():
                    if key.split('|')[1] in x and key.split('|')[0]==var:
                        dictionary[key].append(1)
                    elif key.split('|')[0]==var:
                        dictionary[key].append(0)
        X = pd.DataFrame(dictionary)
        dataset = X

    else:
        X = dataset.iloc[:,0:-1]
        if(variables==global_variables.numericas):
            X = X.astype(np.float)

    # Missing values imputation, on X (using KNN)
    imp = KNNImputer(n_neighbors=15)
    X = imp.fit_transform(X)

    scaler = MaxAbsScaler() 
    X = scaler.fit_transform(X)

    return dataset,X,y