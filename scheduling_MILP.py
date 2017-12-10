# -*- coding: utf-8 -*-

from gurobipy import *
import numpy as np

sizeI = 8
sizeJ = 9
sizeS = 4
sizeL = 3
TL = 16

C = np.array([7, 5, 5, 4, 4, 4, 4, 3])
SQ_tmp = np.array([[3, 2, 1, 0],
     [0, 2, 0, 3],
     [2, 2, 0, 1],
     [2, 1, 1, 0],
     [0, 1, 3, 0],
     [2, 0, 0, 2],
     [0, 2, 2, 0],
     [0, 2, 0, 1]])
RQ = np.array([[6, 7, 2, 1],
     [2, 4, 3, 1],
     [6, 7, 3, 2],
     [3, 5, 4, 1],
     [2, 2, 3, 4],
     [6, 4, 2, 3],
     [4, 2, 4, 1],
     [1, 3, 4, 5],
     [5, 3, 2, 5]])
OC = np.array([150, 150, 125, 145, 140, 150, 135, 145, 150])
T = np.array([5, 4, 3, 5, 3, 5, 4, 2, 3])

SQ = np.zeros((sizeI, sizeS, sizeL))
for i in range(sizeI):
    for s in range(sizeS):
        for l in range(sizeL):
            if l+1 <= SQ_tmp[i,s] : SQ[i,s,l] = 1
                            
                            
Pred = np.zeros((sizeJ, sizeJ))
Pred[0,3] = Pred[1,2] = Pred[2,3] = Pred[4,5] = Pred[2,6] = Pred[5,6] = Pred[2,8] = Pred[1,5] = 1


    
# Model
m = Model("workforce")

# Variables
x = m.addVars(sizeI, sizeJ, vtype=GRB.BINARY, name="x")
y = m.addVars(sizeJ, vtype=GRB.BINARY, name="y")
z = m.addVars(sizeJ, sizeJ, vtype=GRB.BINARY, name="z")
p = m.addVars(sizeJ, sizeJ, vtype=GRB.BINARY, name="p")
ct = m.addVars(sizeJ, vtype=GRB.INTEGER, name="ct")

# Constraint
m.addConstrs((x[i,j]+x[i,jj]<=2-z[j,jj] for i in range(sizeI) for j in range(sizeJ) for jj in range(sizeJ) if j!=jj), "c1")
m.addConstrs((sum((x[i,j]*SQ[i,s,l]) for i in range(sizeI) for l in range(sizeL)) >= RQ[j,s]*(1-y[j]) for j in range(sizeJ) for s in range(sizeS)), "c2")
m.addConstrs((ct[j] <= TL for j in range(sizeJ)), "c3")
m.addConstrs((Pred[j,jj]*ct[j]<=ct[jj]-T[jj] for j in range(sizeJ) for jj in range(sizeJ)), "c4")
m.addConstrs((0<=(ct[jj]-ct[j])+2*TL*p[j,jj] for j in range(sizeJ) for jj in range(sizeJ)), "c5")
m.addConstrs((0<=(ct[jj]-ct[j])-(1-z[j,jj])*T[jj]+2*TL*p[j,jj] for j in range(sizeJ) for jj in range(sizeJ)), "c6")
m.addConstrs(((ct[jj]-ct[j]+0.5)<=2*TL*(1-p[j,jj]) for j in range(sizeJ) for jj in range(sizeJ)), "c7")


# Objective
m.setObjective((sum((C[i]*x[i,j]*T[j]) for i in range(sizeI) for j in range(sizeJ))+(sum((OC[j]*y[j]) for j in range(sizeJ)))), GRB.MINIMIZE)


m.optimize()