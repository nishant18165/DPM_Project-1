from flask import Flask, render_template
from flask import request,redirect

app = Flask(__name__)

@app.route("/error")
def error():
    return render_template('error.html')
    
direct='none'
@app.route("/",methods=['GET','POST'])
def main():
    global direct
    if(request.method=='POST'):
        print("clicked")
        direct=request.form['sel']
        if(direct=="movie"):
            return redirect('/movie')
        elif(direct=="subject"):
            return redirect('/subject')
        elif(direct=="person"):
            return redirect('/person')
        elif(direct=="leader"):
            return redirect('/leader')

        else:
            return redirect('/')
    else:
        print("not clicked")
        return render_template('index.html')


@app.route('/movie', methods=['GET','POST'])
def movie():
    if(request.method=='POST'):
        print('clicked movie')
        movie_name=request.form['movie_name']
        no_tweet=request.form['number_of_tweet']
        print(movie_name,no_tweet)
        return redirect('/')
    else:
        print('not clicked movie')
        return render_template('movie.html')


@app.route('/subject', methods=['GET','POST'])
def subject():
    if(request.method=='POST'):
        subject_name=request.form['subject@name']
        no_tweet=request.form['no@tweet']
        print(subject_name,no_tweet)
        print('clicked subject')
        return redirect('/')
    else:
        print('not clicked subject')
        return render_template('subject.html')


@app.route('/person', methods=['GET','POST'])
def personal():
    #name_list=['Narendra Modi','Donald Trump','Joe Biden','Rahul Gandhi','Boris Johnson','Justin Treudo','Scott Morison','Angela Markel','Jacinda Ardern','Cyril Ramaphosa']
    if(request.method=='POST'):
        person_name=request.form['person_name']
        start_date=request.form['Start_Date']
        end_date=request.form['End_Date']
        print(person_name,start_date,end_date)
        print('clicked personal')
        return redirect('/')
    else:
        print('not clicked personal')
        return render_template('person.html')

@app.route('/leader', methods=['GET','POST'])
def leader():
    name_list=['Narendra Modi','Donald Trump','Joe Biden','Rahul Gandhi','Boris Johnson','Justin Treudo','Scott Morison','Angela Markel','Jacinda Ardern','Cyril Ramaphosa']
    if(request.method=='POST'):
        person_name=request.form['leader@name']
        start_date=request.form['Start_Date']
        end_date=request.form['End_Date']
        print(person_name,start_date,end_date)
        print('clicked leader')
        return redirect('/leader')
    else:
        print('not clicked leader')
        return render_template('leader.html',name_list=name_list)

if __name__ == "__main__":
    app.run(debug=True)