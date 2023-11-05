#!/bin/bash

# 换源
echo "
deb https://mirrors.cernet.edu.cn/ubuntu/ jammy main restricted universe multiverse
deb https://mirrors.cernet.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse
deb https://mirrors.cernet.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse
deb https://mirrors.cernet.edu.cn/ubuntu/ jammy-security main restricted universe multiverse
" | sudo tee /etc/apt/sources.list

# 开启 i386 支持
sudo dpkg --add-architecture i386
sudo apt-get update

# 安装常用软件
## C++ 开发
sudo apt install -y clang-format g++ gfortran cmake ninja-build qtcreator qtbase5-doc-html qtbase5-examples libgdal-dev qtbase5-dev
sudo apt -t bullseye-backports install libqgis-dev
## python 开发
sudo apt install -y python3-openpyxl spyder jupyter-notebook python3-pandas python3-bs4 python3-lxml python3-venv python3-cdo python3-gdal
## java 开发
sudo apt install -y default-jdk
## R 语言开发
sudo apt install -y r-cran-lme4 r-cran-irkernel r-cran-sp r-cran-stars r-cran-tidyverse
## LaTeX 工具
sudo apt install -y texstudio texlive-lang-chinese texlive-science texlive-pictures texlive-xetex latexmk biber 
## 系统工具
sudo apt install -y flatpak virtualbox virtualbox-ext-pack virtualbox-guest-additions-iso ocl-icd-opencl-dev opencl-headers intel-opencl-icd clinfo vlc ffmpeg fonts-wqy-microhei baobab proxychains4 apt-file  stellarium gimp inkscape blender simplescreenrecorder peek perl winetricks  shadowsocks-libev chrony gufw bash-completion screen openssh-server fish htop
## 科研工具
sudo apt install -y cdo gdal-bin gmt qgis

# 工具设置
## 设置flatpak
sudo apt install gnome-software-plugin-flatpak
sudo flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
sudo flatpak remote-modify flathub --url=https://mirror.sjtu.edu.cn/flathub

## 设置 ss-local 
sudo apt install -y shadowsocks-libev
sudo nano /etc/shadowsocks-libev/config.json
sudo sed 's/ss-server/ss-local/' -i /lib/systemd/system/shadowsocks-libev.service
sudo systemctl daemon-reload
sudo systemctl restart shadowsocks-libev.service
sudo systemctl status shadowsocks-libev.service
## 设置 proxychains4
sudo sed '/^socks4/d' -i /etc/proxychains4.conf
echo "socks5 127.0.0.1 7070" | sudo tee -a /etc/proxychains4.conf
## 设置 wine32
sudo mkdir -pm755 /etc/apt/keyrings
sudo wget -O /etc/apt/keyrings/winehq-archive.key https://dl.winehq.org/wine-builds/winehq.key
sudo wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/ubuntu/dists/jammy/winehq-jammy.sources
sudo apt install --install-recommends winehq-stable
WINEARCH=win32 WINEPREFIX=~/.wine wine wineboot
## 设置 pip
pip config set global.index-url https://mirrors.cernet.edu.cn/pypi/web/simple
## jupyter notebook 扩展
proxychains jupyter nbextension install https://github.com/drillan/jupyter-black/archive/master.zip --user
jupyter nbextension enable jupyter-black-master/jupyter-black
## 设置 git
git config --global init.defaultBranch main
git config --global user.name "Zheng Xueke"
git config --global user.email xueke0114@foxmail.com

# 非apt仓库的软件
## flatpak
flatpak install flathub io.github.shiftey.Desktop org.hdfgroup.HDFView -y
## snap
sudo snap install typora zotero-snap
## Wine版微信
sudo apt install libjpeg62
proxychains winetricks riched20
wget https://github.com/tom-snow/wechat-windows-versions/releases/download/v3.0.0.57/WeChatSetup-3.0.0.57.exe
wine WeChatSetup-3.0.0.57.exe
