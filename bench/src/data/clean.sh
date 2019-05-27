#!/usr/bin/env bash

#Deletes bpl and bc files that were last modified more than 2 hours ago
find . -maxdepth 1 -name "*.bpl" -mmin +30 | xargs -n 1 -P 32 rm -r
find . -maxdepth 1 -name "*.bc" -mmin +30 | xargs -n 1 -P 32 rm -r
find . -maxdepth 1 -name "*.bc-*" -mmin +30 | xargs -n 1 -P 32 rm -r
find . -maxdepth 1 -name "*.ll" -mmin +30 | xargs -n 1 -P 32 rm -r
find . -maxdepth 1 -name "*.dot" -mmin +30 | xargs -n 1 -P 32 rm -r
find . -maxdepth 1 -name "*.i" -mmin +30 | xargs -n 1 -P 32 rm -r
find . -maxdepth 1 -name "*.c" -mmin +30 | xargs -n 1 -P 32 rm -r
find . -maxdepth 1 -name "*.bin" -mmin +30 | xargs -n 1 -P 32 rm -r
