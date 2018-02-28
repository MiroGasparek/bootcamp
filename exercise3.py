# 27 February 2018 Miroslav Gasparek
# Python bootcamp tutorials: Exercise 3

# First import modules
import numpy as np
import matplotlib.pyplot as plt
# Import ODE module out of scipy
from scipy.integrate import odeint
# Some pretty Seaborn settings
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)
# Exercise 3.2

# a)
# Load in the data
data_WTlac = np.loadtxt('data/wt_lac.csv', delimiter=',', skiprows=3)
data_Q18Alac = np.loadtxt('data/q18a_lac.csv', delimiter=',', skiprows=3)
data_Q18Mlac = np.loadtxt('data/q18m_lac.csv', delimiter=',', skiprows=3)

# b)
# Plot each of the data sets
iptg_WTlac = data_WTlac[:,0]
fold_WTlac = data_WTlac[:,1]

iptg_Q18Alac = data_Q18Alac[:,0]
fold_Q18Alac = data_Q18Alac[:,1]

iptg_Q18Mlac = data_Q18Mlac[:,0]
fold_Q18Mlac = data_Q18Mlac[:,1]

# Plot the data
fig1 = plt.figure(1)
plt.plot(iptg_WTlac,fold_WTlac, marker='.', markersize='10',linestyle='none', color='green')
plt.plot(iptg_Q18Alac,fold_Q18Alac, marker='.', markersize='10',linestyle='none', color='blue')
plt.plot(iptg_Q18Mlac,fold_Q18Mlac, marker='.', markersize='10',linestyle='none', color='red')
plt.xscale('log')
plt.xlabel('[IPTG] (mM)')
plt.ylabel('repression fold change')
plt.margins(0.02)

# c)
def fold_change(c, RK, KdA=0.017, KdI=0.002, Kswitch=5.8):
    """ Function computes the theoretical fold change in repression."""
    # Compute fold change
    fold_change = (1 + RK*((1+c/KdA))**2/((1+c/KdA)**2 + Kswitch*(1+c/KdI)**2))**(-1)
    # Return concentration array and fold change array
    return fold_change

# d)
# 1. Create densely spaced points on the log axis
c = np.logspace(-5.0,3.0, num=50)
# 2. Compute theoretical fold change
fold_WTlac_the = fold_change(c,141.5)
fold_Q18Alac_the = fold_change(c,16.56)
fold_Q18Mlac_the = fold_change(c,1332)
# 3. Plot the smooth curves on the same plot with the data.
plt.plot(c,fold_WTlac_the, color='green')
plt.plot(c,fold_Q18Alac_the, color='blue')
plt.plot(c,fold_Q18Mlac_the, color='red')
plt.legend(('WT_lac','Q18A_lac','Q18M_lac','predicted WT_lac','predicted Q18A_lac','predicted Q18M_lac'),loc='upper left')
fig1.show()

# e)
# 1. Write a function bohr_parameter
def bohr_parameter(c, RK, KdA=0.017, KdI=0.002, Kswitch=5.8):
    """ The function that computes the Bohr parameter."""
    # Compute Bohr parameter
    Fc = - np.log(RK) - np.log((1+c/KdA)**2/((1+c/KdA)**2+Kswitch*(1+c/KdI)**2))
    return Fc

# 2. Write a function that gives the fold change as a function of the Bohr parameter
def fold_change_bohr(bohr_parameter):
    """ The function that computes fold change as a function of the Bohr parameter."""
    # Compute fold change
    fold_change = 1/(1+np.exp(-bohr_parameter))
    # Return fold change
    return fold_change

# 3. Generate the values of the Bohr parameter ranging from -6 to 6
# 4. Compute the theoretical fold change as a function of the Bohr parameter
BP_vals = np.linspace(-6.0,6.0,num=200)
fc_vals = fold_change_bohr(BP_vals)
# Plot the Bohr parameter values
fig2 = plt.figure(2)
plt.plot(BP_vals,fc_vals, color='gray')
plt.xlabel('Bohr parameter')
plt.ylabel('Repression fold change')

# f)
# 1. Convert the IPTG conc. into Bohr parameter
bohr_WTlac = bohr_parameter(iptg_WTlac,141.5)
bohr_Q18Alac = bohr_parameter(iptg_Q18Alac,16.56)
bohr_Q18Mlac = bohr_parameter(iptg_Q18Mlac,1332)
# 2. Plot the experimental fold change
fc_WTlac = fold_change_bohr(bohr_WTlac)
fc_Q18Alac = fold_change_bohr(bohr_Q18Alac)
fc_Q18Mlac = fold_change_bohr(bohr_Q18Mlac)

plt.plot(bohr_WTlac,fc_WTlac, marker='.', markersize='10', linestyle='none', color='green')
plt.plot(bohr_Q18Alac,fc_Q18Alac, marker='.', markersize='10', linestyle='none', color='blue')
plt.plot(bohr_Q18Mlac,fc_Q18Mlac, marker='.', markersize='10', linestyle='none', color='red')
plt.legend(('Theoretical curve','WTlac','Q18Alac','Q18Mlac'),loc='upper left')
plt.margins(0.02)
fig2.show()


# Exercise 3.3: Bacterial growth-Euler model

# Specify parameter
k = 1
# Specify incremental time step
delta_t = 0.01
# Make an array of time points, evenly spaced up to 10
t = np.arange(0,10,delta_t)
# Make an array to store the number of bacteria
n = np.empty_like(t)
# Set the initial number of bacteria
n[0] = 1
# Write a for loop to keep updating n as time goes on
for i in range(1, len(t)):
    n[i] = n[i-1] + delta_t*k*n[i-1]
# Plot the result
fig3 = plt.figure(3)
plt.plot(t, n)
plt.margins(0.02)
plt.xlabel('time')
plt.ylabel('number of bacteria')
fig3.show()

# Solution to Lotka-Volterra equations
# Specify parameters
alpha = 1
beta = 0.2
delta = 0.3
gamma = 0.8
delta_t = 0.001
t = np.arange(0, 60, delta_t)

# Set the empty arrays
r = np.empty_like(t)
f = np.empty_like(t)
# Specify the initial conditions
r[0] = 10
f[0] = 1

# Write a for loop to keep updating r and f as time goes on
for i in range(1, len(t)):
    r[i] = r[i-1] + alpha*r[i-1]*delta_t - beta*f[i-1]*r[i-1]*delta_t
    f[i] = f[i-1] + delta*f[i-1]*r[i-1]*delta_t - gamma*f[i-1]*delta_t

# Plot the results
fig4 = plt.figure(4)
plt.plot(t,r, color='red')
plt.plot(t,f, color='blue')
plt.xlabel('Time')
plt.ylabel('Populations')
plt.legend(('Rabbits','Foxes'), loc='upper left')
plt.margins(0.02)
fig4.show()

# b)
# Define the functions
def LotkaVolterra(y, time, alpha, beta, gamma, delta):
    """ Definition of the system of ODE for the Lotka-Volterra system."""
    r, f = y
    dydt = [alpha*r - beta*f*r, delta*f*r - gamma*f]
    return dydt

# Define initial conditions
y0 = [10, 1]
# Define solution time
time = np.linspace(0, 60, 501)
# Solve the ode
sol = odeint(LotkaVolterra, y0, time, args=(alpha, beta, gamma, delta))
# Plot the solution
fig5 = plt.figure(5)
plt.plot(time,sol[:,0],'r', label='rabbits(t)')
plt.plot(time,sol[:,1],'b',label='foxes(t)')
plt.legend(loc='best')
plt.xlabel('Time')
plt.ylabel('Popoulations')
plt.grid()
plt.margins(0.02)
fig5.show()
