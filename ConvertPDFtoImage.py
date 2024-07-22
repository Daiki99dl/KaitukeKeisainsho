import fitz  # PyMuPDF
import base64
import io
from PIL import Image

def main(base64_pdf):
    # デコードされたバイトデータを使ってPDFを読み込む
    pdf_bytes = base64.b64decode(base64_pdf)
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    # ページごとに変換する
    page_images = []
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        # PixmapをPNG形式のバイナリデータに変換
        png_image = Image.open(io.BytesIO(pix.tobytes("png")))
        rotatedPng_image = png_image.rotate(-90, expand=True)
        
        # PNGイメージをBase64文字列に変換
        buffered = io.BytesIO()
        # rotatedPng_image.save(r"C:\\Users\\daiki\\OneDrive\\デスクトップ\\フィッシュマンジャパン\\テスト\\画像ファイル\\A\\C.png")
        rotatedPng_image.save(buffered, format="PNG")
        png_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        page_images.append(png_base64)

    # Close the PDF document
    pdf_document.close()
    
    return page_images
