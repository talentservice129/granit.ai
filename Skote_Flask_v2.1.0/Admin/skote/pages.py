from flask import Blueprint,render_template, request
from flask_login import login_required
import pandas as pd

pages = Blueprint('page',__name__,template_folder='templates',
    static_folder='static',)
date_column = 'Last Scan Date'

@pages.route('/main')
@login_required
def page_main():
    dp_fields = ['DP_001', 'DP_002', 'DP_003', 'DP_004', 'DP_005', 'DP_006', 'DP_007', 'DP_008', 'DP_009', 'DP_010', 'DP_016', 'DP_017', 'DP_018', 'DP_019', 'DP_049', 'DP_051','DP_052', 'DP_053', 'DP_054', 'DP_055', 'DP_056', 'DP_500', 'DP_501', 'DP_502', 'DP_503', 'DP_504', 'DP_505', 'DP_506', 'DP_507', 'DP_508', 'DP_509', 'DP_510', 'DP_511', 'DP_512', 'DP_513', 'DP_514', 'DP_515', 'DP_516', 'DP_517']
    df = pd.read_csv('../../Sample_Data.csv', encoding='iso-8859-1')
    df = df.query('DP_ID in @dp_fields')
    df['Internal ID'] = ''
    extract = request.args.get("extract")
    df[date_column] = df['Filing_Date']

    if extract == 'true':
        latest = df.pivot_table(index=['RCS_ID', date_column], columns='DP_Name', values='DP_Value', aggfunc='first').reset_index()
        latest[date_column] = pd.to_datetime(latest[date_column],format='mixed')
        latest = latest.sort_values(by=date_column, ascending=False)
        latest[date_column] = latest[date_column].dt.strftime('%m/%d/%Y')
    else:
        pivot_df = df.pivot_table(index=['RCS_ID', date_column], columns='DP_Name', values='DP_Value', aggfunc='first').reset_index()
        pivot_df[date_column] = pd.to_datetime(pivot_df[date_column],format='mixed')
        df_sorted = pivot_df.sort_values(by=date_column, ascending=False)
        latest = df_sorted.groupby('RCS_ID').first().reset_index()

        for index, row in latest.iterrows():
            filtered = df_sorted[(df_sorted['RCS_ID'] == row['RCS_ID']) & ((df_sorted['Capital Fixed'] == 'TRUE') | (df_sorted['Capital Variable'] == 'TRUE'))]

            print(filtered.iloc[0]['Capital amount'])

            if filtered.empty == False:
                latest.at[index, 'Capital Fixed'] = filtered.iloc[0]['Capital Fixed']
                latest.at[index, 'Capital Variable'] = filtered.iloc[0]['Capital Variable']
                latest.at[index, 'Capital amount'] = filtered.iloc[0]['Capital amount']

            filtered = df_sorted[(df_sorted['RCS_ID'] == row['RCS_ID']) & ((df_sorted['Duration unlimited'] == 'TRUE') | (df_sorted['Duration limited'] == 'TRUE') | (df_sorted['Duration extended'] == 'TRUE'))]

            if filtered.empty == False:
                latest.at[index, 'Duration unlimited'] = filtered.iloc[0]['Duration unlimited']
                latest.at[index, 'Duration limited'] = filtered.iloc[0]['Duration limited']
                latest.at[index, 'Duration extended'] = filtered.iloc[0]['Duration extended']
                latest.at[index, 'Duration end date'] = filtered.iloc[0]['Duration end date']
            
        latest[date_column] = latest[date_column].dt.strftime('%m/%d/%Y')

    return render_template('pages/main.html', headers = latest.columns.tolist(), data = latest.values)

@pages.route('/main/kpis')
@login_required
def page_main_kpis():
    df = pd.read_csv('../../Sample_Data.csv', encoding='iso-8859-1')
    df['Internal ID'] = ''
    extract = request.args.get("extract")

    if extract == 'true':
        latest_data_per_field_id = df
    else:
        date_column = 'Filing_Date'
        df[date_column] = pd.to_datetime(df[date_column])
        df_sorted = df.sort_values(by=date_column, ascending=False)
        latest_data_per_field_id = df_sorted.groupby('RCS_ID').first().reset_index()
        latest_data_per_field_id[date_column] = latest_data_per_field_id[date_column].dt.strftime('%m/%d/%Y')

    return render_template('pages/main-kpis.html', headers = latest_data_per_field_id.columns.tolist(), data = latest_data_per_field_id.values)

@pages.route('/main/history')
@login_required
def page_main_history():
    df = pd.read_csv('../../Sample_Data.csv', encoding='iso-8859-1')
    df = df.drop(['Only API', 'SQL_002', 'DP_ID', 'Unique_ID'], axis=1)
    return render_template('pages/main-history.html', headers = df.columns.tolist(), data = df.values)

@pages.route('/entity')
@login_required
def page_entity():
    dp_fields = ['DP_500', 'DP_501', 'DP_502', 'DP_507', 'DP_508', 'DP_503', 'DP_504', 'DP_505', 'DP_506', 'DP_513', 'DP_514', 'DP_509', 'DP_510', 'DP_511', 'DP_512', 'DP_515','DP_516', 'DP_517', 'DP_002', 'DP_003', 'DP_004', 'DP_005', 'DP_055', 'DP_056']
    df = pd.read_csv('../../Sample_Data.csv', encoding='iso-8859-1')
    df = df.query('DP_ID in @dp_fields')
    df['Jurisdiction'] = ''
    df[date_column] = df['Filing_Date']

    pivot_df = df.pivot_table(index=['RCS_ID', date_column], columns='DP_Name', values='DP_Value', aggfunc='first').reset_index()
    pivot_df[date_column] = pd.to_datetime(pivot_df[date_column])
    df_sorted = pivot_df.sort_values(by=date_column, ascending=False)
    latest = df_sorted.groupby('RCS_ID').first().reset_index()
    latest[date_column] = latest[date_column].dt.strftime('%m/%d/%Y')
    
    return render_template('pages/entity.html', headers = latest.columns.tolist(), data = latest.values)

@pages.route('/entity/accounting')
@login_required
def page_entity_accounting():
    dp_fields = ['DP_051', 'DP_052', 'DP_053', 'DP_054', 'DP_006', 'DP_007', 'DP_008', 'DP_009']
    df = pd.read_csv('../../Sample_Data.csv', encoding='iso-8859-1')
    df = df.query('DP_ID in @dp_fields')
    df['Jurisdiction'] = ''
    df[date_column] = df['Filing_Date']

    pivot_df = df.pivot_table(index=['RCS_ID', date_column], columns='DP_Name', values='DP_Value', aggfunc='first').reset_index()
    pivot_df[date_column] = pd.to_datetime(pivot_df[date_column], format='mixed')
    df_sorted = pivot_df.sort_values(by=date_column, ascending=False)
    latest = df_sorted.groupby('RCS_ID').first().reset_index()
    latest[date_column] = latest[date_column].dt.strftime('%m/%d/%Y')

    for index, row in latest.iterrows():
        filtered = df_sorted[(df_sorted['RCS_ID'] == row['RCS_ID']) & ((df_sorted['Capital Fixed'] == 'TRUE') | (df_sorted['Capital Variable'] == 'TRUE'))]

        if filtered.empty == False:
            latest.at[index, 'Capital Fixed'] = filtered.iloc[0]['Capital Fixed']
            latest.at[index, 'Capital Variable'] = filtered.iloc[0]['Capital Variable']
            latest.at[index, 'Capital amount'] = filtered.iloc[0]['Capital amount']
    
    return render_template('pages/entity-accounting.html', headers = latest.columns.tolist(), data = latest.values)

@pages.route('/entity/registrations')
@login_required
def page_entity_registrations():
    return render_template('pages/entity-registrations.html')

@pages.route('/entity/smo')
@login_required
def page_entity_smo():
    dp_fields = ['DP_011', 'DP_012', 'DP_039', 'DP_040', 'DP_041', 'DP_042', 'DP_043', 'DP_013', 'DP_014', 'DP_015', 'DP_044', 'DP_045', 'DP_049', 'DP_050', 'DP_033', 'DP_035', 'DP_034', 'DP_032', 'DP_037', 'DP_038', 'DP_036']
    df = pd.read_csv('../../Sample_Data.csv', encoding='iso-8859-1')
    df1 = df.query('DP_ID in @dp_fields')

    pivot_df1 = df1.pivot_table(index=['RCS_ID', 'Filing_Date'], columns='DP_Name', values='DP_Value', aggfunc='first').reset_index()
    pivot_df1['Filing_Date'] = pd.to_datetime(pivot_df1['Filing_Date'], format='mixed')
    df_sorted1 = pivot_df1.sort_values(by='Filing_Date', ascending=False)
    latest1 = df_sorted1.groupby('RCS_ID').first().reset_index()
    latest1['Filing_Date'] = latest1['Filing_Date'].dt.strftime('%m/%d/%Y')

    for index, row in latest1.iterrows():
        filtered = df_sorted1[(df_sorted1['RCS_ID'] == row['RCS_ID']) & ((df_sorted1['Mandate: limited'] == 'TRUE') | (df_sorted1['Mandate: unlimited'] == 'TRUE'))]

        if filtered.empty == False:
            latest1.at[index, 'Mandate: limited'] = filtered.iloc[0]['Mandate: limited']
            latest1.at[index, 'Mandate: unlimited'] = filtered.iloc[0]['Mandate: unlimited']
            latest1.at[index, 'Mandate: appointment / renewal date'] = filtered.iloc[0]['Mandate: appointment / renewal date']
            latest1.at[index, 'Mandate: expiration (Date)'] = filtered.iloc[0]['Mandate: expiration (Date)']
            latest1.at[index, 'Mandate: expiration (date of AGM)'] = filtered.iloc[0]['Mandate: expiration (date of AGM)']

    dp_fields1 = ['DP_016', 'DP_017', 'DP_018', 'DP_019', 'DP_039', 'DP_040', 'DP_041', 'DP_042', 'DP_043', 'DP_044', 'DP_045', 'DP_49', 'DP_050', 'DP_033', 'DP_035', 'DP_034', 'DP_032', 'DP_037', 'DP_038', 'DP_036']
    df2 = df.query('DP_ID in @dp_fields')

    pivot_df2 = df2.pivot_table(index=['RCS_ID', 'Filing_Date'], columns='DP_Name', values='DP_Value', aggfunc='first').reset_index()
    pivot_df2['Filing_Date'] = pd.to_datetime(pivot_df2['Filing_Date'], format='mixed')
    df_sorted2 = pivot_df2.sort_values(by='Filing_Date', ascending=False)
    latest2 = df_sorted2.groupby('RCS_ID').first().reset_index()
    latest2['Filing_Date'] = latest2['Filing_Date'].dt.strftime('%m/%d/%Y')

    for index, row in latest2.iterrows():
        filtered = df_sorted2[(df_sorted2['RCS_ID'] == row['RCS_ID']) & ((df_sorted2['Mandate: limited'] == 'TRUE') | (df_sorted2['Mandate: unlimited'] == 'TRUE'))]

        if filtered.empty == False:
            latest2.at[index, 'Mandate: limited'] = filtered.iloc[0]['Mandate: limited']
            latest2.at[index, 'Mandate: unlimited'] = filtered.iloc[0]['Mandate: unlimited']
            latest2.at[index, 'Mandate: appointment / renewal date'] = filtered.iloc[0]['Mandate: appointment / renewal date']
            latest2.at[index, 'Mandate: expiration (Date)'] = filtered.iloc[0]['Mandate: expiration (Date)']
            latest2.at[index, 'Mandate: expiration (date of AGM)'] = filtered.iloc[0]['Mandate: expiration (date of AGM)']

    return render_template('pages/entity-smo.html', headers1 = latest1.columns.tolist(), data1 = latest1.values, headers2 = latest2.columns.tolist(), data2 = latest2.values)

@pages.route('/entity/kpis')
@login_required
def page_entity_kpis():
    return render_template('pages/entity-kpis.html')

@pages.route('/entity/files')
@login_required
def page_entity_files():
    return render_template('pages/entity-files.html')

@pages.route('/entity/summary')
@login_required
def page_entity_summary():
    return render_template('pages/entity-summary.html')
