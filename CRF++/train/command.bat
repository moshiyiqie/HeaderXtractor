crf_learn -a MIRA n_template ntrain.txt n_model
crf_test -m n_model ntest.txt > result.txt
judgeResult.py

crf_learn -a MIRA ./train/nmodel/n_template ./train/nmodel/ntrain.txt ./train/nmodel/n_model2
crf_test -m ./train/nmodel/n_model2 ./train/nmodel/ntest2.txt > ./train/nmodel/result.txt