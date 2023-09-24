//
// Created by xueke on 23-9-24.
//
// from https://doc.qt.io/qt-6/qrandomgenerator.html#bounded-2
#include <QRandomGenerator>
#include <QDebug>
int main(){
    qDebug()<<QRandomGenerator::global()->bounded(0 ,10);
}