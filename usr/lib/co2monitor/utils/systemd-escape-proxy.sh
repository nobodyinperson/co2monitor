#!/bin/sh

PATH="/bin:$PATH"

if hash systemd-escape;then
    systemd-escape $@
fi
