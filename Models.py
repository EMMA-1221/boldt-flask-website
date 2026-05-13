def cim_industry_model(industry):
    """
    CIM prediction based on industry only.
    """
    healthcare  = 1 if industry == 'Healthcare'   else 0
    industrial  = 1 if industry == 'Industrial'   else 0
    institutional = 1 if industry == 'Institutional' else 0
    power       = 1 if industry == 'Power'        else 0

    return (0.07679
            - 0.05988 * healthcare
            - 0.03864 * industrial
            - 0.06722 * institutional
            - 0.02548 * power)


def cim_contract_model(contract):
    """
    CIM prediction based on contract type only.
    """
    ilpd = 1 if contract == 'ILPD' else 0
    ls   = 1 if contract == 'LS'   else 0
    tm   = 1 if contract == 'TM'   else 0

    return (0.024510
            - 0.028579 * ilpd
            + 0.017016 * ls
            + 0.024405 * tm)


def fpm_industry_model(industry):
    """
    FPM prediction based on industry only.
    """
    healthcare    = 1 if industry == 'Healthcare'   else 0
    industrial    = 1 if industry == 'Industrial'   else 0
    institutional = 1 if industry == 'Institutional' else 0
    power         = 1 if industry == 'Power'        else 0

    return (0.175515
            - 0.045351 * healthcare
            + 0.011242 * industrial
            - 0.049213 * institutional
            + 0.006175 * power)


def fpm_contract_model(contract):
    """
    FPM prediction based on contract type only.
    """
    ilpd = 1 if contract == 'ILPD' else 0
    ls   = 1 if contract == 'LS'   else 0
    tm   = 1 if contract == 'TM'   else 0

    return (0.132791
            - 0.067536 * ilpd
            + 0.050698 * ls
            + 0.050820 * tm)


def cim_model(person):
    """
    CIM prediction using Alexa's decision tree (per person).
    Input: person dict with keys: days, industry, contract, is_pragmatist
    Output: predicted CIM value
    """
    days          = person['days']
    healthcare    = 1 if person['industry'] == 'Healthcare'   else 0
    industrial    = 1 if person['industry'] == 'Industrial'   else 0
    institutional = 1 if person['industry'] == 'Institutional' else 0
    contract_ls   = 1 if person['contract'] == 'LS'           else 0
    contract_gmp  = 1 if person['contract'] == 'GMP'          else 0
    is_pragmatist = person['is_pragmatist']

    # Node 1
    L1 = (-0.0000260 * days
          - 0.049 * healthcare
          - 0.040 * industrial
          - 0.107 * institutional
          + 0.021 * contract_ls)

    if L1 <= -0.1097:
        if days <= 115.50:
            # Node 4
            pred = -11.71 + 0.109 * days
        else:
            if contract_gmp == 1:
                # Node 11
                pred = 0.30 - 0.32 * institutional
            else:
                if days <= 900.50:
                    # Node 20
                    pred = 0.38 - 0.00110 * days + 0.16 * is_pragmatist
                else:
                    # Node 21
                    pred = -0.017 + 0.000024 * days
    else:
        # Node 3
        pred = (0.0804
                - 0.000064 * days
                - 0.052 * healthcare
                - 0.038 * industrial
                - 0.041 * institutional)

    return pred


def fpm_model(person):
    """
    FPM prediction using Alexa's decision tree (per person).
    Input: person dict with keys: days, primary_e, industry, contract, is_reflector, env_d, proactivity
    Output: predicted FPM value
    """
    days          = person['days']
    primary_e     = person['primary_e']
    healthcare    = 1 if person['industry'] == 'Healthcare'   else 0
    institutional = 1 if person['industry'] == 'Institutional' else 0
    contract_ls   = 1 if person['contract'] == 'LS'           else 0
    contract_tm   = 1 if person['contract'] == 'TM'           else 0
    contract_ilpd = 1 if person['contract'] == 'ILPD'         else 0
    is_reflector  = person['is_reflector']
    env_d         = person['env_d']
    proactivity   = person['proactivity']

    # Node 1
    L1 = (-0.000041 * days
          - 0.0012 * primary_e
          - 0.035 * healthcare
          - 0.12 * institutional
          + 0.027 * contract_ls
          + 0.026 * contract_tm)

    if L1 <= 0.0105:
        L2 = (-0.000029 * days
              - 0.0014 * primary_e
              - 0.035 * healthcare
              - 0.11 * institutional
              + 0.036 * contract_tm)

        if L2 <= -0.0272:
            L4 = (-0.084 * institutional
                  + 0.041 * contract_ls
                  + 0.095 * contract_tm)

            if L4 <= -0.0634:
                if days <= 101:
                    # Node 16
                    pred = -0.69 - 0.0079 * days + 0.0104 * proactivity
                else:
                    # Node 17
                    pred = 0.096 - 0.000107 * days
            else:
                if days <= 146.50:
                    # Node 18
                    pred = 0.18 - 0.076 * healthcare
                else:
                    # Node 19
                    pred = 0.092 - 0.087 * institutional
        else:
            # Node 5
            pred = (0.16
                    - 0.0000904 * days
                    - 0.12 * contract_ilpd
                    - 0.026 * contract_ls
                    + 0.022 * is_reflector)
    else:
        # Node 3
        pred = 0.18 - 0.00013 * days - 0.001003 * env_d

    return pred


def get_person_data(name, role, P3, project):
    """
    Build a person dict with all variables needed for CIM and FPM models.
    If name is None (no PM or Sup selected), use median values.
    """
    medians = {
        'PM':  {'primary_e': -3,  'env_d': 0,  'proactivity': 70, 'is_pragmatist': 0, 'is_reflector': 0},
        'Sup': {'primary_e': -5,  'env_d': 1,  'proactivity': 70, 'is_pragmatist': 0, 'is_reflector': 0},
        'PE':  {'primary_e': -2,  'env_d': -2, 'proactivity': 70, 'is_pragmatist': 0, 'is_reflector': 0},
        'PC':  {'primary_e': -3,  'env_d': -10,'proactivity': 70, 'is_pragmatist': 0, 'is_reflector': 0},
        'PEx': {'primary_e': -3,  'env_d': 0,  'proactivity': 70, 'is_pragmatist': 0, 'is_reflector': 0},
    }

    if name is None or name == '':
        defaults = medians.get(role, medians['PM'])
        return {
            'name': '',
            'role': role,
            'days': project['length'],
            'industry': project['industry'],
            'contract': project['contract'],
            **defaults
        }

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
