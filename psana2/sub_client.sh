#!/bin/bash

for i in $(seq 1 10)
do
    python sub_client.py > client_$i.log &
done
