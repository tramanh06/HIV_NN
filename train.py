__author__ = 'TramAnh'

import numpy as np
import csv
import cPickle as pickle
from math import sqrt
from pybrain.datasets.supervised import SupervisedDataSet as SDS
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure import SigmoidLayer

MAXLENGTH = 297
def encoding(seq):
    splitted = ()
    for each_char in seq:
        encoded_char = encode_char(each_char.lower())
        if encoded_char:
            splitted = splitted + (encoded_char,)
        else: #return None if one of the character is not ATCG
            return None

    'Padding zeros for sequence thats less than MAXLENGTH'
    if len(splitted)<MAXLENGTH:
        padding_length = MAXLENGTH - len(splitted)
        splitted = splitted + (0,)*padding_length

    return splitted

def encode_char(x):
    if x=='a':
        return 0.25
    elif x=='t':
        return 0.5
    elif x=='c':
        return 0.75
    elif x=='g':
        return 1
    else:
        return None

# load data

def load_data(filename):
    '''
    Load data from csv and encode and do data validation
    :param filename: in csv format
    :return: Return numpy array of encoded sequence, each character separated by comma, x_data is input, y_data is target
    '''
    x_data = []
    y_data = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        print ' Encode every sequence with ATCG from 1->4'
        for row in reader:
            x = encoding(row[0].strip())    # week0 sequence
            y = encoding(row[1].strip())    # final week sequence
            if x and y:
                x_data.append(x)
                y_data.append(y)

    print 'Finish encoding. Returning np array..'
    return np.array(x_data), np.array(y_data)

def train_fn(hiddennodes):
    trainval_file = 'trainval.csv'
    output_model_file = 'model_{0}_nodes.pkl'.format(str(hiddennodes))

    hidden_size = hiddennodes
    epochs = 600

    print 'Loading data..'
    x_train, y_train = load_data(trainval_file)

    input_size = x_train.shape[1]
    target_size = y_train.shape[1]

    # Normalize
    # x_train = x_train /4.0
    # y_train = y_train /4.0

    # print 'in train.py'
    # print x_train
    # print y_train

    # prepare dataset

    ds = SDS( input_size, target_size )
    ds.setField( 'input', x_train )
    ds.setField( 'target', y_train )

    # init and train

    net = buildNetwork(input_size, hidden_size, target_size, bias = True, hiddenclass=SigmoidLayer,
                       outclass=SigmoidLayer)
    trainer = BackpropTrainer(net,ds)

    # print "training for {} epochs...".format( epochs )
    #
    # for i in range(epochs):
    #     mse = trainer.train()
    #     rmse = sqrt( mse )
    #     print "training RMSE, epoch {}: {}".format( i + 1, rmse )

    print 'Training..'
    trainer.trainUntilConvergence(verbose = True, validationProportion = 0.15, maxEpochs = 1000, continueEpochs = 10 )

    print 'Finish training. Serializing model...'
    pickle.dump( net, open( output_model_file, 'wb' ))


