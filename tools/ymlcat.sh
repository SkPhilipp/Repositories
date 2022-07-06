#!/usr/bin/env sh
#
# This script cats YAML files, with file metadata and document separators added.
#
# Usage: ymlcat.sh <file 1> <file 2> ...
#

set -e -o pipefail -o errtrace -o functrace
trap 'echo "erred at ${LINENO} ${BASH_COMMAND}"' ERR

for param in "$@"
do
  export file=$param
  export file_extension=$(basename $file | cut -d'.' -f2)
  export file_name=$(basename $file .$file_extension)
  export file_directory=$(dirname $file)
  if [ ! -f $file ]; then
    echo "File $file does not exist"
    exit 1
  fi
  # output the file as an array element with file metadata added
  yq '._meta.file.path=env(file)
    | ._meta.file.name=env(file_name)
    | ._meta.file.extension=env(file_extension)
    | ._meta.file.directory=env(file_directory)
    |  [.] ' $file
  # split the array into individual documents, with a separator
  # ('| cat' is to resolve compatibility issues on Windows where yq visually mangles output in git bash)
done | yq '.[] | split_doc' | cat
