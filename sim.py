### CONFIGURATION ###
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
import get_data
from scipy.optimize import minimize


### SIMULATION ###
def heaviside(t):
    if t > 0:
        return 1

    return 0

def simulate(
    growth_coeff,               # Starting a for a(t)
    death_coeff,
    alpha,                      # Exponent coefficient
    t_decay,                    # Is supposed to determine postponement of growth
    eta,                        # Used to stifle YFP increase
    mu,                         # Stretches the YFP axis, not really used right now
    time_grid,                  # Time array that holds the steta of the simulation
    time_step,                  # Infinitesimal step in time
    initial_bacteria_condition, # First assumed value for bacteria (od)
    initial_yfp_condition       # First assumed value for YFP
    # t_decay_2=100,            # Is supposed to determine postponement of growth
    # alpha_2=0                 # Exponent coefficient
    ):
    '''
    Does the simulation according to euler method with these equations:
        dB/dt =a(t)*B
        a(t) = a(0)(H(t_decay - t) +  exp(-alpha(t-t_decay)) * H(t - t_decay))
        dF/dt = mu(dB/dt) - eta*F
    And using the method from here https://pythonnumericalmethods.berkeley.edu/notebooks/chapter22.03-The-Euler-Method.html
    '''
    a = lambda t: ( growth_coeff * (heaviside(t_decay - t) + heaviside(t - t_decay)*np.exp(-alpha*(t - t_decay))) - death_coeff)
    f = lambda t, B: a(t)*B #dB/dt
    g = lambda t, B, Y: mu*f(t,B) - eta*Y #dY/dt

    B = np.zeros(len(time_grid)) # B for Bacteria
    B[0] = initial_bacteria_condition
    Y = np.zeros(len(time_grid))
    Y[0] = initial_yfp_condition

    for i in range(0, len(time_grid) - 1):
        B[i + 1] = B[i] + time_step*f(time_grid[i], B[i])
        Y[i + 1] = Y[i] + time_step*g(time_grid[i], B[i], Y[i])

    return B, Y

def compare_simulation_to_data(test_data, used_well, growth_coeff, alpha, t_decay, eta, t_decay_2=100, t_lag=0,alpha_2=0):
    #[a, b, lag_phase, od_start, od_end] = estimate_lag_phase_and_exponential_coefficients(test_data['od']['time'], test_data['od'][used_well], test_config['starting_bacteria'], test_config['liquid_per_well'], epsilon=4*10**-3, average_n=6)
    dT = test_data['od']['time'][1] - test_data['od']['time'][0]
    time_grid = test_data['od']['time'].copy()
    initial_conditions=10**-4
    
    # plotting graphs with sliders (apparently there's no interactive plot here so sliders don't work.. needs to be downladed)
    fig, ax = plt.subplots(1,2)
    plt.subplots_adjust(left=0.3,bottom=0.3)
    
    line_yfp, =ax[1].plot(test_data['yfp']['time'],
             simulate(
                        growth_coeff=growth_coeff,
                        alpha=alpha,
                        alpha_2=alpha_2,
                        t_decay_2=t_decay_2,
                        t_decay=t_decay,
                        eta=eta,
                        mu=1,
                        time_grid=time_grid,
                        time_step=dT,
                        initial_bacteria_condition=initial_conditions,
                        initial_yfp_condition=initial_conditions,
                    )[1],
             )
    ax[1].plot(test_data['yfp']['time'],
             test_data['yfp'][used_well][0:444]/yfp_simulation_stretch_constant,'.')
    ax[1].set_title("YFP of well : "+str(used_well))
    
    line_OD, =ax[0].plot(test_data['yfp']['time'],
             simulate(
                        growth_coeff=growth_coeff,
                        alpha=alpha,
                        alpha_2=alpha_2,
                        t_decay_2=t_decay_2,
                        t_decay=t_decay,
                        eta=eta,
                        mu=1,
                        time_grid=time_grid,
                        time_step=dT,
                        initial_bacteria_condition=initial_conditions,
                        initial_yfp_condition=initial_conditions,
                    )[0],
             )
    ax[0].plot(test_data['od']['time'],
             test_data['od'][used_well][0:444])
    ax[0].set_title("OD of well : "+str(used_well))

    axalpha = plt.axes([0.05, 0.25, 0.0225, 0.63])
    axalpha2 = plt.axes([0.15, 0.25, 0.0225, 0.63])
    axlag = plt.axes([0.25, 0.03, 0.65, 0.03])
    axdecay = plt.axes([0.25, 0.1, 0.65, 0.03])
    axdecay2 = plt.axes([0.25, 0.17, 0.65, 0.03])
    slider_alpha = slider(
                        ax=axalpha,
                        label="alpha",
                        valmin=0,
                        valmax=10,
                        valinit=1,
                        orientation="vertical"
                    )
    slider_decay = slider(
                        ax=axdecay,
                        label="t_decay",
                        valmin=0,
                        valmax=40,
                        valinit=19,
                    )
    slider_alpha_2 = slider(
                        ax=axalpha2,
                        label="alpha 2",
                        valmin=0,
                        valmax=10,
                        valinit=0,
                        orientation="vertical"
                    )
    slider_decay_2 = slider(
                        ax=axdecay2,
                        label="t_decay 2",
                        valmin=0,
                        valmax=40,
                        valinit=21,
                    )
    slider_lag = slider(
                        ax=axlag,
                        label="t_lag",
                        valmin=0,
                        valmax=40,
                        valinit=3,
                    )
    def update(val):
        line_yfp.set_ydata(
            simulate(growth_coeff=growth_coeff,
                alpha=slider_alpha.val,
                alpha_2=slider_alpha_2.val,
                t_decay_2=slider_decay_2.val,
                t_decay=slider_decay.val,
                eta=eta,
                mu=1,
                time_grid=time_grid,
                time_step=dt,
                initial_bacteria_condition=initial_conditions,
                initial_yfp_condition=initial_conditions,)[1]
                )
        line_yfp.set_xdata(test_data['yfp']['time']+slider_lag.val)
        line_od.set_ydata(
            simulate(growth_coeff=growth_coeff,
                alpha=slider_alpha.val,
                alpha_2=slider_alpha_2.val,
                t_decay_2=slider_decay_2.val,
                t_decay=slider_decay.val,
                eta=eta,
                mu=1,
                time_grid=time_grid,
                time_step=dt,
                initial_bacteria_condition=initial_conditions,
                initial_yfp_condition=initial_conditions,)[0]
                )
        line_od.set_xdata(test_data['yfp']['time']+slider_lag.val)
        fig.canvas.draw_idle()
    slider_alpha.on_changed(update)
    slider_alpha_2.on_changed(update)
    slider_decay.on_changed(update)
    slider_decay_2.on_changed(update)
    slider_lag.on_changed(update)

    plt.show()


# Minimization


def fit(data_time,
        data_B,
        data_Y,
        lag_phase,
        initial_bacteria_condition = 10**(-4),
        initial_yfp_condition = 10**(-4)
        ):

    data_B = np.array(data_B)
    data_Y = np.array(data_Y)
    
    time_grid = np.array(data_time)
    time_step = time_grid[1] - time_grid[0]
    end_time = time_grid[end]

    cut_index = np.argmin(np.array(np.abs(time_grid- lag_phase)))

    data_B = data_B[cut_index:]
    data_Y = data_Y[cut_index:]
    time_grid = time_grid[cut_index:]
    def LMS_B(*args):
        all_args = list(args[0])

        growth_coeff = all_args[0]
        alpha = all_args[1]
        t_decay = all_args[2]
        eta = all_args[3]
        mu = all_args[4]
        B_sim, YFP_sim = simulate(
            growth_coeff=growth_coeff, 
            death_coeff = death_coeff,
            alpha=alpha, 
            t_decay=t_decay, 
            eta=eta, 
            mu=mu,
            time_grid=data_time, 
            time_step=time_step, 
            initial_bacteria_condition=initial_bacteria_condition,
            initial_yfp_condition=initial_yfp_condition,
        )

        total_sum = np.sum( # Vector norm of both OD and YFP data
                        np.sqrt( 
                            np.power( (data_B - B_sim)/data_B,2 ) 
                                )
                            )
        return total_sum


    initial_guess_array = [               #initial values for the minimization
             a,             # Growth coefficient
             0.40,          # alpha
             end_time,      # t_decay
             0.4,           # eta
             10**5,             # mu
    ]

    res = minimize(
        fun=LMS,  # Function to minimize
        x0=initial_guess_array, # Initial guess array
        method='Nelder-Mead',
        options={'maxiter': 10**3, 'xtol': 10**(-12), 'ftol': 10**(-12)},
    )
    return res.x

growth_coeff = params[0]
alpha = params[1]
t_decay = params[2]
eta = params[3]
mu = params[4]

