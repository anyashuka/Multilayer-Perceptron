import pandas as pd
import numpy as np
import tools as tools
import matplotlib.pyplot as plt
import preprocess as prep


# def relu_prime(z):
#     if z > 0:
#         return 1
#     return 0

# def cost(yHat, y):
#     return 0.5 * (yHat - y)**2

# def cost_prime(yHat, y):
#     return yHat - y

# cross entropy
# def compute_loss(yHat, y):
#     m = yHat.shape[1]
#     cost = -1 / m * (np.dot(y, np.log(yHat).T) + np.dot(1 - y, np.log(1 - yHat).T))
#     return np.squeeze(cost)

    # Avoid division by zero
    # yHat = np.clip(yHat, 1e-15, 1 - 1e-15)
    # return - y * np.log(yHat) - (1 - y) * np.log(1 - yHat)

    # predictions = np.clip(yHat, 1e-15, 1 - 1e-15)
    # n = yHat.shape[0]
    # ce = -np.sum(y*np.log(yHat+1e-9))/n
    # return ce

    # return np.where(y == 1, -np.log(yHat), -np.log(1 - yHat))
    # if y == 1:
    #   return -log(yHat)
    # else:
    #   return -log(1 - yHat)

# MSE
# def compute_loss(y_hat, y):
    # return ((y_hat - y)**2).sum()

LAYER1_NEURONS = 16
LAYER2_NEURONS = 16
LAYER3_NEURONS = 16
LAYER4_NEURONS = 2

# The ReLufunction performs a threshold operation to each input element 
# where values less than zero are set to zero.
def ReLU(z):
    return np.maximum(0, z)

def ReLU_prime(z):
    return 1 * (z > 0)
    # return 1 if z > 0 else 0

# leaky_ReLU
def leaky_ReLU(z, alpha = 0.01):
	return np.where(z >= 0, z, z * alpha)
    # return max(alpha * z, z)

def leaky_ReLU_prime(z, alpha = 0.01):
    return np.where(z >= 0, 1, alpha)
	# return 1 if x > 0 else alpha

# sigmoid
def sigmoid(z):
    return 1/(1+np.exp(-z))

# sigmoid derivative
def sigmoid_prime(z):
  return sigmoid(z) * (1-sigmoid(z))


# def softmax(x):
#     z = np.exp(x) / np.exp(x).sum(axis=1) [:,None]
#     return z

# def softmax_prime(self,grad):
    # return self.old_y * (grad -(grad * self.old_y).sum(axis=1)[:,None])

# what I was using when the NN wasn't learning
def softmax(z):
    e = np.exp(z - np.max(z))
    return e / e.sum()

    # return np.exp(z) / np.sum(np.exp(z)) 

	# e = np.exp(float(z))
	# return (e/np.sum(e))

def softmax_prime(z):
  return softmax(z) * (1-softmax(z))

# derivative for f is f(1-f) for respective cost functions
# THIS IS CORRECT FOR sigmoid and softmax
# def activation_derivative(activation):
    # return activation * (1.0 - activation)

# def activation_derivative(z, f):
# 	if fn == SIGMOID:
# 		f = sigmoid
# 	elif fn == SOFTMAX:
# 		f = softmax
# 	return f(z)*(1-f(z))

# def accuracy(Y_hat, Y):
    # Y_hat_ = convert_prob_into_class(Y_hat)
    # return (Y_hat_ == Y).all(axis=0).mean()

epsilon = 1e-5  

# binary cross-entropy loss
def compute_loss(yhat, y):
    # m = yhat.shape[1]
    m = len(y)
    loss = -1/m * (np.sum(np.dot(np.log(yhat + epsilon).T, y) + np.dot((1 - y).T, np.log(1 - yhat + epsilon))))
    return loss

class NeuralNetwork:
    def __init__(self, x, y):
        self.input      = x
        self.weights1   = np.random.rand(self.input.shape[1], LAYER1_NEURONS) * np.sqrt(2/self.input.shape[1]) ## * 0.01 # self.input.shape[1] is num_features
        self.weights2   = np.random.rand(LAYER1_NEURONS, LAYER2_NEURONS) * np.sqrt(2/LAYER1_NEURONS) ## * 0.01
        self.weights3   = np.random.rand(LAYER2_NEURONS, LAYER3_NEURONS) * np.sqrt(2/LAYER2_NEURONS) ## * 0.01
        self.weights4   = np.random.rand(LAYER3_NEURONS, 2) * np.sqrt(2/LAYER3_NEURONS) ## * 0.01  # if multiple classification, it should (NUM_NEURONS, output_size(# of classes))

        self.bias1       = np.zeros((1, LAYER1_NEURONS)) # 4 x 1
        self.bias2       = np.zeros((1, LAYER2_NEURONS))
        self.bias3       = np.zeros((1, LAYER3_NEURONS))
        self.bias4       = np.zeros((1, 2)) # (1, num_of_classes)... maybe last layer shouldn't have bias
       
        self.y           = y.to_numpy().reshape(y.shape[0], 1)
        self.output     = np.zeros((self.y.shape[0], 2))

        # print("y {}".format(self.y))
        # print("output {}".format(self.output))
        # print("weights 1 {}".format(self.weights1))

    def feedforward(self, activation = softmax, activation_hidden = leaky_ReLU):
        
        self.layer1 = activation_hidden(np.dot(self.input, self.weights1) + self.bias1) 
        self.layer2 = activation_hidden(np.dot(self.layer1, self.weights2) + self.bias2)
        self.layer3 = activation_hidden(np.dot(self.layer2, self.weights3) + self.bias3)
        self.output = activation(np.dot(self.layer3, self.weights4) + self.bias4) # layer = theta(weight_l * a_l-1 + b_l)
        
        # print("activation layer 1{}".format(activation_hidden(np.dot(self.input, self.weights1) + self.bias1)))
        # print("activation layer 2{}".format(activation_hidden(np.dot(self.layer1, self.weights2) + self.bias2)))
# 
        # print("layer1 {}".format(self.layer1))
        # print("layer2 {}".format(self.layer2))
        # print("layer3 {}".format(self.layer3))
        # print("output {}".format(self.output))

        # print("layer1 {0}, input {1}, weights1 {2}, bias {3}".format(self.layer1.shape, self.input.shape, self.weights1.shape, self.bias1.shape))
        # print("layer2 {0}, layer1 {1}, weights2 {2}, bias {3}".format(self.layer2.shape, self.layer1.shape, self.weights2.shape, self.bias2.shape))
        # print("layer3 {0}, layer2 {1}, weights3 {2}, bias {3}".format(self.layer3.shape, self.layer2.shape, self.weights3.shape, self.bias3.shape))
        # print("output {0}, layer3 {1}, weights4 {2}, bias {3}".format( self.output.shape, self.layer3.shape, self.weights4.shape, self.bias4.shape))

    ## application of the chain rule to find derivative of the loss function with respect to weights2 and weights1
    def backprop(self, d_activation = softmax_prime, d_activation_hidden = leaky_ReLU_prime, learning_rate = 0.01):
        m = self.input.shape[0] # num examples or batch size
        # weights and d_weights should have the same dimensions

        # output layer
        d_Z4 = d_activation(self.output - self.y) # not sure if we need activation derivative on output
        d_weights4 = np.dot(self.layer3.T, d_Z4)
        d_bias4 = np.sum(d_Z4, axis = 0, keepdims=True) # should be either axis 0 or 1, should create shape of 1,1 
        d_A3 = np.dot(d_Z4, self.weights4.T)

        # hidden layers
        d_Z3 = d_A3 * d_activation_hidden(self.layer3)
        d_weights3 = np.dot(self.layer2.T, d_Z3)  # (layer-1) * output error
        d_bias3 = np.sum(d_Z3, axis = 0, keepdims=True)
        d_A2 = np.dot(d_Z3, self.weights3.T)

        d_Z2 = d_A2 *  d_activation_hidden(self.layer2)
        d_weights2 = np.dot(self.layer1.T, d_Z2) # (layer-1) * output error
        d_bias2 = np.sum(d_Z2, axis = 0, keepdims=True) 
        d_A1 = np.dot(d_Z2, self.weights2.T)

        d_Z1 = d_A1 * d_activation_hidden(self.layer1)
        d_weights1 = np.dot(self.input.T, d_Z1) # (layer-1) * output error
        d_bias1 = np.sum(d_Z2, axis = 0, keepdims=True)
       
        ## update the weights with the derivative (slope) of the loss function
        self.weights1 -= learning_rate * (d_weights1 / m) 
        self.weights2 -= learning_rate * (d_weights2 / m)
        self.weights3 -= learning_rate * (d_weights3 / m)
        self.weights4 -= learning_rate * (d_weights4 / m)

        self.bias1 -= learning_rate * (d_bias1 / m)
        self.bias2 -= learning_rate * (d_bias2 / m)
        self.bias3 -= learning_rate * (d_bias3 / m)
        self.bias4 -= learning_rate * (d_bias4 / m)

        # print
        # print("d_weights1 {}".format(d_weights1))
        # print("d_weights2 {}".format(d_weights2))
        # print("d_weights3 {}".format(d_weights3))
        # print("d_weights4 {}".format(d_weights4))

        # print
        # print("bias1 {}".format(self.bias1))
        # print("bias2 {}".format(self.bias2))
        # print("bias3 {}".format(self.bias3))
        # print("bias4 {}".format(self.bias4))

        # print("d_Z4 {0} - layer3 {1} - d_weights4 {2} - d_bias4 {3}".format(d_Z4.shape, self.layer3.shape, d_weights4.shape, d_bias4.shape))
        # print("weights3 {} - d_Z4 {} - d_layer3 {}".format(self.weights3.shape, d_Z4.T.shape, activation_derivative(self.layer3).shape))
        # print("d_A3 {}".format(d_A3.shape))
        # print("d_Z3 {0} - layer2 {1} - d_weights3 {2} - d_bias3 {3}".format(d_Z3.shape, self.layer2.shape, d_weights3.shape, d_bias3.shape))
        # print("layer2 {} - d_Z3 {}".format(self.layer2.shape, d_Z3.shape))
        # print("weights2 {} - d_Z3.T {} - d_layer2 {}".format(self.weights2.shape, d_Z3.T.shape, activation_derivative(self.layer2).shape))
        # print("weights4 {} - d_weights4 {} - weights3 {} - d_weights3{}".format(self.weights4.shape, d_weights4.shape, self.weights3.shape, d_weights3.shape))
        # print("d_weights1 {} - d_weights2 {} - d_weights3 {} - d_weights4 {}".format(d_weights1.shape, d_weights2.shape, d_weights3.shape, d_weights4.shape))
        # print("self.weights1 {} - self.weights2 {} - self.weights3 {} - self.weights4 {}".format(self.weights1.shape, self.weights2.shape, self.weights3.shape, self.weights4.shape))

def main():
    # X = np.array([[0,0,1],
    #               [0,1,1],
    #               [1,0,1],
    #               [1,1,1]])
    # y = np.array([[0],[1],[1],[0]])

    data = pd.read_csv('./data/data_labeled.csv')
    data = prep.preprocess(data)
    # visualize(data)
    train_set, test_set = prep.split(data)

    # X, y = train_set.iloc[:, 1:], train_set.iloc[:, 0]
    X, y = train_set.iloc[:5, 1:], train_set.iloc[:5, 0]
    # print("X {}".format(X))
    # print("y {}".format(y))

    # X = tmp_X[:2]
    
    # y = y.reshape(y.shape[0], 1)
    # y = y.to_numpy().shape[0]

    # X = numpy_array[:, 1:26]
    # y = numpy_array[:, 0]
    # X_train, X_test = X[:index], X[index:]
    # y_train, y_test = y[:index], y[index:]

    nn = NeuralNetwork(X, y)
    loss_values = []

    for i in range(150000):
        nn.feedforward()
        nn.backprop()
        loss = compute_loss(nn.output, nn.y)
        # print("output = {}".format(nn.output))
        print("loss = {}".format(loss))
        loss_values.append(loss)

    # print(nn.output.shape)
    # print(nn.y.shape)

    # print(nn.output)
    print(f" final loss : {loss}")

    plt.plot(loss_values)
    plt.show()

if __name__ == '__main__':
    main()


# # softmax activation layer : compute values for each sets of scores in x
# # not sure this works