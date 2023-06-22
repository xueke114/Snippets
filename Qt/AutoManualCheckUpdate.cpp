//
// Created by xueke on 2023/6/22.
//
#include <QApplication>
#include <QMainWindow>
#include <QMenuBar>
#include <QMessageBox>
#include <QNetworkRequest>
#include <QUrl>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QJsonDocument>

class exampleWindow : public QMainWindow {
Q_OBJECT

public:
    exampleWindow();

private:
    QString version = "1.0.0";
    bool fromManual = false;
    bool haveNewVersion = false;
    QNetworkAccessManager manager;
    QScopedPointer<QNetworkReply, QScopedPointerDeleteLater> reply;

private:
    QMenu *helpMenu;
    QAction *checkUpdateAct;
    QAction *aboutQtAct;

private:
    void createActions();

    void createMenus();


private slots:

    void checkUpdate();

    void showCheckResult();

    void manualCheckUpdate();
};

exampleWindow::exampleWindow() {
    setMinimumSize(400, 300);

    createActions();
    createMenus();

    checkUpdate();
}

void exampleWindow::createActions() {
    aboutQtAct = new QAction("关于Qt", this);
    checkUpdateAct = new QAction("检查更新", this);
    connect(checkUpdateAct, &QAction::triggered, this, &exampleWindow::manualCheckUpdate);
    connect(aboutQtAct, &QAction::triggered, qApp, &QApplication::aboutQt);

}

void exampleWindow::createMenus() {
    helpMenu = menuBar()->addMenu("帮助");
    helpMenu->addAction(checkUpdateAct);
    helpMenu->addSeparator();
    helpMenu->addAction(aboutQtAct);

}

void exampleWindow::manualCheckUpdate() {
    fromManual = true;
    checkUpdate();
}

void exampleWindow::checkUpdate() {
    auto req = QNetworkRequest(QUrl("http://216.127.171.19/checkversion/zxky.json"));
    req.setTransferTimeout(2000);
    reply.reset(manager.get(req));
    connect(reply.get(), &QNetworkReply::finished, this, &exampleWindow::showCheckResult);
}

void exampleWindow::showCheckResult() {
    QString checkResult = "检查更新失败";
    if (reply->attribute(QNetworkRequest::HttpStatusCodeAttribute) == 200) {
        // 解析返回的JSON
        auto data = QJsonDocument::fromJson(reply->readAll())[0];
        auto newVersion = data["version"].toString();
        auto changelog = data["changelog"].toString();

        if (newVersion <= version) {
            checkResult = "当前已是最新版本";
        } else {
            haveNewVersion = true;
            checkResult = QString("当前版本：%1 <b>最新版本：%2</b><br>更新日志：<br>%3").
                    arg(version, newVersion, changelog);
        }
    }

    if (fromManual || haveNewVersion) {
        QMessageBox msgBox;
        msgBox.setText(checkResult);
        msgBox.exec();
    }


}

int main(int argc, char **argv) {
    QApplication app(argc, argv);
    exampleWindow d;
    d.show();
    return QApplication::exec();
}

#include "AutoManualCheckUpdate.moc"