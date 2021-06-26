import sys
import json
#from typing import final

#from pandas.core.algorithms import mode
#import xlsxwriter
import extract_info
#from fit_sheet_wrapper import FitSheetWrapper
#from xlwt import Workbook
#import openpyxl
from openpyxl import load_workbook, workbook
import random
import pandas as pd
#import extract_info

def main(input):
    testcases = input
    #testcases = input.split("\n")
    results = []
    for testcase in testcases:
        result = extract_info.main(testcase, "whatsapp")
        r = []
        r.append(result['case_id'])
        r.append(testcase)
        r.append(result['action'])
        if len(result['inputs']) > 0:
            r.append(result['inputs'])
        else:
            r.append('-')
        r.append(result['expectation'])
        r.append(result['type'])
        results.append(r)
    df = pd.DataFrame(results, columns = ['Case id', 'Test case', 'Test Case Description', 'Expected Inputs', 'Expected Result', 'Type predicted'])
    #print(df)
    
    filename = 'example.xlsx'
    sheet_name = 'Sheet 1'
    #df.to_excel('example.xlsx', index=False, sheet_name=sheet_name)
    with pd.ExcelWriter(filename, engine='openpyxl', mode='a') as writer:
        workbook = writer.book
        try:
           workbook.remove(workbook[sheet_name])
        except:
           print("Worksheet does not exist")
        finally:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    code = True
    return results

#df = main(sys.argv[1])
#df.to_excel("wtf.xlsx")
print(main(sys.argv[1:]))
sys.stdout.flush()

# if __name__ == '__main__':
#     #input = sys.argv[1:]
#     #input = main(input)
#     #print(input)
#     #df = main(input)
#     print(json.loads(main(sys.argv[1])))
#     #print(main(sys.argv[1]))
#     sys.stdout.flush()