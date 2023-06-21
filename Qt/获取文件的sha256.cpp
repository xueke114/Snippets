//
// Created by xueke on 2023/6/21.
//
#include <QFile>
#include <QDebug>
#include <QCryptographicHash>

int main(){

    QFile file("C:\\GeoDatasets\\CN-border-La.gmt");
    QCryptographicHash hash(QCryptographicHash::Sha256);
    if(file.open(QIODevice::ReadOnly)){
        hash.addData(file.readAll());
    }
    qDebug()<<hash.result().toHex();
}

