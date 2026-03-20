#imports
from flask import Flask, request, jsonify, render_template
import os
import json
from dataset import data_import, project_data
from Models import all_data_model, industry_model, revenue_model, length_model, contract_model

app = Flask(__name__)

# Load data once at startup
print("Loading data...")
data = data_import()
P3 = data[0]
zip_codes = data[1]
names = P3['Name'].to_list()
print("Data loaded!")

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "GET":
        return render_template('index.html', team_names=names)
    else:
        data = request.json
        row = project_data(data, P3, zip_codes)
        if type(row) == type('string'):
            response = {'error': row}
            return json.dumps(response)
        all_data = round(all_data_model(row),2)
        industry = round(industry_model(row),2)
        revenue = round(revenue_model(row),2)
        length = round(length_model(row),2)
        contract = round(contract_model(row),2)
        avg = round((all_data + industry + revenue + length + contract) / 5,2)
        if avg < .604177:
            result = 'in bottom 1/4 of teams'
        elif (avg >= .604177) and (avg < 1.205):
            result = 'in 2nd quartile of teams'
        elif (avg >= 1.205) and (avg < 2.39):
            result = 'in 3rd quartile of teams'
        else:
            result = 'in top 1/4 of teams'
        response = {'Overall': str(all_data),
                    'Industry': str(industry),
                    'Revenue': str(revenue),
                    'Length': str(length),
                    'Contract': str(contract),
                    'Average': str(avg),
                    'Result': result}
        return json.dumps(response)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
