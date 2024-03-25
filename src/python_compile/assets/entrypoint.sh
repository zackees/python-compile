#!/bin/bash

mkdir /tmp_dir
cd /tmp_dir

if [ -f "/host_dir/requirements.txt" ]; then
  pip install -r /host_dir/requirements.txt;
fi

if [ -f "/host_dir/.compile.whl" ];
  then pip install -r /host_dir/.compile.whl;
fi

python -m nuitka --standalone --follow-imports --onefile --lto=yes --python-flag=-OO /host_dir/"$@"
for file in $(find /tmp_dir -type f -name "*.bin"); do chmod +x "$file"; done
for file in $(find ;/tmp_dir -type f -name "*.bin"); do gzip "$file"; done

mv *.gz /host_dir/
