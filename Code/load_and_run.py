import math
import numpy as np
import pandas as pd
import global_variables
import variables_translater

import warnings
warnings.filterwarnings("ignore")
# from IPython.display import display

from sklearn import preprocessing
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from imblearn.combine import SMOTETomek
from imblearn.combine import SMOTEENN
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import MaxAbsScaler
# Classification Metrics
from sklearn.metrics import recall_score
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import accuracy_score
# Regression Metrics
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

from dtreeviz.trees import *
import pydotplus
from sklearn.tree import export_graphviz

from yellowbrick.regressor import ResidualsPlot
import copy

import matplotlib.pyplot as plt
from sklearn.metrics import auc as auc_calc
from sklearn.metrics import plot_roc_curve

def load_data(output,variables,filepath="./bd.xlsx"):
    data = pd.read_excel(open(filepath, 'rb'), skiprows=1)

    # Resolve minor inconsistencies
    data.replace('sem dados', float('nan'),inplace=True)
    data.replace('x', float('nan'),inplace=True)
    data.fillna(float('nan'), inplace=True)

    # Select the features and the output
    dataset = data.loc[:,variables+[output]]

    # To drop every line that has a NaN value on the TARGET column
    dataset.dropna(how="any",subset=dataset.columns[[-1]], inplace=True)

    return dataset

def tree_plot_regression(clf,dataset,headers,to_dummify,name=None):
    X_train, X_test, y_train, y_test = train_test_split(dataset.iloc[:,0:-1], dataset.iloc[:,-1], test_size=0.33, random_state=42)
    
    # Missing values imputation, on X (using KNN)
    imp = KNNImputer(n_neighbors=15)
    X_train = imp.fit_transform(X_train)
    X_test = imp.transform(X_test)

    X_train = pd.DataFrame(X_train,columns=headers[0:-1])
    X_test = pd.DataFrame(X_test,columns=headers[0:-1])
    
    for col in to_dummify:
      try:
        X_train[col]=X_train[col].round(0)
        X_test[col]=X_test[col].round(0)
      except:
        pass

    # Dummification
    encoder = OneHotEncoder(handle_unknown='ignore')

    temp1 = encoder.fit_transform(X_train.loc[:,to_dummify])
    temp2 = encoder.transform(X_test.loc[:,to_dummify])

    labels_dummified = encoder.get_feature_names(to_dummify)
    X_train = X_train.drop(columns=to_dummify)
    X_test = X_test.drop(columns=to_dummify)
    
    temp1 = pd.DataFrame(temp1.toarray(),columns=labels_dummified)
    temp2 = pd.DataFrame(temp2.toarray(),columns=labels_dummified)

    X_train = pd.concat([X_train,temp1],axis=1)
    X_test = pd.concat([X_test,temp2],axis=1)

    X_column_labels = X_train.columns

    # print(X_train.shape)
    # print(y_train.shape)
    # # Resampling (for imbalanced problems)
    # smt = SMOTEENN(random_state=42)
    # X_train, y_train = smt.fit_resample(X_train, y_train)

    # Normalization
    scaler = MaxAbsScaler() 
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    X_train = pd.DataFrame(X_train,columns=X_column_labels)
    X_test = pd.DataFrame(X_test,columns=X_column_labels)

    clf.fit(X_train, y_train)
    
    # if(name=='XGB'):
    #     print("gblinear")
    # else:
    lista = list(zip(variables_translater.tradutor(list(X_train.columns)), clf.feature_importances_))
    lista = sorted(lista, key=lambda par: par[1])
    lista.reverse()
    for el in lista:
      print(el)

    if(name=='Decision Tree'):

        dot_data = export_graphviz(clf, 
                    out_file=None, 
                    feature_names = variables_translater.tradutor(list(X_train.columns)),
                    filled = True)
        graph = pydotplus.graph_from_dot_data(dot_data)
        nodes = graph.get_node_list()

        predicted_leafs = clf.apply(X_test)
        results = [(predicted_leafs[i],y_test.values[i]) for i in range(len(predicted_leafs))]

        children_left = clf.tree_.children_left
        children_right = clf.tree_.children_right

        for node in nodes:
            if node.get_name() not in ('node', 'edge'):
                node.set_colorscheme('rdylgn10')
                
                leaf_value = clf.tree_.value[int(node.get_name())][0][0]
                total_guesses = 0
                total_error = 0
                if (children_left[int(node.get_name())] == children_right[int(node.get_name())]):
                    for pair in results:
                        if(pair[0]==int(node.get_name())):
                            total_guesses += 1
                            total_error += abs(pair[1]-leaf_value)
                    if(total_guesses==0):
                      node.set_fillcolor('lightgray')
                      continue
                    color_index = 10-int((total_error/total_guesses)*2.5) #erro de 1 unidade tem o espector todo das cores
                    if color_index < 1:
                        color_index = 1
                    node.set_fillcolor(str(color_index))
                    node.set_label(node.get_label()+'\nleaf_mae = '+str(round(total_error/total_guesses,2)))
                else:
                    node.set_fillcolor('white')

        graph.write_png('colored_tree.png')

def tree_plot_classification(clf,dataset,headers,to_dummify,name=None):
    X_train, X_test, y_train, y_test = train_test_split(dataset.iloc[:,0:-1], dataset.iloc[:,-1], test_size=0.33, random_state=42, stratify=dataset.iloc[:,-1])
    
    # Missing values imputation, on X (using KNN)
    imp = KNNImputer(n_neighbors=15)
    X_train = imp.fit_transform(X_train)
    X_test = imp.transform(X_test)

    X_train = pd.DataFrame(X_train,columns=headers[0:-1])
    X_test = pd.DataFrame(X_test,columns=headers[0:-1])
    
    for col in to_dummify:
      try:
        X_train[col]=X_train[col].round(0)
        X_test[col]=X_test[col].round(0)
      except:
        pass

    # Dummification
    encoder = OneHotEncoder(handle_unknown='ignore')

    temp1 = encoder.fit_transform(X_train.loc[:,to_dummify])
    temp2 = encoder.transform(X_test.loc[:,to_dummify])

    labels_dummified = encoder.get_feature_names(to_dummify)
    X_train = X_train.drop(columns=to_dummify)
    X_test = X_test.drop(columns=to_dummify)
    
    temp1 = pd.DataFrame(temp1.toarray(),columns=labels_dummified)
    temp2 = pd.DataFrame(temp2.toarray(),columns=labels_dummified)

    X_train = pd.concat([X_train,temp1],axis=1)
    X_test = pd.concat([X_test,temp2],axis=1)

    X_column_labels = X_train.columns

    # Resampling (for imbalanced problems)
    smt = SMOTEENN(random_state=42)
    X_train, y_train = smt.fit_resample(X_train, y_train)

    # Normalization
    scaler = MaxAbsScaler() 
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    X_train = pd.DataFrame(X_train,columns=X_column_labels)
    X_test = pd.DataFrame(X_test,columns=X_column_labels)

    clf.fit(X_train, y_train)
    
    lista = list(zip(variables_translater.tradutor(list(X_train.columns)), clf.feature_importances_))
    lista = sorted(lista, key=lambda par: par[1])
    lista.reverse()
    for el in lista:
      print(el)

    if(name=='Decision Tree'):

        dot_data = export_graphviz(clf, 
                    out_file=None, 
                    feature_names = variables_translater.tradutor(list(X_train.columns)),
                    class_names = ['0','1','2','3','4','5','6','7'],
                    rounded = True,
                    filled = True)
        graph = pydotplus.graph_from_dot_data(dot_data)
        nodes = graph.get_node_list()

        predicted_leafs = clf.apply(X_test)
        results = [(predicted_leafs[i],y_test.values[i]) for i in range(len(predicted_leafs))]

        children_left = clf.tree_.children_left
        children_right = clf.tree_.children_right

        for node in nodes:
            if node.get_name() not in ('node', 'edge'):
                node.set_colorscheme('rdylgn10')
                    
                values = clf.tree_.value[int(node.get_name())][0]
                leaf_value = np.nonzero(values)[0][0]
                total_guesses = 0
                correctly_guessed = 0
                if (children_left[int(node.get_name())] == children_right[int(node.get_name())]):
                    for pair in results:
                        if(pair[0]==int(node.get_name())):
                            total_guesses += 1
                            if (pair[1]==leaf_value):
                                correctly_guessed +=1
                    if(total_guesses==0):
                      node.set_fillcolor('lightgray')
                      continue
                    color_index = int(((correctly_guessed/total_guesses)*10)+1)
                    if color_index > 10:
                        color_index = 10
                    node.set_fillcolor(str(color_index))
                    node.set_label(node.get_label()+'\nleaf_accuracy = '+str(round(correctly_guessed/total_guesses,2)))
                else:
                    node.set_fillcolor('white')
                    

        graph.write_png('colored_tree.png')

def data_preprocess(X_train, X_test, y_train, y_test, to_dummify, headers, resample=False):
     # Missing values imputation, on X (using KNN)
    imp = KNNImputer(n_neighbors=15)
    X_train = imp.fit_transform(X_train)
    X_test = imp.transform(X_test)

    X_train = pd.DataFrame(X_train,columns=headers[0:-1])
    X_test = pd.DataFrame(X_test,columns=headers[0:-1])

    for col in to_dummify: # problem with imputer giving float values to categoric variables...
      try:
        X_train[col]=X_train[col].round(0)
        X_test[col]=X_test[col].round(0)
      except:
        pass

    # Dummification of categoric variables
    transformer = ColumnTransformer(transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), to_dummify)], remainder='passthrough')        
    X_train = transformer.fit_transform(X_train)
    X_test = transformer.transform(X_test)

    if(resample):
      # Resampling (for imbalanced problems)
      smt = SMOTEENN(random_state=42)
      X_train, y_train = smt.fit_resample(X_train, y_train)

    # Normalization
    scaler = MaxAbsScaler() 
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test

def k_fold(clf,dataset,headers,to_dummify):
    # Lists to store the results of k-fold iterations
    kappa = []
    recall = []
    auc = []
    accuracy = []

    # Vars for ROC curve plot
    # tprs = []
    # aucs = []
    # mean_fpr = np.linspace(0, 1, 100)
    # fig, ax = plt.subplots()
    # i=1

    skf = StratifiedKFold(n_splits=10, random_state=42, shuffle=True) #Stratified because of imbalance (avoid missing some classes randomly)
    for train_index, test_index in skf.split(dataset[:,:-1], dataset[:,-1]): 

        X_train, X_test, y_train, y_test = data_preprocess(dataset[:,:-1][train_index], dataset[:,:-1][test_index], dataset[:,-1][train_index], dataset[:,-1][test_index], to_dummify, headers, resample=True)

        try:
          clf.fit(X_train, y_train)
        except:
          X_train = X_train.toarray()
          X_test = X_test.toarray()
          clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        y_pred_proba = clf.predict_proba(X_test)
        if(len(y_pred_proba[0])==2):
          y_pred_proba = [el[-1] for el in y_pred_proba]
        
        recall.append(recall_score(y_test, y_pred, average=None))
        kappa.append(cohen_kappa_score(y_test, y_pred))
        auc.append(roc_auc_score(y_test, y_pred_proba,multi_class='ovo'))
        accuracy.append(accuracy_score(y_test, y_pred))

        ########## ROC CURVE ###########
        # viz = plot_roc_curve(clf, X_test, y_test,name='ROC fold {}'.format(i),alpha=0.3, lw=1, ax=ax)
        # interp_tpr = np.interp(mean_fpr, viz.fpr, viz.tpr)
        # interp_tpr[0] = 0.0
        # tprs.append(interp_tpr)
        # aucs.append(viz.roc_auc)
        # i+=1
        ################################

    print('Kappa = '+str(sum(kappa)/len(kappa)))
    recall_avg = np.zeros(len(recall[0]))
    for scr in recall:
      for i in range(0,len(scr)):
        recall_avg[i]+=scr[i]
    for i in range(0,len(recall_avg)):
        recall_avg[i] = round(recall_avg[i]/len(recall),3)
    print('Recall = '+str(recall_avg))
    print('AUC = '+str(sum(auc)/len(auc)))
    print('Accuracy = '+str(sum(accuracy)/len(accuracy)))
    print("------------------------------------")
    print("kappa",kappa)
    print("recall",recall)
    print("AUC",auc)
    print("accuracy",accuracy)
    print("\n")

    ######## PLOT ROC CURVE ###########
    # ax.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',label='Chance', alpha=.8)

    # mean_tpr = np.mean(tprs, axis=0)
    # mean_tpr[-1] = 1.0
    # mean_auc = auc_calc(mean_fpr, mean_tpr)
    # std_auc = np.std(aucs)
    # ax.plot(mean_fpr, mean_tpr, color='b',label=r'Mean ROC (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),lw=2, alpha=.8)

    # std_tpr = np.std(tprs, axis=0)
    # tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
    # tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
    # ax.fill_between(mean_fpr, tprs_lower, tprs_upper, color='grey', alpha=.2,label=r'$\pm$ 1 std. dev.')

    # ax.set(xlim=[-0.05, 1.05], ylim=[-0.05, 1.05],title="Receiver operating characteristic '"+variables_translater.tradutor([headers[-1]])[0]+"'")
    # ax.legend(bbox_to_anchor=(1.00, 1), loc='upper left')
    # plt.savefig('roc_k_fold_'+headers[-1]+'_'+type(clf).__name__+'.png',dpi=300, bbox_inches = "tight")
    ###################################

    return 1-np.mean(recall_avg)
    # return 1-(sum(kappa)/len(kappa))
    # return 1-sum(auc)/len(auc)

def reg_k_fold(reg, dataset, headers, to_dummify, n_outputs = 1):

    # model = copy.deepcopy(reg)
    mae = []
    rmse = []
    r2 = []

    kappa = []
    recall = []
    accuracy = []

    cv = KFold(n_splits = 10, random_state = 42, shuffle = True)
    for train_index, test_index in cv.split(dataset[:,:-1], dataset[:,-1]):
        
        X_train, X_test, y_train, y_test = data_preprocess(dataset[:,:-1][train_index], dataset[:,:-1][test_index], dataset[:,-1][train_index], dataset[:,-1][test_index], to_dummify, headers)

        try:
          reg.fit(X_train, y_train)
        except TypeError:
          X_train = X_train.toarray()
          X_test = X_test.toarray()
          reg.fit(X_train, y_train)
        except:
          print("***###***FAILED_FIT***###***")
          print("X_train:")
          for col in X_train:
            print("\n")
            for li in col:
              print(li, end =" ")
          print("y_train:", *y_train)
          for x in X_train:
            if(pd.isnull(np.array(x)).any):
              print(x)
        y_pred = reg.predict(X_test)
        
        # Metrics
        if(pd.isnull(np.array(y_pred)).any()):
          print("***###***FAILED_PREDICT***###***")
          print("y_pred:", *y_pred)
          # print("X_test:")
          # X_test
          # print("y_test:", *y_test)
        mae.append(mean_absolute_error(y_test, y_pred))
        rmse.append(mean_squared_error(y_test, y_pred, squared=False))
        r2.append(r2_score(y_test, y_pred))

        # Discrete Metrics
        y_test = [str(int(x)) if (int(x) <= n_outputs and int(x) >= 0) else (str(n_outputs) if int(x) > n_outputs else '0') for x in y_test]
        y_pred = [str(int(x)) if (int(x) <= n_outputs and int(x) >= 0) else (str(n_outputs) if int(x) > n_outputs else '0') for x in y_pred]
        
        recall.append(recall_score(y_test, y_pred, average=None))
        kappa.append(cohen_kappa_score(y_test, y_pred))
        accuracy.append(accuracy_score(y_test, y_pred))

    print('Kappa = '+str(sum(kappa)/len(kappa)))
    recall_avg = np.zeros(len(recall[0]))
    for scr in recall:
      for i in range(0,len(scr)):
        recall_avg[i]+=scr[i]
    for i in range(0,len(recall_avg)):
        recall_avg[i] = round(recall_avg[i]/len(recall),3)
    print('Recall = '+str(recall_avg))
    print('Accuracy = '+str(sum(accuracy)/len(accuracy)))
    print("------------------------------------")

    print("MAE = "+str(sum(mae)/len(mae)))
    print("RMSE = "+str(sum(rmse)/len(rmse)))
    print("R2 = "+str(sum(r2)/len(r2)))
    print("------------------------------------")

    print("mae",mae)
    print("rmse",rmse)
    print("r2",r2)
    print("-------------------------------------")

    print("kappa",kappa)
    print("recall",recall)
    print("accuracy",accuracy)
    print("\n")

    ###### Plot Residuals ########
    # X_train, X_test, y_train, y_test = train_test_split(dataset[:,0:-1], dataset[:,-1], test_size=0.33, random_state=42)
    # X_train, X_test, y_train, y_test = data_preprocess(X_train, X_test, y_train, y_test, to_dummify, headers)
    # try:
    #   visualizer = ResidualsPlot(model)
    #   visualizer.fit(X_train, y_train)
    #   visualizer.score(X_test, y_test)
    #   visualizer.show(outpath='roc_k_fold_'+headers[-1]+'_'+type(model).__name__+'.png',dpi=300, bbox_inches = "tight")
    # except:
    #   pass
    ##############################

    return sum(mae)/len(mae)