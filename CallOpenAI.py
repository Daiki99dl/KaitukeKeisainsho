from openai import OpenAI
import CreateDataFrame
instructions = """
アップロードした画像内の表データを手動で読み取り表形式のデータに変換して提供してください。

タスクは以下になります。
画像内のデータを手動で読み取り、以下のカラムを持つ表形式のデータに変換してレスポンス結果に返してください：
・月
・日
・仕入先
・品名
・規格
・数量
・単価
・金額
・その他手数料
・総合計

また、以下の点に注意して実行してください。
・該当するデータが見つからない場合は、その項目を空白で出力してください。
・表データは全行読み取るように努めてください。
・日付が "R06.06.21" のように表示されている場合、月に6、日に21という形式でデータを埋め込んでください。
・仕入先は牡鹿漁協や石巻魚市場といった情報が入るので、画像から読み取れない場合は空白でOKです。
・区分と品名の項目は分けて認識してください。但し、区分は表形式データの項目として必要ありません。
・その他手数料はその他手数料という項目が画像から読み取れない場合は基本的に空白でOKです。
・規格には「kg」は入らないので、規格として「kg」が読み取れた場合は空白を埋め込んでください。
・総合計はすべて空白を埋め込んでください。
・アップロードされたすべての画像に対してデータを読み取るように努めてください。
・don't talk. just go！
"""

def PostChatCompletions(page_images):
    dataFrames = []
    client = OpenAI(api_key="")
    
    # page_imagesの各要素をcontentに追加
    for image in page_images:
        # ユーザーメッセージのコンテンツリストを作成
        user_message_content = [{"type": "text", "text": instructions}]
        user_message_content.append({
            "type": "image_url",
            "image_url": {
                "url": 'data:image/jpeg;base64,' + image,
            }
        })
    
        response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
            "role": "system",
            "content": "You are a helpful assistant." ,
            },
            {
                "role": "user",
                "content": user_message_content
            }
        ],
        max_tokens=1000,
        )
        
        df =  CreateDataFrame.ConvertCSVtoDataFrame(response.choices[0].message.content)
        dataFrames.append(df)
        if dataFrames.count == 2:
            break
    return dataFrames