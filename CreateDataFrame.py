import pandas as pd
from io import StringIO

def ConvertCSVtoDataFrame(data):
    # データをPandas DataFrameに読み込む
    df = pd.read_csv(StringIO(data), sep='|', engine='python', skipinitialspace=True)
    #ヘッダと明細の間の不必要な行を削除
    df = df.drop(0)

    # 列名のリストをきれいにする
    df.columns = [col.strip() for col in df.columns]

    # 数値型に変換
    # OCRでどうしても安定しないので文字列で読み込み→Excel側で整形する
    # df['数量'] = df['数量'].str.replace(',', '').astype(float)
    # df['単価'] = df['単価'].str.replace(',', '').astype(float)
    # df['金額'] = df['金額'].str.replace(',', '').astype(float)
    # df['その他手数料'] = df['その他手数料'].str.replace(',', '').astype(float)
    # df['総合計'] = df['総合計'].str.replace(',', '').astype(float)

    return df
 
 # 二つのDataFrameを結合
def JoinDataFrames(dataFrames):
    data = {
    "月": [],
    "日": [],
    "仕入先": [],
    "品名": [],
    "規格": [],
    "数量": [],
    "単価": [],
    "金額": [],
    "その他手数料": [],
    "総合計": []
    }
    combined_df = pd.DataFrame(data)
    for df in dataFrames: 
     combined_df = pd.concat([combined_df, df], ignore_index=True)
    return combined_df
