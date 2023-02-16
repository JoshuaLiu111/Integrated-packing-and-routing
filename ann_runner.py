# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 11:47:17 2023

@author: Joshualiu
"""

import pandas as pd
import numpy as np
import pickle
import statistics
from scipy.stats import skew
import random
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as io
io.renderers.default='svg'
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping


#read instance into features
def instance2vector(input_instance):
    
    #unlist
    De_list,B_list,P_list,T_list,D_list,desmap = input_instance
    
    #number of boxes
    b_num = len(B_list)
    
    #capcity ratio
    b_vs = [b.v for b in B_list]
    b_v_mean = np.mean(b_vs)
    p_Vs = [p.V for p in P_list]
    p_V_mean = np.mean(p_Vs)
    t_Ts = [t.T for t in T_list]
    t_T_mean = np.mean(t_Ts)
    
    #number and max of destination
    b_ds = [b.D for b in B_list]
    b_d_num = len(np.unique(b_ds))
    b_d_max = max(np.unique(b_ds, return_counts=True)[1])
    
    #mean and standard deviation of destination cost
    desmap_nonzero = [dp for d in desmap for dp in d if dp != 0]
    d_mean = np.mean(desmap_nonzero)
    d_sd = statistics.stdev(desmap_nonzero)
    d_skewness = skew(desmap_nonzero)
    
    #cost ratio
    t_Cs = [t.C for t in T_list]
    t_C_mean = np.mean(t_Cs)
    
    #record
    input_vector = [b_num/b_d_num,p_V_mean/b_v_mean,t_T_mean/p_V_mean,
                    b_d_max,d_sd,d_skewness,d_mean/t_C_mean]
        
    return input_vector


if __name__ == "__main__":
    #read feedings
    with open('ann_data.pkl','rb') as f:
        input_instances,cost_results,targets = pickle.load(f)
    
    #to vector
    input_list = []
    for ins in input_instances:
        input_list.append(instance2vector(ins))
        
    #padding unbalanced data    
        
    index_of_MBF = [i for i, e in enumerate([test[0] \
                    == 1 for test in targets]) if e == 1]
    index_of_ABF = [i for i, e in enumerate([test[1] \
                    == 1 for test in targets]) if e == 1]
    index_of_KDC = [i for i, e in enumerate([test[2] \
                    == 1 for test in targets]) if e == 1]    
    index_of_PP  = [i for i, e in enumerate([test[3] \
                    == 1 for test in targets]) if e == 1]
    index_input = np.random.choice(index_of_MBF,150).tolist()\
        + np.random.choice(index_of_ABF,150).tolist()\
            + np.random.choice(index_of_KDC,150).tolist()\
                + np.random.choice(index_of_PP,150).tolist()
    
    #shuffle the feed
    random.shuffle(index_input)    
    
    X = pd.DataFrame([input_list[i] for i in index_input])
    # convert to numpy arrays
    X = np.array(X)
    
    dummy_y = pd.DataFrame([targets[i] for i in index_input])
    dummy_y = np.array(dummy_y)
    
    # build a model
    model = Sequential()
    model.add(Dense(16, input_shape=(X.shape[1],), activation='relu')) # input shape is (features,)
    model.add(Dense(8, activation='relu'))
    model.add(Dense(4, activation='softmax'))
    model.summary()

    # compile the model
    model.compile(optimizer='adam', 
                  loss='categorical_crossentropy', # this is different instead of binary_crossentropy (for regular classification)
                  metrics=['accuracy'])

    # early stopping callback
    # This callback will stop the training when there is no improvement in  
    # the validation loss for 10 consecutive epochs.  
    es = EarlyStopping(monitor='val_loss', 
                       mode='min',
                       patience=50, 
                       restore_best_weights=True) # important - otherwise you just return the last weights...

    # now we just update our model fit call
    history = model.fit(X,
                        dummy_y,
                        callbacks=[es],
                        epochs=8000000, # you can set this to a big number!
                        batch_size=10,
                        shuffle=True,
                        validation_split=0.2,
                        verbose=1)

    history_dict = history.history

    # learning curve
    # accuracy
    acc = history_dict['accuracy']
    val_acc = history_dict['val_accuracy']

    # loss
    loss = history_dict['loss']
    val_loss = history_dict['val_loss']

    # range of X (no. of epochs)
    epochs = range(1, len(acc) + 1)

    # plot
    df = pd.DataFrame(dict(
         Epochs = list(epochs)*2,
         Accuracy = acc + val_acc,
         Type = ['Training accuracy']*len(epochs) 
         + ['Validation accuracy']*len(epochs)))
    
    fig = px.line(df, x="Epochs", y="Accuracy", color='Type')
    
    fig.show()
    
    fig.write_image('Figures/ann_training.png')
    

    preds = model.predict(X) # see how the model did!

    # Almost a perfect prediction
    # actual is left, predicted is top
    # names can be found by inspecting Y
    matrix = confusion_matrix(dummy_y.argmax(axis=1), preds.argmax(axis=1))

    # more detail on how well things were predicted
    print(classification_report(dummy_y.argmax(axis=1), preds.argmax(axis=1)))

    
    

    #compare results
    MBF_perform = [temp[0] for temp in [cost_results[i] for i in index_input]]
    ABF_perform = [temp[1] for temp in [cost_results[i] for i in index_input]]
    KDC_perform = [temp[2] for temp in [cost_results[i] for i in index_input]]
    PP_perform = [temp[3] for temp in [cost_results[i] for i in index_input]]
    ANN_perform = [costs[index] for index,costs in zip(preds.argmax(axis=1),[cost_results[i] for i in index_input])]
    OPT_perform = [a*b for tar,costs in zip(targets,cost_results) for a,b in zip(tar,costs)]
    OPT_perform = [ele for ele in OPT_perform if ele != 0]
    OPT_perform = [OPT_perform[i] for i in index_input]
    
    #combine
    combine_perform = [MBF_perform,ABF_perform,KDC_perform,PP_perform,
                       ANN_perform,OPT_perform]
    
    #extract box num index
    b_num_list = [len(input_instances[i][1]) for i in index_input]
    index_of_b20 = [i for i, e in enumerate([test \
                    == 20 for test in b_num_list]) if e == 1]
    index_of_b40 = [i for i, e in enumerate([test \
                    == 40 for test in b_num_list]) if e == 1]
    index_of_b60 = [i for i, e in enumerate([test \
                    == 60 for test in b_num_list]) if e == 1]  
    index_of_b80 = [i for i, e in enumerate([test \
                    == 80 for test in b_num_list]) if e == 1]     
    
    #get index of manual best algorithm MAN
    combine_perform_20_mean = [np.mean([fun[i] for i in index_of_b20]) for fun in combine_perform[:4]]
    combine_perform_40_mean = [np.mean([fun[i] for i in index_of_b40]) for fun in combine_perform[:4]]
    combine_perform_60_mean = [np.mean([fun[i] for i in index_of_b60]) for fun in combine_perform[:4]]
    combine_perform_80_mean = [np.mean([fun[i] for i in index_of_b80]) for fun in combine_perform[:4]]
    
    MAN_20 = combine_perform_20_mean.index(min(combine_perform_20_mean))
    MAN_40 = combine_perform_40_mean.index(min(combine_perform_40_mean))
    MAN_60 = combine_perform_60_mean.index(min(combine_perform_60_mean))
    MAN_80 = combine_perform_80_mean.index(min(combine_perform_80_mean))
    
    combine_perform_20 = [[fun[i] for i in index_of_b20] for fun in 
                          [combine_perform[MAN_20], combine_perform[4],
                           combine_perform[5]]]
    combine_perform_40 = [[fun[i] for i in index_of_b40] for fun in 
                          [combine_perform[MAN_40], combine_perform[4],
                           combine_perform[5]]]
    combine_perform_60 = [[fun[i] for i in index_of_b60] for fun in 
                          [combine_perform[MAN_60], combine_perform[4],
                           combine_perform[5]]]
    combine_perform_80 = [[fun[i] for i in index_of_b80] for fun in 
                          [combine_perform[MAN_80], combine_perform[4],
                           combine_perform[5]]]
    
    #generate boxplot
    Fun_num = 3
    
    color = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 180, Fun_num)]
    fun_name = ['MAN','ANN','OPT']
    x = ['20']*len(index_of_b20) + ['40']*len(index_of_b40) \
        + ['60']*len(index_of_b60) + ['80']*len(index_of_b80)
    
    fig = go.Figure()
    
    for i in range(Fun_num):    
        perform = combine_perform_20[i] + combine_perform_40[i] \
            + combine_perform_60[i] + combine_perform_80[i]  
        fig.add_trace(go.Box(
            y = perform,
            x = x,
            name = fun_name[i],
            marker_color = color[i]
        ))
    

    fig.update_layout(
        xaxis = dict(title='Box number',
                     tickfont = dict(size=25),
                     titlefont = dict(size = 25)),
        yaxis = dict(title='Total cost',
                     tickfont = dict(size=25),
                     titlefont = dict(size = 25)),
        legend = dict(font = dict(size = 25)),
        boxmode='group' # group together boxes of the different traces for each value of x
    )
    
    fig.write_image('Figures/ann_perform.png')
    
    #relative perform
    allmean_combine_perform_20 = np.mean([[fun[i] for i in index_of_b20] for fun in combine_perform[:4]], axis=0)
    allmean_combine_perform_40 = np.mean([[fun[i] for i in index_of_b40] for fun in combine_perform[:4]], axis=0)
    allmean_combine_perform_60 = np.mean([[fun[i] for i in index_of_b60] for fun in combine_perform[:4]], axis=0)
    allmean_combine_perform_80 = np.mean([[fun[i] for i in index_of_b80] for fun in combine_perform[:4]], axis=0)
    
    relative_combine_perform_20 = (100*(allmean_combine_perform_20-np.array(combine_perform_20))/allmean_combine_perform_20).tolist()
    relative_combine_perform_40 = (100*(allmean_combine_perform_40-np.array(combine_perform_40))/allmean_combine_perform_40).tolist()
    relative_combine_perform_60 = (100*(allmean_combine_perform_60-np.array(combine_perform_60))/allmean_combine_perform_60).tolist()
    relative_combine_perform_80 = (100*(allmean_combine_perform_80-np.array(combine_perform_80))/allmean_combine_perform_80).tolist()
    
    #clean data
    relative_combine_perform_20 = [[read if read > -10 else -10 for read in fun] for fun in relative_combine_perform_20]
    relative_combine_perform_40 = [[read if read > -10 else -10 for read in fun] for fun in relative_combine_perform_40]
    relative_combine_perform_60 = [[read if read > -10 else -10 for read in fun] for fun in relative_combine_perform_60]
    relative_combine_perform_80 = [[read if read > -10 else -10 for read in fun] for fun in relative_combine_perform_80]
    
    fig = go.Figure()
    
    for i in range(Fun_num):    
        perform = relative_combine_perform_20[i] + relative_combine_perform_40[i] \
            + relative_combine_perform_60[i] + relative_combine_perform_80[i]  
        fig.add_trace(go.Box(
            y = perform,
            x = x,
            name = fun_name[i],
            marker_color = color[i]
        ))
    

    fig.update_layout(
        xaxis = dict(title='Box number',
                     tickfont = dict(size=25),
                     titlefont = dict(size = 25)),
        yaxis = dict(title='Relative cost improvement',
                     tickfont = dict(size=25),
                     titlefont = dict(size = 25)),
        legend = dict(font = dict(size = 25)),
        boxmode='group' # group together boxes of the different traces for each value of x
    )
    
    fig.write_image('Figures/ann_perform_rel.png')
