### REALM run 

evaluate = realm.Evaluation()
evaluate.add_evaluator(code_name='openmc',fitness_map={0:'PF', 1:'keff'})
 # could create a function with both openmc and moltres outputs 
evalOpenMC = evaluate.eval_fn_generator()

# DEAP toolbox setup 
creator.create("FuelMin", base.Fitness, weights=(-1.0,))
creator.create("Ind", list, fitness=creator.FuelMin, keff=1.0)
toolbox = base.Toolbox()
toolbox.register('pf',random.uniform,0.005,0.1)
toolbox.register('poly',random.uniform,-1,1)
toolbox.register('individual',f_cycle)
toolbox.register('population', tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evalOpenMC)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutPolynomialBounded, eta=0.5, 
                 low=[0.005,-1,-1,-1,-1], up=[0.1,1,1,1,1], indpb=0.5)
toolbox.register("select", tools.selBest, k=10, fit_attr='fitness')

constraints = Constraints()
constraints.add_constraint(fitness_index=1, operator_type=operator.gt, value=1.0)

model = realm.GenerateReactor(deap_toolbox=toolbox, constraint_obj=constraints)
model.generate() 