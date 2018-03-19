#Artificial Neural Network Agent

from Environment_Class import IP_env
import random
import numpy as np
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import median, mean
from collections import Counter
from time import sleep
from math import pi

LR = 1e-3
env = IP_env()
env.close_window()
goal_steps = 500
score_requirement = 150
initial_games = 1000

def initial_population():
    training_data = []
    scores = []
    accepted_scores = []
    while len(accepted_scores)<100:
        score = 0
        game_memory = []
        prev_observation = []
        for _ in range(goal_steps):
            action = random.choice([0,1])
            observation, reward, done, info = env.step(action)
            game_memory.append([observation, action])
            score+=reward
            if done: break

        if score >= score_requirement:
            accepted_scores.append(score)
            for data in game_memory:
                # convert to one-hot (this is the output layer for our neural network)
                if data[1] == 0:
                    output = [0,1]
                elif data[1] == 1:
                    output = [1,0]
                    
                # saving our training data
                training_data.append([data[0], output])

        # reset env to play again
        env.reset()
        # save overall scores
        scores.append(score)
    
    return training_data,accepted_scores
def neural_network_model(input_size):

    network = input_data(shape=[None, input_size, 1], name='input')

    network = fully_connected(network, 128, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 512, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 128, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 2, activation='softmax')
    network = regression(network, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')
    model = tflearn.DNN(network)

    return model
def train_model(training_data, model=False):

    X = np.array([i[0] for i in training_data]).reshape(-1,len(training_data[0][0]),1)
    y = [i[1] for i in training_data]

    if not model:
        model = neural_network_model(input_size = len(X[0]))
    
    model.fit({'input': X}, {'targets': y}, n_epoch=2, snapshot_step=1, show_metric=True)
    return model

if __name__=="__main__":
    training_data,training_scores = initial_population()
    model = train_model(training_data)
    scores = []
    choices = []
    for each_game in range(10):
        score = 0
        game_memory = []
        #env.close_window()
        obs = env.get_obs()
        for _ in range(goal_steps):
            sleep(env.dt)
            action = np.argmax(model.predict(obs.reshape(-1,len(obs),1))[0])
            choices.append(action)

            obs, reward, done, info = env.step(action)
            game_memory.append([obs, action])
            score+=reward
            #print((-pi/12)<obs[0]<(pi/12)or(-2.4<obs[2]<2.4),done)
            if done: break

        scores.append(score)

    print('Average Score:',mean(scores))
    print('choice 1:{}  choice 0:{}'.format(choices.count(1)/len(choices),choices.count(0)/len(choices)))
    print(score_requirement)
    print('Average accepted score:',mean(training_scores))
    print('Median score for accepted scores:',median(training_scores))
    print(Counter(training_scores))
