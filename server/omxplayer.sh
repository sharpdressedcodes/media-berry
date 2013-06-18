#!/bin/bash

videoPath="$1"
controlFilePath="$2"

/usr/bin/omxplayer -o local "$videoPath" < "$controlFilePath"
