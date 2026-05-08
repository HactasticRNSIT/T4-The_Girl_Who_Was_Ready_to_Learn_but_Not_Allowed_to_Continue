from flask import Flask, request, render_template_string
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# Load dataset
data = pd.read_csv("students.csv")

# Features and target
X = data[['attendance', 'marks', 'income', 'distance']]
y = data['risk']

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# HTML PAGE
html = """
<!DOCTYPE html>
<html>

<head>

<title>Female Education Risk Predictor</title>

<style>

body{
    font-family: Arial;
    background:#f2f2f2;
    text-align:center;
    padding-top:50px;
}

.box{
    background:white;
    width:400px;
    margin:auto;
    padding:30px;
    border-radius:10px;
}

input{
    width:90%;
    padding:10px;
    margin:10px;
}

button{
    padding:10px 20px;
    background:blue;
    color:white;
    border:none;
    border-radius:5px;
}

</style>

</head>

<body>

<div class="box">

<h1>Female Education Risk Predictor</h1>

<form method="POST">

<input type="number" name="attendance" placeholder="Attendance %" required>

<input type="number" name="marks" placeholder="Marks" required>

<input type="number" name="income" placeholder="Family Income" required>

<input type="number" name="distance" placeholder="Distance to School" required>

<button type="submit">Predict</button>

</form>

<h2>{{result}}</h2>

</div>

</body>

</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        attendance = int(request.form["attendance"])
        marks = int(request.form["marks"])
        income = int(request.form["income"])
        distance = int(request.form["distance"])

        prediction = model.predict([[attendance, marks, income, distance]])

        if prediction[0] == 1:
            result = "High Risk of Dropping Out"
        else:
            result = "Low Risk"

    return render_template_string(html, result=result)

if __name__ == "__main__":
    app.run(debug=True)