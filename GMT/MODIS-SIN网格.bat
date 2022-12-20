@REM 还不完美，标注没有在网格中间
gmt begin MODIS-SIN-GRID png
gmt set MAP_TICK_LENGTH_PRIMARY 0p
gmt set FONT_ANNOT_PRIMARY 8p
gmt basemap -JX15c/-7.5c -R0/35/0/17 -BWNbr -Bxa1+lh -Bya1+lv
gmt grdimage @earth_day_05m_p -Rd -J+proj=sinu+R=6371007.181+width=15c -t50
gmt basemap -Rd -JQ15c -Bg10


@REM 单独绘制一块
echo 117.3564 40.0849 >> h27v05.txt
echo 130.5645 39.9985 >> h27v05.txt
echo 115.3881 29.8298 >> h27v05.txt
echo 103.7008 29.9063 >> h27v05.txt
gmt plot h27v05.txt -L -A -W1p,red -J+proj=sinu+R=6371007.181+width=15c
del h27v05.txt

gmt end