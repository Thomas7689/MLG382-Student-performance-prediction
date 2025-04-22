from flask import Flask, request, jsonify, render_template
from MLModels import ReadFile, TrainModel
import pandas as pd
import joblib
import os
import itertools

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
        selected_columns = data['columns']
        
        # Generate the filename based on the selected model and columns
        filename = os.path.join('models', f"model_{typeOfModel}_{'_'.join(selected_columns)}.joblib")
        
        # Load the trained model
        if os.path.exists(filename):
            MLModel = joblib.load(filename)
        else:
            return jsonify({"error": "Model not found"}), 404
        
        # Convert input_data to a DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Ensure the input_df only contains the selected columns
        input_df = input_df[selected_columns]
        
        # Convert columns to appropriate data types
        for col in input_df.columns:
            if col in ['StudyTimeWeekly', 'Absences', 'GPA']:
                input_df[col] = pd.to_numeric(input_df[col], errors='coerce')
            elif col in ['ParentalEducation', 'Tutoring', 'ParentalSupport']:
                input_df[col] = input_df[col].astype('category').cat.codes
        
        # Fill any NaN values that may have resulted from conversion
        input_df = input_df.fillna(0)
        
        # Make a prediction
        prediction = MLModel.predict(input_df)
        
        return jsonify({'prediction': prediction.tolist(), 'selected_columns': selected_columns})
    else:
        return jsonify({"error": "Unsupported Media Type"}), 415

@app.route('/list_models', methods=['GET'])
def list_models():
    model_files = [f for f in os.listdir('models') if f.endswith('.joblib')]
    models_info = {}
    for model_file in model_files:
        parts = model_file.split('_')
        model_type = parts[1]
        columns = parts[2:]
        columns = '_'.join(columns).replace('.joblib', '').split('_')
        model_name = f"{model_type}_{'_'.join(columns)}"
        models_info[model_name] = columns
    return jsonify({'models': models_info if models_info else {'None': []}})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
