#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
import glob
import math
import numpy as np
from matplotlib.widgets import Slider
import mpld3
from mpld3 import plugins

#Postprocessing für output-Typ "OneTimestepOneFile"

#Einlesen der Input-Files, später: Eingabe über input

output_files = sorted(glob.glob("/home/jonas/Dokumente/WHK/Marzipan/Quellcode/pyMANGA/test/testoutputs/*.csv"))

#Auslesen der Spalten-Namen, evt. wichtig für später siehe unten [*]

data=pd.read_csv(output_files[0])

colNames = []
for i in range(len(data.columns)):
    colNames.append(data.columns[i])


bm=[]
bm_sum=[]
x=[]
y=[]
delta_bm=[]
ts = []
k=0

#Einlesen der Werte für die Biomasse und x- und y-Koordinate
#Werte werden in einer Liste gespeichert, in der pro Zeitschritt eine weitere
#Liste pro Eintrag die Informationen für einen Baum enthält
#Biomasse definiert über Stammvolumen, evt. später miteinbezug des Kronenradius 
#(Abhängkeit sowieso schon gegeben?)
#Später: Werte werden über festgelegte Spalten-Indizes eingelesen. Evt. Besser:
#Suche nach Schlagwort in Spalten-Namen und danach Bestimmung des Spalten-Indizes,
#Frage: Variiert Anordnung mit Anordnung der output-Variablen im xml-Steurfile? 

for files in output_files:
    data = pd.read_csv(files)
    print(data)
    ts.append(data.values[:,:])
    bm.append([])
    x.append([])
    y.append([])
    i=0
    for n_rows in range(np.shape(ts[k])[0]):
        bm[k].append(float(((ts[k][i,4:5])**2)*math.pi*(ts[k][i,5:6])))
        x[k].append(float(ts[k][i,2:3]))
        y[k].append(float(ts[k][i,3:4]))
        i=i+1
    bm_sum.append(sum(bm[k]))
    delta_bm.append(bm_sum[k]-bm_sum[k-1])
    k=k+1

##############################################################################

#Visualisation of developing of biomass

fig, ax = plt.subplots()

ax.set(xlabel='timestep [n]',
       title='dynamic development of biomass')

ax.plot(bm_sum,color='blue')
ax.tick_params(axis='y', labelcolor='blue')
ax.set_ylabel('sum biomass [m²]', color='blue')

ax_delta = ax.twinx()
ax_delta.plot(delta_bm,color='green')
ax_delta.tick_params(axis='y', labelcolor='green')
ax_delta.set_ylabel('delta biomass [m²]', color='green')


ax.grid()

fig.tight_layout()

plt.show()




html_str = mpld3.fig_to_html(fig)
Html_file= open("index.html","w")
Html_file.write(html_str)
Html_file.close()

##############################################################################
            
#Visulisation of trees

fig, ax = plt.subplots()
ax.set(xlabel='x',
       title='existing trees in respective time step')
ax.set_ylabel('y')

plt.subplots_adjust(bottom=0.25)
f0 = 0
delta_f = 1
#s = a0 * np.sin(2 * np.pi * f0 * t)
#l, = plt.plot(t, s, lw=2)
for i in range(len(x[0])):
    ax.scatter(x[0][i],y[0][i],s=4000000*bm[0][i],c='green')
ax.margins(x=0)

axcolor = 'blue'
axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)

ts_val = Slider(axfreq, 'Timestep', 0, len(x), valinit=f0, valstep=delta_f)


def update(val):
    ts = int(ts_val.val)
    ax.cla()
    ax.set(xlabel='x',
       title='existing trees in respective time step')
    ax.set_ylabel('y')
    for i in range(len(x[ts])):
        ax.scatter(x[ts][i],y[ts][i],s=4000000*bm[ts][i],c='green')
    fig.canvas.draw_idle()

ts_val.on_changed(update)

plt.show()

#_____________________________________________________________________________


#Backup:

#for ets in range(len(ts)):
#    for k in range(len(arrayzeilen))
#    bm.append(((ts[i][i,5:6].values)**2)*math.pi*(ts[i][i,5:6].values))
    
#y=ts[1][:,1:2]


#for files in output_files:
#    data = pd.read_csv(files)
#    ts.append(data.values[:,0:1].tolist())
#    v.append([]) 
#    
#    for k in range(len(ts[i])):        
#        v[i].append(data['tree'].values.tolist()[i])
#        t[i].append(data['	 time'].values.tolist()[i])
#        x[i].append(data['	 x'].values.tolist()[i])
#        y[i].append(data['	 y'].values.tolist()[i])
#        r_stem[i].append(data['	r_stem'].values.tolist()[i])
#        h_stem[i].append(data['	h_stem'].values.tolist()[i])
#        r_crown[i].append(data['	k_geom'].values.tolist()[i])

#    i=i+1
    
#v_rc=[]
#t_rc=[]
#x_rc=[]
#y_rc=[]
#r_stem_rc=[]
#h_stem_rc=[]
#r_crown_rc=[]

#v_ic=[]
#t_ic=[]
#x_ic=[]
#y_ic=[]
#r_stem_ic=[]
#h_stem_ic=[]
#r_crown_ic=[]

#ts = []
#i=0
    
#    for k in range(len(ts[i])):
#        q=1
#        q=str[ts[i][k]].find("Recruiting")
#        if q is not -1:            
#            v_rc.append(data['tree'].values.tolist()[i])
#            t_rc.append(data['	 time'].values.tolist()[i])
#            x_rc.append(data['	 x'].values.tolist()[i])
#            y_rc.append(data['	 y'].values.tolist()[i])
#            r_stem_rc.append(data['	r_stem'].values.tolist()[i])
#            h_stem_rc.append(data['	h_stem'].values.tolist()[i])
#            r_crown_rc.append(data['	k_geom'].values.tolist()[i])
#        else:
#            v_ic.append(data['tree'].values.tolist()[i])
#            t_ic.append(data['	 time'].values.tolist()[i])
#            x_ic.append(data['	 x'].values.tolist()[i])
#            y_ic.append(data['	 y'].values.tolist()[i])
#            r_stem_ic.append(data['	r_stem'].values.tolist()[i])
#            h_stem_ic.append(data['	h_stem'].values.tolist()[i])
#            r_crown_ic.append(data['	k_geom'].values.tolist()[i])
#    i=i+1
            



#k=0
#ts_rc = [[] for i in range(len(t_rc)) ]       
#for i in range(1,len(v_rc)):
#    ts_rc[k].append(r_stem_rc[i-1])
#    if not t_rc[i] == t_rc[i-1]:
#        k=k+1
#        ts_rc[k].append(r_stem_rc[i+1])

        

#p_ic=[]
        
#for i in range(len(t_ic)):
#        if timestep in t_ic[i]:
#            p_ic.append(i)
            
#########ic_p = [i for i, o in enumerate(v) if o == 'Recruiting']
#########rc_p = [i for i, o in enumerate(v) if o == 'Initial']

#def. biomasse: r_stem**2*pi*h_stem

#fig, axs = plt.subplots(1,2)

#for i in range(len(p_ic)):
#    axs[0].scatter(x_ic[p_ic[i]],y_ic[p_ic[i]],s=200*r_ic[p_ic[i]],c='brown')
    
#for i in range(len(p_ic)):
#    axs[1].scatter(x_rc[p_rc[i]],y_ic[p_rc[i]],s=200*r_rc[p_rc[i]],c='green')
    

#plt.show()

#for i in range(len(x_ic)):
#    plt.scatter(x_ic[i],y_ic[i],s=200*r_ic[i],c='brown')
    
#for i in range(len(x_rc)):
#    plt.scatter(x_rc[i],y_ic[i],s=200*r_rc[i],c='green')

#data=pd.read_csv()

#data=pd.read_csv(output_files)

           
 



#fig, ax = plt.subplots()
#ax.scatter(x, y, s, c, marker=verts)


# Fixing random state for reproducibility

#colNames = []
#for i in range(len(data.columns)):
#    colNames.append(data.columns[i])


#x=data['	 x '].values.tolist()
#y=data['	 y '].values.tolist()
#r=data['	r_crown'].values.tolist()

#plt.scatter(x[0],y[0],s=200*r[0],c='brown')

#plt.show()

#w=range(len(x))
#
#for i in range(len(x)):
#    print(i)
#    coords.append([x(i),y(i)])
#    
#print(coords)
#
#colValues = np.array(data1)
#x = colValues[:,1]
#y = colValues[:,2]

#plt.show()
