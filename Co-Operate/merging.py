# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 17:27:35 2020

@author: ttk96
"""

import pandas as pd
import Reuters_StockDataBase as db

mapper = db.SP500_map
# flip map
mapper = {industry:{v.upper():k.upper() for k, v in m.items()} for industry, m in mapper.items()}

cat_list = list(db.SP500.keys())

for cat in cat_list:
    
    print(cat)
    normal_data = f'SP500_NormalData_{cat}.csv'
    eps_data = f'SP500_{cat}.csv'
    
    df_normal = pd.read_csv(normal_data)
    df_eps = pd.read_csv(eps_data)
    # change name of stock
    df_eps['Stock'] = [mapper[cat][x] for x in df_eps['Stock']]
    # rename
    df_eps.rename(columns={
            "Fiscal Period": "Period",
            'Quarterly Diluted Normalized EPS Score': 'Quarterly EPS Score',
            'Quarterly Diluted Normalized EPS % Change': 'Quarterly EPS Changed %',
            'Annual Diluted Normalized EPS Score': 'Annual EPS Score',
            'Annual Diluted Normalized EPS % Change': 'Annual EPS Changed %',
            }, inplace=True)
    df_normal.drop(columns=['Quarterly EPS Score','Quarterly EPS Changed %','Annual EPS Score','Annual EPS Changed %'], inplace=True)
    
#    if len(df_normal) != len(df_eps):
#        print('***************')
#        print(f'Normal: {len(df_normal)} EPS: {len(df_eps)}')
#        print('***************')
#        continue

    df_final = pd.merge(df_normal, df_eps, on=['Stock', "Period"])
    
#    df_final['Quarterly EPS Score'] = df_final['Quarterly Diluted Normalized EPS Score']
#    df_final['Quarterly EPS Changed %'] = df_final['Quarterly Diluted Normalized EPS % Change']
#    df_final['Annual EPS Score'] = df_final['Annual Diluted Normalized EPS Score']
#    df_final['Annual EPS Changed %'] = df_final['Annual Diluted Normalized EPS % Change']
    
    df_final.to_csv(f'SP500_{cat}_Final.csv', index=False)
    
    ## ------------------Final Score--------------------------#
    fscore_normal_data = f'SP500_TotalScore_{cat}.csv'
    fscore_eps_data = f'SP500_{cat}_score.csv'
    df_score_normal = pd.read_csv(fscore_normal_data)
    df_score_eps = pd.read_csv(fscore_eps_data)
    
    # change name of stock
    df_score_eps['Stock'] = [mapper[cat][x] for x in df_score_eps['Stock']]
    # rename
    df_score_eps.rename(columns={
            'Quarterly Diluted Normalized EPS Total Score': 'Total Quarterly EPS Score',
            'Annual Diluted Normalized EPS Total Score': 'Total Annual EPS Score',
            }, inplace=True)
    df_score_normal.drop(columns=['Total Quarterly EPS Score', 'Total Annual EPS Score', 'Total Score'], inplace=True)
    
#    if len(df_normal) != len(df_eps):
#        print('***************')
#        print(f'Normal: {len(df_normal)} EPS: {len(df_eps)}')
#        print('***************')
#        continue

    df_score_final = pd.merge(df_score_normal, df_score_eps, on=['Stock'])
    df_score_final['Total Score'] = [sum(row[1:]) for index, row in df_score_final.iterrows()]
    
    df_score_final.to_csv(f'SP500_TotalScore_{cat}_Final.csv', index=False)
    
    
    
    