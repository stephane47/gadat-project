Final Project: Predicting the return of peer to peer loans
======
------
## Project goals:

###1. Create model for predicting loan success
###2. Improve model by adding another source of information

![alt text](images/path5131.png "no title")

---

## Incorporating Zillow data:


* LC data contains insufficient date information for accurate combination
* Using the slope of the rents over the interval that the loans occurred. 
* Add slope & intercept as features to the model

![alt text](images/sample-rent-fits.png "no title")


---


## Model Performance & Comparison:
### Model fit & accuracy Scores

* Using grid search with logistic regression to fit a model both with and without the zip code data.
Results: slightly different models!

![alt text](images/pred-prob.png "no title")
![alt text](images/pred-probz.png "no title")

* Accuracy scores shown for y_test:

![alt text](images/gridsearch-results.png "no  title")

---
## Model Performance & Comparison:
### Confusion Matrices

* For another comparison of performance, look at the confusion matrices:
Very small difference in predictions


![alt text](images/confustions.png "no title")

---
## Model Performance & Comparison:
### ROC & AUC 

* Where to adjust the threshold

![alt text](images/roc-auc.png "no title")
![alt text](images/tpr-tnr-thresh.png "no title")

---

