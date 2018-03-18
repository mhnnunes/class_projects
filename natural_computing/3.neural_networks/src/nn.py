#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017 Matheus Nunes <mhnnunes@dcc.ufmg.br>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
from keras import optimizers
from keras.layers import Dense
from keras.models import Sequential
from keras.initializers import lecun_uniform


class NeuralNet(object):
    def __init__(self, hidden_layers, neurons, nclasses, nattr, activation,
                 epochs, batch_size, learning_rate, decay, seed):
        self.neurons = neurons
        self.hidden_layers = hidden_layers
        self.epochs = epochs
        self.input_dim = nattr
        self.size_output = nclasses
        self.activation = activation
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.decay = decay
        self.seed = seed
        # Fix random seed for reproducibility
        np.random.seed(self.seed)

    def create_model(self):
        """ Create a model from calls to Keras library, saves this model
        as a class variable
        """
        model = Sequential()
        # Input layer
        model.add(Dense(self.neurons, input_dim=self.input_dim,
                        kernel_initializer=lecun_uniform(self.seed),
                        activation=self.activation))
        # Hidden layers
        for i in range(self.hidden_layers):
            model.add(Dense(self.neurons,
                            kernel_initializer=lecun_uniform(self.seed),
                            activation=self.activation))
        # Output layer
        model.add(Dense(self.size_output,
                        kernel_initializer=lecun_uniform(self.seed),
                        activation='softmax'))
        # Define optimizer for the model (Stochastic Gradient Descent)
        sgd = optimizers.SGD(lr=self.learning_rate, decay=self.decay)
        # Compile model
        model.compile(loss='categorical_crossentropy', optimizer=sgd,
                      metrics=['accuracy'])
        self.model = model

    def fit_model(self, X, Y, train, valid):
        """ Fit the model and evaluate it using 3-fold cross validation
        """
        history = self.model.fit(X[train], Y[train], epochs=self.epochs,
                                 batch_size=self.batch_size, verbose=0)
        # Save an array containing the accuracy for each epoch in the
        # training phase
        epochs = np.arange(0, self.epochs)
        accbyep = np.column_stack((epochs,
                                   np.array(history.history['acc'])))
        result = self.model.evaluate(X[valid], Y[valid], verbose=0)
        valid_err = result[1]
        # Return the training accuracy for each epoch, and the validation 
        # accuracy
        return accbyep, valid_err
