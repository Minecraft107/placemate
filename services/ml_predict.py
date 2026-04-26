import pickle
import numpy as np

# Load once at module level — not inside the function (performance)
with open('ml/model_rf.pkl', 'rb') as f:
    rf_model = pickle.load(f)

with open('ml/model_lr.pkl', 'rb') as f:
    lr_model = pickle.load(f)

with open('ml/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

FEATURES = ['cgpa', 'backlogs', 'internship_done', 'projects_count', 
            'skills_count', 'ats_score', 'communication_score']

def predict_placement(data: dict, model_choice='rf'):
    features = np.array([[
        data.get('cgpa', 0),
        data.get('backlogs', 0),
        data.get('internship_done', 0),
        data.get('projects_count', 0),
        data.get('skills_count', 0),
        data.get('ats_score', 0),
        data.get('communication_score', 5)
    ]])
    
    features_scaled = scaler.transform(features)
    
    model = rf_model if model_choice == 'rf' else lr_model
    prediction = model.predict(features_scaled)[0]
    probability = model.predict_proba(features_scaled)[0]
    
    outcome = "Placed" if prediction == 1 else "Not Placed"
    confidence = round(float(max(probability)) * 100, 1)
    
    return {
        'outcome': outcome,
        'confidence': confidence,
        'placed_probability': round(float(probability[1]) * 100, 1),
        'model_used': 'Random Forest' if model_choice == 'rf' else 'Logistic Regression'
    }