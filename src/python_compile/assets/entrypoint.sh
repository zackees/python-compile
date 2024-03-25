#!/bin/bash



WHEELS=$(find / -type f -name "*.whl")
REQUIREMENTS=/requirements.txt

# if [ -f "/host_dir/requirements.txt" ]; then
if [ -f "$REQUIREMENTS" ]; then
  #echo "Installing requirements at /host_dir/requirements.txt"
  #pip install -r /host_dir/requirements.txt;
  echo "Installing requirements at $REQUIREMENTS"
  pip install -r $REQUIREMENTS;
else
  # echo "No requirements.txt found in /host_dir"
  echo "Did not find requirements at $REQUIREMENTS"
fi


if [ ! -z "$WHEELS" ]; then
  for WHEEL in $WHEELS
  do
    echo "Installing wheel at $WHEEL"
    pip install $WHEEL --force-reinstall;
  done
else
  echo "Did not find any .whl files in root directory"
fi

python -m nuitka --standalone --follow-imports --onefile --lto=yes --python-flag=-OO /host_dir/"$@"
for file in $(find /tmp_dir -type f -name "*.bin"); do chmod +x "$file"; done
for file in $(find /tmp_dir -type f -name "*.bin"); do gzip "$file"; done

mv *.gz /host_dir/
