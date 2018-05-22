# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 15:16:45 2018
@author: Vaibhaw
Function: Perceptron Learning Algorithm
"""
verbose = False
visualize = False

import csv 
if visualize: import matplotlib.pyplot as plt

def execute_perceptron (dataset) :
    # initialize weights [ w0 , w1 , w2 ]
    weights = [0.0, 0.0, 0.0]
    list_weights = []
    fx = 0
    cnt = 0
    while True:
        error = 0
        for datarow in dataset:
            fx = weights[0] + weights[1]*datarow[0] + weights[2]*datarow[1]
            error = fx * datarow[2]
            if error <= 0 : # if an error adjust weights Wj = Wj + Yi*Xi
                weights [0] = weights [0] + datarow[2] 
                weights [1] = weights [1] + datarow[2] * datarow[0]
                weights [2] = weights [2] + datarow[2] * datarow[1]
        if verbose: print ("Itr: %d >> Error: %d || w_1, w_2, b : %d, %d, %d"%
                           (cnt, error, weights[1], weights[2], weights[0]))
        weight_copy = weights [:]
        list_weights.append(weight_copy)
        #Check for convergence
        if cnt > 0 :
            # if convergence achieved, return list_weights
            if list_weights[cnt] == list_weights[cnt-1]:
                return list_weights
        # else continue iteration
        cnt += 1

def main(): 
    if verbose: print ("Starting...")
    
    # Get training data from file
    dataset = load_file("input1.csv")    

    # Calculate weights
    convergence_of_weights = execute_perceptron(dataset)
    if verbose: print ("convergence_of_weights",convergence_of_weights)
    
    # write weights
    write_file("output1.csv", convergence_of_weights)
    
    # Visualize
    if visualize : matPlot (dataset, "I. Perceptron Learning Algorithm")
    
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
    
def matPlot(dataset, theTitle):
    plt.title (theTitle)
    # plot points
    for x, y, z in dataset:
        if z >= 1 : plt.plot (x,y,'bo')
        else: plt.plot (x,y,'ro')
    #plot line  [x1,x2]      [y1,y2]
    #          (0,39,'gs')  (15.6,0,'gs')
    #          (0,15.6,'gs')  (15.6,-8,'gs')
    #plt.plot([0,15.6],[39,0],'g-')
    plt.plot([0,15.6],[15.6,-8],'g-')
    plt.show()

main()