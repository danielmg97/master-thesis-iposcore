import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import unidecode
import math
import re

data = pd.read_excel(open('bd.xlsx', 'rb'))
data2= pd.read_excel(open('bd2.xlsx', 'rb'), skiprows=1)
complicacao = data.loc[:,"complicação pós-cirúrgica"].values   


def plot_single_bar(positive,negative,labels,column):
    x = labels
    y = [positive[i]/(positive[i]+negative[i]) for i in range(0,len(positive))]
    fig, ax = plt.subplots()
    plt.bar(x, y)
    # plt.xticks(np.arange(min(x), max(x)+1, 1.0))
    plt.ylim(0, 1)
    ax.set_title(column+" (% complicações)")
    for i, v in enumerate(y):
        plt.text(i-0.15,v + 0.02,"{0:.2}".format(v)) #this line has a problem for two factors, change x[i] to i
    fig.tight_layout()
    # plt.xticks(rotation=90) #use only if there are too many labels
    plt.show()


def plot_double_bar(positive,negative,labels,column):
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, negative, width, label='No Complication')
    rects2 = ax.bar(x + width/2, positive, width, label='Complication')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('')
    ax.set_xlabel('')
    ax.set_title(column)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    # plt.xticks(rotation=90) #use only if there are too many labels
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()

    plt.show()
'''
# ACS Prcedimento retirar só os números:
procedimentos_dict = {}
procedimento_column = data.loc[:,"ACS_procedimento"].values
for x in range(0,len(procedimento_column)):
    res = re.search("[0-9]{5}",str(procedimento_column[x]))
    if(res):
        numero = re.findall("[0-9]{5}",procedimento_column[x])[-1]
        if(complicacao[x]==1):
            if(str(numero)+"_1" in procedimentos_dict.keys()):
                procedimentos_dict[str(numero)+"_1"]+=1
            else:
                procedimentos_dict[str(numero)+"_1"]=1
        elif(complicacao[x]==0):
            if(str(numero)+"_0" in procedimentos_dict.keys()):
                procedimentos_dict[str(numero)+"_0"]+=1
            else:
                procedimentos_dict[str(numero)+"_0"]=1
# print(procedimentos_dict) # Não sei bem como vizualizar estes dados. São muitos para barras, mas não posso discretizar por intervalos.
'''
# selected = data.loc[:,"ACS idade":"ACS peso"]
# selected = data.loc[:,"ACS altura":"ACS peso"]
# selected = data.loc[:,"ARISCAT Idade":"SCORE ARISCAT"]
# selected = data2.loc[:,"LOCALIZAÇÃO "]
# localizacao = selected.values
# for x in range(0,len(localizacao)):
#     if isinstance(localizacao[x], str):
#         localizacao[x] = unidecode.unidecode(localizacao[x]).upper()
# fatores = localizacao
# selected = pd.concat([data.loc[:,"ACS idade":"ACS peso"],data.loc[:,"idade"]],axis=1) 
# selected = data.loc[:,"PP idade":"% mortalidade P-Possum"]
# selected = data.loc[:,"complicações sérias (%)":"ACS - previsão dias internamento"]
# selected = data.loc[:,"ACS altura":"ACS peso"]
selected = pd.concat([data.loc[:,"destino após IPO"],data.loc[:,"óbito até 1 ano "]],axis=1) 
fatores=selected.values
# bmi = [ round((x[1]/((x[0]/100)**2)),2) for x in fatores]
# positive = [] 
# negative = []
# labels = []
# temp=[]

# for element in range(0,len(bmi)):
#     if (bmi[element]>12.77 and bmi[element]<42.77):
#         temp.append([bmi[element]])
#     else:
#         temp.append([float('nan')])
# fatores=temp

def process_numbers(fatores,complicacao,selected):
    for column in range(0,len(fatores[0])):
        dictionary = {}
        i = -1
        for x in fatores:
            i+=1
            if(isinstance(list(x)[column],str)):
                x[column]=float('nan')
            if(math.isnan(list(x)[column])):
                continue
            if(math.isnan(complicacao[i])):
                continue
            if(str(list(x)[column])+"_"+str(complicacao[i]) not in dictionary.keys()):
                dictionary[str(list(x)[column])+"_"+str(complicacao[i])]=1
            else:
                dictionary[str(list(x)[column])+"_"+str(complicacao[i])]+=1
            if(str(list(x)[column])+"_1.0" not in dictionary.keys()):
                dictionary[str(list(x)[column])+"_1.0"]=0
            if(str(list(x)[column])+"_0.0" not in dictionary.keys()):
                dictionary[str(list(x)[column])+"_0.0"]=0
        # print(dictionary)
        positive=[]
        negative=[]
        labels = []
        if len(dictionary)>10:
            value_list=[]
            for k,w in dictionary.items():
                for times in range(0,w):
                    value_list.append(float(k.split('_')[0]))
            minimo = min(value_list)
            maximo = max(value_list)
            bin_number = round((maximo-minimo)/10)+1
            positive = np.zeros(bin_number)
            negative = np.zeros(bin_number)
            labels=[str(minimo+(10*number))+"-"+str(minimo+(10*(number+1))) for number in range(0,bin_number)]
            for j,v in enumerate(value_list):
                if complicacao[j]==1:
                    if(v==maximo):
                        positive[-1]+=1
                    else:
                        positive[int((v-minimo)/10)]+=1
                elif complicacao[j]==0:
                    if (v==maximo):
                        negative[-1]+=1
                    else:
                        negative[int((v-minimo)/10)]+=1

        else:
            dicio = sorted(dictionary)
            for x in dicio:
                if("_1" in x):
                    positive.append(dictionary[x])
                elif("_0" in x):
                    negative.append(dictionary[x])
                    labels.append(x.split("_")[0])
            # labels.sort()
        
        nome_coluna=str(list(selected.columns.values.tolist())[column])
        # nome_coluna="BMI"
        plot_double_bar(positive,negative,labels,nome_coluna)
        plot_single_bar(positive,negative,labels,nome_coluna)

def process_words(fatores,complicacao,selected):
    dictionary={}
    positive=[]
    negative=[]
    labels = []
    for el in range(0,len(fatores)):
        if(not isinstance(fatores[el],str)):
            continue
        if fatores[el]+"_"+str(complicacao[el]) not in dictionary:
            dictionary[fatores[el]+"_"+str(complicacao[el])] = 1
        elif fatores[el]+"_"+str(complicacao[el]) in dictionary:
            dictionary[fatores[el]+"_"+str(complicacao[el])] += 1
        if fatores[el]+"_0.0" not in dictionary:
            dictionary[fatores[el]+"_0.0"] = 0
        if fatores[el]+"_1.0" not in dictionary:
            dictionary[fatores[el]+"_1.0"] = 0
    for x in set(fatores):
        if(not isinstance(x,str)):
            continue
        else:
            if(dictionary[str(x)+"_1.0"]+dictionary[str(x)+"_0.0"]>3): #filtrei todas as localizações com menos de 3 ocorrências randomly
                positive.append(dictionary[str(x)+"_1.0"])
                negative.append(dictionary[str(x)+"_0.0"])
                labels.append(x)
    nome_coluna = ""        
    plot_double_bar(positive,negative,labels,nome_coluna)
    plot_single_bar(positive,negative,labels,nome_coluna)

if (isinstance(fatores[0],str)):
    process_words(fatores,complicacao,selected)
else:
    process_numbers(fatores,complicacao,selected)
