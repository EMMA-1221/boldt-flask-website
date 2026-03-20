#imports
from flask import Flask, request, jsonify, render_template
import os
import codecs
import re
import json
from dataset import data_import, project_data
from Models import all_data_model, industry_model, revenue_model, length_model, contract_model
app = Flask(__name__)
P3 = 0
zip_codes = 0
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "GET":
        global P3
        global zip_codes
        data = data_import()
        P3 = data[0]
        zip_codes = data[1]
        names = P3['Name'].to_list()
        # delete：read app.js 's code（Railway 文件系统只读会报错）
        # delete：re.sub 修改 js code
        # delete：write app.js code
        return render_template('index.html', team_names=names)  # change：把 names 传给模板
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
