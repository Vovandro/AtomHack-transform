from app import app, models
from flask import render_template
from flask import helpers, redirect, url_for
import catboost as cb


@app.route('/')
@app.route('/index')
def index():
    df = models.getTransformsList()
    df.sort_values('name_transfomr', inplace=True)
    return render_template("index.html", title='Home', df=df)


@app.route('/t/<int:id>')
def t(id):
    df = models.getTransforms(id)
    return render_template("detailed.html", df=df)


@app.route('/update')
def update():
    model_1 = cb.CatBoostClassifier().load_model("./app/model1")
    model_2 = cb.CatBoostRegressor().load_model("./app/model2")
    df = models.getTransformsList()
    for row in df.iterrows():
        data = models.getTestData(row[0])

        predict = model_1.predict(data)
        predict2 = model_2.predict(data).astype(int)

        models.updateTransform(row[0], predict[0], predict2)

    #helpers.flash('Updated', 'info')
    return redirect('/')
