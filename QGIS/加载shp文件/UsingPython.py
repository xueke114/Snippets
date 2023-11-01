import sys
from qgis.PyQt.QtCore import QFileInfo
from qgis.PyQt.QtWidgets import QMainWindow, QFileDialog, QMenu, QAction
from qgis.core import QgsApplication, QgsVectorLayer
from qgis.gui import QgsMapCanvas


class TestViewer(QMainWindow):
    def __init__(self, parent=None):
        super(TestViewer, self).__init__(parent)
        self.menu_file = QMenu("File")
        self.action_open_file = QAction("Open")
        self.map_canvas = QgsMapCanvas()
        self.layers = []

        self.resize(600, 400)
        self.setCentralWidget(self.map_canvas)
        self.menuBar().addMenu(self.menu_file)
        self.menu_file.addAction(self.action_open_file)
        self.action_open_file.triggered.connect(self.on_open_action)

    def on_open_action(self):
        file_name = QFileDialog.getOpenFileName(
            self, "选择要展示的文件", "", "Shape Files (*.shp)"
        )[0]
        if file_name:
            basename = QFileInfo(file_name).baseName()
            vector_layer = QgsVectorLayer(file_name, basename)
            self.layers.append(vector_layer)
            self.map_canvas.setLayers(self.layers)
            self.map_canvas.setExtent(vector_layer.extent())
            self.map_canvas.refresh()


if __name__ == "__main__":
    app = QgsApplication([], True)
    app.initQgis()

    v = TestViewer()
    v.show()

    sys.exit(app.exec_())
