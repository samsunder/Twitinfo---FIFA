import csv
from textblob import TextBlob
import re
import matplotlib.pyplot as plt
import os
import csv
import pandas as pd
maindir = os.path.dirname(os.path.abspath(__file__))

tweets = []

infile1 = 'positive.csv'
infile2 = 'worldcities.csv'
outfile= open("test_countries_positve.csv","w")

print('MAIN\n')


pddata3 = pd.read_csv(infile1,encoding='latin-1')
pddata4 = pd.read_csv(infile2,encoding='latin-1')

for x in pddata3:
        print(x)

df = pd.DataFrame(pddata3)
c = df.groupby('Country').count()

print (c)










