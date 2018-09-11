# Symbolic Regression using Genetic Programming  

### Description  

This work tackles Symbolic Regression using Genetic Programming. Symbolic Regression consists in, given a set of inputs to a previously unknown function and the related outputs, fit a model that most accurately represents this function, in terms of accuracy and simplicity. This model is built by combining function building blocks and measuring its accuracy.  

### Problem Modeling  

The Chromossome is modeled as a binary tree, in which each node is one of four types of operators: binary functions, unary functions, constants and variables. It represents a function, and its fitness is calculated using the RMSE (_Root Mean-Square Error_) from the result of the input's evaluation on the Chromossome and the expected output. Three datasets (saved in the _datasets_ directory) were used in this work.  

### Implementation   

This work was implemented in _Python_, using _Keras_ as Neural Nets library with _TensorFlow_ as backend. We built a 3-layered MLP (_Multi-Layer Perceptron_). The hidden layer contained 16 neurons, each using _ReLU_ as activation function. The output layer's activation function was _Softmax_. The cost function used was _Categorical Cross-Entropy_, and the training was done using _Mini-Batch Gradient Descent_ with a batch size of 32 examples. The training stage was done using _3-fold Cross Validation_, to avoid overfitting the model.   

### Results  

The results showed that after 250 epochs in training phase, an accuracy of 62% was achieved. This model, applied to validation data, obtained an accuracy of 58%.   

<!-- Train accuracy across epochs:  
![train] (img/final_line.png)  

Train accuracy vs test accuracy:  
![traintest] (img/final_train_test_2.png)  --> 

### Dependencies  

No additional _Python_ packages are required to run this program.

### Execution  

The program can be executed by running the following commands:  

```bash  
cd src
python symbolic.py --train PATH_to_TRAIN_FILE --test PATH_to_TEST_FILE --out PATH_to_OUTPUT_FILE --pop-size POPULATION_SIZE --gen NUMBER_OF_GENERATIONS --tour-size TOURNAMENT_SIZE --max-depth MAXIMUM_CHROMOSSOME_DEPTH --prob-cross CROSSOVER_PROBABILITY --prob-mut MUTATION_PROBABILITY --seed RANDOM_SEED
```  

#### Parameters  

The programs accepts the following parameters as input:  

* *--train* [str] This parameter sets the path to the input file that holds training data (required)  
* *--test* [str] This parameter sets the path to the input file that holds test data (required)  
* *--out* [str] This parameter sets the path to the output file (required)  
* *--gen* [int] Sets the number of generations used in the GP (Default: 50)  
* *--pop-size* [int] Sets the population size for the GP (Default: 50)  
* *--tour-size* [int] Sets the tournament size for the GP (Default: 2)  
* *--max-depth* [int] Sets the maximum depth for the chromossome tree (Default: 7)  
* *--elitism* [boolean] Sets the elitism property of the GP (Default: True)  
* *--prob-cross* [float] Sets the crossover probability for chromossomes in the GP (Default: 0.9)  
* *--prob-mut* [float] Sets the crossover probability for chromossomes in the GP (Default: 0.05)  
* *--seed* [int]  Sets random seed for reproducibility (Default: 1)  
