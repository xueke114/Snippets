//
// Created by xueke on 2023/10/20.
//

#include <QObject>
#include <QNetworkReply>
#include <QCoreApplication>
#include <QNetworkAccessManager>


class MyObj : public QObject {
public:
    MyObj();

private:
    QNetworkAccessManager qnam;
    QNetworkReply *reply;
private slots:

    void httpFinished();
};

MyObj::MyObj() {
    QString defaultUrl = "http://74.48.9.241/CheckVersion/kytools.json";

    QNetworkRequest qnr(defaultUrl);
    reply = qnam.get(qnr);
    connect(reply, &QNetworkReply::finished, this, &MyObj::httpFinished);

}

void MyObj::httpFinished() {
    qDebug() << reply->readAll();

}

int main(int argc, char **argv) {
    QCoreApplication app(argc, argv);
    MyObj obj;
    return QCoreApplication::exec();
}
