//指定した宛先からのメールのPDFファイルを保存し、そのBase64文字列を返す
function getPDFFileIdInEmails(params) {
  Logger.log('メールアドレス' + params.senderEmail);
  Logger.log('フォルダID' + params.folderId);
  
  var folder = DriveApp.getFolderById(params.folderId);
  
  // 条件に一致するメールを取得
  var threads = GmailApp.search('from:' + params.senderEmail);
  
  // メールのスレッドごとに処理
  for (var i = 0; i < threads.length; i++) {
    var messages = threads[i].getMessages();
    
    for (var j = 0; j < messages.length; j++) {
      var message = messages[j];
      
      // メールに対して実行するアクション
      Logger.log("Subject: " + message.getSubject());
      Logger.log("Date: " + message.getDate());
      
      // 添付ファイルの取得
      var attachments = message.getAttachments();
      for (var k = 0; k < attachments.length; k++) {
        var attachment = attachments[k];
        
        // 添付ファイルがPDFかどうか確認
        if (attachment.getContentType() === "application/pdf") {
          // 指定したフォルダにGoogleドライブに保存
          var file = folder.createFile(attachment);
          Logger.log("PDF saved: " + file.getName());

          // ファイルIDの取得
          var fileId = file.getId();
          Logger.log("PDF file ID: " + fileId);
          return GetPDFBase64(fileId)
        }
      }
    }
  }
}

//指定したファイルIDのBase64文字列を返す
function GetPDFBase64(fileId){
  const blob = DriveApp.getFileById(fileId).getBlob();
  const bytes = blob.getBytes();
  return Utilities.base64Encode(bytes);
}
