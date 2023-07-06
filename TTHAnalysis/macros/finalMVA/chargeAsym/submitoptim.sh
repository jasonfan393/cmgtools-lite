for opt in SGD Adam RMSprop; do 
    for momentum in 0. 0.2 0.5 .9; do 
	for lr in 1e-6 1e-7 1e-5 5e-5; do 
	    echo sbatch -p long -t 7-00:00:00 submitwithconda.sh $PWD/ python trainLeptonIdr.py --learning-rate ${lr} --batch-size 256 --optimizer ${opt}  --momentum ${momentum} --model-prefix model_v2
	    done
	done
done
