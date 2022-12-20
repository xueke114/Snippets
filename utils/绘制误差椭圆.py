from cProfile import label
from math import sqrt, atan, degrees
from turtle import color
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib import font_manager

# 配置中文字体
fontP = font_manager.FontProperties()
fontP.set_family("SimHei")
fontP.set_size(12)

# 输入参数
Cx1, Cy1, Cxy1 = 1.7355, 1.5112, 0.1323
Cx2, Cy2, Cxy2 = 2.6437, 1.9973, 0.8295
Cx3, Cy3, Cxy3 = 2.7687, 2.1223, 0.9545

# 计算椭圆参数
K1 = sqrt((Cx1 - Cy1) ** 2 + 4 * Cxy1 * Cxy1)
E1 = sqrt(0.5 * (Cx1 + Cy1 + K1))
F1 = sqrt(0.5 * (Cx1 + Cy1 - K1))
ct1 = degrees(atan(2 * Cxy1 / (Cx1 - Cy1)) / 2)

K2 = sqrt((Cx2 - Cy2) ** 2 + 4 * Cxy2 * Cxy2)
E2 = sqrt(0.5 * (Cx2 + Cy2 + K2))
F2 = sqrt(0.5 * (Cx2 + Cy2 - K2))
ct2 = degrees(atan(2 * Cxy2 / (Cx2 - Cy2)) / 2)

K3 = sqrt((Cx3 - Cy3) ** 2 + 4 * Cxy3 * Cxy3)
E3 = sqrt(0.5 * (Cx3 + Cy3 + K3))
F3 = sqrt(0.5 * (Cx3 + Cy3 - K3))
ct3 = degrees(atan(2 * Cxy3 / (Cx3 - Cy3)) / 2)

# 绘制椭圆

fig, ax = plt.subplots(subplot_kw={"aspect": "equal"})
ellipse1 = Ellipse(
    (0, 0), E1, F1, angle=ct1, alpha=1, fill=False, color="r", label="不考虑 $S$、$S_1$"
)
ellipse2 = Ellipse(
    (0, 0), E2, F2, angle=ct2, alpha=1, fill=False, color="g", label="考虑 $S$"
)
ellipse3 = Ellipse(
    (0, 0), E3, F3, angle=ct3, alpha=1, fill=False, color="b", label="考虑 $S$、$S_1$"
)

ax.add_artist(ellipse1)
ax.add_artist(ellipse2)
ax.add_artist(ellipse3)

# 绘制斜线
ax.plot([-1.5, 1.5], [-1.5, 1.5], color="#ff17f0")

# 绘制坐标轴箭头与名称
ax.plot(1, -2.2, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
ax.plot(-2.2, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)
ax.text(2.4, -2.2, "X", horizontalalignment="center", verticalalignment="center")
ax.text(-2.2, 2.4, "Y", horizontalalignment="center", verticalalignment="center")


# 设置坐标轴范围
ax.set_xlim(-2.2, 2.2)
ax.set_ylim(-2.2, 2.2)

# 隐藏刻度与上、右轴线
ax.set_xticks([])
ax.set_yticks([])
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

# 绘制图例
ax.legend(prop=fontP)

# 保存绘制结果为文件
plt.savefig("Assets/errorEllipse.png", dpi=300)

