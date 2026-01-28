#!/bin/bash
while true; do py play_random_song.py; sleep $(($RANDOM%100)); [ $(($RANDOM%100)) ] && break; done
