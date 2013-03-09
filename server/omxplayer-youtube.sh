#!/bin/bash

videoPath="$1"
controlFilePath="$2"

/usr/bin/omxplayer $(youtube-dl -g "$videoPath") < "$controlFilePath"
