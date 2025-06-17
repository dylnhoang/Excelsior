import pandas as pd

def parse_excel_preview(path: str):
    xl = pd.ExcelFile(path)
    sheet_name = xl.sheet_names[0]
    df = xl.parse(sheet_name)
    
    headers = list(df.columns)
    sample = df.head().fillna("").values.tolist()

    return {
        "sheets": xl.sheet_names,
        "headers": headers,
        "sample": sample
    }