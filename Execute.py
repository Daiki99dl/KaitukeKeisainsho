import CallGAS
import ConvertPDFtoImage
import CallOpenAI
import CreateDataFrame
import OperateExcel

# GASへの認証
service = CallGAS.AuthorizeScript()
# GmailよりPDFデータを取得
base64_pdf = CallGAS.PostGAS_getPDFFileIdInEmails(service)
if base64_pdf != "":
    # PDFデータを画像データに取得
    page_images = ConvertPDFtoImage.main(base64_pdf)
    # 画像データをChatGPTに投げる
    dataFrames = CallOpenAI.PostChatCompletions(page_images)
    # 結果を一つのDataFrameに結合
    df = CreateDataFrame.JoinDataFrames(dataFrames)
    # Excelに転記
    OperateExcel.WriteDataFrameToExcel(df)
    