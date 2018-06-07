from sklearn.naive_bayes import GaussianNB
import numpy as np
import pandas as pd



#import csv and separate data from targets
matchdata = pd.read_csv('data/WC18_competition_stats.csv')
data = matchdata.iloc[:, range(1,11)]
targets = matchdata.iloc[:, -1]

print data.head(1)
print targets.head(1)
gnb = GaussianNB()
model = gnb.fit(data, targets)
print model
prob_matrix = np.zeros((32,32))
#For each pair of teams, find predicted label, convert to probability.

teamdata = pd.read_csv('data/WC18_processed.csv')


for i in range(0,32):
    for j in range(i,32):
        teamA = teamdata.iloc[i,:]
        teamB = teamdata.iloc[j,:]

        point = [teamA.Attack, teamB.Attack, teamA.Defence, teamB.Defence, teamA.Midfield, teamB.Midfield, teamA.Rating, teamB.Rating, teamA.Tier, teamB.Tier]
        df = pd.DataFrame(np.array(point).reshape((1,10)), columns=data.columns)
        winner = gnb.predict(df)
        probs = gnb.predict_proba(df)

        prob_matrix[i,j] = .5 * probs[0,1] + probs[0,2]
        prob_matrix[(j,i)] = .5 * probs[0,1] + probs[0,0]
print point
print df
#print prob_matrix