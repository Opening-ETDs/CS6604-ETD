Retraining Neural ParsCit. 

Steps to generate the training data.
1. Run the script batch_run.sh.
   This script creates data in 9 different citation styles based in the CSL format

2. Run the jupyter notebook Create_Train_Data.ipynb
   This notebook creates the training data and outputs in token label format.

3. File run_batch.sh is the batch job file to train the data. This file requires the following files/folders that can be found in https://github.com/WING-NUS/Neural-ParsCit
	- train.py
	- model.py
	- nn.py
	- loader.py	
	- utils.py
	- optimization.py
	- evaluation
	- word embedding found in http://wing.comp.nus.edu.sg/~wing.nus/resources/	 NParsCit/vectors_with_unk.tar.gz
	- Be sure to have a models and a result folder as the training results for each f	  old are stored accordingly.