
# NLP: Online Luxury Car Affinity Groups
This project models language used by current and potential owners of luxury electric SUVs to better target markets: can a trained model correctly classify posts from a Tesla Model X or Porsche Taycan forum?

I gathered data from the <a href = https://www.reddit.com/r/ModelX/> Model X </a> and <a href = "https://www.reddit.com/r/Taycan/"> Taycan </a> subreddits, and cleaned to train 2 models using 3 estimators and 2 transformers to classify the posts. A `Multinomial Naïve Bayes` estimator on text transformed with `Count Vectorizer` accurately classified `0.77` dictionaries from the test corpus. Reviewing misclassified posts confirms the model perfoms well on topical language. 

-----
## Data Acquisition & Cleaning 

I used a custom python script `redditpull.py` to gather and save data as `csv`: with <a href = "https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html" > `praw` </a>, a wrapper for <a href = "http://reddit-api.readthedocs.io/en/latest/"> `Pushshift API` </a>, I collected `2000` submissions and comments, `4000` total observations from each subreddit: `8000` total, but `4537` unique observations after cleaning: 

* 43% of collected observations/dictionaries were omitted: 
    * null (images, videos)
    * duplicate 

<center>

subreddit   | observations | balance
---         |---        | --
Taycan      | 2235      | 49.3%
Model X     | 2302      | 50.7%

</center>

Before modelling, I determined the most common words (excluding `english` stop-words in `sklearn`) for the whole dataset, as well as for each class/subreddit, and selected additional custom `stop words`. 

<center>

CUSTOM      | STOP      | WORDS
---         |---        | ---
porsche     | tesla     | taycan
model       | xplaid    |turbo
turismo     | _elon_    | _musk_ 

</center>

### Additional cleaning steps: 
* removed all numbers to remove specific vehicle-model numbers 
* flattened to _lower case_

<center>

<img src = images/overallwords.png><br>
<i>Top 25 Words, Overall</i> 
<br> <br>

<img src = images/taycanwords.png><br>
<i>Top 25 Words, Taycan</i> 
<br> <br>

<img src = images/xwords.png><br>
<i>Top 25 Words, Model X  </i>

</center>

## Modeling & Results

With _ACCURACY_ as metric, _transformer_, _classifer_ and results for selected models are shown below. Models 1 and 2 (denoted with *) were trained with default hyper-parameters, and the remainder were trained with best hyperparameters estimated though a _GridSearchCV_, but all improved accuracy from baseline `0.5074`.

<center>


Model   | Transformer       | Classifier            | $n$  | x-val   | Train    | Test   
---     |---                | ---                   | ---  | ---     | ---      | ---    
1*      | Count Vectorizer  | Logistic Regressor    | 2605 | 0.7373  | 0.9723   | 0.7515 
2*      | Count Vectorizer  | Logistic Regressor    | 4537 | 0.7111  | 0.9568   | 0.7436 
3       | Count Vectorizer  | Random Forest	        | 4537 | 0.7569  | 0.9855   | 0.7154 
4       | Count Vectorizer  | Naïve Bayes	        | 4537 | 0.7587  | 0.8628   | 0.7722 
5       | TF-IDF            | SVM                   | 4537 | 0.7834  | 0.9793   | 0.7509 
6       | TF-IDF            | Logistic Regressor    | 4537 | 0.7834  | 0.9671   | 0.7296   
7       | TF-IDF            | Naïve Bayes           | 4537 | 0.7834  | 0.8989   | 0.7659  
8       | Count Vectorizer  | Naïve Bayes	        | 4537 | 0.7593  | 0.8823   | 0.7740 
9       | Count Vectorizer  | Naïve Bayes, <i>elon, musk</i>        | 4537 | 0.7594  | 0.8823  | 0.7730 

<br>
<img src = 'images/allmodels.png'>
<br>
<br>

</center>


* Both `model 1` an `model 2` preformed surprisingly well for the data provided, the stopwords and the lack of hyperparameter tuning over a gridsearch. 
* _Random Forests_ `accuracy` for test vs train sets showed a very overfit model, even with optimized hyperparameters over a gridsearch, and worse performance than previous models.
* _Naïve Bayes_ on data transformed with _Count Vectorizer_ produced a model with the best results: train accuracy was `0.86`, and test accuracy was `0.77`, only about `0.9` diffence compared over `0.2` $\Delta$ for Random Forest. 
* _Naïve Bayes_ with _TF-IDF_ but accuracy was comparable to best models, but more overfit. 
* _Logistic Regression_ and _Naïve Bayes_ with_Count Vectorizer_ produced the best models, and endeavor to imporve using _TF-IDF_ was unsusccessful
    * Naïve Bayes Multinomial _"normally requires integer feature counts. However, in practice, fractional counts such as TF-IDF may also work."_ Term-frequency times inverse document-frequency is a weighting scheme, so while the documentation states it _may_ work, there was no improvement in either _Logistic Regression_ or _Naïve Bayes_ model performance using fractional weights.  
* Running best over a `hyperparameter` _GridSearch_ to optimize hyperparameters improved _accuracy_ for '`model 9` less than 0.5% compared to `model 4`.
* Model 9 includes additional stop words `elon`, `musk`, whcih decreased acccuracy from `0.7740` to `0.7730`.


 # Conclusion
 Model performace strongly suggests we can use specific language to tailor different markets, or use the lexicon of one group to persuade them to a different product. This best model, _Naïve Bayes_ on data transformed with _Count Vectorizer_, used `4537` total observations from two subbredits for an accuracy of `0.77` on test data. However, the next steps to produce a more rigorous model include: 

 * obtain more data from the same sources
 * source from different, adjacent subreddits: 
    * r/tesla 
    * r/porsche 
* source from different venues: 
    * product-specific forums 
    * facebook 
    * twitter
    * tiktok 