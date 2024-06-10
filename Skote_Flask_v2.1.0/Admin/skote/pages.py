from flask import Blueprint,render_template, request
from flask_login import login_required
import pandas as pd

pages = Blueprint('page',__name__,template_folder='templates',
    static_folder='static',)

@pages.route('/main')
@login_required
def page_main():
    dp_fields = ['DP_001', 'DP_002', 'DP_003', 'DP_004', 'DP_005', 'DP_006', 'DP_007', 'DP_008', 'DP_009', 'DP_010', 'DP_016', 'DP_017', 'DP_018', 'DP_019', 'DP_049', 'DP_051','DP_052', 'DP_053', 'DP_054', 'DP_055', 'DP_056', 'DP_500', 'DP_501', 'DP_502', 'DP_503', 'DP_504', 'DP_505', 'DP_506', 'DP_507', 'DP_508', 'DP_509', 'DP_510', 'DP_511', 'DP_512', 'DP_513', 'DP_514', 'DP_515', 'DP_516', 'DP_517']
    df = pd.read_csv('../../Sample_Data.csv', encoding='iso-8859-1')
    df = df.query('DP_ID in @dp_fields')
    df['Internal ID'] = ''
    extract = request.args.get("extract")
    date_column = 'Last Scan Date'
    df[date_column] = df['Filing_Date']

    if extract == 'true':
        latest = df.pivot_table(index=['RCS_ID', date_column], columns='DP_Name', values='DP_Value', aggfunc='first').reset_index()
        latest[date_column] = pd.to_datetime(latest[date_column])
        latest = latest.sort_values(by=date_column, ascending=False)
        latest[date_column] = latest[date_column].dt.strftime('%m/%d/%Y')
    else:
        pivot_df = df.pivot_table(index=['RCS_ID', date_column], columns='DP_Name', values='DP_Value', aggfunc='first').reset_index()
        pivot_df[date_column] = pd.to_datetime(pivot_df[date_column])
        df_sorted = pivot_df.sort_values(by=date_column, ascending=False)
        latest = df_sorted.groupby('RCS_ID').first().reset_index()

        for index, row in latest.iterrows():
            filtered = df_sorted[(df_sorted['RCS_ID'] == row['RCS_ID']) & ((df_sorted['Capital Fixed'] == 'TRUE') | (df_sorted['Capital Variable'] == 'TRUE'))]

            if filtered.empty == False:
                latest.at[index, 'Capital Fixed'] = filtered.at[1, 'Capital Fixed']
                latest.at[index, 'Capital Variable'] = filtered.at[1, 'Capital Variable']
                latest.at[index, 'Capital amount'] = filtered.at[1, 'Capital amount']

            filtered = df_sorted[(df_sorted['RCS_ID'] == row['RCS_ID']) & ((df_sorted['Duration unlimited'] == 'TRUE') | (df_sorted['Duration limited'] == 'TRUE') | (df_sorted['Duration extended'] == 'TRUE'))]

            if filtered.empty == False:
                latest.at[index, 'Duration unlimited'] = filtered.at[1, 'Duration unlimited']
                latest.at[index, 'Duration limited'] = filtered.at[1, 'Duration limited']
                latest.at[index, 'Duration extended'] = filtered.at[1, 'Duration extended']
                latest.at[index, 'Duration end date'] = filtered.at[1, 'Duration end date']
            
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
    return render_template('pages/entity.html')

@pages.route('/entity/accounting')
@login_required
def page_entity_accounting():
    return render_template('pages/entity-accounting.html')

@pages.route('/entity/registrations')
@login_required
def page_entity_registrations():
    return render_template('pages/entity-registrations.html')

@pages.route('/entity/smo')
@login_required
def page_entity_smo():
    return render_template('pages/entity-smo.html')

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
