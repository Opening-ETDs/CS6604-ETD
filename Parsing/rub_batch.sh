#!/bin/bash
#SBATCH --nodes=1 
#SBATCH --exclusive
#SBATCH -t 04:00:00
#SBATCH -p normal_q
#SBATCH -A waingram_lab
#SBATCH -W group_list=cascades
cd $SLURM_SUBMIT_DIR


WORD_DIM=500
LOWER=0
CAP_DIM=0
ZEROES=0
DATA_ID=REPORT_SMALL_SUBSET
PATH_TO_FOLDS=$(pwd)/report_small_subset/training/folds
PATH_TO_WB=$(pwd)/vectors_with_unk.kv
PATH_TO_TEST=$(pwd)/report_small_subset/test/test.txt
PATH_TO_RESULTS=$(pwd)/results

echo $PATH_TO_FOLDS
for d in $(ls -l $PATH_TO_FOLDS | grep '^d'| tr -s ' ' | cut -d ' ' -f9);
do
  if [ $d -gt 0 ]
  then
    echo "Running fold #$d..." && ~/.conda/envs/p27/bin/python train.py \
    --train $PATH_TO_FOLDS/$d/train.txt \
    --test $PATH_TO_TEST \
    --dev $PATH_TO_FOLDS/$d/val.txt \
    --pre_emb $PATH_TO_WB \
    --word_dim $WORD_DIM \
    --lower $LOWER \
    --cap_dim $CAP_DIM \
    --zeros $ZEROES \
    --reload 0 > $PATH_TO_RESULTS/ETD_${WORD_DIM}_${LOWER}_${CAP_DIM}_${ZEROES}_${DATA_ID}_fold_$d.out
  fi
  
  if [[ $? -eq 0 ]]; then
    echo "$d fold has completed successfully."
  fi
done

tar cvfz $DATA_ID.tar.gz results/ models/ 

exit;
