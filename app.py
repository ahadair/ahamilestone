from flask import Flask,render_template,request,redirect, Markup
import requests
import simplejson as json
from datetime import datetime
from bokeh.plotting import figure, show
from bokeh.embed import components




app = Flask(__name__)
app.vars={}



def get_date(jsondate):
    return int(jsondate[:4]), int(jsondate[5:7]), int(jsondate[8:])






@app.route('/index_lulu',methods=['GET','POST'])
def index_lulu():
    if request.method == 'GET':
        return render_template('userinfo.html')
    else:
        #request was a POST
        app.vars['ticker'] = request.form['ticker_lulu']
        app.vars['cprice'] = request.form['cprice_lulu']
        app.vars['aprice'] = request.form['aprice_lulu']
        app.vars['volume'] = request.form['volume_lulu']

        stock = app.vars['ticker']
        path = 'https://www.quandl.com/api/v3/datasets/WIKI/%s.json' % (stock)
        r = requests.get(path)
        thedict = json.loads(r.text)
        newestdate = thedict["dataset"]["newest_available_date"]
        newestyear, newestmonth, newestday = get_date(newestdate)
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
        data = thedict["dataset"]["data"]


        #range okay
        p = figure(width=800, height=500, x_axis_type="datetime", x_range=(datetime(prioryear,priormonth,priorday), datetime(newestyear,newestmonth,newestday)))


        datelist = []
        closecollist = []
        volumecollist = []
        adjclosecollist = []
        for row in data:
            rowyear, rowmonth, rowday = get_date(row[datecol])
            datelist.append(datetime(rowyear,rowmonth,rowday))
            closecollist.append(row[closecol])
            volumecollist.append(row[volumecol])
            adjclosecollist.append(row[adjclosecol])

        if app.vars['volume']=='checked':
            p.line(datelist, volumecollist, color='red', alpha=0.5, legend='volume')

        if app.vars['aprice']=='checked':
            p.line(datelist, adjclosecollist, color='green', alpha=0.5, legend='adj. close')

        if app.vars['cprice']=='checked':
            p.line(datelist, closecollist, color='navy', alpha=0.5, legend='close')


        p.title = "%s Stock Fluctations for ~ the last month" % (stock)
        p.xaxis.axis_label = 'date'

        script, div = components(p)
        return render_template("graph.html", script=Markup(script),div=Markup(div))




if __name__ == "__main__":
    app.run()
