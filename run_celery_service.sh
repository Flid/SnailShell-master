#!/usr/bin/env sh
set -e

celery worker -A snailshell_cp.tasks -Q snailshell_cp_srv -n celery-worker-2@%h -c2
