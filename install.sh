#!/bin/sh

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3 get-pip.py \
    && python3 -m pip install playwright \
    && playwright install chromium \
    && git clone https://github.com/fishsouprecipe/ahmeds-testing.git \
    && python3 -m pip install ./ahmeds-testing \
    && botpark  # run help

rm -rf get-pip.py
