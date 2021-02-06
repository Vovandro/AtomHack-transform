from app import app, models
from flask import render_template
from flask import helpers, redirect, url_for
import catboost as cb
from matplotlib.figure import Figure
import base64
from io import BytesIO

@app.route('/')
@app.route('/index')
def index():
    df = models.getTransformsList()
    df.sort_values('name_transfomr', inplace=True)
    return render_template("index.html", df=df, counts=df.groupby('status')['name_transfomr'].count())


@app.route('/t/<int:id>')
def t(id):
    df = models.getTransforms(id)

    data = []
    for i, name in enumerate(['H2', 'CO', 'C2H4', 'C2H2']):
        fig = Figure()
        ax = fig.subplots()
        ax.plot(df[name], label=name)
        ax.set_xticks([])
        ax.legend()

        buf = BytesIO()
        fig.savefig(buf, format="png")
        data.append(base64.b64encode(buf.getbuffer()).decode("ascii"))

    return render_template("detailed.html", graph=data, last=df.iloc[-1])


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
