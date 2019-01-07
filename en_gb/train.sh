#!/bin/sh
data=./beep.dict
max_order=9

mkdir -p models

for i in `seq $max_order`
do
        if [ ! -f models/order-$i ]
        then
                [ $i -eq 1 ] && g2p.py -t $data -d 5% -n models/order-$i || g2p.py -m models/order-$(($i-1)) -r -t $data -d 5% -n models/order-$i
        fi
        [ -f models/order-$i ] && [ ! -f models/order-$i.result ] && g2p.py -m models/order-$i -x $data > models/order-$i.result &
done
