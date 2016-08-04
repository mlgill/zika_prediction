#!/usr/bin/env zsh

src=.
dest=aws2:/home/ubuntu/project_mcnulty

rsync --recursive --update --delete --verbose --append \
--exclude .ipynb_checkpoints --exclude .DS_Store \
${src} ${dest}
