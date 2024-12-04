import pandas as pd
import numpy as np 
import statsmodels.api as sm
from statsmodels.regression.linear_model import OLS 


#read the processed file 
df = pd.read_csv('ms_data_with_insurance.csv')

summarize_data = pd.DataFrame({
    'Column': df.columns,
    'Dtype': df.dtypes.values,
})
print(summarize_data)
print(df.shape)

#do the correct conversions and sort 
df['patient_id'] = df['patient_id'].astype('string')
df['visit_date'] = pd.to_datetime(df['visit_date']) 
df['age'] = df['age'].astype(float) 
df['education_level'] = df['education_level'].astype('category') 
df['walking_speed'] = df['walking_speed'].astype(float)
df = df.sort_values(by=['patient_id', 'visit_date']) 

# assign random insurance types to each patient_id 
insurance_types = ['Bronze', 'Gold', 'Silver']
id_list = np.unique(df['patient_id'])
insurance_type = {}

for patient_id in id_list:
    insurance_type[patient_id] = np.random.choice(insurance_types)

df['insurance_type'] = df['patient_id'].map(insurance_type)

df['visit_cost'] = np.nan

for i in range(len(df)):
    if df.loc[i, 'insurance_type'] == 'Bronze':
        df.loc[i, 'visit_cost'] = round(1000 * np.random.uniform(low=0.8, high=1.2), 2)
    elif df.loc[i, 'insurance_type'] == 'Gold':
        df.loc[i, 'visit_cost'] = round(750 * np.random.uniform(low=0.8, high=1.2), 2)
    elif df.loc[i, 'insurance_type'] == 'Silver':
        df.loc[i, 'visit_cost'] = round(500 * np.random.uniform(low=0.8, high=1.2), 2)
df = df.drop(columns=['insurance'], errors='ignore')
df.to_csv('ms_data_with_insurance.csv', sep=',', index=False)

#find the mean walking speed by education level
mean_speed_education = df.groupby('education_level', observed=True)['walking_speed'].mean() 

#age effects on walking speed
X = sm.add_constant(df['age'])  
y = df['walking_speed']
model = OLS(y, X)
results = model.fit()

# find the mean costs by insurance type
mean_costs_insurance = df.groupby('insurance_type', observed=True)['visit_cost'].mean() 

#results
with open("summary_statistics.txt", "w") as file:
    file.write("Summary Statistics\n")
    file.write("===================\n\n")

    file.write("Mean Walking Speed by Education Level:\n")
    file.write(mean_speed_education.to_string())
    file.write("\n\n")
    
    file.write("Mean Visit Cost by Insurance Type:\n")
    file.write(mean_costs_insurance.to_string())
    file.write("\n\n")

    file.write("=== Linear Regression for Walking Speed by Age ===\n")
    file.write("==============================================================================\n")
    file.write(results.summary().tables[1].as_text())
    file.write("\n")