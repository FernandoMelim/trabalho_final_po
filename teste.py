from re import A
import gurobipy as gp

m = gp.Model("teste")

x = m.addVar(vtype=gp.GRB.BINARY, name="x")
y = m.addVar(vtype=gp.GRB.BINARY, name="y")
z = m.addVar(vtype=gp.GRB.BINARY, name="z")
m.update()

a = x + y + 2*z
m.setObjective(a, gp.GRB.MAXIMIZE)
print("a ---------------------------------")
print(a)

m.addConstr(x + 2*y + 3*z <= 4, name="c0")
m.addConstr(x + y >= 1, name="c1")

m.optimize()

m.printAttr('X')
