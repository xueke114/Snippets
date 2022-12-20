:: 还不完美，标注没有在网格中间
gmt begin MODIS-SIN-GRID png
gmt set MAP_TICK_LENGTH_PRIMARY 0p
gmt set FONT_ANNOT_PRIMARY 8p
gmt basemap -JX15c/-7.5c -R0/35/0/17 -BWNbr -Bxa1+lh -Bya1+lv
gmt grdimage @earth_day_05m_p -Rd -J+proj=sinu+R=6371007.181+width=15c -t50
gmt basemap -Rd -JQ15c -Bg10
gmt end