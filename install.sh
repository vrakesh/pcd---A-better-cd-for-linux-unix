#!/usr/bin/env sh
CURR_DIR=$(pwd)

cat $CURR_DIR/func >> $HOME/.bashrc

ln -s $CURR_DIR/pycd.py  /usr/bin/pycd
