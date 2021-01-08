#!bin/sh

USER_AGENT="Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"

mkdir -p ~/.cache/instalooter/2.4.4/
echo -n $USER_AGENT > ~/.cache/instalooter/2.4.4/user-agent.txt

cd /app
python3 main.py
