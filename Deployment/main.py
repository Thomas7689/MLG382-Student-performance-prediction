from flask import Flask, request, jsonify, render_template
from Deployment.MLModels import ReadFile, TrainModel
import pandas as pd
import joblib
import os

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
        
        # Load the trained model and selected columns
        model_filename = f"{typeOfModel}_model.pkl"
        columns_filename = f"{typeOfModel}_columns.pkl"
        MLModel = joblib.load(model_filename)
        selected_columns = joblib.load(columns_filename)
        
        # Convert input_data to a DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Ensure the input_df only contains the selected columns
        input_df = input_df[selected_columns]
        
        # Convert columns to appropriate data types
        for col in input_df.columns:
            if col in ['Age', 'StudyTimeWeekly', 'Absences', 'GPA']:
                input_df[col] = pd.to_numeric(input_df[col], errors='coerce')
            elif col in ['Gender', 'Ethnicity', 'ParentalEducation', 'Tutoring', 
                         'ParentalSupport', 'Extracurricular', 'Sports', 'Music', 
                         'Volunteering']:
                input_df[col] = input_df[col].astype('category').cat.codes
        
        # Fill any NaN values that may have resulted from conversion
        input_df = input_df.fillna(0)
        
        # Make a prediction
        prediction = MLModel.predict(input_df)
        
        return jsonify({'prediction': prediction.tolist(), 'selected_columns': selected_columns})
    else:
        return jsonify({"error": "Unsupported Media Type"}), 415

@app.route('/train', methods=['POST'])
def train():
    if request.is_json:
        data = request.get_json()
        typeOfModel = data['model']
        selected_columns = data['columns']
        print(selected_columns)
        # Read the data
        df = ReadFile()
        
        # Convert categorical columns to category type
        categorical_columns = ['Gender', 'Ethnicity', 'ParentalEducation', 'Tutoring', 
                               'ParentalSupport', 'Extracurricular', 'Sports', 'Music', 
                               'Volunteering']
        for col in categorical_columns:
            df[col] = df[col].astype('category')
        
        # Train the model
        MLModel = TrainModel(df, selected_columns, typeOfModel)
        
        # Save the trained model and selected columns to files
        model_filename = f"{typeOfModel}_model.pkl"
        columns_filename = f"{typeOfModel}_columns.pkl"
        joblib.dump(MLModel, model_filename)
        joblib.dump(selected_columns, columns_filename)
        
        return jsonify({'message': 'Model trained successfully!'})
    else:
        return jsonify({"error": "Unsupported Media Type"}), 415
@app.route('/list_models', methods=['GET'])
def list_models():
    model_files = [f.split('_model.pkl')[0] for f in os.listdir() if f.endswith('_model.pkl')]
    models_info = {}
    for model in model_files:
        columns_filename = f"{model}_columns.pkl"
        if os.path.exists(columns_filename):
            selected_columns = joblib.load(columns_filename)
            models_info[model] = selected_columns
    return jsonify({'models': models_info if models_info else {'None': []}})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
