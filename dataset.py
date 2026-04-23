#imports
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
import pgeocode
import math

def data_import():
    # import datasets
    P3 = pd.DataFrame()
    for file in os.listdir(os.path.join('Databases', 'Expanded Data')):
        data = pd.read_json(os.path.join('Databases', 'Expanded Data', file))
        P3 = pd.concat([P3, data], ignore_index=True)

    P3 = P3.rename(columns={'Survey Date': 'Survey_Date'})

    # extract data
    P3_extra = pd.DataFrame(columns=[
        'Pri_D', 'Pri_E', 'Pri_P', 'Pri_C',
        'Env_D', 'Env_E', 'Env_P', 'Env_C',
        'High_Trait', 'Low_Trait', 'Decision_Style', 'Leadership_Style',
        'Energy_Category', 'Stress_Category', 'Stress', 'Energy',
        'Proactivity', 'Self-Monitoring'
    ])

    for record in P3['Profile Report']:
        priD = int(record['Summary']['Trait']['Primary Profile']['Dominance'])
        priE = int(record['Summary']['Trait']['Primary Profile']['Extroversion'])
        priP = int(record['Summary']['Trait']['Primary Profile']['Patience'])
        priC = int(record['Summary']['Trait']['Primary Profile']['Conformity'])
        envD = int(record['Summary']['Trait']['Environmental Profile']['Dominance'])
        envE = int(record['Summary']['Trait']['Environmental Profile']['Extroversion'])
        envP = int(record['Summary']['Trait']['Environmental Profile']['Patience'])
        envC = int(record['Summary']['Trait']['Environmental Profile']['Conformity'])
        High = str(record['Summary']['Primary Profile']['High Trait'])
        Low = str(record['Summary']['Primary Profile']['Low Trait'])
        Dec = str(record['Summary']['Primary Profile']['Decision Making'])
        Energy = str(record['Summary']['Primary Profile']['Energy'])
        Stress = str(record['Summary']['Primary Profile']['Stress'])
        Lead = str(record['Summary']['Primary Profile']['Leadership Style'])
        Stress_num = float(record['Stress Level']['Score'])
        Energy_num = float(record['Energy Level']['Score'])
        Proact_num = float(record['Proactivity']['Score'])
        Self_num = float(record['Self-Monitoring']['Score'])

        P3_extra.loc[len(P3_extra)] = [
            priD, priE, priP, priC, envD, envE, envP, envC,
            High, Low, Dec, Lead, Energy, Stress,
            Stress_num, Energy_num, Proact_num, Self_num
        ]

    # add to dataset
    P3 = pd.concat([P3, P3_extra], axis=1)
    P3.drop(columns=['Profile Type', 'Id', 'Profile Report', 'Export Date'], inplace=True)

    # convert months
    def monthToNum(shortMonth):
        return {
            'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
            'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
            'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
        }[shortMonth]

    # read P3 data for conscientiousness
    Cons = pd.read_csv(os.path.join('Databases', 'Boldt All Employee Basic P3 Data.csv'))
    Date = Cons['Survey Date'].str.split('-')
    Cons['Day'] = Date.str[0].astype(int)
    Cons['Month'] = Date.str[1].apply(monthToNum)
    Cons['Year'] = Date.str[2].astype(int) + 2000
    Cons['Survey_Date'] = Cons['Month'].astype(str) + '/' + Cons['Day'].astype(str) + '/' + Cons['Year'].astype(str)
    Cons = Cons.rename(columns={'Conscientiousness': 'Cons'})
    Cons['Name'] = (Cons['First Name'].str.strip() + ' ' + Cons['Last Name'].str.strip()).str.lower()

    # build P3 Name column first
    P3['Name'] = (P3['First Name'].str.strip() + ' ' + P3['Last Name'].str.strip()).str.lower()

    # take most recent Cons per person
    Cons['Survey_Date'] = pd.to_datetime(Cons['Survey_Date'])
    Cons = Cons.sort_values('Survey_Date', ascending=False)
    Cons = Cons.drop_duplicates(subset=['Name'])

    # merge Cons into P3 by Name
    P3 = P3.merge(Cons[['Name', 'Cons']], on='Name', how='left')

    # read Drake P3 Profiles for Learning Style
    Drake = pd.read_excel(os.path.join('Databases', 'Drake_P3_Profiles.xlsx'), engine='openpyxl')
    Drake['Name'] = (Drake['FIRST NAME'].str.strip() + ' ' + Drake['LAST NAME'].str.strip()).str.lower()
    Drake = Drake.drop_duplicates(subset=['Name'])
    Drake = Drake[['Name', 'LEARNING STYLE']]
    Drake = Drake.rename(columns={'LEARNING STYLE': 'Learning_Style'})

    # merge Learning Style into P3
    P3 = P3.merge(Drake[['Name', 'Learning_Style']], on='Name', how='left')

    # create binary columns for Pragmatist and Reflector
    P3['Is_Pragmatist'] = (P3['Learning_Style'] == 'Pragmatist').astype(int)
    P3['Is_Reflector'] = (P3['Learning_Style'] == 'Reflector').astype(int)

    P3 = P3[['Name', 'First Name', 'Last Name', 'Survey_Date',
             'Pri_D', 'Pri_E', 'Pri_P', 'Pri_C',
             'Cons', 'Env_D', 'Env_E', 'Env_P', 'Env_C',
             'High_Trait', 'Low_Trait', 'Decision_Style', 'Leadership_Style',
             'Energy_Category', 'Stress_Category', 'Energy', 'Stress',
             'Proactivity', 'Self-Monitoring',
             'Learning_Style', 'Is_Pragmatist', 'Is_Reflector']]

    P3.rename(columns={'First Name': 'First', 'Last Name': 'Last'}, inplace=True)
    P3['First'] = P3['First'].str.strip().str.lower()
    P3['Last'] = P3['Last'].str.strip().str.lower()
    P3 = P3.sort_values(['Last', 'First'], ignore_index=True)

    # take most recent survey per person
    P3['Survey_Date'] = pd.to_datetime(P3['Survey_Date'])
    P3 = P3.sort_values(['First', 'Last', 'Survey_Date'], ascending=False)
    P3 = P3.drop_duplicates(subset=['Name'])
    P3 = P3.sort_values(['First', 'Last'], ascending=True).reset_index(drop=True)

    # fill missing values
    P3['Cons'] = P3['Cons'].fillna(0)
    P3['Is_Pragmatist'] = P3['Is_Pragmatist'].fillna(0)
    P3['Is_Reflector'] = P3['Is_Reflector'].fillna(0)

    # add flex to P3 data
    P3['Total_Flex'] = 0
    for index, test in P3.iterrows():
        flex = (
            abs(test['Pri_D'] - test['Env_D']) +
            abs(test['Pri_E'] - test['Env_E']) +
            abs(test['Pri_P'] - test['Env_P']) +
            abs(test['Pri_C'] - test['Env_C'])
        )
        P3.at[index, 'Total_Flex'] = flex

    # all employees default to zip code 53703
    zip_codes = pd.DataFrame({
        'Name': P3['Name'].tolist(),
        'Zip Code': ['53703'] * len(P3)
    })

    print(f"Total employees loaded: {len(P3)}")
    print(f"Cons null count: {P3['Cons'].isna().sum()}")
    print(f"Cons zero count: {(P3['Cons'] == 0).sum()}")
    print(f"Is_Pragmatist count: {P3['Is_Pragmatist'].sum()}")
    print(f"Is_Reflector count: {P3['Is_Reflector'].sum()}")

    return [P3, zip_codes]


def project_data(data, P3, zip_codes):
    project_data = {}

    project_data['industry'] = data['industry']
    project_data['revenue'] = int(data['revenue'].replace(',', ''))
    project_data['contract'] = data['contract']
    project_data['length'] = int(data['length'].replace(',', ''))

    num_emp = 0
    roles = {'PM': [], 'PE': [], 'PC': [], 'Sup': [], 'PEx': []}
    team = []

    for i in range(1, 11):
        if data[f'name_{i}'] != '':
            num_emp += 1
            role = data[f'role_{i}']
            name = data[f'name_{i}'].strip().lower()
            roles[role] += [name]
            team += [name]

    project_data['sum_emp_std'] = num_emp / project_data['revenue'] * 1000000

    # distance - all employees use default zip 53703
    us = pgeocode.GeoDistance('US')
    project_data['corp_dist'] = us.query_postal_code('54911', data["zip"]) * .621371
    team_dist = us.query_postal_code('53703', data["zip"]) * .621371
    project_data['team_dist'] = team_dist

    # team P3 variables
    P3_data = {}
    P3_data['team_flex'] = 0
    P3_data['team_decision_style'] = 0
    P3_data['energy'] = 0
    P3_data['stress'] = 0
    P3_data['energy_deficit'] = 0
    P3_data['monitoring'] = 0
    P3_data['proactivity'] = 0

    for role in ['team', 'PM', 'PE', 'PEx', 'PC', 'Sup']:
        P3_data[f'{role}_pri_d'] = 0
        P3_data[f'{role}_pri_e'] = 0
        P3_data[f'{role}_pri_p'] = 0
        P3_data[f'{role}_pri_c'] = 0
        P3_data[f'{role}_cons'] = 0
        P3_data[f'{role}_env_d'] = 0
        P3_data[f'{role}_env_e'] = 0
        P3_data[f'{role}_env_p'] = 0
        P3_data[f'{role}_env_c'] = 0
        P3_data[f'{role}_FLAG'] = 0

    for member in team:
        P3_data['team_pri_d'] += P3[P3['Name'] == member]['Pri_D'].item()
        P3_data['team_pri_e'] += P3[P3['Name'] == member]['Pri_E'].item()
        P3_data['team_pri_p'] += P3[P3['Name'] == member]['Pri_P'].item()
        P3_data['team_pri_c'] += P3[P3['Name'] == member]['Pri_C'].item()
        P3_data['team_cons'] += P3[P3['Name'] == member]['Cons'].item()
        P3_data['team_env_d'] += P3[P3['Name'] == member]['Env_D'].item()
        P3_data['team_env_e'] += P3[P3['Name'] == member]['Env_E'].item()
        P3_data['team_env_p'] += P3[P3['Name'] == member]['Env_P'].item()
        P3_data['team_env_c'] += P3[P3['Name'] == member]['Env_C'].item()
        P3_data['team_flex'] += P3[P3['Name'] == member]['Total_Flex'].item()

        decision_style = P3[P3['Name'] == member]['Decision_Style'].item()
        if decision_style == 'Dual':
            P3_data['team_decision_style'] += 0.5
        elif decision_style == 'Rational':
            P3_data['team_decision_style'] += 0
        elif decision_style == 'Intuitive':
            P3_data['team_decision_style'] += 1

        P3_data['energy'] += P3[P3['Name'] == member]['Energy'].item()
        P3_data['stress'] += P3[P3['Name'] == member]['Stress'].item()
        P3_data['energy_deficit'] += (
            P3[P3['Name'] == member]['Energy'].item() -
            P3[P3['Name'] == member]['Stress'].item()
        )
        P3_data['monitoring'] += P3[P3['Name'] == member]['Self-Monitoring'].item()
        P3_data['proactivity'] += P3[P3['Name'] == member]['Proactivity'].item()

    P3_data = {k: v / len(team) for k, v in P3_data.items()}

    medians = {
        'PM_pri_d': -7, 'PM_pri_e': -3, 'PM_pri_p': 2, 'PM_pri_c': 9,
        'PM_cons': 42, 'PM_env_d': 0, 'PM_env_e': -7, 'PM_env_p': 3, 'PM_env_c': 4,
        'PE_pri_d': -10, 'PE_pri_e': -2, 'PE_pri_p': 4, 'PE_pri_c': 8,
        'PE_cons': 40, 'PE_env_d': -2, 'PE_env_e': -6, 'PE_env_p': 6, 'PE_env_c': 4,
        'PC_pri_d': -15, 'PC_pri_e': -3, 'PC_pri_p': 8, 'PC_pri_c': 11,
        'PC_cons': 42, 'PC_env_d': -10, 'PC_env_e': -6, 'PC_env_p': 8, 'PC_env_c': 7,
        'Sup_pri_d': -4, 'Sup_pri_e': -5, 'Sup_pri_p': 4, 'Sup_pri_c': 10,
        'Sup_cons': 40, 'Sup_env_d': 1, 'Sup_env_e': -7, 'Sup_env_p': 3, 'Sup_env_c': 4,
        'PEx_pri_d': -6, 'PEx_pri_e': -3, 'PEx_pri_p': 3, 'PEx_pri_c': 7,
        'PEx_cons': 37, 'PEx_env_d': 0, 'PEx_env_e': -8, 'PEx_env_p': 3, 'PEx_env_c': 2
    }

    for role in ['PM', 'PE', 'PEx', 'PC', 'Sup']:
        if len(roles[role]) == 0:
            P3_data[f'{role}_pri_d'] = medians[f'{role}_pri_d']
            P3_data[f'{role}_pri_e'] = medians[f'{role}_pri_e']
            P3_data[f'{role}_pri_p'] = medians[f'{role}_pri_p']
            P3_data[f'{role}_pri_c'] = medians[f'{role}_pri_c']
            P3_data[f'{role}_cons'] = medians[f'{role}_cons']
            P3_data[f'{role}_env_d'] = medians[f'{role}_env_d']
            P3_data[f'{role}_env_e'] = medians[f'{role}_env_e']
            P3_data[f'{role}_env_p'] = medians[f'{role}_env_p']
            P3_data[f'{role}_env_c'] = medians[f'{role}_env_c']
            P3_data[f'{role}_FLAG'] = 1
        else:
            for member in roles[role]:
                P3_data[f'{role}_pri_d'] += P3[P3['Name'] == member]['Pri_D'].item()
                P3_data[f'{role}_pri_e'] += P3[P3['Name'] == member]['Pri_E'].item()
                P3_data[f'{role}_pri_p'] += P3[P3['Name'] == member]['Pri_P'].item()
                P3_data[f'{role}_pri_c'] += P3[P3['Name'] == member]['Pri_C'].item()
                P3_data[f'{role}_cons'] += P3[P3['Name'] == member]['Cons'].item()
                P3_data[f'{role}_env_d'] += P3[P3['Name'] == member]['Env_D'].item()
                P3_data[f'{role}_env_e'] += P3[P3['Name'] == member]['Env_E'].item()
                P3_data[f'{role}_env_p'] += P3[P3['Name'] == member]['Env_P'].item()
                P3_data[f'{role}_env_c'] += P3[P3['Name'] == member]['Env_C'].item()

            P3_data[f'{role}_pri_d'] /= len(roles[role])
            P3_data[f'{role}_pri_e'] /= len(roles[role])
            P3_data[f'{role}_pri_p'] /= len(roles[role])
            P3_data[f'{role}_pri_c'] /= len(roles[role])
            P3_data[f'{role}_cons'] /= len(roles[role])
            P3_data[f'{role}_env_d'] /= len(roles[role])
            P3_data[f'{role}_env_e'] /= len(roles[role])
            P3_data[f'{role}_env_p'] /= len(roles[role])
            P3_data[f'{role}_env_c'] /= len(roles[role])

    project_data.update(P3_data)
    return project_data
