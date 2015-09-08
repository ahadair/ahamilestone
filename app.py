from flask import Flask,render_template,request,redirect
import requests
import simplejson as json
from datetime import datetime
from bokeh.plotting import figure, show, output_file
#from bokeh.plotting import figure, show, output_notebook
#from bokeh.plotting import figure, show, output_server

app_lulu = Flask(__name__)
app_lulu.vars={}



def get_date(jsondate):
    return int(jsondate[:4]), int(jsondate[5:7]), int(jsondate[8:])




print "Declarations"



@app_lulu.route('/index_lulu',methods=['GET','POST'])
def index_lulu():
    print "Index Lulu"
    if request.method == 'GET':
        return render_template('userinfo_lulu.html')
    else:
        #request was a POST
        app_lulu.vars['ticker'] = request.form['ticker_lulu']
        app_lulu.vars['cprice'] = request.form['cprice_lulu']
        app_lulu.vars['aprice'] = request.form['aprice_lulu']
        app_lulu.vars['volume'] = request.form['volume_lulu']

        print "Ticker Value =", app_lulu.vars['ticker']
        print "CPrice =", app_lulu.vars['cprice']
        print "APrice =", app_lulu.vars['aprice']
        print "Volume =", app_lulu.vars['volume']


        #stock = 'GOOG'
        stock = app_lulu.vars['ticker']
        path = 'https://www.quandl.com/api/v3/datasets/WIKI/%s.json' % (stock)
        r = requests.get(path)
        thedict = json.loads(r.text)
        newestdate = thedict["dataset"]["newest_available_date"]
        newestyear, newestmonth, newestday = get_date(newestdate)
        #newestdate = dt.strptime(thedict["dataset"]["newest_available_date"], '%Y-%M-%d')
        prioryear = newestyear
        priormonth = newestmonth - 1
        priorday = newestday
        if priormonth == 0:
            priormonth = 12
            prioryear = prioryear - 1
        priordate = '%s-%s-%s' % (prioryear, priormonth, priorday)
        columnnames = thedict["dataset"]["column_names"]
        datecol = columnnames.index("Date")
        closecol = columnnames.index("Close")
        adjclosecol = columnnames.index("Adj. Close")
        volumecol = columnnames.index("Volume")
        print newestdate, newestyear, newestmonth, newestday
        print priordate, prioryear, priormonth, priorday
        #print datecol, closecol, volumecol, adjclosecol
        data = thedict["dataset"]["data"]

        #output_server("AHAmarkers.html")
        output_file("markers.html")
        #output_notebook
        #range okay
        p = figure(width=800, height=500, x_axis_type="datetime", x_range=(datetime(prioryear,priormonth,priorday), datetime(newestyear,newestmonth,newestday)))


        datelist = []
        closecollist = []
        volumecollist = []
        adjclosecollist = []
        for row in data:
            rowyear, rowmonth, rowday = get_date(row[datecol])
            #print rowyear, rowmonth, rowday
            datelist.append(datetime(rowyear,rowmonth,rowday))
            closecollist.append(row[closecol])
            volumecollist.append(row[volumecol])
            adjclosecollist.append(row[adjclosecol])

        if app_lulu.vars['volume']=='checked':
            p.line(datelist, volumecollist, color='red', alpha=0.5, legend='volume')

        if app_lulu.vars['aprice']=='checked':
            p.line(datelist, adjclosecollist, color='green', alpha=0.5, legend='adj. close')

        if app_lulu.vars['cprice']=='checked':
            p.line(datelist, closecollist, color='navy', alpha=0.5, legend='close')


        p.title = "%s Stock Fluctations for ~ the last month" % (stock)
        p.xaxis.axis_label = 'date'

        show(p)
            








        return redirect('/main_lulu')



@app_lulu.route('/main_lulu')
def main_lulu2():
    print "Main lulu2"
    return render_template('end_lulu.html')


if __name__ == "__main__":
    app_lulu.run()
