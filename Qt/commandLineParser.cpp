#include <QCoreApplication>
#include <QCommandLineOption>
#include <QCommandLineParser>
#include <QDebug>
int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);
    app.setApplicationName("test_command_line"); //默认是程序名，输出version时会显示该名称
    app.setApplicationVersion("1.0.0");

    /*创建一个命令行解析器*/
    QCommandLineParser parser;
    parser.setApplicationDescription("Description: Prints a greeting to the specified name");
    /*添加命令行选项*/
    parser.addHelpOption();
    parser.addVersionOption();
    /*增加自己的参数*/
    QCommandLineOption nameOption(QStringList({"n", "name"}), "output name", "name", "Jhon");
    parser.addOption(nameOption); //亦可直接parser.addOption({{"n", "name"},"output name","name","Jhon"})

    parser.process(app);

    if (parser.optionNames().isEmpty())
    {
        qDebug("Error: Must specify an argument.\n");
        parser.showHelp(1);
    }

    auto nameValue = parser.value(nameOption);
    qDebug() << "hello " << nameValue;
}