#!/usr/bin/env zsh

src=.
dest=vultr:/home/mlgill/zika_prediction

rsync --recursive --update --delete --verbose --append \
--exclude .ipynb_checkpoints --exclude .DS_Store --dry-run \
${src} ${dest}
