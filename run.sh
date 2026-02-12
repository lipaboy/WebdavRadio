#!/bin/bash
while true; do python $(dirname -- ${BASH_SOURCE})/play_random_song.py; sleep $(($RANDOM%100)); [ $(($RANDOM%100)) -ge 80 ] && break; done
