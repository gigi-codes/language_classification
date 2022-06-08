#pip install pmaw

# IMPORTS
import pandas as pd
import datetime as dt
import pmaw
from pmaw import PushshiftAPI

#CONFIG 
pd.options.display.max_columns = 50
pd.options.display.max_rows = 150

##### extract/ import data using pmaw
api = PushshiftAPI()
# time limit 
before = int(dt.datetime(2022,3,26,0,0).timestamp())
after = int(dt.datetime(2010,12,1,0,0).timestamp())

# limt for pull: 1000 pulls 1000 from comments and submissions for both, a total of 4000
limit=1000

sub_name_1 = 'ModelX'             # 1 = model x 
sub_name_2 = 'Taycan'

print("PULLING COMMENTS FROM SUBREDDIT 1... ")
sub_1_comments = api.search_comments(subreddit=sub_name_1, limit=limit, before=before, after=after)
sub_1_submissions = api.search_submissions(subreddit=sub_name_1, limit=limit, before=before, after=after)
print('COMPLETED PULL FROM SUB 1, PULLING SUB 2 ... ')

sub_2_comments = api.search_comments(subreddit=sub_name_2, limit=limit, before=before, after=after)
sub_2_submissions = api.search_submissions(subreddit=sub_name_2, limit=limit, before=before, after=after)
print('COMPLETED PULL FROM BOTH.')

print(f'Retrieved {len(sub_1_comments) + len(sub_1_submissions)} comments and submissions from {sub_name_1}')
print(f'Retrieved {len(sub_2_comments) + len(sub_2_submissions)} comments and submissions from {sub_name_2}')

print('CONVERTING TO DF, EXTRACTING SELECTED DATA, CONCACTANATING DFs... ')
# convert generator object to pd.df
sub1_com_df = pd.DataFrame(sub_1_comments)
sub1_sub_df = pd.DataFrame(sub_1_submissions)

sub2_com_df = pd.DataFrame(sub_2_comments)
sub2_sub_df = pd.DataFrame(sub_2_submissions)

# extract column of interest from each df
sub1_com_df = sub1_com_df['body']
sub1_sub_df = sub1_sub_df['selftext']

sub2_com_df = sub2_com_df['body']
sub2_sub_df = sub2_sub_df['selftext']

# concact comment + submissions df 
sub_1  = pd.concat((sub1_com_df, sub1_sub_df), axis = 0)
sub_2  = pd.concat((sub2_com_df, sub2_sub_df), axis = 0)

# print (sub_1.shape, sub_2.shape)

# convert to df again? Then add class-series
sub_1 = pd.DataFrame(sub_1)
sub_1['class'] = 1

sub_2 = pd.DataFrame(sub_2)
sub_2['class'] = 0

# print (sub_1.shape, sub_2.shape)

# concact both classes
corpus = pd.concat((sub_1, sub_2), axis = 0)
corpus.shape

# renaming text corpus
corpus.rename(columns = {'0': 'corpus'}, inplace=True)


filename = '../data/' + 'reddit' + str(limit) + '.csv'

print (f'EXPORTING {filename} TO CSV...')

corpus.to_csv(filename, index = False)

print ("DONE. ")