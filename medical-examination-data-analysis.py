# importing required libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# reading csv file
df = pd.read_csv('medical-data.csv') 


# creating a bmi column
df['bmi'] = df['weight'] / ((df['height']/100)**2)

df['Overweight']=1



# normalizing data by coverting values into '0' and '1' ('0' represents positive state and '1' represents negative state)

df.loc[df['bmi']< 25, 'Overweight']=0

df.loc[df['cholesterol']==1 , 'cholesterol'] = 0

df.loc[df['cholesterol']>1 , 'cholesterol'] = 1

df.loc[df['gluc']==1 , 'gluc'] = 0

df.loc[df['gluc']>1 , 'gluc'] = 1



# dropping unnecessary columns
drp = df.drop(columns = ['id','age','sex','height','weight','ap_lo','ap_hi','bmi'])


# splitting cardio into '0' and '1'

val_0 = drp.loc[df['cardio']==0] 
val_1 = drp.loc[df['cardio']==1] 


# melting columns 

melted_df0 = pd.melt(val_0 , value_vars =['active', 'alco', 'cholesterol', 'gluc', 'Overweight', 'smoke'],
                    var_name='Variables', value_name='Binary Value')


melted_df1 = pd.melt(val_1 , value_vars = ['active', 'alco', 'cholesterol', 'gluc', 'Overweight', 'smoke'],
                    var_name='Variables', value_name='Binary Value')


# plotting data in the form of grouped bar graph


def plot0():
    plotting = sns.catplot(data=melted_df0 , x = 'Variables', hue = 'Binary Value' , kind='count', height = 4, aspect = 2)
    #plotting.set_axis_labels('Variables','Total') seaborn syntax for labelling x,y coord
    plt.xlabel('Variable')
    plt.ylabel('Total')
    plt.title('Cardio = 0')
    # plotting.legend(title="Binary Value", labels=["0", "1"])
    plt.savefig('plot0')
    plt.show()
    
    
def plot1():
    plotting = sns.catplot(data=melted_df1 , x = 'Variables', hue = 'Binary Value' , kind='count', height = 4, aspect = 2)
    #plotting.set_axis_labels('Variables','Total') seaborn syntax for labelling x,y coord
    plt.xlabel('Variable')
    plt.ylabel('Total')
    plt.title('Cardio = 1')
    # plotting.legend(title="Binary Value", labels=["0", "1"])
    plt.savefig('plot1')
    plt.show()
    

plot0()
plot1()



# cleaning data
df = df.loc[(df['ap_lo'] <= df['ap_hi'])]


# height is less than 2.5th percentile
df = df.loc[(df['height'] >= df['height'].quantile(0.025))]    


# height is more than 97.5th percentile
df = df.loc[(df['height'] <= df['height'].quantile(0.975))]  


# weight is less than 2.5th percentile
df = df.loc[(df['weight'] >= df['weight'].quantile(0.025))]   


# weight is more than 97.5th percentile
df = df.loc[(df['weight'] <= df['weight'].quantile(0.975))]   


# excluding bmi
drop_bmi = df.drop(columns = ['bmi'])


# creating a correlation matrix
data = round(drop_bmi.corr(),1) 


# plotting heatmap
plt.subplots(figsize=(15,10))
mask = np.triu(np.ones_like(data, dtype=bool))
sns.heatmap(data=data, mask=mask, annot=True, fmt='.1f', cmap='Blues')
plt.xticks(rotation=90)
plt.savefig('Heatmap')
plt.show()
