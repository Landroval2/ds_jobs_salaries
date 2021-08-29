import pandas as pd
from datetime import date
import numpy as np

# creating the date object of today's date
todays_date = date.today()
this_year = todays_date.year

df = pd.read_csv('job_data.csv')

# Jobs without a salary estimate will not be particularly useful for our analysis
df = df[df['Salary Estimate'] != -1]

# Parse salary estimate (remove glassdor etc)
salary = df['Salary Estimate'].apply(lambda x: x.replace('K', '').replace('$', '').split('(')[0].strip())

df['min_salary'] = salary.apply(lambda x: int(x.split('-')[0].strip()))
df['max_salary'] = salary.apply(lambda x: int(x.split('-')[1].strip()))
df['avg_salary'] = (df.min_salary + df.max_salary) / 2


# Company name only Divide Location between city and abbreviation of state
def get_state(loc_string):
    if loc_string.lower() == 'remote':
        return 'remote'
    elif len(loc_string.split(',')) < 2:
        return -1
    else:
        return loc_string.split(',')[1].strip()


df['state'] = df['Location'].apply(lambda x: get_state(x))


# state Change the size column to something more useful, it should be a range. Change Founded into years runnning or
# something like that?
def get_years(founded_string):
    if founded_string == -1 or founded_string == '-1':
        return np.nan
    try:
        founded_year = int(founded_string)
        years_running = round(int(this_year - founded_year))
    except:
        years_running = np.nan
    return years_running


df['age'] = df['Founded'].apply(lambda x: get_years(x))


# Take useful information from job description. Possibilities including if python is required,
# machine learning and others.
def find_skill_in_description(description, skill_string):
    if skill_string.lower() in description.lower():
        return 1
    else:
        return 0

    # python


df['python'] = df['Job Description'].apply(lambda x: find_skill_in_description(x, 'python'))
#df.python.value_counts()
# r studio
df['r_studio'] = df['Job Description'].apply(lambda x: find_skill_in_description(x, 'r studio'))
#df.r_studio.value_counts()
# spark
df['spark'] = df['Job Description'].apply(lambda x: find_skill_in_description(x, 'spark'))
#df.spark.value_counts()
# aws
df['aws'] = df['Job Description'].apply(lambda x: find_skill_in_description(x, 'aws'))
#df.aws.value_counts()
# excel
df['excel'] = df['Job Description'].apply(lambda x: find_skill_in_description(x, 'excel'))
#df.python.value_counts()
# tableau
df['tableau'] = df['Job Description'].apply(lambda x: find_skill_in_description(x, 'tableau'))
#df.tableau.value_counts()
# machine learning
df['ml'] = df['Job Description'].apply(lambda x: find_skill_in_description(x, 'machine learning'))
#df.ml.value_counts()


# Drop unnecesary column
df.drop(['Unnamed: 0'], axis=1)

df.to_csv('../job_data_cleaned.csv', index=False)