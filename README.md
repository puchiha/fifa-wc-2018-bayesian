# fifa-wc-2018-bayesian
fifa wc prediction

Using Bayesian methods of Machine Learning to predict the outcome of the World Cup 2018

This project is a Bayesian model to predict the probability that a team will win the competition. To predict the win, lose, draw probabilities using historical data (expert knowledge) as prior information and FIFA ratings as the covariate. The strength of our Bayesian approach is that our sets of knowledge to build the posterior distributions and historical information can be easily updated to overcome the lack of information to characterize the FIFA World Cup 2018. 

The FIFA 18 dataset is imported by scraping the website sofifa.com.  Using these statistics we form the best squad available for each team. A squad must consist of one goalkeeper (GK), 3 to 5 defenders (LB, RB, CB, LWB, RWB), 3 to 5 midfielders (CM, CDM, LM, RM) and 1 to 3 attackers (LW, RW, ST, CAM) to form a total of 11 players. While forming the squads, we assume that each player will be playing to their maximum potential and that they will play with a formation that maximizes the overall team rating. A team is classified into 3 tiers based on their overall rating and current ranking. 

The historical results for the games played by nations over several tournaments and friendly matches was obtained from kaggle.com/martj42/international-football-results-from-1872-to-2017. For this project, we only considered the games played after 1990.

The simulation consistently resulted in France with the highest probability to win the World Cup with 35.94% followed by Spain with $14.10~\%$. Comparing our results with sportsbook betting odds, we notice that our model is comparable.

#### RESULTS
**Country**			**Win Prob**

Panama			3.40782532144e-21 %    
Tunisia			3.33870889796e-17 %    
Costa Rica			1.06054606769e-15 %    
Iceland			1.15047168436e-15 %    
Peru			9.49614627603e-15 %    
Iran			4.08477523177e-13 %    
Australia			5.47302353197e-13 %    
Japan			8.92773312939e-12 %    
Saudi Arabia			1.1233077319e-11 %    
Korea Republic			1.77807982253e-10 %    
Egypt			4.84056461218e-10 %    
Nigeria			6.971036813e-09 %    
Morocco			2.81934931466e-08 %    
Russia			4.39508383554e-08 %    
Mexico			4.64058794879e-08 %    
Sweden			5.89491079778e-08 %    
Serbia			1.16489197847e-07 %    
Colombia			3.24268552996e-07 %    
Senegal			2.89937494555e-05 %    
Denmark			0.000485088548152 %    
Switzerland			0.000500315725254 %    
Poland			0.000868767325681 %    
Croatia			0.000929753461322 %    
Uruguay			0.00958912600344 %    
England			3.69990985263 %    
Portugal			3.77546986039 %    
Belgium			7.85135736102 %    
Germany			10.0409017291 %    
Brazil			11.5166605718 %    
Argentina			13.0688666473 %    
Spain			14.0985860463 %    
France			35.9358452608 %    