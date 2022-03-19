#include <iostream>
#include <qgsvectorlayer.h>
#include <qgsrasterlayer.h>
#include <qgsmapcanvas.h>
#include <qgsapplication.h>
#include <QMainWindow>
#include <QMenuBar>
#include <QFileDialog>
#include <QFileInfo>

class TestViewer : public QMainWindow {
Q_OBJECT
public:
    TestViewer();

private:
    QMenu *menuFile = new QMenu("File");
    QAction *actionOpenFile = new QAction("Open");
    QgsMapCanvas *mapCanvas;
    QList<struct QgsMapLayer *> layers;
private slots:

    void onOpenActionTriggered();
};

TestViewer::TestViewer() {
    this->resize(600, 400);
    this->menuBar()->addMenu(menuFile);
    menuFile->addAction(actionOpenFile);

    mapCanvas = new QgsMapCanvas();
    this->setCentralWidget(mapCanvas);

    connect(actionOpenFile, &QAction::triggered, this, &TestViewer::onOpenActionTriggered);
}

void TestViewer::onOpenActionTriggered() {
    auto fileName = QFileDialog::getOpenFileName(this, "选择要展示的文件", "", "Shape Files (*.shp)");
    if (fileName.isEmpty())
        return;
    auto fileBaseName = QFileInfo(fileName).baseName();
    auto *vectorLayer = new QgsVectorLayer(fileName, fileBaseName);
//    auto fileName = QFileDialog::getOpenFileName(this, "选择要展示的文件", "", "GTIFF files (*.tif *.TIF)");
//    if (fileName.isEmpty())
//        return;
//    auto fileBaseName = QFileInfo(fileName).baseName();
//    auto *rasterLayer = new QgsRasterLayer(fileName, fileBaseName);
    layers.append(vectorLayer);
    mapCanvas->setExtent(vectorLayer->extent());
    mapCanvas->setLayers(layers);
    mapCanvas->refresh();
}


int main(int argc, char **argv) {
    QgsApplication app(argc, argv, true);
    QgsApplication::initQgis();

    TestViewer v;
    v.show();

    return QgsApplication::exec();
}

#include "main.moc"