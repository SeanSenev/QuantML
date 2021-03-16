#!/usr/bin/env python
# coding: utf-8

# In[6]:


get_ipython().system('pip install yfinance')
get_ipython().system('pip install PyPortfolioOpt')
import pypfopt
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pypfopt import risk_models
from pypfopt import plotting
from pypfopt import EfficientFrontier
from pypfopt import DiscreteAllocation


# In[2]:


tickers = ["MSFT", "AMZN", "KO", "MA", "COST", 
           "LUV", "XOM", "PFE", "JPM", "UNH", 
           "ACN", "DIS", "GILD", "F", "TSLA"]


# 
# 

# In[4]:


ohlc = yf.download(tickers, period="max")


# In[7]:


prices = ohlc["Adj Close"].dropna(how="all")


# In[8]:


def covariance(prices):
    sample_cov = risk_models.sample_cov(prices, frequency=252)
    plotting.plot_covariance(sample_cov, plot_correlation=True)
    return sample_cov

def returns(prices):
    mu = expected_returns.capm_return(prices)
    mu.plot.barh(figsize=(10,6));
    return mu

def GMV_port(prices):
    S = covariance(prices)
    ef = EfficientFrontier(None, S, weight_bounds=(None, None))
    ef.min_volatility()
    weights = ef.clean_weights()
    pd.Series(weights).plot.barh();
    ef.portfolio_performance(verbose=True);
    return(weights)

def Max_Sharpe_port(prices):
    mu = returns(prices)
    S = covariance(prices)
    ef = EfficientFrontier(mu, S) 
    ef.max_sharpe()
    weights = ef.clean_weights()
    pd.Series(weights).plot.pie(figsize=(10,10));
    return weights

from pypfopt import objective_functions
risk = 0.15
def return_given_risk(prices, risk):
    mu = returns(prices)
    S = risk_models.sample_cov(prices)
    ef = EfficientFrontier(mu, S)
    ef.add_objective(objective_functions.L2_reg)  # gamme is the tuning parameter
    ef.efficient_risk(0.15)
    weights = ef.clean_weights()
    return weights


def minimize_risk(prices):
    mu = returns(prices)
    S = covariance(prices)
    ef = EfficientFrontier(mu, S, weight_bounds=(None, None))
    ef.add_objective(objective_functions.L2_reg)
    ef.efficient_return(target_return=0.07, market_neutral=True)
    weights = ef.clean_weights()
    ef.portfolio_performance(verbose=True);
    return weights


# In[12]:


get_ipython().system('pip install qiskit')


# In[16]:


get_ipython().run_line_magic('matplotlib', 'inline')
from qiskit.finance import QiskitFinanceError
from qiskit.finance.data_providers import *
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import datetime
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

from qiskit import Aer
from qiskit.circuit.library import TwoLocal
from qiskit.aqua import QuantumInstance
from qiskit.finance.applications.ising import portfolio
from qiskit.optimization.applications.ising.common import sample_most_likely
from qiskit.finance.data_providers import RandomDataProvider
from qiskit.aqua.algorithms import VQE, QAOA, NumPyMinimumEigensolver
from qiskit.aqua.components.optimizers import COBYLA
import numpy as np
import matplotlib.pyplot as plt
import datetime


# In[28]:


data = YahooDataProvider(
                 tickers = ["AEO", "ABBY", "AEP", "AAL"],
                 start=datetime.datetime(2018, 1, 1),
                 end=datetime.datetime(2018, 12, 31))
data.run()


# In[29]:


num_assets = 4

mu = data.get_period_return_mean_vector()
sigma = data.get_period_return_covariance_matrix()


# In[30]:


q = 0.5                   # set risk factor
budget = num_assets // 2  # set budget
penalty = num_assets      # set parameter to scale the budget penalty term

qubitOp, offset = portfolio.get_operator(mu, sigma, q, budget, penalty)


# In[31]:


def index_to_selection(i, num_assets):
    s = "{0:b}".format(i).rjust(num_assets)
    x = np.array([1 if s[i]=='1' else 0 for i in reversed(range(num_assets))])
    return x

def print_result(result):
    selection = sample_most_likely(result.eigenstate)
    value = portfolio.portfolio_value(selection, mu, sigma, q, budget, penalty)
    print('Optimal: selection {}, value {:.4f}'.format(selection, value))

    eigenvector = result.eigenstate if isinstance(result.eigenstate, np.ndarray) else result.eigenstate.to_matrix()
    probabilities = np.abs(eigenvector)**2
    i_sorted = reversed(np.argsort(probabilities))
    print('\n----------------- Full result ---------------------')
    print('selection\tvalue\t\tprobability')
    print('---------------------------------------------------')
    for i in i_sorted:
        x = index_to_selection(i, num_assets)
        value = portfolio.portfolio_value(x, mu, sigma, q, budget, penalty)
        probability = probabilities[i]
        print('%10s\t%.4f\t\t%.4f' %(x, value, probability))


# In[32]:


exact_eigensolver = NumPyMinimumEigensolver(qubitOp)
result = exact_eigensolver.run()

print_result(result)


# In[33]:


backend = Aer.get_backend('statevector_simulator')
seed = 50

cobyla = COBYLA()
cobyla.set_options(maxiter=500)
ry = TwoLocal(qubitOp.num_qubits, 'ry', 'cz', reps=3, entanglement='full')
vqe = VQE(qubitOp, ry, cobyla)
vqe.random_seed = seed

quantum_instance = QuantumInstance(backend=backend, seed_simulator=seed, seed_transpiler=seed)

result = vqe.run(quantum_instance)

print_result(result)


# In[34]:


backend = Aer.get_backend('statevector_simulator')
seed = 50

cobyla = COBYLA()
cobyla.set_options(maxiter=250)
qaoa = QAOA(qubitOp, cobyla, 3)

qaoa.random_seed = seed

quantum_instance = QuantumInstance(backend=backend, seed_simulator=seed, seed_transpiler=seed)

result = qaoa.run(quantum_instance)

print_result(result)


# In[ ]:




