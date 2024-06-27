import pandas as pd
from ortools.linear_solver import pywraplp

# Solver function

def solve_lp(df, total_target=1000, deviation=0):
    
    if total_target <= 0:
        raise ValueError("target must be a positive number")
    
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver("GLOP")

    # Create the variables s1, s2, ... sn
    x = {}
    for index, row in df.iterrows():
        x[index] = solver.NumVar(0, row['Weight'], index)

    # Objective function coefficients
    obj_coeff = df['Cost'] + df['Distance']

    # Create the objective function.
    objective = solver.Objective()
    for var_name, var in x.items():
        objective.SetCoefficient(var, obj_coeff[var_name])
    objective.SetMinimization()

    # Create a linear constraint.  n*T(1+e) <= Σ(Bi * Xi) <= n*T(1+e)
   
    ct1 = solver.Constraint(total_target - deviation, total_target + deviation, "ct1")
    for var_name, var in x.items():
        # print(df.loc[var_name, 'B'])
        ct1.SetCoefficient(var, df.loc[var_name, 'Biogas'])

    # Create a linear constraint Σ(xi(Fi-0.1)) <=0
    ct2 = solver.Constraint(-solver.infinity(), 0, "ct2")
    for var_name, var in x.items():
        ct2.SetCoefficient(var, df.loc[var_name, 'Fat'] - 0.1)

    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        return {
            'status': 'optimal',
            'target': total_target,
            'cost': objective.Value(),
            'solution': {var_name: var.solution_value() for var_name, var in x.items()},
        }
    else:
        return {'status': 'infeasible'}