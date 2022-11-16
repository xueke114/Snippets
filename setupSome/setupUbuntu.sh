#!/bin/bash
# 换源
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates
echo "
deb https://mirrors.bfsu.edu.cn/debian/ bullseye main contrib non-free
deb-src https://mirrors.bfsu.edu.cn/debian/ bullseye main contrib non-free

deb https://mirrors.bfsu.edu.cn/debian/ bullseye-updates main contrib non-free
deb-src https://mirrors.bfsu.edu.cn/debian/ bullseye-updates main contrib non-free

deb https://mirrors.bfsu.edu.cn/debian/ bullseye-backports main contrib non-free
deb-src https://mirrors.bfsu.edu.cn/debian/ bullseye-backports main contrib non-free

deb https://mirrors.bfsu.edu.cn/debian-security bullseye-security main contrib non-free
deb-src https://mirrors.bfsu.edu.cn/debian-security bullseye-security main contrib non-free
" | sudo tee /etc/apt/sources.list
# 开启 i386 支持
sudo dpkg --add-architecture i386
sudo apt-get update
# 安装常用软件
## C++ 开发
sudo apt install -y clang-format g++ gfortran cmake ninja-build qtcreator  qtbase5-doc-html qtbase5-examples libgdal-dev qtbase5-dev
sudo apt -t bullseye-backports install libqgis-dev
## python 开发
sudo apt install -y python3-openpyxl spyder  jupyter-notebook python3-pandas python3-bs4 python3-lxml python3-venv python3-cdo python3-gdal
## java 开发
sudo apt install -y default-jdk
## R 语言开发
sudo apt install -y r-cran-lme4 r-cran-irkernel r-cran-sp r-cran-stars r-cran-tidyverse
## LaTeX 工具
sudo apt install -y texstudio texlive-lang-chinese texlive-science texlive-pictures texlive-xetex latexmk biber 
## 系统工具
sudo apt install -y opencl-headers intel-opencl-icd clinfo vlc ffmpeg fonts-wqy-microhei baobab xfce4-weather-plugin proxychains4 command-not-found apt-file  stellarium gimp inkscape blender simplescreenrecorder peek perl wine32  winetricks  shadowsocks-libev chrony gufw bash-completion screen openssh-server fish htop
## 科研工具
sudo apt install -y cdo gdal-bin gmt libreoffice-texmaths
sudo apt install -y -t bullseye-backports qgis libreoffice  
# 工具设置
## 设置 ss-local 
sudo nano /etc/shadowsocks-libev/config.json
sudo sed '/s/ss-server/ss-local/' -i /lib/systemd/system/shadowsocks-libev.service
sudo systemctl daemon-reload
sudo systemctl restart shadowsocks-libev.service
sudo systemctl status shadowsocks-libev.service
## 设置 proxychains4
sudo sed '/^socks4/d' -i /etc/proxychains4.conf
echo "socks5 127.0.0.1 7070" | sudo tee -a /etc/proxychains4.conf
## 设置 wine32
WINEARCH=win32 WINEPREFIX=~/.wine wine wineboot
proxychains winetricks riched20
sudo apt-file update
sudo update-command-not-found
## 设置 pip
pip config set global.index-url https://mirrors.bfsu.edu.cn/pypi/web/simple
## 设置 Vritualbox
sudo apt-get install fasttrack-archive-keyring
echo "
deb https://fasttrack.debian.net/debian-fasttrack/ bullseye-fasttrack main contrib
deb https://fasttrack.debian.net/debian-fasttrack/ bullseye-backports-staging main contrib
" | sudo tee -a  /etc/apt/sources.list
sudo apt-get update
sudo apt-get install virtualbox virtualbox-ext-pack virtualbox-guest-additions-iso -y
## jupyter notebook 扩展
proxychains jupyter nbextension install https://github.com/drillan/jupyter-black/archive/master.zip --user
jupyter nbextension enable jupyter-black-master/jupyter-black
## 设置 git
git config --global init.defaultBranch main
git config --global user.name "Zheng Xueke"
git config --global user.email lengfeng1453@hotmail.com
# 需要手动安装的软件
## Joplin
## GitHub Desktop
## Zotero
## 坚果云
# 移除多余软件
