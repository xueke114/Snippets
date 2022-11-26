// 测试多进程的程序，同时对4个地址进行Ping
// 先使用moc生成文件名.moc
// moc 文件名.cpp -i -o 文件名.moc
// 将文本末尾的#include<main.moc>改为#include<文件名.moc>
// 编译需要指定qt的include路径、指定qt的Lib路径、并链接Qt6Widgets和Qt6Core


#include <iostream>

#include <QtCore/QString>
#include <QtCore/QProcess>
#include <QtWidgets/QWidget>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QApplication>
#include <QtWidgets/QTextBrowser>

using namespace std;

class MultiplePing: public QWidget {
    Q_OBJECT
  public:
    MultiplePing();
  private:
    void setupUi();
  private slots:
    void startPing();
  private:
    QPushButton* pbPingBaidu;
    QPushButton* pbPingTaobao;
    QPushButton* pbPingBing;
    QPushButton* pbPingJD;

    QTextBrowser* tbBaidu;
    QTextBrowser* tbTaobao;
    QTextBrowser* tbBing;
    QTextBrowser* tbJD;


};

MultiplePing::MultiplePing() {
    setupUi();

    connect(pbPingBaidu, &QPushButton::clicked, this, &MultiplePing::startPing);
    connect(pbPingTaobao, &QPushButton::clicked, this, &MultiplePing::startPing);
    connect(pbPingBing, &QPushButton::clicked, this, &MultiplePing::startPing);
    connect(pbPingJD, &QPushButton::clicked, this, &MultiplePing::startPing);
}

void MultiplePing::setupUi() {
    setMinimumSize(700,550);

    pbPingBaidu = new QPushButton("Ping Baidu", this);
    pbPingTaobao = new QPushButton("Ping Taobao", this);
    pbPingBing = new QPushButton("Ping Bing", this);
    pbPingJD = new QPushButton("Ping JD", this);

    tbBaidu = new QTextBrowser(this);
    tbTaobao = new QTextBrowser(this);
    tbBing = new QTextBrowser(this);
    tbJD = new QTextBrowser(this);

    QGridLayout *layout = new QGridLayout(this);

    layout->addWidget(tbBaidu, 0, 0, 1, 1);
    layout->addWidget(pbPingBaidu, 1, 0, 1, 1);

    layout->addWidget(tbTaobao, 0, 1, 1, 1);
    layout->addWidget(pbPingTaobao, 1, 1, 1, 1);

    layout->addWidget(tbBing, 2, 0, 1, 1);
    layout->addWidget(pbPingBing, 3, 0, 1, 1);

    layout->addWidget(tbJD, 2, 1, 1, 1);
    layout->addWidget(pbPingJD, 3, 1, 1, 1);
}


void MultiplePing::startPing() {
    // 所有按钮的组合
    QList<QPushButton *> buttons = {pbPingBaidu, pbPingTaobao, pbPingBing, pbPingJD};
    // 所有文本窗口的组合
    QList<QTextBrowser *> browsers = {tbBaidu, tbTaobao, tbBing, tbJD};
    // 所有执行参数的组合
    QList<QStringList> args = {{"www.baidu.com"}, {"www.taobao.com"}, {"cn.bing.com"}, {"www.jd.com"}};
    // 组合的形式是为了对应相应的按钮输出窗口与执行参数，方便索引

    // 哪个按钮发送的信号
    auto *button = qobject_cast<QPushButton *> (sender() );
    // 这个按钮在按钮组里是第几个
    int index = buttons.indexOf (button);
    // 新建进程
    auto *process = new QProcess;
    // 读取进程的输出什么（输出错误还是标准运行输出）
    process->setReadChannel (QProcess::StandardOutput);
    // 绑定开始信号，当进程开始时，在相应文本窗口显示Start Ping 网址
    connect(process, &QProcess::started, [ = ]() {
        browsers.at(index)->append (tr ("Start Ping %1").arg (args[index][0]) );
    });
    // 绑定输出输出信号，实时在对应的文本窗口输出运行输出内容。采用追加模式append
    connect(process, &QProcess::readyReadStandardOutput, [ = ]() {
        browsers.at(index)->append(QString::fromLocal8Bit(process->readAllStandardOutput()));
    });
    // 绑定结束信号。并在对应的文本从窗口输出结束信息，包括错误码和退出状态（正常退出还是崩溃退出）
    connect(process, QOverload<int, QProcess::ExitStatus>::of (&QProcess::finished),
    [ = ] (int exitcode, QProcess::ExitStatus exitStatus) {
        browsers.at(index)->append (tr ("线程已结束，返回错误代码为%1").arg (exitcode) );
    });
    // 执行ping命令
    process->start("ping", args.at (index) );

}


int main (int argc, char *argv[]) {
    QApplication a (argc, argv);

    MultiplePing w;
    w.show();
    return QApplication::exec();
}
#include "main.moc"
