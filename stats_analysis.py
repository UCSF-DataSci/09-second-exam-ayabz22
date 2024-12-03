import seaborn as sns
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np

#read the data
df = pd.read_csv('ms_data_with_insurance.csv')

#convert education to numerical 
df.loc[df['education_level'] == 'High School', 'education_num'] = 0
df.loc[df['education_level'] == 'Some College', 'education_num'] = 1
df.loc[df['education_level'] == 'Bachelors', 'education_num'] = 2
df.loc[df['education_level'] == 'Graduate', 'education_num'] = 3
df['education_num'] = df['education_num'].astype(float)

#pt 1: analyze walking speed
print("=== PT1: Linear Regression for Walking Speed by Age and Education ===")
model = smf.ols(formula='walking_speed ~ age + education_level', data=df)
results = model.fit()
print(results.summary().tables[1], '\n')

#pt 2: analyze costs 
print("=== PT2: Analyze Costs ===")
print('Overall Visit Cost Statistics:\n', df['visit_cost'].describe(), '\n')

for insurance in df['insurance_type'].unique():
    print(f'{insurance} Insurance Visit Cost Statistics:\n', 
          df.loc[df['insurance_type'] == insurance, 'visit_cost'].describe(), '\n')
    
ax = sns.boxplot(data=df, x='insurance_type', y='visit_cost', palette='pastel')
ax.set_title('Visit Cost Distribution by Insurance Type')
plt.xlabel('Insurance Type')
plt.ylabel('Visit Cost')
plt.savefig('cost_by_insurance.png')
plt.clf()

#pt 3: advanced analysis
print("=== PT3: Advanced Analysis ===")
ax = sns.scatterplot(
    data=df, 
    x='age', 
    y='walking_speed', 
    hue='education_level', 
    alpha=0.5,
    palette='muted'
)
ax.set_title('Walking Speed by Age and Education Level')
plt.xlabel('Age')
plt.ylabel('Walking Speed')
plt.legend(title='Education Level')
plt.savefig('walkingspeed_by_age_and_education.png')
plt.clf()

#confounding analysis
print("=== Examination of Confounding ===")
unadjusted_model = smf.ols(formula='walking_speed ~ age', data=df)
unadjusted_results = unadjusted_model.fit()
print(f'Unadjusted Age Coefficient: {unadjusted_results.params["age"]}')
adjusted_model = smf.ols(formula='walking_speed ~ age + education_level', data=df)
adjusted_results = adjusted_model.fit()
print(f'Adjusted Age Coefficient (controlled for education level): {adjusted_results.params["age"]}')
diff = adjusted_results.params["age"] - unadjusted_results.params["age"]
print(f'Difference in Coefficients: {diff}')
print('Note: If the difference is >10% of the unadjusted coefficient, there is likely confounding.\n')


# Interaction effects
print("=== Interaction Effects of Education Level on Walking Speed by Age ===")
interaction_model = smf.ols(formula='walking_speed ~ age * education_level', data=df)
interaction_results = interaction_model.fit()
print(interaction_results.summary().tables[1])
print('Note: If Pr(>|t|) for age:education_level interaction terms is <0.05, interaction effects are significant.')

