//
// Created by xueke on 2023/6/22.
// 设定一个文件夹，计算该文件夹下的所有文件的sha256
//
#include <QApplication>
#include <QProgressBar>
#include <QDialog>
#include <QGridLayout>
#include <QPushButton>
#include <QFutureWatcher>
#include <QtConcurrent>
#include <QLineEdit>
#include <QToolButton>
#include <QStringList>
#include <QFileDialog>
#include <QLabel>

class exampleDialog : public QDialog {
Q_OBJECT

public:
    explicit exampleDialog();

private:
    QString searchPath;
    QList<QString> allFilePath;
    QFutureWatcher<QString> watcher_progress;
    QFutureWatcher<QStringList> watcher_search;

private:
    QLineEdit *pathLine = new QLineEdit(this);
    QToolButton *selectPathButton = new QToolButton(this);
    QProgressBar *progressBar = new QProgressBar(this);
    QPushButton *startButton = new QPushButton("开始", this);
    QLabel *echoLabel = new QLabel(this);
private:
    void initFace();
    
    static QString clcFilesSha256(QString filePath);

    static QStringList getAllFilesPath(const QString &path);

private slots:

    void startClc();

    void finish();


    void startSearch();

    void showCurrentFilePath(int index);
};

exampleDialog::exampleDialog() {
    initFace();

    connect(startButton, &QPushButton::clicked, this, &exampleDialog::startSearch);
    connect(&watcher_search, &QFutureWatcher<QString>::finished, this, &exampleDialog::startClc);
    connect(&watcher_progress, &QFutureWatcher<QString>::finished, this, &exampleDialog::finish);
    connect(&watcher_progress, &QFutureWatcher<QString>::progressRangeChanged, progressBar, &QProgressBar::setRange);
    connect(&watcher_progress, &QFutureWatcher<QString>::progressValueChanged, progressBar, &QProgressBar::setValue);
    connect(&watcher_progress, &QFutureWatcher<QString>::progressValueChanged, this,
            &exampleDialog::showCurrentFilePath);
}

void exampleDialog::initFace() {
    setMinimumSize(400, 300);

    startButton->setCheckable(true);
    startButton->setDisabled(true);
    selectPathButton->setText("...");
    connect(selectPathButton, &QToolButton::clicked, [this]() {
        searchPath = QFileDialog::getExistingDirectory(this, "选择一个为文件夹", QDir::homePath());
        if (!searchPath.isEmpty()) {
            pathLine->setText(searchPath);
            startButton->setEnabled(true);
        }
    });


    auto *layout = new QGridLayout(this);
    layout->addWidget(pathLine, 0, 0, 1, 1);
    layout->addWidget(selectPathButton, 0, 1, 1, 1);
    layout->addWidget(startButton, 1, 0, 1, 2);
    layout->addWidget(progressBar, 2, 0, 1, 2);
    layout->addWidget(echoLabel, 3, 0, 1, 2);
}

void exampleDialog::startClc() {
    allFilePath = watcher_search.result();
    watcher_progress.setFuture(QtConcurrent::mapped(allFilePath, clcFilesSha256));
}

void exampleDialog::startSearch() {
    if (startButton->isChecked()) {
        startButton->setText("取消");
        progressBar->setValue(0);
        progressBar->setMaximum(0);
        echoLabel->setText("正在获取文件夹下的所有文件路径");
        watcher_search.setFuture(QtConcurrent::run(getAllFilesPath, pathLine->text()));
    } else {
        watcher_search.cancel();
        watcher_progress.cancel();
        progressBar->setValue(0);
        startButton->setText("开始");
        echoLabel->setText(tr("操作已取消"));
    }

}

QStringList exampleDialog::getAllFilesPath(const QString &path) {
    QList<QString> result;
    QDirIterator it(path, QDir::Files, QDirIterator::Subdirectories);
    QMimeDatabase db;
    while (it.hasNext()) {
        QString dir = it.next();
        QMimeType mime = db.mimeTypeForFile(dir);
        if (mime.name().startsWith("image/")) {
            result.append(dir);
        }
    }
    return result;
}

void exampleDialog::finish() {
    if (watcher_progress.isCanceled())
        return;
    progressBar->setValue(0);
    startButton->setChecked(false);
    startButton->setText("开始");
    echoLabel->setText("计算完成");
}

QString exampleDialog::clcFilesSha256(QString filePath) {
    QFile file(filePath);
    QCryptographicHash hash(QCryptographicHash::Sha256);
    if (file.open(QIODevice::ReadOnly)) {
        hash.addData(file.readAll());
    }
    return filePath;
}

void exampleDialog::showCurrentFilePath(int index) {
    if (index == progressBar->maximum())
        index -= 1;
    echoLabel->setText(allFilePath.at(index));
}

int main(int argc, char **argv) {
    QApplication app(argc, argv);
    exampleDialog w;
    w.show();
    return QApplication::exec();
}

#include "miniProgressBar.moc"