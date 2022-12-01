// 打开摄像头，并支持摄像头设备切换
// g++ main.cpp -o main -lQt6GUI -lQt6Core -lQt6Widgets -lQt6Multimedia -lQt6MultimediaWidgets

#include <QCamera>
#include <QDialog>
#include <QComboBox>
#include <QGridLayout>
#include <QVideoWidget>
#include <QApplication>
#include <QMediaDevices>
#include <QDialogButtonBox>
#include <QMediaCaptureSession>


class CameraMonitor: public QDialog {
    Q_OBJECT
  public:
    CameraMonitor();
  private:
    void initMainFace();
  private slots:
    void cameraDiplay(int index);
  private:
    QComboBox *comboBox;
    QVideoWidget *cameraWidget;
    QDialogButtonBox *buttonBox;
  private :
    QCamera *camera;
    QList<QCameraDevice> cameras;
    QMediaCaptureSession *captureSession;

};

CameraMonitor::CameraMonitor() {
    // 初始化界面
    initMainFace();

    // 事件绑定
    connect(buttonBox, &QDialogButtonBox::rejected, this, &QDialog::close);
    connect(comboBox, &QComboBox::currentIndexChanged, this, &CameraMonitor::cameraDiplay);

    // 罗列可用的相机设备
    cameras = QMediaDevices::videoInputs();
    for (const QCameraDevice &cameraDevice : cameras)
        comboBox->addItem(cameraDevice.description());
}

void CameraMonitor::initMainFace() {
    resize(400, 300);
    setMinimumSize(200, 180);
    comboBox = new QComboBox(this);
    cameraWidget = new QVideoWidget(this);
    captureSession = new QMediaCaptureSession(this);

    buttonBox = new QDialogButtonBox(this);
    buttonBox->setOrientation(Qt::Horizontal);
    buttonBox->setStandardButtons(QDialogButtonBox::Cancel | QDialogButtonBox::Ok);

    auto layout = new QGridLayout(this);
    layout->addWidget(comboBox, 0, 0, 1, 1);
    layout->addWidget(cameraWidget, 1, 0, 1, 1);
    layout->addWidget(buttonBox, 2, 0, 1, 1);
}

void CameraMonitor::cameraDiplay(int index) {
    if(index == -1)
        return;

    camera = new QCamera(cameras[index]);
    captureSession->setCamera(camera);
    captureSession->setVideoOutput(cameraWidget);

    camera->start(); // to start the camera
}

int main(int argc, char*argv[]) {
    QApplication app(argc, argv);
    CameraMonitor CM;
    CM.show();
    return app.exec();
}

#include "main.moc"
