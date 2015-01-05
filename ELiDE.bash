#!/bin/bash
if [ -z "$LISE_PATH" ]; then
    LISE_PATH="`dirname "$0"`/LiSE";
fi;

if [ -e "$LISE_PATH" ] && [ -f "$LISE_PATH/.installed" ]; then
    cd "$LISE_PATH";
    git pull;
    git submodule update;
    python3 setup.py install --user --upgrade;
    python3 -m ELiDE;
else
    if [ -e "$LISE_PATH" ]; then
        # clean out failed installation
        rm -rf "$LISE_PATH";
    fi;

    mkfifo announce;
    mkfifo addapt;
    echo '
    echo "About to install dependencies. This involves setting up two PPAs."
sudo add-apt-repository -y ppa:thopiekar/pygame
sudo add-apt-repository -y ppa:kivy-team/kivy-daily
echo "Added pygame and kivy-daily PPAs." >announce &
sleep 1
exit' >addapt &
    if [ -n "`which gnome-terminal`" ]; then
        gnome-terminal -x bash --rcfile addapt;
    else if [ -n "`which konsole`" ]; then
        konsole -e bash --rcfile addapt;
    else if [ -n "`which xterm`" ]; then
        xterm -e bash --rcfile addapt;
    else
        bash --rcfile addapt;
    fi; fi; fi;

    echo <announce;
    rm addapt;
    rm announce;

    echo "Updating package lists."
    sudo apt-get -y update;
    echo "Installing dependencies."
    sudo apt-get -y install git cython3 python3-dev python3-setuptools python3-kivy;

    cd "`dirname "$0"`";
    git clone https://github.com/LogicalDash/LiSE.git;
    cd LiSE;
    git submodule init;
    git submodule update;
    python3 setup.py install --user;

    mkdir -p $HOME/.local/share/applications/ELiDE.desktop;
    echo "[Desktop Entry]
Comment=Development environment for LiSE
Exec=\"`dirname \"$0\"`/ELiDE\"
Name=ELiDE
Type=Application
Categories=Development;
" >$HOME/.local/share/applications/ELiDE.desktop;
    xdg-desktop-menu forceupdate;

    touch "$LISE_PATH/.installed";

    python3 -m ELiDE;
fi
