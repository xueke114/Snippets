# from 文心一言，gpt太可怕了，理解得很精准

from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem
import sys


class TreeWidgetDemo(QTreeWidget):
    def __init__(self, parent=None):
        super(TreeWidgetDemo, self).__init__(parent)
        self.setMinimumSize(500, 600)
        self.setColumnCount(1)
        self.setHeaderLabels(["Name"])

        # 1. 中国
        china_item = QTreeWidgetItem(self)
        china_item.setText(0, "中国")

        # 1.1 广州
        guangzhou_item = QTreeWidgetItem(china_item)
        guangzhou_item.setText(0, "广州")

        # 1.2 许昌
        xuchang_item = QTreeWidgetItem(china_item)
        xuchang_item.setText(0, "许昌")

        # 2. 美国
        usa_item = QTreeWidgetItem(self)
        usa_item.setText(0, "美国")

        # 2.1 洛杉矶
        los_angeles_item = QTreeWidgetItem(usa_item)
        los_angeles_item.setText(0, "洛杉矶")

        # 2.2 纽约
        new_york_item = QTreeWidgetItem(usa_item)
        new_york_item.setText(0, "纽约")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tree = TreeWidgetDemo()
    tree.show()
    sys.exit(app.exec_())
