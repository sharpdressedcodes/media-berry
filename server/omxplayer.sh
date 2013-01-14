#!/bin/bash

videoPath="$1"
controlFilePath="$2"

/usr/bin/omxplayer "$videoPath" < "$controlFilePath"
