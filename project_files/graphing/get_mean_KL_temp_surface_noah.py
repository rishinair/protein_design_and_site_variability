import sys, os, math, string, re, gzip, urllib, shutil, Bio
import subprocess
import cStringIO
from numpy import *
from pylab import *
from scipy.stats import *
import matplotlib.pyplot as plt

#This takes a list of values that are string values and creates an array
def make_array(list_of_values):
    new_value_list = []
    for value in list_of_values:
        new_value = value.rstrip()
        new_value = float(new_value)
        new_value_list.append(new_value)
    value_array = array(new_value_list)
    return value_array

def get_mean_designed_data(file_of_data):
    designed_mean_RSA_values = []
    designed_mean_entropy_values = []
    designed_cor_entropy_RSA_values = []
    designed_mean_KL_values = []
    designed_data = []
    protein_file = open(file_of_data, "r")
    designed_protein_data = protein_file.readlines()
    protein_file.close()
    header = designed_protein_data.pop(0)

    for line in designed_protein_data:  
        data = re.split("\t", line)
        designed_data.append(data)
    
    for data in designed_data: 
        designed_mean_RSA_values.append(data[2])
        designed_mean_entropy_values.append(data[3])
        designed_cor_entropy_RSA_values.append(data[4])
        designed_mean_KL_values.append(data[5])
        #all_temp_cor_entropy_RSA_values.append(designed_cor_entropy_RSA_values_00)
    return designed_mean_RSA_values, designed_mean_entropy_values, designed_cor_entropy_RSA_values, designed_mean_KL_values

def get_plot_color(color_increment, natural_cor_entropy_RSA_value):
    #Start Blue and Go to Red tuple = RGB
    #Start Blue
    #color_start = (1,0,0) <
    green = 0
    #switch_to_red = int(num_total_plots/2)
    if(natural_cor_entropy_RSA_value < 0.2): 
        red = .95 - (0.001 * natural_cor_entropy_RSA_value)
        blue = 0 
        color = (red, green, blue)
    elif(natural_cor_entropy_RSA_value>=0.2 and natural_cor_entropy_RSA_value<0.4):
        red = 1 - (1.2*natural_cor_entropy_RSA_value)
        blue = 1 - (1.2*natural_cor_entropy_RSA_value)
        color = (red,green,blue)
    elif(natural_cor_entropy_RSA_value>=0.4 and natural_cor_entropy_RSA_value<=1):
        red = .4 - (0.65 * natural_cor_entropy_RSA_value)
        blue = 1 - (0.6*natural_cor_entropy_RSA_value)
        color = (red, green, blue)
    else:
        print "Correlation over 1!!!!!"
    return color

def get_plot_format(xaxis_label, yaxis_label, ax):
    xlabel(xaxis_label)
    ylabel(yaxis_label)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    plt.xlim(-0.2, 1.4)
    plt.ylim(0.5, 3)
    plt.xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2])
    plt.yticks([-0.2, 0.0, 0.2, 0.4, 0.6])
    #plt.text(0.9, 0.9, "Text",horizontalalignment = 'center', verticalalignment = 'center', transform = ax.transAxes) #Independent of size since it is relative to the axes


'''
def get_plot_format_cor_plot(xaxis_label, yaxis_label, ax):
    xlabel(xaxis_label)
    #ylabel(yaxis_label)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    plt.xlim(-0.3, 1.5)
    plt.ylim(-0.3, 0.6)
    plt.xticks([-0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4], ["FB", "0.0","0.2", "0.4", "0.6", "0.8", "1.0", "1.2", "NS"])
    plt.yticks([-0.2, 0.0, 0.2, 0.4, 0.6])
'''

def save_figure(figure_title, PDB):
    save_fig_title = figure_title + PDB +  ".pdf"
    savefig(save_fig_title, format = None)

count = 1
natural_data = []

pdb_names = []
chain_names = []
natural_mean_RSA_values = []
natural_mean_entropy_values = []
natural_cor_entropy_RSA_values = []

designed_mean_RSA_values_00 = []
designed_mean_RSA_values_01 = []
designed_mean_RSA_values_03 = []
designed_mean_RSA_values_06 = []
designed_mean_RSA_values_09 = []
designed_mean_RSA_values_12 = []
designed_mean_RSA_values_003 = []

designed_mean_entropy_values_00 = []
designed_mean_entropy_values_01 = []
designed_mean_entropy_values_03 = []
designed_mean_entropy_values_06 = []
designed_mean_entropy_values_09 = []
designed_mean_entropy_values_12 = []
designed_mean_entropy_values_003 = []

designed_cor_entropy_RSA_values_00 = []
designed_cor_entropy_RSA_values_01 = []
designed_cor_entropy_RSA_values_03 = []
designed_cor_entropy_RSA_values_06 = []
designed_cor_entropy_RSA_values_09 = []
designed_cor_entropy_RSA_values_12 = []
designed_cor_entropy_RSA_values_003 = []

designed_mean_KL_values_00 = []
designed_mean_KL_values_003 = []
designed_mean_KL_values_01 = []
designed_mean_KL_values_03 = []
designed_mean_KL_values_06 = []
designed_mean_KL_values_09 = []
designed_mean_KL_values_12 = []

all_temp_cor_entropy_RSA_values = []
all_temp_entropy_values = []
natural_mean_split_KL_values = []

temps = [0.0, 0.03, 0.1, 0.3, 0.6, 0.9, 1.2]
temp_array = array(temps)

modified_temps = [-0.2, 0.03, 0.1, 0.3, 0.6, 0.9, 1.2, 1.4]
modified_temp_array = array(modified_temps)
protein_file = open("graph_mean_data_natural_noah.csv", "r")
natural_protein_data = protein_file.readlines()
protein_file.close()


index = 0
for element in all_temp_cor_entropy_RSA_values:
    new_array = []
    for num in element:
        value = num
        value = value.rstrip()
        new_value = float(value)
        new_array.append(new_value)
    all_temp_cor_entropy_RSA_values_array.append(new_array)
#print len(all_temp_cor_entropy_RSA_values_array)

for element in all_temp_entropy_values:
    new_array = []
    for num in element:
        value = num
        value = value.rstrip()
        new_value = float(value)
        new_array.append(new_value)
    all_temp_entropy_values_array.append(new_array)
    
#show()

mean_KL_temp_file = open("graph_mean_KL_surface_temp_data_noah.csv", "r")
mean_KL_temp_data = mean_KL_temp_file.readlines()
mean_KL_temp_file.close()
header = mean_KL_temp_data.pop(0)

mean_KL_temp_ordered_file = open("graph_mean_KL_surface_temp_data_ordered_noah.csv", "r")
mean_KL_temp_ordered_data = mean_KL_temp_ordered_file.readlines()
mean_KL_temp_ordered_file.close()
ordered_header = mean_KL_temp_ordered_data.pop(0)

mean_entropy_temp_file = open("graph_mean_entropy_surface_temp_data_noah.csv", "r")
mean_entropy_temp_data = mean_entropy_temp_file.readlines()
mean_entropy_temp_file.close()
header = mean_entropy_temp_data.pop(0)

all_temp_data = []
all_temp_mean_entropy_data_array = [] 
for line in mean_entropy_temp_data:
    data = re.split("\t", line)
    data.pop(0)
    data_array = make_array(data)
    all_temp_data.append(data_array)
    #mean_KL_temp_values2 = data.pop()
    mean_entropy_temp_values_array = make_array(data)
    #mean_KL_temp_values2_array = make_array(mean_KL_temp_values2_array)
all_temp_mean_entropy_data_array = array(all_temp_data)

all_temp_data = []
all_temp_mean_KL_data_array = [] 
for line in mean_KL_temp_data:
    data = re.split("\t", line)
    data.pop(0)
    data_array = make_array(data)
    all_temp_data.append(data_array)
    #mean_KL_temp_values2 = data.pop()
    mean_KL_temp_values_array = make_array(data)
    #mean_KL_temp_values2_array = make_array(mean_KL_temp_values2_array)
all_temp_mean_KL_data_array = array(all_temp_data)


all_temp_ordered_data = []
all_temp_ordered_mean_KL_data_array = [] 
for line in mean_KL_temp_ordered_data:
    data = re.split("\t", line)
    data.pop(0)
    data_array = make_array(data)
    all_temp_ordered_data.append(data_array)
    #mean_KL_temp_values2 = data.pop()
    mean_KL_ordered_temp_values_array = make_array(data)
    #mean_KL_temp_values2_array = make_array(mean_KL_temp_values2_array)
all_temp_ordered_mean_KL_data_array = array(all_temp_ordered_data)

count = 0
#Make boxplot for Temp vs Mean KL
rcParams['font.size'] = 20     
rcParams['figure.figsize'] = [14,6]
rcParams['lines.linewidth'] = 2
fig2 = plt.figure(count, dpi = 400)
#ax1 = axes([0.07,0.08,0.43, 0.85])
ax1 = axes([0.07, 0.118, 0.43, 0.849])
text(-0.4, 3.5, "A", fontweight = 'bold', ha = 'center', va = 'center', fontsize = 20)
#grid()
b1 = boxplot(all_temp_mean_KL_data_array, sym = "ko")
setp(b1['whiskers'], color = 'black', linestyle = '-')
setp(b1['boxes'], color =  'black')
setp(b1['caps'], color = 'black')
setp(b1['medians'], color = 'black')
setp(b1['fliers'], color  = 'black')
#p2 = ax2.plot(temp_array, mean_KL_temp_values_array, "ko")
xlabel("Temperature")
ylabel("Mean KL Divergence")
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
#text(-0.38, 3.0, "A", fontweight = 'bold', ha = 'center', va = 'center', fontsize = 12) 
text(9.85, 3.5, "B", fontweight = 'bold', ha = 'center', va = 'center', fontsize = 20)
ax1.get_xaxis().tick_bottom()
ax1.get_yaxis().tick_left()
plt.ylim(0.0, 3.5)
plt.yticks([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5], ["0.0", "0.5", "1.0", "1.5", "2.0", "2.5", "3.0", "3.5"])
plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9], ["FB", "Soft", "0.3", "0.6", "0.9", "1.2", "1.8", "2.4", "NS"])
count = count + 1
#show()

#Make boxplot for Temp vs Mean KL    
#grid()
ax2 = axes([0.56, 0.118, 0.43, 0.849])
b2 = boxplot(all_temp_ordered_mean_KL_data_array, sym = "ko")
setp(b2['whiskers'], color = 'black', linestyle = '-')
setp(b2['boxes'], color =  'black')
setp(b2['caps'], color = 'black')
setp(b2['medians'], color = 'black')
setp(b2['fliers'], color  = 'black')
xlabel("Temperature")
ax2.get_xaxis().tick_bottom()
ax2.get_yaxis().tick_left()
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
#plt.rc('font', size = 10)
plt.ylim(0.0, 3.5)
plt.yticks([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5], ["0.0", "0.5", "1.0", "1.5", "2.0", "2.5", "3.0", "3.5"])
plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9], ["FB", "Soft", "0.3", "0.6", "0.9", "1.2", "1.8", "2.4", "NS"])
save_fig_title = "Mean_KL_vs_Temp_Surface_Boxplot_Noah" + ".pdf"
savefig(save_fig_title, format = None)
count = count + 1
#show()


#Make boxplot for Temp vs Mean KL    
fig = plt.figure(count, dpi = 500, figsize = (11,8))
#Make boxplot for Temp vs Mean KL
rcParams['font.size'] = 20     
rcParams['figure.figsize'] = [11,8]
rcParams['lines.linewidth'] = 2
ax = axes([0.095,0.12,0.90, 0.83])
#all_temp_cor_entropy_RSA_values
b4 = ax.boxplot(all_temp_mean_entropy_data_array, sym = 'ko')
setp(b4['whiskers'], color = 'black', linestyle = '-')
setp(b4['boxes'], color =  'black')
setp(b4['caps'], color = 'black')
setp(b4['medians'], color = 'black')
setp(b4['fliers'], color  = 'black')
xlabel("Temperature")
ylabel("Mean Entropy")

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
plt.ylim(0.15, 2.75)
#plt.xlim(0.8, 9.2)
plt.yticks([0.25, 0.75, 1.25,1.75, 2.25, 2.75], ["0.25", "0.75", "1.25", "1.75", "2.25", "2.75"])
plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9], ["FB", "Soft", "0.3", "0.6", "0.9", "1.2", "1.8", "2.4", "NS"])
save_fig_title = "Mean_Entropy_vs_Temp_Surface_Boxplot_Noah" + ".pdf"
savefig(save_fig_title, format = None)
count = count + 1
#show()
