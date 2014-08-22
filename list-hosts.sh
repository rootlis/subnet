#!/bin/bash

nmap -sn -R 192.168.2.0/24 | awk '/192\.168\.2\./ {print $5} /MAC Address: / {print substr($0,14,length($0))}' | paste -d ' ' - -
