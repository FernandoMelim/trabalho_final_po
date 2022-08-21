from gurobipy import gurobipy
from decimal import *

file = open('input.csv')
lines = file.readlines()
file.close()

endlist = []

# formatando
for i in lines:
    endlist.append(i.replace("\n", "").replace(',', '.'))

# criando modelo
model = gurobipy.Model('doceria')

# declarando variaveis
vars = []
for i in endlist[0].split(';'):
    vars.append(model.addVar(vtype=gurobipy.GRB.CONTINUOUS, name=i))

# model.update()

# definindo custos
costs = []
for i in endlist[1].split(';'):
    costs.append(i)

# montando função objetivo
expression = ''
for i in range(0, len(endlist[0].split(';'))):
    expression += float(costs[i]) * vars[i]

model.setObjective(expression, gurobipy.GRB.MINIMIZE)

# montando restrições
k = 1
for i in range(2, len(endlist)):

    consts = []
    endlistSplited = endlist[i].split(';')

    for j in range(0, len(endlistSplited) - 2):
        consts.append(endlistSplited[j])

    expression = ''
    for j in range(0, len(consts)):
        expression += consts[j] * vars[j]

    if (endlistSplited[-2] == '='):
        expression = expression == float(endlistSplited[-1])
    elif (endlistSplited[-2] == '<='):
        expression = expression <= float(endlistSplited[-1])
    elif (endlistSplited[-2] == '>='):
        expression = expression >= float(endlistSplited[-1])
    elif (endlistSplited[-2] == '<'):
        expression = expression < float(endlistSplited[-1])
    elif (endlistSplited[-2] == '>'):
        expression = expression > float(endlistSplited[-1])

    model.addConstr(expression, "r" + str(k))
    k += 1

# otimizando
model.optimize()

results = model.getAttr('X')

# escrevendo resultado em arquivo
f = open("output.txt", "w")

f.write("Custo total minimizado: R$ " +
        str(model.ObjVal).replace('.', ',') + '\n')

for i in range(0, len(vars)):
    f.write(str(vars[i])
            .replace('<gurobi.Var ', '')
            .replace(' (value ', ' - ')
            .replace(')>', '')
            .replace('.', ',') + '\n')

f.close()
