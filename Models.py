def all_data_model(row):
    return 1.5299628 + \
            -.0009855*row['corp_dist']*row['PEx_env_d'] + \
            .0117729*row['PM_pri_p']*row['PM_env_c'] + \
            -0.0201809*(row['PC_env_e']**2)

def industry_model(row):
    industry = row['industry']
    if industry == "Industrial":
        return -.2259 + 1.3365 * row['sum_emp_std']
    
    elif industry == "Commercial":
        return -.2259 + 1.3365 * row['sum_emp_std']
    
    elif industry == "Healthcare":
        return 1.443 + -0.06901*row['sum_emp_std']*row['team_env_d'] + \
                -.1252*row['sum_emp_std']*row['Sup_env_d'] + \
                .0006951*row['team_dist']*row['PE_pri_p'] + \
                -.08912*row['team_pri_e']*row['energy_deficit'] + \
                -.004186*row['team_pri_c']*row['PE_cons'] + \
                .0288*row['PM_pri_p']*row['PC_pri_e'] + \
                -.01073*row['PC_pri_d']*row['PEx_env_p'] + \
                -.0000000009594*(row['corp_dist']**3)
    
    elif industry == "Institutional":
        return -3.30544 + .05231*row['PM_pri_p']*row['PM_env_c']
        
    elif industry == "Power":
        return -1.3945 + -.3135*row['sum_emp_std']
        
def revenue_model(row):
    revenue = row['revenue']
    if revenue < 3000000:
        return 2.847 + -.9053*row['sum_emp_std']
        
    elif (revenue > 3000000) & (revenue < 10000000):
        return -4.054 + \
                -.0003381*row['corp_dist']*row['team_env_p'] +\
                -.0002166*row['corp_dist']*row['PEx_env_d'] +\
                .0007864*row['corp_dist']*row['PEx_env_p'] +\
                -.0009598*row['team_dist']*row['team_pri_d'] +\
                -.03612*row['team_pri_e']*row['PC_env_e'] +\
                .02957*row['PM_pri_p']*row['PM_env_c'] +\
                -.01029*row['PM_env_e']*row['PE_pri_d'] +\
                -.006630*row['PM_env_e']*row['PC_env_e'] +\
                .009439*row['PM_env_p']*row['Sup_pri_d'] +\
                -.008287*row['PE_env_p']*row['PC_pri_e'] +\
                -.02423*row['PC_pri_e']*row['PC_env_e'] +\
                .02056*row['PC_env_d']*row['Sup_pri_p'] +\
                0.01866*row['PC_env_e']*row['Sup_pri_d'] +\
                -.009108*row['PC_env_p']*row['Sup_pri_p'] +\
                -.007453*row['Sup_cons']*row['Sup_env_e'] +\
                .02981*row['Sup_cons']*row['monitoring'] +\
                .03481*row['Sup_env_e']*row['monitoring'] +\
                .007397*(row['PE_pri_p']**2) +\
                .005016*(row['PC_env_e']**2) +\
                .000008593*(row['PM_cons']**3)
        
    elif (revenue > 10000000):
        return 1.055 +\
                -.1380*row['PM_pri_d'] +\
                -.2974*row['PEx_pri_d'] +\
                -.0000694*(row['team_cons']**3)
    
def length_model(row):
    length = int(row['length'])
    if length < 365:
        return 1.453 + -.000000001372*(row['corp_dist']**3)
    elif length >= 365:
        return 6.12574 +\
                0.17014*row['PM_cons'] +\
                .17587*row['PE_pri_e'] +\
                .16681*row['PC_env_e'] +\
                -.068*row['PC_env_p'] +\
                .42522*row['PEx_env_p']
    
def contract_model(row):
    contract = row['contract']
    if contract == "LS":
        return -1.3940 + .9463*row['sum_emp_std']
    elif contract == "TM":
        return -11.00867 +\
                .48638*row['team_env_e'] +\
                -.54357*row['team_env_c'] +\
                -.03081*row['PM_pri_c'] +\
                -.28070*row['PM_env_d'] +\
                .49849*row['PE_cons'] +\
                .25397*row['PC_pri_p'] +\
                .26425*row['PC_pri_c'] +\
                -.25786*row['Sup_cons'] +\
                -.1624*row['PEx_pri_d'] +\
                -.07265*row['PEx_pri_e'] +\
                .10856*row['PEx_pri_c'] +\
                -14.48496*row['team_decision_style'] +\
                .95866*row['stress'] +\
                .11916*row['proactivity'] +\
                -.93993*row['PM_FLAG'] +\
                -2.09484*row['Sup_FLAG']
    
    elif contract == "GMP":
        return 1.160271 +\
                -.0230663*row['Sup_env_d'] +\
                .006645*(row['PC_env_d']**2)
        
    elif contract == "TM-GMP":
        return .4561284 +\
                -.0010625*row['team_dist']*row['PM_env_c'] +\
                -.004444*row['PM_pri_c']*row['PE_cons'] +\
                .0077118*row['Sup_cons']*row['PEx_env_p']
