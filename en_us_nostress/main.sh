#!/bin/sh
data=/usr/share/cmusphinx/g2p_models/en_us_nostress/cmudict-5prealpha.dict
max_order=9

for i in `seq 1 $max_order`
do
	if [ ! -f model-$i ]
	then
		[ $i -eq 1 ] && g2p.py -t $data -d 5% -n model-$(($i+1)) || g2p.py -m model-$(($i-1)) -r -t $data -d 5% -n model-$i
	fi
	[ -f model-$i ] && [ ! -f model-$i.result ] && g2p.py -m model-$i -x $data > model-$i.result &
done
