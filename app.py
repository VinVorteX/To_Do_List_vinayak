from crypt import methods
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __init__(self, title, desc):
        self.title = title
        self.desc = desc

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    

@app.route('/home', methods=['GET', 'POST'])
def hello():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    print(allTodo)
    return render_template('index.html', allTodo = allTodo)
   # return 'hello world!'

@app.route('/show')
def product():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'product page'

@app.route('/Delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/home')

@app.route('/Update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    
    if todo is None:
        return "Todo not found", 404
    
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo.title = title
        todo.desc = desc
        db.session.commit()
        return redirect('/home')

    return render_template('update.html', todo=todo)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True, port = 4000)