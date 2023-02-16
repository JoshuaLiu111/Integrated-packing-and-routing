import pyomo.environ as pyo

def define_model() -> pyo.AbstractModel:
    
    model = pyo.AbstractModel()

    # Set of boxes
    model.I = pyo.Set()
    # Set of pallets
    model.J = pyo.Set()
    # Set of trucks
    model.K = pyo.Set()
    # Set of destinations
    model.DP = pyo.Set()

    # depot node
    model.d0 = pyo.Param(within=model.DP)
    # volume of box
    model.v = pyo.Param(model.I)
    # capacity of pallet
    model.V = pyo.Param(model.J)
    # fix cost of pallet
    model.c = pyo.Param(model.J)
    # capacity of truck
    model.T = pyo.Param(model.K)
    # fix cost of truck
    model.C = pyo.Param(model.K)
    # boxes' destinations
    model.g0 = pyo.Param(model.I*model.DP)
    # travel cost
    model.cp = pyo.Param(model.DP*model.DP)    

    # epsilon - a small value
    model.epsilon = pyo.Param()
    # Upsilon - a large value
    model.Upsilon = pyo.Param()

    # size of box
    model.l = pyo.Param(model.I)
    model.w = pyo.Param(model.I)
    model.h = pyo.Param(model.I)
    # size of pallet
    model.L = pyo.Param(model.J)
    model.W = pyo.Param(model.J)
    model.H = pyo.Param(model.J)


    # if box i is in pallet j
    model.p0 = pyo.Var(model.I*model.J, within=pyo.Boolean)
    # if pallet j is used
    model.u0 = pyo.Var(model.J, within=pyo.Boolean)
    # if pallet j is calling at destination d
    model.g1 = pyo.Var(model.J*model.DP, within=pyo.Boolean)
    # if pallet j is in truck k
    model.p1 = pyo.Var(model.J*model.K, within=pyo.Boolean)
    # if truck k is used
    model.u1 = pyo.Var(model.K, within=pyo.Boolean)
    # if pallet j in k is delivered to d
    model.eta1 = pyo.Var(model.J*model.K*model.DP, within=pyo.Boolean)
    # if truck k is calling at destination d
    model.g2 = pyo.Var(model.K*model.DP, within=pyo.Boolean)
    # if truck k uses the route d to d'
    model.gs = pyo.Var(model.K*model.DP*model.DP, within=pyo.Boolean)
    # MTZ auxiliary variable at d for truck k
    model.e = pyo.Var(model.K*model.DP, within=pyo.PositiveIntegers)

    # location of box
    model.x = pyo.Var(model.I, within=pyo.NonNegativeIntegers)
    model.y = pyo.Var(model.I, within=pyo.NonNegativeIntegers)
    model.z = pyo.Var(model.I, within=pyo.NonNegativeIntegers)
        
    # if box i is on the right of box i'
    model.xp = pyo.Var(model.I*model.I, within=pyo.Boolean)
    # if box i is behind box i'
    model.yp = pyo.Var(model.I*model.I, within=pyo.Boolean)
    # if box i is above box i'
    model.zp = pyo.Var(model.I*model.I, within=pyo.Boolean)

    # Minimize the summation of fix cost and variable cost
    def total_cost(model):
        return (sum(model.c[j]*model.u0[j] for j in model.J) + sum(model.C[k]*model.u1[k] for k in model.K) 
                + sum(model.cp[d,dp]*model.gs[k,d,dp] for k in model.K for d in model.DP for dp in model.DP))
    model.total = pyo.Objective(rule=total_cost, sense=pyo.minimize)

    # The maximum capacity of each pallet j cannot be exceeded:
    def cap_0(model, j):
        return sum(model.v[i]*model.p0[i,j] for i in model.I) <= model.V[j]*model.u0[j]
    model.capacity_0 = pyo.Constraint(model.J, rule=cap_0)

    # Each box is allocated to exactly one pallet:
    def assign_0(model, i):
        return sum(model.p0[i,j] for j in model.J) == 1
    model.assignment_0 = pyo.Constraint(model.I, rule=assign_0)

    # The maximum capacity of each truck k cannot be exceeded:
    def cap_1(model, k):
        return sum(model.V[j]*model.p1[j,k] for j in model.J) <= model.T[k]*model.u1[k]
    model.capacity_1 = pyo.Constraint(model.K, rule=cap_1)

    # Each pallet in use is allocated to exactly one truck:
    def assign_1(model, j):
        return sum(model.p1[j,k] for k in model.K) == model.u0[j]
    model.assignment_1 = pyo.Constraint(model.J, rule=assign_1)

    # Each pallet is calling at a destination if it contains boxes go to that destination:
    def des_1(model, j, d):
        return sum(model.p0[i,j]*model.g0[i,d] for i in model.I) <= model.g1[j,d]*model.Upsilon
    model.destination_1 = pyo.Constraint(model.J, model.DP, rule=des_1)

    # Adding an auxiliary variable eta1 that takes value 1 if p1 and g1 are both 1:
    def des_2(model, j, k, d):
        return 2*model.eta1[j,k,d] <= model.p1[j,k] + model.g1[j,d]
    model.destination_2 = pyo.Constraint(model.J, model.K, model.DP, rule=des_2)
    def des_2p(model, j, k, d):
        return model.p1[j,k] + model.g1[j,d] <= model.eta1[j,k,d] + 1
    model.destination_2p = pyo.Constraint(model.J, model.K, model.DP, rule=des_2p)

    # Each truck goes to a destination if it contains pallets go to that destination:
    def des_3(model, k, d):
        return sum(model.eta1[j,k,d] for j in model.J) <= model.g2[k,d]*model.Upsilon
    model.destination_3 = pyo.Constraint(model.K, model.DP, rule=des_3)

    # The route d to dp can only be used by truck k if the truck is calling at both destination d and destination dp:
    def routeallow_1(model, k, d, dp):
        if d == pyo.value(model.d0) or dp == pyo.value(model.d0):
            return pyo.Constraint.Skip
        return 2*model.gs[k,d,dp] <= model.g2[k,d] + model.g2[k,dp]
    model.routeallow_1 = pyo.Constraint(model.K, model.DP, model.DP, rule=routeallow_1)

    # The route d to d0 can only be used by truck k if the truck is calling at destination d:
    def routeallow_2(model, k, d, dp):
        if dp != pyo.value(model.d0):
            return pyo.Constraint.Skip
        return model.gs[k,d,dp] + model.gs[k,dp,d] <= 2*model.g2[k,d]
    model.routeallow_2 = pyo.Constraint(model.K, model.DP, model.DP, rule=routeallow_2)

    # Each destination is entered once by each truck if and only if the truck is calling at that destination:
    def routeassign_1(model, k, dp):
        return sum(model.gs[k,d,dp] for d in model.DP if d!=dp) == model.g2[k,dp]
    model.routeassignment_1 = pyo.Constraint(model.K, model.DP, rule=routeassign_1)

    # Each destination is left by same number of times as it is entered:
    def routeassign_2(model, k, d):
        return sum(model.gs[k,d,dp] for dp in model.DP if d!=dp) == model.g2[k,d]
    model.routeassignment_2 = pyo.Constraint(model.K, model.DP, rule=routeassign_2)

    # MTZ subtour elimination constraints:
    def detour_1(model, k, d, dp):
        if d == pyo.value(model.d0) or dp == pyo.value(model.d0):
            return pyo.Constraint.Skip
        return model.e[k,d] - model.e[k,dp] + model.Upsilon*model.gs[k,d,dp] <= model.Upsilon - 1
    model.detour_1 = pyo.Constraint(model.K, model.DP, model.DP, rule=detour_1)
    def detour_2(model, k, d):
        return 1 <= model.e[k,d]
    model.detour_2 = pyo.Constraint(model.K, model.DP, rule=detour_2)
    def detour_2p(model, k, d):
        return model.e[k,d] <= model.Upsilon
    model.detour_2p = pyo.Constraint(model.K, model.DP, rule=detour_2p)

    # boxes do not exceed their pallet size:
    def size_x(model, i):
        return model.x[i] + model.l[i] <= sum(model.L[j]*model.p0[i,j] for j in model.J)
    model.size_x = pyo.Constraint(model.I, rule=size_x)
    def size_y(model, i):
        return model.y[i] + model.w[i] <= sum(model.W[j]*model.p0[i,j] for j in model.J)
    model.size_y = pyo.Constraint(model.I, rule=size_y)
    def size_z(model, i):
        return model.z[i] + model.h[i] <= sum(model.H[j]*model.p0[i,j] for j in model.J)
    model.size_z = pyo.Constraint(model.I, rule=size_z)

    # there is no overlap:
    def pos(model, i, ip, j):
        if i == ip:
            return pyo.Constraint.Skip
        return (model.xp[i,ip]+model.xp[ip,i]+model.yp[i,ip]+model.yp[ip,i]+model.zp[i,ip]+model.zp[ip,i] >=
               model.p0[i,j]+model.p0[ip,j]-1)
    model.pos = pyo.Constraint(model.I, model.I, model.J, rule=pos)
    def pos_x(model, i, ip):
        return model.x[ip] + model.l[ip] <= model.x[i] + (1-model.xp[i,ip])*model.Upsilon
    model.pos_x = pyo.Constraint(model.I, model.I, rule=pos_x)
    def pos_xp(model, i, ip):
        return model.x[i] + model.epsilon <= model.x[ip] + model.l[ip] + model.xp[i,ip]*model.Upsilon
    model.pos_xp = pyo.Constraint(model.I, model.I, rule=pos_xp)
    def pos_y(model, i, ip):
        return model.y[ip] + model.w[ip] <= model.y[i] + (1-model.yp[i,ip])*model.Upsilon
    model.pos_y = pyo.Constraint(model.I, model.I, rule=pos_y)
    def pos_yp(model, i, ip):
        return model.y[i] + model.epsilon <= model.y[ip] + model.w[ip] + model.yp[i,ip]*model.Upsilon
    model.pos_yp = pyo.Constraint(model.I, model.I, rule=pos_yp)
    def pos_z(model, i, ip):
        return model.z[ip] + model.h[ip] <= model.z[i] + (1-model.zp[i,ip])*model.Upsilon
    model.pos_z = pyo.Constraint(model.I, model.I, rule=pos_z)

    return model