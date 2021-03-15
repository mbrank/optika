DEFAULT_SOLVER = {'name': 'Solver_1',
                  'Equation' : 'Heat Equation',
                  'Procedure' : '"HeatSolve" "HeatSolver"',
                  'Variable 1' : 'Temperature',
                  'Exec Solver' : 'Always',
                  'Stabilize' : 'True',
                  'Bubbles' : 'False',
                  'Lumped Mass Matrix' : 'False',
                  'Optimize Bandwidth' : 'True',
                  'Steady State Convergence Tolerance' : '1.0e-10',
                  'Nonlinear System Convergence Tolerance' : '1.0e-20',
                  'Nonlinear System Max Iterations' : '20',
                  'Nonlinear System Newton After Iterations' : '3',
                  'Nonlinear System Newton After Tolerance' : '1.0e-20',
                  'Nonlinear System Relaxation Factor' : '0.2',
                  'Linear System Solver' : 'Iterative',
                  'Linear System Iterative Method' : 'BiCGstab',
                  'Linear System Max Iterations' : '500',
                  'Linear System Convergence Tolerance' : '1.0e-20',
                  'BiCGstabl polynomial degree' : '1',
                  'Linear System Preconditioning' : 'Diagonal',
                  'Linear System ILUT Tolerance' : '1.0e-3',
                  'Linear System Abort Not Converged' : 'False',
                  'Linear System Residual Output' : '1',
                  'Linear System Precondition Recompute' : '1',
                  'Linear System Solver' : 'Direct',
                  'Linear System Direct Method' : 'Banded'}

DEFAULT_GENERAL_SETTINGS = {'Header':{'Mesh DB' : "." ".",
                                      'Include Path' : "",
                                      'Results Directory':"" },
                            'Simulation':
                            {'Max Output Level' : '5',
                             'Coordinate System' : 'Cartesian',
                             'Coordinate Mapping(3)' : '1 2 3',
                             'Simulation Type' : 'Steady state',
                             'Steady State Max Iterations' : '1',
                             'Output Intervals' : '1',
                             'Timestepping Method' : 'BDF',
                             'BDF Order' : '1',
                             'Solver Input File' : 'case.sif',
                             'Post File' : 'case.vtu'},
                            'Constants':
                            {'Gravity(4)' : '0 -1 0 9.82',
                             'Stefan Boltzmann' : '5.67e-08',
                             'Permittivity of Vacuum' : '8.8542e-12',
                             'Boltzmann Constant' : '1.3807e-23',
                             'Unit Charge' : '1.602e-19'}}
