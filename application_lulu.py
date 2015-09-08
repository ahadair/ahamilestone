from flask import Flask,render_template,request,redirect
app_lulu = Flask(__name__)

app_lulu.vars={}

app_lulu.questions={}
#app_lulu.questions['How many eyes do you have?']=('1','2','3')


#app_lulu.getclosingprice = False
#app_lulu.getadjustedclosingprice = False
#app_lulu.getvolume = False



#####app_lulu.questions['Which fruit do you like best?']=('banana','mango','pineapple')
#####app_lulu.questions['Do you like cupcakes?']=('yes','no','maybe')

app_lulu.nquestions=len(app_lulu.questions)
#should be 3

print "Declarations"



@app_lulu.route('/index_lulu',methods=['GET','POST'])
def index_lulu():
    print "Index Lulu"
    nquestions=app_lulu.nquestions
    if request.method == 'GET':
        return render_template('userinfo_lulu.html',num=nquestions)
    else:
        #request was a POST
        #        app_lulu.vars['name'] = request.form['name_lulu']
        #        app_lulu.vars['age'] = request.form['age_lulu']
        app_lulu.vars['ticker'] = request.form['ticker_lulu']

        #print "CPrice Value =", request.form['cprice_lulu']
        #app_lulu.vars['cprice'] = request.form['cprice_lulu']

        app_lulu.vars['cprice'] = request.form['cprice_lulu']
        app_lulu.vars['aprice'] = request.form['aprice_lulu']
        app_lulu.vars['volume'] = request.form['volume_lulu']

        print "Ticker Value =", app_lulu.vars['ticker']
        print "CPrice =", app_lulu.vars['cprice']
        print "APrice =", app_lulu.vars['aprice']
        print "Volume =", app_lulu.vars['volume']


        #f = open('%s_%s_%s.txt'%(app_lulu.vars['name'],app_lulu.vars['age'], app_lulu.vars['ticker']),'w')
        f = open('%s.txt'%(app_lulu.vars['ticker']),'w')
        #f = open('%s%s%s%s.txt'% (app_lulu.vars['ticker'],app_lulu.vars['cprice'],app_lulu.vars['aprice'],app_lulu.vars['volume'],'w')


        #f.write('Name: %s\n'%(app_lulu.vars['name']))
        #f.write('Age: %s\n\n'%(app_lulu.vars['age']))
        f.write('Ticker: %s\n\n'%(app_lulu.vars['ticker']))

        #f.write('Closing Price: %s\n\n'%(app_lulu.vars['cprice']))
        #f.write('Adjusted Closing Price: %s\n\n'%(app_lulu.vars['aprice']))
        #f.write('Volume: %s\n\n'%(app_lulu.vars['volume']))

        f.close()

        return redirect('/main_lulu')



@app_lulu.route('/main_lulu')
def main_lulu2():
    print "Main lulu2"
    return render_template('end_lulu.html')


#    if len(app_lulu.questions)==0 : return render_template('end_lulu.html')
#    return redirect('/next_lulu')


#
######################################
### IMPORTANT: I have separated /next_lulu INTO GET AND POST
### You can also do this in one function, with If and Else.
#
#@app_lulu.route('/next_lulu',methods=['GET'])
#def next_lulu():  #remember the function name does not need to match the URL
#    print "Next Lulu"
#    # for clarity (temp variables):
#    n=app_lulu.nquestions-len(app_lulu.questions)+1
#    q=app_lulu.questions.keys()[0] #python indexes at 0
#    a1=app_lulu.questions[q][0]
#    a2=app_lulu.questions[q][1]
#    a3=app_lulu.questions[q][2]
#
#    # save current question
#    app_lulu.currentq=q
#
#    return render_template('layout_lulu.html',num=n,question=q,ans1=a1,ans2=a2,ans3=a3)
#
#
#
#@app_lulu.route('/next_lulu',methods=['POST'])
#def next_lulu2():  #can't have two functions with the same name
#    # Here, we will collect data from the user.
#    # Then, we return to the main function, so it can tell us whether to 
#    # display another question page, or to show the end page.
#    print "Next Lulu2"
#
#
#    #f=open('%s_%s_%s.txt'%(app_lulu.vars['name'],app_lulu.vars['age'],app_lulu.vars['ticker']),'a') #a is for append
#    f=open('%s.txt'%(app_lulu.vars['ticker']),'a') #a is for append
#    f.write('%s\n'%(app_lulu.currentq))
#    f.write('%s\n\n'%(request.form['answer_from_layout_lulu'])) #do you know where answer_lulu comes from?
#    f.close()
#
#    app_lulu.questions.pop(app_lulu.currentq)
#
#    return redirect('/main_lulu')

if __name__ == "__main__":
    app_lulu.run()
