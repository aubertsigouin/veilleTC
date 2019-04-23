import xlsxwriter
import string
import pandas as pd
import sys
import warnings

warnings.simplefilter(action='ignore', category=UserWarning)


sys.path.append("..")

def write_to_excel(df_list, path, themes_path = 'src/params/themes.xlsx'):
    
    themes = pd.read_excel(themes_path)
    
    workbook = xlsxwriter.Workbook('{}.xlsx'.format(path))

    worksheet = workbook.add_worksheet('Général - EN')
    worksheet_2 = workbook.add_worksheet('QC - FR')
    worksheet_3 = workbook.add_worksheet('Thèmes')

    # Add a format for the header cells.
    header_format = workbook.add_format({
        'font_name' : 'Arial',
        'font_size' : 12,
        'font_color' : 'white',
        'border': 1,
        'bg_color': '#ed7d31',
        'bold': True,
        'text_wrap': True,
        'align': 'center',
        'valign': 'vcenter',
        'indent': 1,

    })

    text_format = [workbook.add_format({
        'border': 0,
        'bg_color': '#FFFFFF',
        'bold': False,
        'text_wrap': True,
        'valign': 'vcenter',
        'indent': 1,
    }), workbook.add_format({
        'border': 0,
        'bg_color': '#e5e5e5',
        'bold': False,
        'text_wrap': True,
        'valign': 'vcenter',
        'indent': 1,
    })]

    df_en = df_list[0].fillna('')
    df_qc = df_list[1].fillna('')

    worksheets = [worksheet, worksheet_2]

    for x in range(len(worksheets)):
        worksheets[x].set_column('A:N', 15)
        worksheets[x].set_column('B:B', 30)
        worksheets[x].set_column('C:C', 60)
        worksheets[x].set_row(0, 36)
        worksheets[x].set_default_row(60)




    for idx, month in enumerate(list(themes[0])):
        worksheet_3.write(idx,0,list(themes[0])[idx])

    col_l = list(df_en.columns)

    for x in range(len(col_l)):
        worksheet.write('{}1'.format(list(string.ascii_uppercase)[x]), col_l[x], header_format)
        worksheet_2.write('{}1'.format(list(string.ascii_uppercase)[x]), col_l[x], header_format)


    for y in range(len(df_en)):
        for x in range(len(df_en.iloc[y].keys())):
            if x != 2:
                worksheet.write('{}{}'.format(list(string.ascii_uppercase)[x], y+2), str(df_en.iloc[y,x]), text_format[y%2])
            else:
                worksheet.write_url(
                    '{}{}'.format(list(string.ascii_uppercase)[x], y+2), 
                    url = str(df_en.loc[y,'link']), 
                    string = str(df_en.loc[y,'title']),
                    cell_format = text_format[y%2])
                
    for y in range(len(df_qc)):
        for x in range(len(df_qc.iloc[y].keys())):
            if x != 2:
                worksheet_2.write('{}{}'.format(list(string.ascii_uppercase)[x], y+2), str(df_qc.iloc[y,x]), text_format[y%2])
            else:
                worksheet_2.write_url(
                    '{}{}'.format(list(string.ascii_uppercase)[x], y+2), 
                    url = str(df_qc.loc[y,'link']), 
                    string = str(df_qc.loc[y,'title']),
                    cell_format = text_format[y%2])


    sheet_reference_str = '=' + 'Thèmes' + '!$A$1:$A$30'

    worksheet.data_validation('A2:A{}'.format(len(df_en)+2), {'validate': 'list',
                                      'source': sheet_reference_str})
    
    worksheet_2.data_validation('A2:A{}'.format(len(df_qc)+2), {'validate': 'list',
                                      'source': sheet_reference_str})

    workbook.close()


def render_table(xls_in, xls_out):
    
    df_qc = pd.read_excel('{}.xlsx'.format(xls_in), sheet_name='QC - FR')
    df_en = pd.read_excel('{}.xlsx'.format(xls_in), sheet_name='Général - EN')
    coded_df = pd.concat([df_qc,df_en]).reset_index(drop=True)
    themes = list(set(coded_df['category'].dropna()))
    
    allItems_sorted = [
    'Ressources humaines et milieu de travail', 'Québec', 'Canada : politique de société', 'Relève', 
    'Formation continue', 'Grandes tendances', 'Transformation numérique', 'Intelligence artificielle', 
    'Cybersécurité', 'Infonuagique', 'Objets connectés', 'Jeu électronique', 'Créativité numérique', 
    'Communications et médias numériques', 'Télécommunications', 'Commerce électronique', 'Matériels informatiques', 
    'Logiciels', 'Systèmes informatiques', 'Chaîne de blocs', 'Cryptomonnaie','Fintech', 
    'Conformité et réglementation', 'Éthique', "Entreprises TI à l'international"
    ]

    themes_sorted = []

    for x in range(len(allItems_sorted)):
        if allItems_sorted[x] in themes :
            themes_sorted.append(allItems_sorted[x])
            
    themes = themes_sorted
        
    workbook = xlsxwriter.Workbook(xls_out)
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:A', 93)
    
    title = workbook.add_format({'font_name' : 'Arial','font_size' : 12,
                                 'font_color' : 'white','right': 1, 'left' :1, 'top' :1,
                                 'bg_color': '#f65e2f','bold': True,
                                 'text_wrap': True,'align': 'center',
                                 'valign': 'vcenter','indent': 0})

    sub_title = workbook.add_format({'font_name' : 'Calibri Light','font_size' : 11,
                                 'font_color' : '#26282a','right': 1, 'left' :1,
                                 'bg_color': '#d0cece','bold': True,
                                 'text_wrap': True,'align': 'left',
                                 'valign': 'vcenter','indent': 0})

    blank = workbook.add_format({'right':1, 'left' :1})

    link = workbook.add_format({'font_name' : 'Calibri','font_size' : 11,
                                 'font_color' : '#0563c1','right': 1, 'left' :1,
                                 'underline' :1,'bold': False,
                                 'text_wrap': True,'align': 'left',
                                 'valign': 'vcenter','indent': 0})

    name = workbook.add_format({'font_name' : 'Calibri Light','font_size' : 11,
                                 'font_color' : 'black','right': 1, 'left' :1, 'bold': True,
                                 'text_wrap': True,'align': 'left',
                                 'valign': 'vcenter','indent': 0})


    worksheet.write('A1',"Articles d'actualité recueillis par TECHNOCompétences", title)

    c = 1
    for x in range(len(themes)):
        worksheet.write(c,0, themes[x], sub_title)
        c += 1
        sub = coded_df[coded_df['category']==themes[x]].reset_index(drop=True)
        worksheet.write(c,0, '', blank)
        c += 1
        for y in range(len(sub)):
            
            
            if 'Google' not in sub['name'][y]:
                worksheet.write_url(c, 0, url = sub['link'][y], 
                                    string = str(sub['title'][y]), 
                                    cell_format = link)
            else:
                worksheet.write_url(c, 0, url = sub['link'][y], 
                                    string = str(sub['title'][y]).split(' - {}'.format(sub['source'][y]))[0], 
                                    cell_format = link)          
                
            c += 1
            if 'Google' not in sub['name'][y]:
                worksheet.write(c,0, sub['name'][y], name)
            else :
                worksheet.write(c,0, sub['source'][y], name)
            c += 1
            worksheet.write(c,0,'', blank)
            c += 1



    worksheet.write(c-1,0,'', workbook.add_format({'bottom' :1, 'right' :1, 'left' : 1}))
    

    workbook.close()