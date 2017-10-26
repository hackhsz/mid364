import pdb
import requests
import json
from flask import render_template
from flask import Flask, request
import difflib
from flask import Flask, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, SubmitField
from wtforms.validators import Required
from flask import make_response
#from flask import set_cookie
app = Flask(__name__)
app.config['SECRET_KEY']='my birthday wer123234'
#app.debug = True


class PokeForm(FlaskForm):
    name = StringField("Enter your favourite pokemon's name", validators=[Required()])
    submit = SubmitField('Submit')
    

@app.route('/')
def hello_world():
    #resp = make_response(render_template('pokemon.html'))
    
    return 'Hi Mauli and Jackie!'




@app.route('/pokemon')
def get_name():
    pokemonForm=PokeForm()
    resp = make_response(render_template('pokemon.html',form=pokemonForm))
    resp.set_cookie('pok','Machop')
    return resp


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internalerror(e):
    return render_template('500.html'),500


@app.route('/getname',methods=['GET','POST'])
def calcualte_2():
    form = PokeForm(request.form)
    print(form.name.data)
    if request.method == 'POST' and form.validate_on_submit():
        yourchosename = form.name.data
        with open('en.json') as data:
            d = json.load(data)
            names = d['pokemons']
            temp = {}
            sdf = []
            if yourchosename not in names:
                return render_template("404.html")
            for item in names:
                seq = difflib.SequenceMatcher(None,item,yourchosename)
                d = seq.ratio()*100
                if d > 40:
                    sdf.append(item)
            temp['similar']=sdf
            temp['main'] = yourchosename
        return render_template('pokemon_stats.html',data=temp)
    else:
        pokename = request.cookies.get('pok')
        with open('en.json') as data:
            d = json.load(data)
            names = d['pokemons']
            temp = {}
            sdf = []
            for item in names:
                seq = difflib.SequenceMatcher(None,item,pokename)
                d = seq.ratio()*100
                if d > 40:
                    sdf.append(item)
            temp['similar']=sdf
            temp['main'] = pokename
        return render_template('pokemon_stats.html',data=temp)
        #return render_template('pokemon_stats.html',data=temp)
    flash('All fields are required!')
    return redirect(url_for('get_name'))
        



            
@app.route('/getname/items/<pokemon_name>')
def blz(pokemon_name):
    if request.method == 'GET':
        
        response = requests.get('https://pokeapi.co/api/v2/pokemon/'+pokemon_name.lower())
        #if response.status_code != 200:
            #return redirect(url_for('get_name'))
        
        result = json.loads(response.text)
        return render_template('thispokemondata.html',data=result)
    flash('Please Fill In All Data')
    return redirect(url_for('get_name'))

@app.route('/gettype/<type>')
def aha(type):
    if request.method == 'GET':
        response = requests.get('https://pokeapi.co/api/v2/type/'+type.lower())
        result = json.loads(response.text)
 #       pdb.set_trace()
#        print(result.keys())
        return render_template('typeinfo.html',data = result)
    return redirect(url_for('get_name'))


if __name__ == '__main__':
    app.run()
