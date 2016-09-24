#!/usr/bin/env zsh

src=.
dest=vultr:/home/ubuntu/project_mcnulty

rsync --recursive --update --delete --verbose --append \
--exclude .ipynb_checkpoints --exclude .DS_Store --dry-run \
${src} ${dest}
