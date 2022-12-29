### CONFIGURATION ###
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt


def estimate_lag_phase_and_exponential_coefficients(time, od, starting_bacteria_estimate, liquid_per_well, epsilon=5 * 10**-3, average_n=5, show_graphs=False):
    averaged_time = average_n_dots(time.to_numpy(), average_n)
    averaged_od = average_n_dots(od.to_numpy(), average_n)

    distances = np.abs(averaged_od[1:] - averaged_od[:-1])
    rise = np.argwhere(distances > epsilon)
    start = rise[0][0] * average_n
    end = rise[-average_n][0] * average_n
    start -= 1
    end -= 1

    # Convert from od to bacteria number
    amount_of_bacteria = od * BACTERIA_PER_ML_1_OD * liquid_per_well

    # Estimate the exponent coefficient via polynomial fit to log of the data
    a, b = np.polyfit(x=time[start:end], y=np.log(amount_of_bacteria[start:end]), deg=1) # Fit is ax + b

    # Create that fit and see where it meets the estimated starting population to get the lag phase
    linear_fit_y = np.linspace(b, b + time.iloc[-1]*a, 1000) # Linear fit
    linear_fit_x = np.linspace(0, time.iloc[-1], 1000)
    estimated_start_point_line = np.linspace(np.log(starting_bacteria_estimate), np.log(starting_bacteria_estimate), 1000)

    distance_between_graphs = np.abs(estimated_start_point_line - linear_fit_y) # Distance between linear graph and horizontal line
    suspected_lag_phase = np.argwhere(distance_between_graphs == min(distance_between_graphs))[0][0] # Returns the index of the minimal distance between graph and horizontal line
    
    if show_graphs:
        plt.plot(time, np.log(amount_of_bacteria), '.')
        plt.plot(time[start:end], np.log(amount_of_bacteria[start:end]), '.')
        plt.plot(linear_fit_x, linear_fit_y, '--', linewidth = '1', color = 'black')
        plt.plot(linear_fit_x, estimated_start_point_line, '--', linewidth = '1', color = 'red')
        plt.grid()            
        print("The lag phase is :", linear_fit_x[suspected_lag_phase])
        plt.show()

    lag_phase = linear_fit_x[suspected_lag_phase]

    return [a, b, lag_phase, start, end]
