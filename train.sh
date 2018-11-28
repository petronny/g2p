#!/bin/sh
data=./beep.dict
max_order=9

mkdir -p model

for i in `seq $max_order`
do
        if [ ! -f model/order-$i ]
        then
                [ $i -eq 1 ] && g2p.py -t $data -d 5% -n model/order-$i || g2p.py -m model/order-$(($i-1)) -r -t $data -d 5% -n model/order-$i
        fi
        [ -f model/order-$i ] && [ ! -f model/order-$i.result ] && g2p.py -m model/order-$i -x $data > model/order-$i.result &
done

