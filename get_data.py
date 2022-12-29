import pandas as pd
import random
import numpy as np


path_old = 'YogevMatanYoavindGFPslong.xlsx'
path_new = 'NewData.xlsx'
path_2_6_2022 = 'YogevMatanYoavTecanExp5.xlsx'
path_9_6_2022 = 'FinalExperiment.xlsx'

TIME_COLUMN = 'Time [s]'
SEC = 1
MIN = SEC * 60
HOUR = MIN * 60

ML = 1
MML = ML / 1000

BACTERIA_PER_ML_1_OD = 10**9

excel_config = [
    {
        'path': path_old,
        'starting_bacteria': 10**4,
        'liquid_per_well': 180 * MML,
        'sheet_name': 'Sheet4', # Third experiment (Glucose and Amino)
        'od': [60,356],
        'yfp': [1063, 1359],
        'well_layout': [
                              'B5', 'B6', 'B7', 'B8', 'B9',        'B11',
            'C2', 'C3', 'C4', 'C5', 'C6', 'C7',             'C10', 'C11',
            'D2', 'D3', 'D4', 'D5', 'D6', 'D7',             'D10', 'D11',
            'E2', 'E3', 'E4',             'E7',             'E10', 'E11',
            'F2', 'F3', 'F4',             'F7',             'F10', 'F11',
        ],
        'data_cleaning': {
            ('C4', '0.5A'): ['C2', 'C3',],
            ('D4', '0.5A'): ['D2', 'D3',],
            ('E4', 'A'): ['E2', 'E3',],
            ('F4', 'A'): ['F2', 'F3'],
            ('C7', '0.5A_G'): ['C5', 'C6'],
            ('D7', '0.5A_G'): ['D5', 'D6'],
            ('B7', 'G'): ['B5', 'B6', 'B8', 'B9'],
            ('C4', '0.5A_control'): ['C11'],
            ('D4', '0.5A_control'): ['D11'],
            ('E4', 'A_control'): ['E11'],
            ('F4', 'A_control'): ['F11'],
            ('C7', '0.5A_G_control'): ['C10'],
            ('D7', '0.5A_G_control'): ['D10'],
            ('B7', 'G_control'): ['E10', 'F10'],
        },
    },
    {
        'path': path_old,
        'starting_bacteria': 10**4,
        'liquid_per_well': 200 * MML,
        'sheet_name': 'Sheet3', # Second experiment we did (Different ATC's)
        'od': [60, 386],
        'yfp': [1063, 1389],
        'well_layout': [
            'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11',
            'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11',
            'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11',
            'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11',
            'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11',
            'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11',
        ],
        'data_cleaning': {
            ('G11', 'type_1_500'): ['B2', 'C2'],
            ('G11', 'type_2_500'): ['D2', 'E2'],
            ('G11', 'type_3_500'): ['F2', 'G2'],
            ('G11', 'type_1_1000'): ['B3', 'C3'],
            ('G11', 'type_2_1000'): ['D3', 'E3'],
            ('G11', 'type_3_1000'): ['F3', 'G3'],
            ('G11', 'type_1_1500'): ['B4', 'C4'],
            ('G11', 'type_2_1500'): ['D4', 'E4'],
            ('G11', 'type_3_1500'): ['F4', 'G4'],
            ('E11', 'type_1_2500'): ['B5', 'C5'],
            ('E11', 'type_2_2500'): ['D5', 'E5'],
            ('E11', 'type_3_2500'): ['F5', 'G5'],
            ('E11', 'type_1_5000'): ['B6', 'C6'],
            ('E11', 'type_2_5000'): ['D6', 'E6'],
            ('E11', 'type_3_5000'): ['F6', 'G6'],
            ('E11', 'type_1_7500'): ['B7', 'C7'],
            ('E11', 'type_2_7500'): ['D7', 'E7'],
            ('E11', 'type_3_7500'): ['F7', 'G7'],
            ('C11', 'type_1_10000'): ['B8', 'C8'],
            ('C11', 'type_2_10000'): ['D8', 'E8'],
            ('C11', 'type_3_10000'): ['F8', 'G8'],
            ('C11', 'type_1_15000'): ['B9', 'C9'],
            ('C11', 'type_2_15000'): ['D9', 'E9'],
            ('C11', 'type_3_15000'): ['F9', 'G9'],
            ('C11', 'type_1_20000'): ['B10', 'C10'],
            ('C11', 'type_2_20000'): ['D10', 'E10'],
            ('C11', 'type_3_20000'): ['F10', 'G10'],
            ('C11', 'type_1_control'): ['B11'],
            ('C11', 'type_2_control'): ['D11'],
            ('C11', 'type_3_control'): ['F11'],
        },
    },
    {
        'path': path_old,
        'starting_bacteria': 10**4,
        'liquid_per_well': 180 * MML,
        'sheet_name': 'Sheet2', # First experiment we did
        'od': [61, 287],
        'yfp': [1064, 1290],
        'well_layout': [
            'B5', 'B6',
            'C5', 'C6', 'C7',
            'D5', 'D6', 'D7',
            'E5', 'E6', 'E7',
            'F5', 'F6', 'F7',
            'G5', 'G6', 'G7',
        ],
        'data_cleaning': {
            ('B5', 'no_atc'): ['E5', 'F5', 'G5'],
            ('B6', 'atc'): ['E6', 'F6', 'G6'],
            ('C7', 'double_atc'): ['E7', 'F7', 'G7'],
        },
    },
    {
        'path': path_new,
        'starting_bacteria': 10**4,
        'liquid_per_well': 180 * MML,
        'sheet_name': 'Sheet2', # Fourth experiment (More Glucose and Amino)
        'od': [67, 511],
        'yfp': [2073, 2517],
        'well_layout': [
            'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9',
            'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
            'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9',
            'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9',
            'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
            'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9',
        ],
        'data_cleaning': {
            ('G2', '0.5A'): ['B2', 'C2', 'D2'],
            ('G2', '0.5A_control'): ['E2', 'F2'],
            ('G3', '0.75A'): ['B3', 'C3', 'D3'],
            ('G3', '0.75A_control'): ['E3', 'F3'],
            ('G4', 'A'): ['B4', 'C4', 'D4'],
            ('G4', 'A_control'): ['E4', 'F4'],
            ('G5', '0.5A_0.5G'): ['B5', 'C5', 'D5'],
            ('G5', '0.5A_0.5G_control'): ['E5', 'F5'],
            ('G6', '0.5A_G'): ['B6', 'C6', 'D6'],
            ('G6', '0.5A_G_control'): ['E6', 'F6'],
            ('G7', 'A_0.5G'): ['B7', 'C7', 'D7'],
            ('G7', 'A_0.5G_control'): ['E7', 'F7'],
            ('G8', '0.75A_G'): ['B8', 'C8', 'D8'],
            ('G8', '0.75A_G_control'): ['E8', 'F8'],
            ('G9', 'A_G'): ['B9', 'C9', 'D9'],
            ('G9', 'A_G_control'): ['E9', 'F9'],
        },
    },
    {
        'path': path_2_6_2022,
        'starting_bacteria': 6*10**4,
        'liquid_per_well': 180 * MML,
        'sheet_name': 'Sheet2', # Fifth experiment (More Glucose and Amino)
        'od': [47, 535],
        'yfp': [1050, 1538],
        'well_layout': [
            'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10',
            'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10',
            'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10',
            'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10',
            'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10',
            'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10',
        ],
        'data_cleaning': {
            ('G2',  '0.5A'): ['B2', 'C2', 'D2'], 
            ('G2',  '0.5A_control'): ['E2', 'F2'],
            ('G3',  '0.6A'): ['B3', 'C3', 'D3'],
            ('G3',  '0.6A_control'): ['E3', 'F3'],
            ('G4',  '0.75A'): ['B4', 'C4', 'D4'],
            ('G4',  '0.75A_control'): ['E4', 'F4'],
            ('G5',  'A'): ['B5', 'C5', 'D5'],
            ('G5',  'A_control'): ['E5', 'F5'],
            ('G6',  '1.5A'): ['B6', 'C6', 'D6'],
            ('G6',  '1.5A_control'): ['E6', 'F6'],
            ('G7',  '0.5A_0.5G'): ['B7', 'C7', 'D7'],
            ('G7',  '0.5A_0.5G_control'): ['E7', 'F7'],
            ('G8',  '0.5A_G'): ['B8', 'C8', 'D8'],
            ('G8',  '0.5A_G_control'): ['E8', 'F8'],
            ('G9',  'A_0.5G'): ['B9', 'C9', 'D9'],
            ('G9',  'A_0.5G_control'): ['E9', 'F9'],
            ('G10', 'A_G'): ['B10', 'C10', 'D10'],
            ('G10', 'A_G_control'): ['E10', 'F10'],
        },
     },
     {
        'path': path_9_6_2022,
        'starting_bacteria': 6*10**4,
        'liquid_per_well': 180 * MML,
        'sheet_name': 'Sheet2', # Sixth experiment (Different amino acid composition in solution)
        'od': [60, 403],
        'yfp': [866, 1209],
        'well_layout': [
            'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10',
            'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10',
            'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10',
            'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10',
            'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10',
            'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10',
        ],
        'data_cleaning': {
            ('G2',  'A'): ['B2', 'C2', 'D2'], 
            ('G2',  'A_control'): ['E2', 'F2'],
            ('G3',  'A_ala'): ['B3', 'C3', 'D3'],
            ('G3',  'A_ala_control'): ['E3', 'F3'],
            ('G4',  'A_ala_gly'): ['B4', 'C4', 'D4'],
            ('G4',  'A_ala_gly_control'): ['E4', 'F4'],
            ('G5',  'A_G'): ['B5', 'C5', 'D5'],
            ('G5',  'A_G_control'): ['E5', 'F5'],
            ('G6',  'A_G_ala'): ['B6', 'C6', 'D6'],
            ('G6',  'A_G_ala_control'): ['E6', 'F6'],
            ('G7',  'A_G_ala_gly'): ['B7', 'C7', 'D7'],
            ('G7',  'A_G_ala_gly_control'): ['E7', 'F7'],
            ('G8',  '0.5A_0.5G'): ['B8', 'C8', 'D8'],
            ('G8',  '0.5A_0.5G_control'): ['E8', 'F8'],
            ('G9',  '0.5A_G'): ['B9', 'C9', 'D9'],
            ('G9',  '0.5A_G_control'): ['E9', 'F9'],
            ('G10', 'A_0.5G'): ['B10', 'C10', 'D10'],
            ('G10', 'A_0.5G_control'): ['E10', 'F10'],
        },
    },
]

### PARSING AND UTILS ###

def recreate_clean_data(raw_data, time_column, data_cleaning):
    clean_wells = {}
    clean_wells['time'] = raw_data[time_column] * (SEC/HOUR)  # Convert to hours

    for control_well, wells in data_cleaning.items():
        for index, well in enumerate(wells):
            well_index = index
            new_well_name = '{well_name}_{index}'.format(well_name=control_well[1], index=well_index)
            while new_well_name in clean_wells:
                well_index += 1
                new_well_name = '{well_name}_{index}'.format(well_name=control_well[1], index=well_index + 1)

            clean_wells[new_well_name] = np.abs(raw_data[well] - raw_data[control_well[0]])

    return pd.DataFrame(clean_wells)


def parse_excel_files(path, sheet_name, od, yfp, well_layout, data_cleaning):
    columns_to_keep = [TIME_COLUMN] + well_layout
    data = {}
    data['od_raw'] = pd.read_excel(
        io=path,
        sheet_name=sheet_name,
        header=0,
        skiprows=od[0] - 1,
        nrows=od[1] - od[0],
        na_values=['OVER'], # For some reason this appears in some cells
    )

    data['od_raw'] = data['od_raw'][columns_to_keep]
    clean_data = recreate_clean_data(
        raw_data=data['od_raw'],
        time_column=TIME_COLUMN,
        data_cleaning=data_cleaning,
    )
    data['od'] = clean_data
    
    data['yfp_raw'] = pd.read_excel(
        io=path,
        sheet_name=sheet_name,
        header=0,
        skiprows=yfp[0] - 1,
        nrows=yfp[1] - yfp[0],
        na_values=['OVER'], 
    )

    data['yfp_raw'] = data['yfp_raw'][columns_to_keep]
    clean_data = recreate_clean_data(
        raw_data=data['yfp_raw'],
        time_column=TIME_COLUMN,
        data_cleaning=data_cleaning,
    )
    data['yfp'] = clean_data

    return data

def average_n_dots(x, n):
    if len(x) % n != 0:
        cut_length = len(x) % n
        x = x[:-cut_length]

    averaged_data = np.mean(x.reshape(-1, n), axis=1)
    return averaged_data

def get(data='all'):
    conf=[]
    res=[]
    if data=='all':
        for i in range(len(excel_config)):
            conf[i] = excel_config[i]
            res[i] = parse_excel_files(
                conf[i]['path'],
                conf[i]['sheet_name'],
                conf[i]['od'],
                conf[i]['yfp'],
                conf[i]['well_layout'],
                conf[i]['data_cleaning']
                )
    elif type(data)==int:
        conf[data] = excel_confdata g[i]
        res[data] = parse_excel_files(
            conf[data]['path'],
            conf[data]['sheet_name'],
            conf[data]['od'],
            conf[data]['yfp'],
            conf[data]['well_layout'],
            conf[data]['data_cleaning']
            )
    return res[:]