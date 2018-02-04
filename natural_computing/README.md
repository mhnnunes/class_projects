# Protein Placement Using Neural Networks  

### Description  

This work consists in a supervised learning problem, which's goal is to find protein placement in cells using Neural Networks. A protein can be located in one of 7 places: cytoplasm (CYT), mitochondria (MIT), 3 different cell membrane parts (ME1, ME2, ME3), or outside of the cell (EXC).  

The training dataset contained 1429 labeled examples, each one with 8 attributes.  

### Implementation  

This work was implemented in _Python_, using _TensorFlow_ as library for the Neural Net. We used a 3-layer Multi-Layer Perceptron. The hidden layer contained 16 neurons, each using _ReLU_ as activation function. The output layer's activation function was _Softmax_. The cost function used was _Categorical Cross-Entropy_, and the training was done using _Mini-Batch Gradient Descent_ with a batch size of 32 examples. The training stage was done using _3-fold Cross Validation_, to avoid overfitting the model.   

### Results

The results showed that after 250 epochs in training phase, an accuracy of 62% was achieved. This model, applied to validation data, obtained an accuracy of 58%.   