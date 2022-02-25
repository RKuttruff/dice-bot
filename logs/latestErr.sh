#!/bin/bash

TO_EXTRACT=$(zipinfo err.zip | tail -2 | head -1 | tr -s ' ' | cut -d ' ' -f 9)

# unzip -c err.zip $TO_EXTRACT | less
unzip -p err.zip $TO_EXTRACT | less
