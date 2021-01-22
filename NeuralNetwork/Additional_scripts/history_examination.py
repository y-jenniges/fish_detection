import json
import os
import pickle
import matplotlib.pyplot as plt

# for minimal NN and transfer learninf variations
pathes = ["../data/output/150/trainHistory-L1.pickle", 
          "../data/output/250/trainHistory-L1.pickle",
          "../data/output/350/trainHistory-L1.pickle",
          "../data/output/450/trainHistory-L1.pickle",
              "../data/output/500/trainHistory-L1.pickle",
            # "../data/output/600/trainHistory-L1.pickle",
            # "../data/output/700/trainHistory-L1.pickle",
            "../data/output/500/trainHistory-L2.pickle",
            #"../data/output/600/trainHistory-L2.pickle",
            #"../data/output/700/trainHistory-L2.pickle",
          ]

pathes_100 = ["../data/output/151/trainHistory-L1.pickle", 
              "../data/output/251/trainHistory-L1.pickle",
              "../data/output/351/trainHistory-L1.pickle",
              "../data/output/451/trainHistory-L1.pickle", 
              "../data/output/501/trainHistory-L1.pickle",
              "../data/output/501/trainHistory-L2.pickle",
              ]

histories = []
for i in pathes + pathes_100:
    with open(i,'rb') as file:
        raw_data = file.read()
    history = pickle.loads(raw_data)
    histories.append(history)

# plt.plot(histories[0]["mae"])
# plt.plot(histories[1]["mae"])
# plt.plot(histories[2]["mae"])
# plt.plot(histories[3]["mae"])
# plt.plot(histories[4]["mae"] + histories[5]["mae"])
# plt.yscale("log")
# plt.legend(['Min CNN', 'No layers', 'Last layers', 'All layers', 'All layers delayed'], loc='upper right')

# plt.plot(histories[6]["mae"])
# plt.plot(histories[7]["mae"])
# plt.plot(histories[8]["mae"])
# plt.plot(histories[9]["mae"])
# plt.plot(histories[10]["mae"] + histories[11]["mae"])
# plt.yscale("log")
# plt.legend(['Min CNN', 'No layers', 'Last layers', 'All layers', 'All layers delayed'], loc='upper right')

# plt.plot(histories[3]["mae"][-20:])
# plt.plot(histories[5]["mae"][-20:])
# plt.plot(histories[9]["mae"][-20:])
# plt.plot(histories[11]["mae"][-20:])
# plt.legend(['All layers, 60 epochs', 'All layers delayed, 60 epochs', 'All layers, 110 epochs', 'All layers delayed, 110 epochs'], loc='lower right')

#plt.plot(histories[2]["mae"][-20:])
plt.plot(histories[5]["mae"][-20:])
#plt.plot(histories[8]["mae"][-20:])
plt.plot(histories[11]["mae"][-20:])
#plt.legend(['Last layers, 60 epochs', 'All layers delayed, 60 epochs', 'Last layers, 110 epochs', 'All layers delayed, 110 epochs'], loc='lower right')
plt.legend(["60 epochs", "110 epochs"])

# plt.plot(histories[9]["mae"])
# plt.plot(histories[9]["val_mae"])
# plt.yscale("log")
# plt.legend(["Train", "Validation"])

plt.ylabel("MAE")
plt.xlabel('Epoch')
#plt.savefig("TL_train_mae_last10layers.png")
#plt.savefig("training_loss_until10_50epochs.png")
#plt.savefig("TL_train_mae_100epochs.png")
#plt.savefig("TL_train_mae_allLayers.png")
#plt.savefig("TL_train_mae_allLayersDelayed_last20.png")
plt.show()


# vergleiche 50 / 100 epcohs model für delayed und all



pathes_l1 = ["../data/output/800/trainHistory-L1.pickle", 
              "../data/output/801/trainHistory-L1.pickle", 
          "../data/output/900/trainHistory-L1.pickle",  
          "../data/output/901/trainHistory-L1.pickle", 
          ]

pathes = [  "../data/output/800/trainHistory-L2.pickle", 
          "../data/output/900/trainHistory-L2.pickle",         
    ]

pathes_100 = [  "../data/output/801/trainHistory-L2.pickle", 
          "../data/output/901/trainHistory-L2.pickle",         
    ]

pathes_h = ["../data/output/800/trainHistory-H.pickle", 
              "../data/output/801/trainHistory-H.pickle", 
          "../data/output/900/trainHistory-H.pickle",  
          "../data/output/901/trainHistory-H.pickle", 
          ]

histories_l1 = []
for i in pathes_l1:
    with open(i,'rb') as file:
        raw_data = file.read()
    history = pickle.loads(raw_data)
    histories_l1.append(history)
    
histories_h = []
for i in pathes_h:
    with open(i,'rb') as file:
        raw_data = file.read()
    history = pickle.loads(raw_data)
    histories_h.append(history)

histories = []
for i in pathes:
    with open(i,'rb') as file:
        raw_data = file.read()
    history = pickle.loads(raw_data)
    histories.append(history)

histories_100 = []
for i in pathes_100:
    with open(i,'rb') as file:
        raw_data = file.read()
    history = pickle.loads(raw_data)
    histories_100.append(history)
    

key = "mae"
#key = "loss"
#print(f"key: {history[key]}")

# x = range(0,10)
# plt.plot(x, histories[0][key][:10])
# plt.plot(x, histories[1][key][:10])
# plt.plot(x, histories[2][key][:10])
# plt.plot(x, histories[3][key][:10])
# plt.plot(x, histories[4][key])
# #plt.plot(x, histories[5][key])
# #plt.plot(x, histories[6][key])

# x = range(10,50)
# plt.plot(x, histories[0][key][10:])
# plt.plot(x, histories[1][key][10:])
# plt.plot(x, histories[2][key][10:])
# plt.plot(x, histories[3][key][10:])
# plt.plot(x, histories[4][key][:40])
# #plt.plot(x, histories[5][key][:40])
# #plt.plot(x, histories[6][key][:40])

#for history in histories:
#     plt.plot(x, history[key][10:]) # training
    #plt.plot(history[f'val_{key}'][10:]) # validation

for history in histories:
    plt.plot(history[key]) # training
    #plt.plot(history[f'val_{key}'][10:]) # validation

for history in histories_100:
    plt.plot(history[key]) # training
    #plt.plot(history[f'val_{key}']) # validation

for history in histories_l1:
    plt.plot(history[key])

x = range(10,20)    
for history in histories_h:
    plt.plot(x, history[key][10:])

x1 = range(0,50)
x2 = range(0,100)


# plt.plot(histories_l1[0][key] + histories[0][key])
# plt.plot(histories_l1[1][key] + histories_100[0][key])
# #plt.plot(histories[0]["val_"+key])
# #plt.plot(histories_100[0]["val_"+key])
# plt.plot(histories_l1[2][key] + histories[1][key])
# plt.plot(histories_l1[3][key] + histories_100[1][key])
plt.ylim(ymin=0)

plt.legend(["No weights, 60 epochs", "No weights, 110 epochs", "Weights, 60 epochs", "Weights, 110 epochs"],loc='lower right')
#.legend(["Train, 50 epochs", "Train, 100 epochs", "Validation, 50 epochs", "Validation, 100 epochs" ])
#plt.legend(["Train", "Validation"])

#plt.margins(-0.49)  
#plt.axes().set_ylim(bottom=10)
#plt.title("Training MAE")
plt.ylabel("MAE")
plt.xlabel('Epoch')
#plt.yscale("log")
plt.savefig("training_mae_allanimals_secondHalfDecoder.png")
plt.show()


x = range(20)
plt.plot(x, histories[4][key][-20:])
plt.plot(x, histories_100[4][key][-20:])
plt.legend(['50 epochs', '100 epochs'], loc='upper right')
plt.show()



import numpy as np
import pandas as pd

mae_50 = [0.000342185, 0.000150708, 0.000206394, 0.00043281]
mae_100 = [0.000891973, 0.00035759, 0.000129428, 0.00026284]
networks = ["Test - No weights", "Test - Weights", "Train - No weights", "Train - weights"]

mae_50 = [0.00186723, 0.007828287, 
          0.00177989, 0.001063326, 
          0.001002867]#, 0.00010042, 0.000142527]
mae_100 = [0.001733721, 0.007959221, 
           0.001336948, 0.000808651, 
           0.000744527#, 0.001315406, 0.000142527
           ]

networks = ["Min CNN", "No layers", "Last layers", "All layers", "All layers delayed"]


N = len(networks)
ind = np.arange(N)  # the x locations for the groups
width = 0.27       # the width of the bars

fig = plt.figure()
ax = fig.add_subplot(111)


rects1 = ax.barh(ind, mae_50, width, color="cornflowerblue")
rects2 = ax.barh(ind+width, mae_100, width, color='orange')


ax.set_xlabel('MAE')
ax.invert_yaxis() 
ax.set_yticks(ind+width)
ax.set_yticklabels( networks )
ax.legend( (rects1[0], rects2[0]), ('50 epochs', '100 epochs') )

def autolabel(rects):
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*h, "",
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

#plt.savefig("tf_delayed_compareEpochs.png")
plt.show()

# plt.rcdefaults()
# fig, ax = plt.subplots()


# y_pos = np.arange(len(networks*2))

# ax.barh(y_pos[::2], mae_50, align='center')
# ax.barh(y_pos[1::2], mae_100, align='center')
# ax.set_yticks(y_pos)
# ax.set_yticklabels(networks)
# ax.invert_yaxis()  # labels read top-to-bottom
# ax.set_xlabel('Performance')
# ax.set_title('How fast do you want to go today?')

# plt.show()











    
