#!/bin/bash
# run an toy example for BTM
set -e

K=$1   # number of topics
W=$2   # vocabulary size

alpha=`echo "scale=3;50/$K"|bc`
beta=0.005
n_day=1
input_dir=$3
output_dir=$4
dwid_dir=${output_dir}/
model_dir=${output_dir}/
pathToOnlineBTM=$5

voca_pt=${output_dir}voca.txt

method=ibtm   # must be obtm or ibtm

echo "=============== Index Docs ============="
python $pathToOnlineBTM/script/indexDocs.py $input_dir $dwid_dir $voca_pt

## learning parameters p(z) and p(z|w)
echo "=============== Topic Learning ============="
make -C ./$pathToOnlineBTM/src
## run obtm
if [ "$method" = "obtm" ]; then
	n_iter=50
	lam=1
	./$pathToOnlineBTM/src/run obtm $K $W $alpha $beta $dwid_dir $n_day $model_dir $n_iter $lam
else
	win=10000
	n_rej=50
	./$pathToOnlineBTM/src/run ibtm $K $W $alpha $beta $dwid_dir $n_day $model_dir $win $n_rej
fi

# ## infer p(z|d) for each doc
echo "================ Infer P(z|d)==============="
for day in `seq 0 $[$n_day-1]`; do
	dwid_pt=${dwid_dir}${day}.txt
	echo "./OnlineBTM/src/infer sum_b $K $day $dwid_pt $model_dir"
	./$pathToOnlineBTM/src/infer sum_b $K $day $dwid_pt $model_dir
done

# ## output top words of each topic
# echo "================ Topic Display ============="
echo "---------- Display --------------"
for day in `seq 0 $[$n_day-1]`; do
	echo "---------- day $day --------------"
	python $pathToOnlineBTM/script/topicDisplay.py $model_dir $K $day $voca_pt
done
