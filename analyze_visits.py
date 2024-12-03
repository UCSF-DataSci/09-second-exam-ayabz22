import pandas as pd
import numpy as np 
import statsmodels.api as sm

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

#find the mean walking speed by education level
mean_speed_education = df.groupby('education_level', observed=True)['walking_speed'].mean() 

#age effects on walking speed
X = sm.add_constant(df['age'])  
y = df['walking_speed']
model = sm.OLS(y, X).fit()
age_coefficient = model.params['age']

# find the mean costs by insurance type
mean_costs_insurance = dat.groupby('insurance_type', observed=True)['visit_cost'].mean()

#results
with open("summary_statistics.txt", "w") as file:
    file.write("Summary Statistics\n")
    file.write("===================\n\n")
    file.write("Mean Walking Speed by Education Level:\n")
    file.write(mean_speed_education.to_string())
    file.write("\n\n")
    file.write("Mean Costs by Insurance Type:\n")
    file.write(mean_costs_insurance.to_string())
    file.write("\n\n")
    file.write(f"Walking speed decreases by {age_coefficient:.4f} feet/second per year.")
