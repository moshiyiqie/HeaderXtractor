crf_learn -a MIRA template crf_train.txt model
crf_test -m model crf_test.txt > result.txt
judgeResult.py