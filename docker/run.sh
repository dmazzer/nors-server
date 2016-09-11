#!/bin/bash
set -xem

# fix vi compatibility mode (for developers)
echo "set nocompatible" > $HOME/.exrc

# repo sync
cd $NORS_PATH
git pull origin $NORS_BRANCH

# run nors server
nors_cmd="python3 nors_srv.py -c nors.conf"

$nors_cmd &

fg
