# ❤️ Heart Disease Prediction System

A web-based **Heart Disease Risk Prediction System** powered by a **1D Convolutional Neural Network (CNN)** trained using **Federated Learning**.

The application allows users to enter patient health parameters and receive a predicted heart disease risk probability through a simple and user-friendly Streamlit interface.

Live URL : https://heart-diseases-prediction-hk8cofjxet3fzwkhp5yrnr.streamlit.app/

##  Features

1. Heart disease risk prediction
2. 1D CNN-based deep learning model
3. Secure user authentication
4. Password hashing using bcrypt
5. Prediction probability display
6. Prediction history for each user
7. Clear prediction history
8. Account dashboard
9. Clean and responsive Streamlit UI
10. SQLite database for user accounts and prediction history
11. Educational medical disclaimer


##  Technology Used

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Streamlit | Web application |
| TensorFlow / Keras | Deep learning model |
| 1D CNN | Heart disease prediction |
| Federated Learning | Privacy-aware model training |
| Pandas | Data processing |
| Scikit-learn | Data preprocessing |
| Joblib | Scaler storage |
| SQLite | User & prediction database |
| bcrypt | Password hashing |

---

##  System Architecture

```text
              Patient Information
                      │
                      ▼
             Streamlit Web App
                      │
                      ▼
             Data Preprocessing
                      │
                      ▼
                Feature Scaling
                      │
                      ▼
             1D CNN Deep Learning
                      │
                      ▼
             Risk Probability
                      │
              ┌───────┴───────┐
              ▼               ▼
         Lower Risk       Higher Risk

```
## Federated Learning

The prediction model is trained using a Federated Learning approach.

Instead of collecting all training data into a single central location, federated learning allows models to be trained across different data sources/clients and combines their learned parameters into a global model.

**Benefits**
Improved data privacy
Decentralized training
Reduced need to centralize sensitive medical data
Collaborative model training

The final global model is used by this application for heart disease risk prediction.

## Input Parameters

The system uses the following patient parameters:

Age
Resting Blood Pressure
Cholesterol
Maximum Heart Rate
ST Depression (Oldpeak)
Number of Major Vessels (CA)
Sex
Chest Pain Type
Fasting Blood Sugar
Resting ECG
Exercise-Induced Angina
ST Segment Slope
Thalassemia

Categorical parameters are converted into the same one-hot encoded format used during model training.


## Project Structure

    ```text
    heart_disease_website/
    │
    ├── model/
    │   ├── heart_disease_model.keras
    │   ├── scaler.pkl
    │   └── columns.json
    │
    ├── app.py
    ├── auth.py
    ├── users.db
    ├── requirements.txt
    ├── .gitignore
    └── README.md
    ```
    
## Important Files

1.app.py
Main Streamlit application containing the user interface and prediction workflow.

2.auth.py
Handles user registration, login, password hashing, and prediction history.

3.heart_disease_model.keras
Trained 1D CNN model used for prediction.

4.scaler.pkl
Saved feature scaler used to preprocess input data.

5.columns.json
Stores the feature order used during model training.

6.users.db
SQLite database containing application users and prediction history.

    
## Installation
1. Clone the repository
    git clone <YOUR_GITHUB_REPOSITORY_URL>
    cd heart_disease_website
2. Create a virtual environment
    python -m venv heartDiseases

    Activate it on Windows:

    heartDiseases\Scripts\activate
3. Install dependencies
    pip install -r requirements.txt
4. Run the application
    streamlit run app.py

The application will open in your browser.


##  Authentication

The application provides:

User registration
Secure password hashing using bcrypt
User login
Logout
User-specific prediction history

Passwords are never stored as plain text.

## Prediction Workflow
    
 1.User logs into the application.
 
 2.Patient health information is entered.
 
 3.Input features are converted into the required format.
 
 4.Features are scaled using the saved scaler.
 
 5.The processed data is passed to the trained 1D CNN model.
 
 6.The model generates a risk probability.
 
 7.The application displays:
 Lower Risk
 Higher Risk
 
 8.The prediction is stored in the user's prediction history.
 

## Future Improvements

1. Deploy with a production database such as PostgreSQL
2. Add model performance metrics
3. Add prediction visualizations
4. Improve federated client simulation
5. Add administrator dashboard
6. Add downloadable prediction reports
7. Deploy the application online
    
## Disclaimer

    This application is developed for educational and demonstration purposes only.

    The prediction generated by this system should not be considered a medical diagnosis or a substitute for professional medical advice.

    Always consult a qualified healthcare professional for medical decisions.


## Author

 Aashik Ali

 MCA | AI / GenAI Enthusiast

  Interested in:

 Artificial Intelligence
 Generative AI
 Machine Learning
 Deep Learning
 Full-Stack Development
