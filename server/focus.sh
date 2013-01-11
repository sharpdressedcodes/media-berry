#!/bin/bash

pid="$1"
wid="$(xdotool search --pid "$pid" | tail -n 1)"
xdotool windowmap --sync "$wid"
xdotool windowfocus --sync "$wid"


