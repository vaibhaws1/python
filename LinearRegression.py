# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 10:55:53 2018
@author: Vaibhaw
Function: Linear Regression with Data Normalization
"""

verbose = True
visualize = False
evaluateRisk = True

import csv 
if visualize: import matplotlib.pyplot as plt

def main(): 
    if verbose: print ("Starting...")
    
    # Get training data from file
    dataset = load_file("input2.csv")    
    #if verbose: print ("dataset:",len(dataset))
    
    #Normalize data
    normalized_dataset = normalize(dataset)
    #if verbose: print ("normalized_dataset:",len(normalized_dataset))
    
    # Run the gradient descent algorithm 
    if verbose: print("Running Gradient Descent ...")
    output_betalist = []
    alpha = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 0.9] #Initialize learning rates
    for a in alpha:
        #initilize beta values
        b_0 = 0 
        b_age = 0
        b_weight = 0
        number_of_iterations = 100
        if verbose: print("> Alpha:",a)
        this_betalist = run_gradient_descent (normalized_dataset,
                              a, number_of_iterations,
                              b_0, b_age, b_weight )
        if verbose: print (">> Beta Values: [b_0=%.05f, b_age=%.05f, b_weight=%.05f]"%
                           (this_betalist[2],this_betalist[3],this_betalist[4]))
        output_betalist.append(this_betalist)

    # write output datalist
    write_file("output2.csv", output_betalist)
    
    # Visualize
    if visualize : matPlot3D (dataset, "II. Linear Regression (raw data)")
    if visualize : matPlot3D (normalized_dataset, "II. Linear Regression (Normalized data)")

def run_gradient_descent (dataset, alpha, iterations, 
                          init_b_0, init_b_age, init_b_weight):
    N = len(dataset)
    
    #initialiing values for Gradient Descent
    beta_values = [init_b_0, init_b_age, init_b_weight] # b_0, b_age, b_weight
    prev_beta_values = [0,0,0,9999] # b_0, b_age, b_weight, risk
    output_values = [alpha,0] # adding alpha, starting iteration count

    # Run for N iterations
    for thisIteration in range (iterations):
        diffPredVsLabel = 0
        # initializing values for an iteraton
        cumu_diff_values = [0,0,0] # cumulative diff holder for b_0, b_age, b_weight
        if evaluateRisk:
            risk = 0 # initializing risk value 
            loss_per_point = 0
            cumu_cost = 0

        # obtain sum ( b_0 + b_age*x1 + b_weight*x2) for entire dataset
        for age, weight, height in dataset:
            #Calculate fx = b_0 + b_age * age + b_weight * weight
            fx = beta_values[0] + beta_values[1] * age + beta_values[2] * weight
            diffPredVsLabel = fx - height
            cumu_diff_values[0] += diffPredVsLabel 
            cumu_diff_values[1] += diffPredVsLabel * age
            cumu_diff_values[2] += diffPredVsLabel * weight

            # the following derived for risk calcs
            if evaluateRisk:
                loss_per_point = (height - fx)**2
                cumu_cost += loss_per_point
        
        #Adjust the beta values
        beta_values[0] -= alpha * (1/N) * cumu_diff_values[0] # b_0
        beta_values[1] -= alpha * (1/N) * cumu_diff_values[1] # b_age
        beta_values[2] -= alpha * (1/N) * cumu_diff_values[2] # b_weight
        
        if evaluateRisk:
            #Check Risk, if decreasing continue, if increasing return previous beta values
            risk = (1/2*N) * cumu_cost #Risk = (1/2*N) * cumu_cost
            if risk > prev_beta_values[3]: # if risk starts increasing return previous value
                # this assumes that functiona has only one optimum
                output_values.extend(prev_beta_values)
                return output_values
            prev_beta_values = [beta_values[0],beta_values[1],beta_values[2],risk]
        output_values[1] = thisIteration + 1
    output_values.extend(beta_values)
    return output_values

def normalize (dataset):
    min_x = 999.00
    min_y = 999.00
    max_x = 0.00
    max_y = 0.00

    # find min and max
    for x, y, z in dataset:
        min_x = min (min_x,x)
        min_y = min (min_y,y)
        max_x = max (max_x,x)
        max_y = max (max_y,y)

    # find standard deviation 
    stdev_x = max_x - min_x
    stdev_y = max_y - min_y
    
    normalized_dataset = []
    norm_x = 0
    norm_y = 0

    # create scaled datalist
    for x, y, z in dataset:
        norm_x = (x - min_x) / stdev_x
        norm_y = (y - min_y) / stdev_y
        normdatarow = [norm_x, norm_y, z]
        normalized_dataset.append(normdatarow)

    if verbose: print ("Data Normalized")
    if verbose: print ("Age >> min:%.6f, max:%.6f, stdev:%.6f"%(min_x,max_x,stdev_x))
    if verbose: print ("Weight >> min:%.6f, max:%.6f, stdev:%.6f"%(min_y,max_y,stdev_y))
        
    return normalized_dataset
    
        
# Load data from csv file and return a list with data
def load_file(filename):
    dataset = list()
    with open(filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader: 
            if not row:
                continue
            row_data_list = []
            for item_in_row in row:
                row_data_list.append(float(item_in_row))
            dataset.append(row_data_list)
    return dataset

#write weights to file
def write_file(filename, weightsList):
    file = open(filename,"w")
    for weights in weightsList:
        lineToWrite = str(weights[1]) + ", " + str(weights[2]) + ", " + str(weights[0]) +"\n"
        file.writelines(lineToWrite )
    file.close()
    
#write list to file
def write_file(filename, aList):
    file = open(filename,"w")
    for items in aList:
        lineToWrite  = str(items[0]) + ", " + str(items[1]) + ", "  
        lineToWrite += str(items[2]) + ", " + str(items[3]) + ", " 
        lineToWrite += str(items[4]) + "\n"
        file.writelines(lineToWrite )
    file.close()
    
def matPlot3D(dataset, theTitle):
    plt.title (theTitle)
    plt3d = plt.figure().add_subplot(111,projections='3d')
    # plot points
    for x, y, z in dataset:
        if x > 1 and x < 5 : plt3d.plot_surface (x,y,z,'bo')
        elif x > 5.01 and x < 7 : plt3d.plot_surface (x,y,z,'go')
        else : plt3d.plot_surface (x,y,z,'ro')
    #plt.plot([0,15.6],[15.6,-8],'g-')
    plt.show()

main()
