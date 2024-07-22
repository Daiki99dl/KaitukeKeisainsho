from __future__ import print_function
import os.path
from googleapiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# GoogleAppsScriptのデプロイIDのこと
SCRIPT_ID = 'AKfycbxSE-nr6L6aNnnBgMcPtuCj656e01fTQQPbW-58XoEr5nV2STN4WhbqOijrBGoWUQ2U'
    
def AuthorizeScript():
    # GoogleCloudPlatformからダウンロードしたJSONファイル    
    JSONFILE=r"C:\\Users\daiki\\OneDrive\\デスクトップ\\プログラム開発\\Python\\フィッシュマンジャパン\\OAuthClient.json"

    # GoogleCloudPlatformでAuth同意画面を作成する で選択したスコープのこと
    SCOPES = [
        'https://www.googleapis.com/auth/script.scriptapp',
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/drive'
    ]

    creds = None

    #　プログラムのある場所にtoken.jsonが自動で作成されます。
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # token.jsonがない場合ブラウザ上で認証画面が表示されます。
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                JSONFILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('script', 'v1', credentials=creds)
    return service

def PostGAS_getPDFFileIdInEmails(service):
    # GoogleAppsScriptで呼び出す関数名の設定・パラメータの設定
    # 下の例だと 関数名=testAPI　キー=test1値=test1の文字
    request = {
                "function": "getPDFFileIdInEmails"
               ,"parameters":{
                              'senderEmail':'daiki99dl@gmail.com'
                             ,'folderId':'1O2ZpwwLVHp7OlGnOeBbp2TDY2rIKmjmb'
                             }
    }

    try:

        response = service.scripts().run(body=request,  
                scriptId=SCRIPT_ID).execute()

        if 'error' in response:

            error = response['error']['details'][0]
            print("Script error message: {0}".format(error['errorMessage']))

            if 'scriptStackTraceElements' in error:

                print("Script error stacktrace:")
                for trace in error['scriptStackTraceElements']:
                    print("\t{0}: {1}".format(trace['function'],
                        trace['lineNumber']))
        else:

            #GoogleAppsScriptでreturanされた値　
            folderSet = response['response'].get('result', {})
            return folderSet

    except errors.HttpError as e:        
        print(e.content)    
    

        
    

