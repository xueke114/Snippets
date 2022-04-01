#include <qgscolorbrewerpalette.h>
#include <qgscolorramp.h>
#include <qgscolorrampshader.h>
#include <qgsmapcanvas.h>
#include <qgsrasterlayer.h>
#include <qgsrastershader.h>
#include <qgssinglebandpseudocolorrenderer.h>

#include <QApplication>
#include <QFileDialog>
#include <QFileInfo>
#include <QMainWindow>
#include <QMenuBar>
class MyWindow : public QMainWindow {
  Q_OBJECT
 public:
  MyWindow();

 private:
  QMenu* menuFile = new QMenu("File");
  QAction* actionOpenFile = new QAction("Open");
  QgsMapCanvas* mapCanvas;
  QList<QgsMapLayer*> layers;
 private slots:
  void onOpen();
};
void MyWindow::onOpen() {
  auto fileName = QFileDialog::getOpenFileName(this, "打开一个tif文件", "./",
                                               "GTIFF文件(*.tif *.TIF)");
  auto fileBaseName = QFileInfo(fileName).baseName();
  auto* rasterLayer = new QgsRasterLayer(fileName, fileBaseName);
  // 所有SchemeColors可以通过QgsColorBrewerPalette::listSchemes()获取
  // SchemeColors的等级，可以通过QgsColorBrewerPalette::listSchemeVariants(SchemeColors)获取
  auto colors = QgsColorBrewerPalette::listSchemeColors("Greens", 9);

  auto* fcn = new QgsColorRampShader();

  fcn->setColorRampType(QgsColorRampShader::Interpolated);
  fcn->setClassificationMode(QgsColorRampShader::Continuous);
  // TODO: 最大值最小值应该自动获取
  float band_max = 7.7;
  float band_min = 0;
  float band_range = band_max - band_min;
  float class_range = band_range / 9.0;
  QList<QgsColorRampShader::ColorRampItem> colorRampItemList = {};
  for (auto& color : colors) {
    colorRampItemList.append(
        QgsColorRampShader::ColorRampItem(band_min, color));
    band_min += class_range;
  }
  fcn->setColorRampItemList(colorRampItemList);

  auto* shader = new QgsRasterShader();
  shader->setRasterShaderFunction(fcn);
  auto* renderer = new QgsSingleBandPseudoColorRenderer(
      rasterLayer->dataProvider(), 1, shader);
  rasterLayer->setRenderer(renderer);
  layers.clear();
  layers.append(rasterLayer);
  mapCanvas->setExtent(rasterLayer->extent());
  mapCanvas->setLayers(layers);
  mapCanvas->refresh();
};
MyWindow::MyWindow() {
  resize(400, 300);
  this->menuBar()->addMenu(menuFile);
  menuFile->addAction(actionOpenFile);
  mapCanvas = new QgsMapCanvas;
  this->setCentralWidget(mapCanvas);
  connect(actionOpenFile, &QAction::triggered, this, &MyWindow::onOpen);
};
int main(int argc, char* argv[]) {
  QApplication app(argc, argv);
  MyWindow w;
  w.show();
  return app.exec();
}
#include "main.moc"
