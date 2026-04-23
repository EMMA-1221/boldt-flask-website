def cim_model(person):
    """
    CIM (Change in Margin) prediction using Alexa's decision tree.
    Input: person dict with keys: days, industry, contract, is_pragmatist, proactivity
    Output: predicted CIM value
    """
    days = person['days']
    healthcare = 1 if person['industry'] == 'Healthcare' else 0
    industrial = 1 if person['industry'] == 'Industrial' else 0
    institutional = 1 if person['industry'] == 'Institutional' else 0
    contract_ls = 1 if person['contract'] == 'LS' else 0
    contract_gmp = 1 if person['contract'] == 'GMP' else 0
    is_pragmatist = person['is_pragmatist']

    # Node 1: L1 = -0.26E-4*Days - 0.49E-1*Healthcare - 0.4E-1*Industrial - 0.107*Institutional + 0.21E-1*LS
    L1 = (-0.0000260 * days
          - 0.049 * healthcare
          - 0.040 * industrial
          - 0.107 * institutional
          + 0.021 * contract_ls)

    if L1 <= -0.1097:
        # Node 2: Days <= 115.50
        if days <= 115.50:
            # Terminal Node 4
            pred = -11.71 + 0.109 * days
        else:
            # Node 5: V1 = GMP
            if contract_gmp == 1:
                # Terminal Node 11
                pred = 0.30 - 0.32 * institutional
            else:
                # Node 10: Days <= 900.50
                if days <= 900.50:
                    # Terminal Node 20
                    pred = 0.38 - 0.00110 * days + 0.16 * is_pragmatist
                else:
                    # Terminal Node 21
                    pred = -0.017 + 0.000024 * days
    else:
        # Terminal Node 3
        pred = (0.0804
                - 0.000064 * days
                - 0.052 * healthcare
                - 0.038 * industrial
                - 0.041 * institutional)

    return pred


def fpm_model(person):
    """
    FPM (Final Profit Margin) prediction using Alexa's decision tree.
    Input: person dict with keys: days, primary_e, industry, contract, is_reflector, env_d, proactivity
    Output: predicted FPM value
    """
    days = person['days']
    primary_e = person['primary_e']
    healthcare = 1 if person['industry'] == 'Healthcare' else 0
    institutional = 1 if person['industry'] == 'Institutional' else 0
    contract_ls = 1 if person['contract'] == 'LS' else 0
    contract_tm = 1 if person['contract'] == 'TM' else 0
    contract_ilpd = 1 if person['contract'] == 'ILPD' else 0
    is_reflector = person['is_reflector']
    env_d = person['env_d']
    proactivity = person['proactivity']

    # Node 1: L1 = -0.41E-4*Days - 0.12E-2*PrimaryE - 0.035*Healthcare - 0.12*Institutional + 0.027*LS + 0.026*TM
    L1 = (-0.000041 * days
          - 0.0012 * primary_e
          - 0.035 * healthcare
          - 0.12 * institutional
          + 0.027 * contract_ls
          + 0.026 * contract_tm)

    if L1 <= 0.0105:
        # Node 2: L2 <= -0.0272
        L2 = (-0.000029 * days
              - 0.0014 * primary_e
              - 0.035 * healthcare
              - 0.11 * institutional
              + 0.036 * contract_tm)

        if L2 <= -0.0272:
            # Node 4: L4 <= -0.0634
            L4 = (-0.084 * institutional
                  + 0.041 * contract_ls
                  + 0.095 * contract_tm)

            if L4 <= -0.0634:
                # Node 8: Days <= 101
                if days <= 101:
                    # Terminal Node 16
                    pred = -0.69 - 0.0079 * days + 0.0104 * proactivity
                else:
                    # Terminal Node 17
                    pred = 0.096 - 0.000107 * days
            else:
                # Node 9: Days <= 146.50
                if days <= 146.50:
                    # Terminal Node 18
                    pred = 0.18 - 0.076 * healthcare
                else:
                    # Terminal Node 19
                    pred = 0.092 - 0.087 * institutional
        else:
            # Terminal Node 5
            pred = (0.16
                    - 0.0000904 * days
                    - 0.12 * contract_ilpd
                    - 0.026 * contract_ls
                    + 0.022 * is_reflector)
    else:
        # Terminal Node 3
        pred = 0.18 - 0.00013 * days - 0.001003 * env_d

    return pred


def get_person_data(name, role, P3, project):
    """
    Build a person dict with all variables needed for CIM and FPM models.
    """
    row = P3[P3['Name'] == name].iloc[0]
    return {
        'name': name,
        'role': role,
        'days': project['length'],
        'industry': project['industry'],
        'contract': project['contract'],
        'primary_e': row['Pri_E'],
        'env_d': row['Env_D'],
        'proactivity': row['Proactivity'],
        'is_pragmatist': int(row['Is_Pragmatist']),
        'is_reflector': int(row['Is_Reflector']),
    }
