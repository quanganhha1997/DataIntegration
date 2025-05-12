import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

cases_df = pd.read_csv('./covid_confirmed_usafacts.csv')
deaths_df = pd.read_csv('./covid_deaths_usafacts.csv')
census_df = pd.read_csv('./acs2017_county_data.csv')

# Load needed columns
test_cases_df = cases_df[['County Name', 'State', '2023-07-23']]
test_deaths_df = deaths_df[['County Name', 'State', '2023-07-23']]
test_census_df = census_df[['County', 'State', 'TotalPop', 'IncomePerCap', 'Poverty', 'Unemployment']]

# Column headers
cases_columns = test_cases_df.columns.tolist()
deaths_columns = test_deaths_df.columns.tolist()
census_columns = test_census_df.columns.tolist()

print(cases_columns, deaths_columns, census_columns)
print(deaths_columns)
print(census_columns)

# Remove trailing spaces from 'County Name'
test_cases_df.loc[:, 'County Name'] = test_cases_df['County Name'].str.strip()
test_deaths_df.loc[:, 'County Name'] = test_deaths_df['County Name'].str.strip()

# Search for "Washington County"
cases_washington = test_cases_df[test_cases_df['County Name'] == 'Washington County']
deaths_washington = test_deaths_df[test_deaths_df['County Name'] == 'Washington County']

# Count how many counties are named "Washington County"
num_cases_washington = len(cases_washington)
num_deaths_washington = len(deaths_washington)

print(f"Number of Washington Counties: {num_cases_washington}")

# Remove rows where 'County Name' is 'Statewide Unallocated'
test_cases_df = test_cases_df[test_cases_df['County Name'] != 'Statewide Unallocated']
test_deaths_df = test_deaths_df[test_deaths_df['County Name'] != 'Statewide Unallocated']

# Count remaining rows
remaining_cases_rows = len(test_cases_df)
remaining_deaths_rows = len(test_deaths_df)

print(f"Number of remaining rows: {remaining_cases_rows}")

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "Virgin Islands, U.S.": "VI",
}
    
# invert the dictionary
abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))

# Rewrite the state abbreviations to full state names 
test_cases_df.loc[:, 'State'] = test_cases_df['State'].map(abbrev_to_us_state)
test_deaths_df.loc[:, 'State'] = test_deaths_df['State'].map(abbrev_to_us_state)
print(test_cases_df.head())

# Create key = 'County' + 'State'
test_cases_df.loc[:, 'key'] = test_cases_df['County Name'] + ', ' + test_cases_df['State']
test_deaths_df.loc[:, 'key'] = test_deaths_df['County Name'] + ', ' + test_deaths_df['State']
test_census_df.loc[:, 'key'] = test_census_df['County'] + ', ' + test_census_df['State']

# Set the 'key' column as index using .set_index()
test_cases_df = test_cases_df.set_index('key')
test_deaths_df = test_deaths_df.set_index('key')
test_census_df = test_census_df.set_index('key')

print(test_census_df.head())

# Change column '2023-07-23' to 'Cases' and '2023-07-23' to 'Deaths'
test_cases_df = test_cases_df.rename(columns={'2023-07-23': 'Cases'})
test_deaths_df = test_deaths_df.rename(columns={'2023-07-23': 'Deaths'})

cases_columns = test_cases_df.columns.values.tolist()
deaths_columns = test_deaths_df.columns.values.tolist()

print(cases_columns)
print(deaths_columns)

# Join three DataFrames
join_df = test_cases_df.join(test_deaths_df[['Deaths']])
join_df = join_df.join(test_census_df[['TotalPop', 'IncomePerCap', 'Poverty', 'Unemployment']])

# Add CasesPerCap and DeathsPerCap
join_df['CasesPerCap'] = join_df['Cases'] / join_df['TotalPop']
join_df['DeathsPerCap'] = join_df['Deaths'] / join_df['TotalPop']

row_count = len(join_df)

print(f"Number of rows in join_df: {row_count}")

# Create the correlation matrix
correlation_matrix = join_df.corr(numeric_only=True)
print(correlation_matrix)

# Create a heatmap of the correlation matrix and save it as a png file
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Correlation Matrix Heatmap')
plt.savefig("./correlation_matrix_heatmap.png")
