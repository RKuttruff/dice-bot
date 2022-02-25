#!/bin/bash

ls -1tr src/*out*.log 2> /dev/null | xargs -I % sh -c 'zip -u logs/out.zip % && rm %'
ls -1tr src/*err*.log 2> /dev/null | xargs -I % sh -c 'zip -u logs/err.zip % && rm %'
