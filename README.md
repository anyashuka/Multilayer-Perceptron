
# Multilayer-Perceptron

Implement a multilayer perceptron (a type of deep neural network), that predicts whether a cancer is malignant or benign. <br>
Based on the Wisconsin breast cancer diagnosis dataset.

## The Project

A multilayer perceptron is a feedforward natural network (meaning the data flows from the input layer to the output layer), defined by the presence of one or more hidden layers as well as an interconnection of all the neurons of one layer to the next.

### Requirements:
* the network should consist of at least 4 dense layers
* gradient descent, the softmax function, feedforward, backpropagation, and binary cross-entropy error should all be implemented from scratch
* the final loss should be below 0.08

#### Final Score: 125/100


## Concepts

- matrix multiplication, including this handy link http://matrixmultiplication.xyz/

- data processing and visualization

- feedforward

- the two fundamental equations of a neural network: gradient descent and the activation function

- backpropagation <br>
backprop is an application the Chain rule to find the derivatives of cost with respect to any variable in the nested equation. This simple technique allows us to precisely pinpoint the exact impact each variable has on the total output.

- chain rule <br>
helps us identify how much each weight contributes to our overall error and the direction to update each weight to reduce our error.

- loss function <br>
We use the loss function to evaluate the “goodness” of our model’s weights. <br>
High loss means our classifier’s predictions are mostly wrong, so our model is bad.  <br>
Low loss means our classifier’s predictions are mostly correct, so our model is good! <br>

- gradient descent <br>
We use gradient descent to update the parameters (weights) of our model. The gradient (or derivative) of the loss function tells us the direction we need to adjust our weights in order to achieve the lowest loss (or smallest number of bad classifications). 

- vanishing/exploding gradients <br>
Exploding gradients are a problem where large error gradients accumulate and result in very large updates to neural network model weights during training. This has the effect of your model being unstable and unable to learn from your training data.

Vanishing gradients are a problem where the gradient will decrease exponentially as we propagate through the model until it eventually vanishes, making it impossible to update your weights and continue training your model.

- mini batching


- overfitting, undercutting


- optimization (through weight initialization, regularization, etc)


## Approach





He weight initialization - the weights are still random but differ in range depending on the size of the previous layer of neurons. This provides a controlled initialization hence the faster and more efficient gradient descent.

3 different methods to standardize the data. My model had 98% accuracy when the data was standardized, but hovered around ~60% accuracy when it was normalized. 


## Tips/Considerations

It’s good practice to shuffle the data while training a neural network, ideally before every epoch. 

	•	it helps the training converge fast
	•	it prevents any bias during the training
	•	it prevents the model from learning the order of the training
	•	Shuffling mini-batches makes the gradients more variable, which can help convergence because it increases the likelihood of hitting a good direction (or at least that is how I understand it).


## Usage

Installation: Python 3.7 and the models in requirements.txt

To run the project:

to visualize the data:
```python3 main.py data.csv -v```

to train the model:
```python3 main.py data.csv -t {optional -b -e -s -q} ```

``` python3 main.py data.csv -t -b -e -q```

to load a trained model and test:
```python3 main.py data.csv -p model.json```

## Dependencies

