#!/bin/bash

TO_EXTRACT=$(zipinfo out.zip | tail -2 | head -1 | tr -s ' ' | cut -d ' ' -f 9)

# unzip -c out.zip $TO_EXTRACT | less
unzip -p out.zip $TO_EXTRACT | less
