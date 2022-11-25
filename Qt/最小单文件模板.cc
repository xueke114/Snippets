#include <QApplication>
#include <QWidget>

class mywidget : public QWidget
{
    Q_OBJECT
public:
    mywidget();
};

mywidget::mywidget()
{
    resize(400, 400);
    setWindowTitle(QString("你好啊Qt"));
}

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    mywidget w;
    w.show();
    return app.exec();
}

// 编译前先运行一下moc
// moc 文件名.cc -i -o 文件名.moc
#include<文件名.moc>
