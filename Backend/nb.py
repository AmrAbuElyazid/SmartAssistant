from sklearn.naive_bayes import MultinomialNB
def classify(X, y, test):
	gnb = MultinomialNB()
	gnb.fit(X, y)
	y_pred = gnb.predict(test)
	return y_pred

