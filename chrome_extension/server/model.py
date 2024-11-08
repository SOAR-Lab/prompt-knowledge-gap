import joblib
import pandas as pd
import shap

def evaluate(input_data):
    # Load the saved pipeline (which includes both scaler and model)
    pipeline = joblib.load("best_model.pkl")
    
    # Ensure the input data is in the right format
    if isinstance(input_data, dict):
        input_data = pd.DataFrame([input_data])
    elif isinstance(input_data, pd.Series):
        input_data = input_data.to_frame().T
    
    # Transform the input data using the pipeline's scaler
    scaled_input = pipeline.named_steps['scaler'].transform(input_data)
    scaled_input_df = pd.DataFrame(scaled_input, columns=input_data.columns)

    # Make a prediction
    prediction = pipeline.predict(scaled_input_df)
    print("Prediction:", prediction)
    
    # Calculate SHAP values for the input to understand feature impact on this specific prediction
    log_reg_model = pipeline.named_steps['log_reg']
    explainer = shap.Explainer(log_reg_model, scaled_input_df)
    shap_values = explainer(scaled_input_df)

    return shap_values.base_values[0]