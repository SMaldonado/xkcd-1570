# https://pypi.org/project/iexfinance/

import pandas as pd
import datetime
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
from iexfinance.stocks import get_historical_data

NEWPLOTS = True

if len(sys.argv) > 1:
    if '-noplot' in sys.argv:
        NEWPLOTS = False

# shitty html generation

contents = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
  <meta content="text/html; charset=ISO-8859-1"
 http-equiv="content-type">
  <title>shitdelity</title>
</head>
<body>'''

contents_bottom = '''</body>
</html>'''

def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N)

def strToFile(text, filename):
#    """Write a file with the given name and the given text."""
    output = open(filename,"w")
    output.write(text)
    output.close()

# We will look at stock prices over the past year, starting at January 1, 2016
start = datetime.datetime(2016,1,1)
end = datetime.date.today()

t = ["SPY", "TSLA", "GOOG", "NVDA", "ADI", "ADBE", "COF", "CGC"]
days_avg = 60
days_avg2 = 7

for s in t:
    df_s = get_historical_data(s, start, end, output_format='pandas')
    dates = df_s.index[days_avg-1:]
    close = df_s.close.values
    avg = running_mean(close, days_avg)
    #avg2 = running_mean(close, days_avg2)
    dif = close[-1]-avg[-1]
    if dif > 0:
        doit = 'sell'
        doitcolor = 'green'
        sign = '+'
    else:
        doit = 'buy'
        doitcolor = 'red'
        sign = '-'

    if(NEWPLOTS):
        plt.figure()
        plt.plot(dates, avg, ls = '--')
        plt.axhline(avg[-1], label = '%s day close avg' % days_avg)
        #plt.plot(df_s.index[days_avg2-1:], avg2, c = 'green', ls = '--', label = '%s day close avg' % days_avg2)
        plt.plot(df_s.index[days_avg-1:-days_avg], close[days_avg-1:-days_avg], ls = '--', c = 'orange')
        plt.plot(df_s.index[-days_avg:], close[-days_avg:], ls = '-', c = 'orange', label = 'close')
        plt.title('%s - close vs %s day close avg' % (s, days_avg))
        plt.xlabel('%s$%0.2f (%0.2f %%) vs %s-day avg --> %s' % (sign, abs(dif), 100.0*abs(dif)/avg[-1], days_avg, doit), color = doitcolor)
        plt.legend()
        plt.savefig('%s.png' % s)


    contents += '''
    <img src = '%s.png' width = '500px'/>
    ''' % (s)

contents += contents_bottom
strToFile(contents, 'index.html')



