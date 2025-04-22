from flask import Flask, request, jsonify, render_template
from MLModels import ReadFile, TrainModel
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.is_json:
        data = request.get_json()
        input_data = data['input_data']
        typeOfModel = data['model']
        
        # Assuming input_data is a dictionary with the required columns
        df = ReadFile()
        columns = ['Age', 'Gender', 'Ethnicity', 'ParentalEducation', 'StudyTimeWeekly', 
                   'Absences', 'Tutoring', 'ParentalSupport', 'Extracurricular', 
                   'Sports', 'Music', 'Volunteering', 'GPA']
        


        # Convert input_data to a DataFrame 
        input_df = pd.DataFrame([input_data])
        
        input_df['Age'] = input_df['Age'].astype(int)
        input_df['StudyTimeWeekly'] = input_df['StudyTimeWeekly'].astype(float)
        input_df['Absences'] = input_df['Absences'].astype(int)
        input_df['GPA'] = input_df['GPA'].astype(float)
        categorical_columns = ['Gender', 'Ethnicity', 'ParentalEducation', 'Tutoring', 'ParentalSupport', 'Extracurricular', 'Sports', 'Music', 'Volunteering', 'GradeClass']
        for col in categorical_columns:
            df[col] = df[col].astype('category')

        # Train the model (or load a pre-trained model)
        MLModel = TrainModel(df, columns, typeOfModel)
        print(MLModel)
        # Make a prediction
        prediction = MLModel.predict(input_df)
        print(prediction)
        return jsonify({'prediction': prediction.tolist()})
    else:
        return jsonify({"error": "Unsupported Media Type"}), 415
    

if __name__ == '__main__':
    df = ReadFile()
    app.run(debug=True, use_reloader=False)
