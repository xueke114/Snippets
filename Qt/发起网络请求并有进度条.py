# coding=utf-8
import json
import sys

from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PySide6.QtCore import QByteArray, QUrl, Qt
from PySide6.QtWidgets import QApplication, QDialog, QMessageBox, QProgressDialog, \
    QPushButton


class progress_dialog(QProgressDialog):
    def __init__(self, url: QUrl):
        super(progress_dialog, self).__init__()
        self.setWindowTitle('下载进度')
        self.setLabelText(f'正在下载{url.toDisplayString()}')
        self.setMinimum(0)
        self.setValue(0)
        self.setMinimumDuration(0)

    def network_reply_progress(self, bytes_read, total_bytes):
        self.setMaximum(total_bytes)
        self.setValue(bytes_read)


class main_window(QDialog):
    def __init__(self):
        super(main_window, self).__init__()
        # 成员变量
        self.qnam = QNetworkAccessManager()
        self.reply = QNetworkReply
        self.http_request_aborted = False

        self.bt_start = QPushButton(self, text='开始')
        self.bt_start.clicked.connect(self.start_request)

    def start_request(self, ):
        token = 'c2FuY2hvcjpNVFF6TkRFME5UZ3lOVUJ4Y1M1amIyMD06MTYzNjk4MjAyNTowNjljMz' \
                'FlZjM4MDhlZjQ2YWFiYzA1NzUwMTYzMDY1ZTQyMWZkYTli'

        url = QUrl(
            'https://ladsweb.modaps.eosdis.nasa.gov/archive/orders/501675589.json')
        self.http_request_aborted = False
        req = QNetworkRequest(url)
        req.setRawHeader(QByteArray('Authorization'), QByteArray('Bearer ' + token))
        self.reply = self.qnam.get(req)
        self.reply.finished.connect(self.http_finished)

        progress = progress_dialog(url)
        progress.setAttribute(Qt.WA_DeleteOnClose)
        progress.canceled.connect(self.cancel_download)
        self.reply.downloadProgress.connect(progress.network_reply_progress)
        self.reply.finished.connect(progress.hide)
        progress.exec()

    def cancel_download(self):
        print('取消啦')
        self.http_request_aborted = True
        self.reply.abort()

    def http_finished(self):
        return_result = self.reply.readAll().data().decode()
        result_json = json.loads(return_result)
        print(return_result)
        print(result_json)
        QMessageBox.question(self, '结果', f'搜索到了{result_json.__len__()}个文件')
        self.reply.deleteLater()
        self.reply = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = main_window()
    w.show()
    sys.exit(app.exec())
