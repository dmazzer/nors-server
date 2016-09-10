#!/bin/bash
set -xem

# repo sync
cd $NORS_PATH
git pull origin $NORS_BRANCH

# run nors server
cd $NORS_PATH/server/
nors_cmd="nors_srv -c nors.conf"

$nors_cmd &

fg
