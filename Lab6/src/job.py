from __future__ import print_function
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model
from datareader import get_data
import numpy as np

def MinimalJobshopSat():
    print("Minimal JOB SHOP Problem")
    # Create the model.
    model = cp_model.CpModel()

MinimalJobshopSat();
