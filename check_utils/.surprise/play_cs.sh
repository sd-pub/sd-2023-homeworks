#!/bin/bash

# Copyright 2020 Darius-Florentin Neatu <neatudarius@gmail.com>

# play cs sound
if [ -z "$ONLINE_JUDGE" ]; then
	if [ $(which mpg123 2>&1 | wc -l) -eq 0 ]; then
		echo "'mpg123' must you install. Checker again must run. Bonus points may you lose!"
		echo "			e.g. sudo apt-get install mpg123"
		echo "			e.g. ./check"
		exit 0
	fi

    cat check_utils/.surprise/yoda.ascii

	printf "\n\t\t\t(please enable sound)\n"
	mpg123 check_utils/.surprise/congrats_gta.mp3 &>/dev/null
fi
