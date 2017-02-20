
from __future__ import print_function
# Importing some common modules
import os, sys
import random
import array

'''
Created on Nov 11, 2016

@author: Make AI Great Again
'''

class Strategy(object):
    def play(self, hist):
        r = random.random();
        if(r < 1/3.0):
            return "R";
        elif(r < 2/3.0):
            return "P";
        else:
            return "S";

class AlwaysRock(Strategy):
    def play(self, hist):
        return "R";

class AlwaysPaper(Strategy):
    def play(self, hist):
        return "P";

class AlwaysScissors(Strategy):
    def play(self, hist):
        return "S";

class UsuallyRock(Strategy):
    def play(self, hist):
        r = random.random();
        if(r < .5):
            return "R";
        elif(r < .75):
            return "P";
        else:
            return "S";
class UsuallyPaper(Strategy):
    def play(self, hist):
        r = random.random();
        if(r < .5):
            return "P";
        elif(r < .75):
            return "R";
        else:
            return "S";
class UsuallyScissors(Strategy):
    def play(self, hist):
        r = random.random();
        if(r < .5):
            return "S";
        elif(r < .75):
            return "P";
        else:
            return "R";
class BeatOpponentsLast(Strategy):
    def play(self, hist):
        if(len(hist)==0):
            return Strategy.play(self,hist);
        else:
            return beat(hist[len(hist)-1][1]);
class CopyOpponentsLast(Strategy):
    def play(self, hist):
        if(len(hist)==0):
            return Strategy.play(self,hist);
        else:
            return hist[len(hist)-1][1];
class FollowPattern(Strategy):
    i = -1;
    patt = ["R"];
    def __init__(self, pat):
        self.patt = pat;
    def play(self, hist):
        if(len(self.patt) == 0):
            return Strategy.play(self, hist)
        else:
            self.i = (self.i+1)%len(self.patt);
            return self.patt[self.i];




def beat(str):
    if(str=="R"):
        return "P";
    elif(str=="P"):
        return "S";
    elif(str=="S"):
        return "R";
    else:
        print("ERROR: INVALID INPUT TO BEAT FUNCTION: " + str);
        return "ERROR";

#1 indicates a win for p1, -1 indicates a win for p2, 0 indicates a tie
def winner(str1, str2):
    if(str1==str2):
        return 0;
    elif(str1 == beat(str2)):
        return 1;
    elif(str2 == beat(str1)):
        return -1;
    else:
        print("ERROR: INVALID INPUT TO WINNER FUNCTION");
        return -2;

def indicator(s1, s2):
    if(s1==s2):
        return 1;
    else:
        return 0;


class MarkovModel():
    def __init__(self, transitions, emissions, initial_state_distribution):
        self.transitions = transitions;
        self.emissions = emissions;
        self.initial_state_distribution = initial_state_distribution;
    def predictNext(self, observations):
        vec = self.forwards(observations)[len(observations)-1];
        vec2 = [sum([vec[i]*self.transitions[i][j] for i in range(0, len(self.initial_state_distribution))]) for j in range(0, len(self.initial_state_distribution))];
        emi = [sum([vec2[i]*self.emissions[i][j] for i in range(0, len(self.transitions))]) for j in range(0, len(self.emissions[0]))];
        for i in range(0, len(emi)):
            if( emi[i] == max(emi)):
                return i;
    def forwards(self, observations):
        return self.forwardsT(observations, len(observations)-1);
    def forwardsT(self, observations, time):
        if(time == 0):
            return [[ self.initial_state_distribution[i]*self.emissions[i][observations[0]] for i in range(0, len(self.initial_state_distribution))]];
        elif (time > 0):
            mat1 = self.forwardsT(observations, time-1);
            vec = [ self.emissions[j][observations[time]] * sum([ mat1[time-1][i]*self.transitions[i][j] for i in range(0, len(self.initial_state_distribution))]) for j in range(0, len(self.initial_state_distribution))];
            mat1.append(vec);
            return mat1;
    def backwards(self, observations):
        return self.backwardsT(observations, 0);
    def backwardsT(self, observations, time):
        if (time == len(observations)-1):
            return [[1 for i in range(0, len(self.initial_state_distribution))]];
        elif (time < len(observations)-1):
            mat2 = self.backwardsT(observations, time+1);
            vec = [[sum([mat2[0][j]*self.transitions[i][j]*self.emissions[j][observations[time+1]] for j in range(0, len(self.initial_state_distribution))]) for i in range(0, len(self.initial_state_distribution))]]
            vec += mat2;
            return vec;
    def update(self, observations, epsilon):
        alpha = self.forwards(observations);
        beta = self.backwards(observations);

        gamma = [[0.0 for i in range(0, len(self.initial_state_distribution))] for t in range(0, len(observations))];
        for t in range(0, len(observations)):
            su = sum([alpha[t][i]*beta[t][i] for i in range(0, len(self.transitions))]);
            if(su == 0):
                gamma[t] = [1/len(self.initial_state_distribution) for i in range(0, len(self.initial_state_distribution))];
            else:
                for i in range(0, len(self.transitions)):
                    gamma[t][i] = (alpha[t][i]*beta[t][i] / su);
        
        xi = [[[0.0 for j in range(0, len(self.transitions))] for i in range(0, len(self.transitions))] for t in range(0, len(observations)-1)];
        for t in range(0, len(observations)-1):
            su = sum([sum([alpha[t][i]*self.transitions[i][j]*beta[t+1][j]*self.emissions[j][observations[t+1]] for j in range(0, len(self.transitions))]) for i in range(0, len(self.transitions))]);
            if(su == 0):
                xi[t] = [[1/len(self.initial_state_distribution) / len(self.initial_state_distribution) for j in range(0, len(self.initial_state_distribution))] for i in range(0, len(self.initial_state_distribution))]
            else:
                for i in range(0, len(self.transitions)):
                    for j in range(0, len(self.transitions)):
                        xi[t][i][j] = alpha[t][i]*self.transitions[i][j]*beta[t+1][j]*self.emissions[j][observations[t+1]]/su;
        
        unchanged = True;
        
        new_transitions = [[0.0 for j in range(0, len(self.initial_state_distribution))] for i in range(0, len(self.initial_state_distribution))]
        for i in range(0, len(new_transitions)):
            if(sum([gamma[t][i] for t in range(0, len(observations)-1)]) == 0):
                new_transitions[i] = [1/len(new_transitions[i]) for j in range(0, len(new_transitions[i]))]
            else:
                for j in range(0, len(new_transitions[i])):
                    new_transitions[i][j] = sum([xi[t][i][j] for t in range(0, len(observations)-1)]) / sum([gamma[t][i] for t in range(0, len(observations)-1)]);
        new_emissions = [[0.0 for j in range(0, len(self.emissions[i]))] for i in range(0, len(self.emissions))]
        for i in range(0, len(new_transitions)):
            if(sum([gamma[t][i] for t in range(0, len(observations))]) == 0):
                new_emissions[i] = [1/len(new_emissions[i]) for j in range(0, len(new_emissions[i]))]
            else:
                for j in range(0, len(new_emissions[i])):
                    new_emissions[i][j] = sum([indicator(observations[t], j) * gamma[t][i] for t in range(0, len(observations))]) / sum([gamma[t][i] for t in range(0, len(observations))]);
        if( epsilon < max([max([self.transitions[i][j] - new_transitions[i][j] for j in range(0, len(self.transitions[i]))]) for i in range(0, len(self.transitions))])):
            unchanged = False;
        if( epsilon < max([max([self.emissions[i][j] - new_emissions[i][j] for j in range(0, len(self.emissions[i]))]) for i in range(0, len(self.emissions))])):
            unchanged = False;
        self.transitions = new_transitions;
        self.emissions = new_emissions;
        return not unchanged;


class HMMPlayer(Strategy):
    def play(self, hist):
        r = random.random();
        i = -1;
        while r > 0:
            i += 1;
            r -= self.mar.emissions[self.state][i];
        j = -1;
        r = random.random();
        while r > 0:
            j += 1;
            r -= self.mar.transitions[self.state][j];
        self.state = j;
        if(i == 0):
            return "R";
        elif(i == 1):
            return "P";
        else:
            return "S";
    def __init__(self, trans, emiss, isd):
        self.mar = MarkovModel(trans, emiss, isd);
        self.state = 0;
#'''
class HMMAI(Strategy):
    def play(self, hist):
        if(hist == []):
            return Strategy.play(self, hist);
        obs = [];
        for i in range(max([0,len(hist)-self.SizeOfWindow]), len(hist)):
            if (hist[i][1] == "R"):
                obs.append(0);
            elif (hist[i][1] == "P"):
                obs.append(1);
            elif (hist[i][1] == "S"):
                obs.append(2);
        NumOfStates = self.NumOfStates;
        NumOfEmissions = 3;
        trans = [[random.random() for j in range(0,NumOfStates)]for i in range(0,NumOfStates)]
        for i in range(0, len(trans)):
            su = sum(trans[i]);
        for j in range(0, len(trans[i])):
            trans[i][j] /= su;
        emiss = [[random.random() for j in range(0,NumOfEmissions)] for i in range(0, NumOfStates)]
        for i in range(0, len(emiss)):
            su = sum(emiss[i]);
            for j in range(0, len(emiss[i])):
                emiss[i][j] /= su;
        isd = [0 for i in range(0, NumOfStates)];
        isd[0] = 1;
        mar = MarkovModel(trans, emiss, isd);
        while(mar.update(obs, .0001)):
            pass;
        x = mar.predictNext(obs);
        if(x==0):
            return "P";
        if(x==1):
            return "S";
        if(x==2):
            return "R";
        return "R";
    def __init__(self, numStates, windowSize):
        self.NumOfStates = numStates;
        self.NumOfEmissions = 3;
        self.SizeOfWindow = windowSize;

def main():
    print("HI I AM THE RPS ALGORITHM");
    random.seed(0);
    hist1 = [];
    hist2 = [];
    
    
    
    player1 = HMMAI(20, 10);
    player2 = UsuallyScissors();
    wins = 0;
    ties = 0;
    losses = 0;
    for i in range(0,1000):
        play1 = player1.play(hist1);
        play2 = player2.play(hist2);
        print(str(i) + "   " + play1 + "   " + play2 + "     " + str(winner(play1, play2)));
        outcome = winner(play1, play2);
        if(outcome == 1):
            wins += 1;
        elif(outcome == 0):
            ties += 1;
        else:
            losses += 1;
        hist1.append([play1, play2]);
        hist2.append([play2, play1]);
    print("OUR AI WON " + str(wins) + " TIMES");
    print("OUR AI TIED " + str(ties) + " TIMES");
    print("OUR AI LOST " + str(losses) + " TIMES");

main();
