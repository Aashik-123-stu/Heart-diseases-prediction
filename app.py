import streamlit as st
import tensorflow as tf
import joblib
import json
import numpy as np
import pandas as pd
import sqlite3
import bcrypt
from auth import init_db, create_user, login_user, save_prediction, get_prediction_history,delete_prediction_history

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Heart Disease Prediction",
    page_icon="❤️",
    layout="centered"
)

# -----------------------------
# Authentication
# -----------------------------

init_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "auth_page" not in st.session_state:
    st.session_state.auth_page = "login"

if "page" not in st.session_state:
    st.session_state.page = "prediction"

if not st.session_state.logged_in:

    # Center the authentication form
    left, center, right = st.columns([1, 2, 1])

    with center:

        st.markdown(
            '<div style="text-align:center; margin-top:35px; margin-bottom:25px;">'
            '<div style="font-size:48px; margin-bottom:8px;">🏥</div>'
            '<div style="font-size:30px; font-weight:600; color:#2f3140;">Hospital Portal</div>'
            '<div style="font-size:14px; color:#777; margin-top:6px;">Heart Disease Prediction System</div>'
            '</div>',
            unsafe_allow_html=True
        )

        # =========================
        # LOGIN
        # =========================

        if st.session_state.auth_page == "login":

            st.markdown(
                '<div class="auth-heading">🔐 Secure Login</div>',
                unsafe_allow_html=True
            )

            username = st.text_input(
                "Username",
                placeholder="Enter your username"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
            )

            if st.button("Login", use_container_width=True,type="primary"):

                if not username or not password:

                    st.warning(
                        "Please enter username and password."
                    )

                elif login_user(username, password):

                    st.session_state.logged_in = True
                    st.session_state.username = username

                    st.rerun()

                else:

                    st.error(
                        "Invalid username or password."
                    )

            st.markdown(
                "<div style='text-align:center; margin-top:15px; color:#666;'>"
                "Don't have an account?"
                "</div>",
                unsafe_allow_html=True
            )

            if st.button(
                "Create an account",
                use_container_width=True
            ):

                st.session_state.auth_page = "signup"
                st.rerun()


        # =========================
        # SIGNUP
        # =========================

        else:

            st.markdown(
                '<div class="auth-heading">📝 Create Account</div>',
                unsafe_allow_html=True
            )

            username = st.text_input(
                "Username",
                placeholder="Choose a username"
            )

            email = st.text_input(
                "Email",
                placeholder="Enter your email"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Create a password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Confirm your password"
            )

            if st.button(
                "Create Account",
                use_container_width=True,
                 type="primary"
            ):

                if not username or not email or not password:

                    st.warning(
                        "Please fill all fields."
                    )

                username = username.strip()
                email = email.strip().lower()

                if len(username) < 3:
                    st.warning("Username must be at least 3 characters.")
                elif "@" not in email or "." not in email:
                    st.warning("Please enter a valid email address.")

                elif password != confirm_password:

                    st.error(
                        "Passwords do not match."
                    )

                elif len(password) < 8:

                    st.warning(
                        "Password must be at least 8 characters."
                    )

                elif not any(char.isdigit() for char in password):

                    st.warning(
                        "Password must contain at least one number."
                    )

                elif not any(char.isupper() for char in password):

                    st.warning(
                        "Password must contain at least one uppercase letter."
                    )

                else:

                    success, message = create_user(
                        username,
                        email,
                        password
                    )

                    if success:

                        st.success(message)

                        st.session_state.auth_page = "login"

                        st.info(
                            "You can now login with your account."
                        )

                    else:

                        st.error(message)

            st.markdown(
                "<div style='text-align:center; margin-top:15px; color:#666;'>"
                "Already have an account?"
                "</div>",
                unsafe_allow_html=True
            )

            if st.button(
                "Back to Login",
                use_container_width=True
            ):

                st.session_state.auth_page = "login"
                st.rerun()

    # Don't show prediction page before login
    st.stop()



# -----------------------------
# Load Model & Preprocessing
# -----------------------------
model = tf.keras.models.load_model("model/heart_disease_model.keras")
scaler = joblib.load("model/scaler.pkl")

with open("model/columns.json", "r") as f:
    columns = json.load(f)

# Remove target column
input_columns = [col for col in columns if col != "num"]


# -----------------------------
# Custom CSS - White Background
# -----------------------------
st.markdown("""
<style>

.main {
    background-color: white;
}

.block-container {
    max-width: 1000px;
    padding-top: 2rem;
}

h1 {
    color: #2f3140;
    text-align: center;
    font-size: 42px;
}

h2 {
    color: #2f3140;
}

label {
    color: #333333 !important;
}

.stButton > button {
    width: 100%;
    background-color: #ff4b4b;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 14px;
    font-size: 15px;
    font-weight: 500;
}

.stButton > button:hover {
    background-color: #e83e3e;
    color: white;
    border: none;
}

.result-box {
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    margin-top: 20px;
}

/* Authentication Card */

.auth-card {
    max-width: 450px;
    margin: 40px auto;
    padding: 35px;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    background: white;
    box-shadow: 0 4px 18px rgba(0,0,0,0.06);
}

.auth-title {
    text-align: center;
    color: #2f3140;
    font-size: 30px;
    font-weight: 600;
    margin-bottom: 5px;
}

.auth-subtitle {
    text-align: center;
    color: #777;
    font-size: 14px;
    margin-bottom: 25px;
}

/* login button */
.auth-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 28px;
    margin-top: 20px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.05);
}

.auth-heading {
    font-size: 24px;
    font-weight: 600;
    color: #333;
    margin-bottom: 18px;
}

.auth-footer {
    text-align: center;
    color: #777;
    font-size: 14px;
    margin-top: 18px;
}

</style>
""", unsafe_allow_html=True)

# -------side bar code --------------

with st.sidebar:
    st.markdown("### 🏥 Heart Health")
    st.write(f"👤 {st.session_state.get('username', 'User')}")
    st.divider()

    if st.button("🏠 Prediction", use_container_width=True):
        st.session_state.page = "prediction"
        st.rerun()

    if st.button("👤 Account", use_container_width=True):
        st.session_state.page = "account"
        st.rerun()

    st.divider()

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.auth_page = "login"
        st.session_state.pop("username", None)
        st.session_state.pop("page", None)
        st.rerun()

# Page routing

if st.session_state.page == "account":

    st.markdown(
        '<div style="text-align:center; padding:20px 0;">'
        '<div style="font-size:38px;">👤</div>'
        '<div style="font-size:28px; font-weight:600;">My Account</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div style="padding:20px; border:1px solid #e5e5e5; '
        'border-radius:10px; margin-top:10px;">'
        '<div style="font-size:16px; font-weight:600;">Account Information</div>'
        f'<div style="margin-top:12px; color:#666;">'
        f'Username: <b>{st.session_state.get("username", "User")}</b>'
        '</div>'
        '<div style="margin-top:8px; color:#666;">'
        'Status: <b>Active</b>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

#   ------ predication table show---------------
    st.markdown("### 📊 Prediction History")

    history = get_prediction_history(
        st.session_state.get("username", "User")
    )

    if history:
        total_predictions = len(history)
        higher_risk = sum(1 for row in history if row[0] == "Higher Risk")
        lower_risk = sum(1 for row in history if row[0] == "Lower Risk")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Predictions", total_predictions)

        with col2:
            st.metric("Higher Risk", higher_risk)

        with col3:
            st.metric("Lower Risk", lower_risk)


    if history:
        history_data = []

        for result, probability, created_at in history:
            history_data.append({
                "Date": created_at,
                "Result": result,
                "Probability of Risk": f"{probability * 100:.2f}%"
            })

        history_df = pd.DataFrame(history_data)
# --------history visualization-----
        def highlight_result(row):
            if row["Result"] == "Higher Risk":
                return ["background-color: #fff0f0"] * len(row)
            else:
                return ["background-color: #f0fff4"] * len(row)


        styled_history = history_df.style.apply(
            highlight_result,
            axis=1
        )

        st.dataframe(
            styled_history,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No prediction history available yet.")

    # --- to delete history
    if history:
        if st.button("🗑️ Clear Prediction History"):
            delete_prediction_history(
                st.session_state.get("username", "User")
            )
            st.success("Prediction history cleared.")
            st.rerun()

# ------------model information display------------------
    st.markdown("### 🧠 Model Information")

    st.markdown(
        '<div style="padding:16px; border:1px solid #e5e5e5; '
        'border-radius:10px; color:#666;">'
        '<b>Model:</b> 1D Convolutional Neural Network (CNN)<br>'
        '<b>Training:</b> Federated Learning<br>'
        '<b>Purpose:</b> Heart Disease Risk Prediction'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("### 📖 About the Project")

    st.markdown(
        '<div style="padding:18px; border:1px solid #e5e5e5; '
        'border-radius:10px; color:#666; line-height:1.7;">'
        '<b>Heart Disease Prediction System</b> uses a '
        '<b>1D Convolutional Neural Network (CNN)</b> trained using '
        '<b>Federated Learning</b> to predict heart disease risk '
        'from patient health parameters.<br><br>'
        'The system provides a predicted risk probability based on '
        'the information entered by the user.'
        '</div>',
        unsafe_allow_html=True
    )
    st.stop()

# -----------------------------
# Heading
# -----------------------------
st.markdown(
    '<div style="text-align:center; padding:15px 0 25px 0;">'
    '<div style="font-size:42px;">❤️</div>'
    '<div style="font-size:32px; font-weight:600; color:#2f3140;">'
    'Heart Disease Risk Assessment'
    '</div>'
    '<div style="font-size:14px; color:#777; margin-top:8px;">'
    'Federated Learning based Heart Disease Risk Prediction'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# -----------------------------
# Patient Information
# -----------------------------
st.markdown(
    '<div style="font-size:24px; font-weight:600; '
    'color:#2f3140; margin:10px 0 4px 0;">'
    'Patient Information'
    '</div>'
    '<div style="font-size:13px; color:#777; '
    'line-height:1.6; margin-bottom:18px;">'
    'Please enter the patient’s health and medical test details below. '
    'These parameters will be analyzed by the trained Federated Learning model '
    'to estimate the predicted risk of heart disease.'
    '</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=40,
        help="Patient's age in years."
    )

    trestbps = st.number_input(
        "Resting Blood Pressure",
        min_value=50,
        max_value=250,
        value=120,
        help="Resting blood pressure in mm Hg."
    )

    chol = st.number_input(
        "Cholesterol",
        min_value=50,
        max_value=600,
        value=200,
        help="Serum cholesterol level in mg/dl."
    )

    thalch = st.number_input(
        "Maximum Heart Rate",
        min_value=50,
        max_value=250,
        value=150,
        help="Maximum heart rate achieved during the test."
    )

    oldpeak = st.number_input(
        "ST Depression (Oldpeak)",
        min_value=0.0,
        max_value=10.0,
        value=1.0,
        step=0.1,
        help="ST depression induced by exercise relative to rest."
    )

    ca = st.number_input(
        "Number of Major Vessels (CA)",
        min_value=0,
        max_value=4,
        value=0,
        help="Number of major vessels colored by fluoroscopy (0–4)."
    )

with col2:
    sex = st.selectbox(
        "Sex",
        ["Female", "Male"],
        help="Patient's biological sex."
    )

    cp = st.selectbox(
        "Chest Pain Type",
        [
            "No / Asymptomatic",
            "Atypical Angina",
            "Non-anginal",
            "Typical Angina"
        ],
        help="Type of chest pain experienced by the patient."
    )

    fbs = st.selectbox(
        "Fasting Blood Sugar",
        ["False", "True", "Unknown"],
        help="Whether fasting blood sugar is greater than 120 mg/dl."
    )

    restecg = st.selectbox(
        "Resting ECG",
        [
            "Normal",
            "ST-T Abnormality",
            "LV Hypertrophy"
        ],
        help="Result of the resting electrocardiogram."
    )

    exang = st.selectbox(
        "Exercise Induced Angina",
        ["False", "True", "Unknown"],
        help="Whether exercise causes angina (chest pain)."
    )

    slope = st.selectbox(
        "ST Segment Slope",
        [
            "Downsloping",
            "Flat",
            "Upsloping"
        ],
        help="Slope of the peak exercise ST segment."
    )

    thal = st.selectbox(
        "Thalassemia",
        [
            "Normal",
            "Fixed Defect",
            "Reversable Defect"
        ],
        help="Thalassemia-related result from the heart test."
    )


# -----------------------------
# Convert Inputs to Model Format
# -----------------------------
if st.button("🔍 Predict Heart Disease Risk",use_container_width=True,type="primary"):

    # Start with all features as 0
    input_data = {column: 0 for column in input_columns}

    # Numerical features
    input_data["age"] = age
    input_data["trestbps"] = trestbps
    input_data["chol"] = chol
    input_data["thalch"] = thalch
    input_data["oldpeak"] = oldpeak
    input_data["ca"] = ca


    # One-hot encoded features
    if sex == "Male":
        input_data["sex_Male"] = 1

    if cp == "Atypical Angina":
        input_data["cp_atypical angina"] = 1
    elif cp == "Non-anginal":
        input_data["cp_non-anginal"] = 1
    elif cp == "Typical Angina":
        input_data["cp_typical angina"] = 1

    if fbs == "True":
        input_data["fbs_True"] = 1
    elif fbs == "Unknown":
        input_data["fbs_Unknown"] = 1

    if restecg == "LV Hypertrophy":
        input_data["restecg_lv hypertrophy"] = 1
    elif restecg == "ST-T Abnormality":
        input_data["restecg_st-t abnormality"] = 1
    elif restecg == "Normal":
        input_data["restecg_normal"] = 1

    if exang == "True":
        input_data["exang_True"] = 1
    elif exang == "Unknown":
        input_data["exang_Unknown"] = 1

    if slope == "Downsloping":
        input_data["slope_downsloping"] = 1
    elif slope == "Flat":
        input_data["slope_flat"] = 1
    elif slope == "Upsloping":
        input_data["slope_upsloping"] = 1

    if thal == "Fixed Defect":
        input_data["thal_fixed defect"] = 1
    elif thal == "Normal":
        input_data["thal_normal"] = 1
    elif thal == "Reversable Defect":
        input_data["thal_reversable defect"] = 1

    # Create DataFrame in EXACT training order
    input_df = pd.DataFrame([input_data], columns=input_columns)

    # Scale
    scaled_data = scaler.transform(input_df)

    # CNN input shape: (1, 23, 1)
    scaled_data = scaled_data.reshape(1, 23, 1)


    # Prediction
    with st.status("🔄 Analyzing patient information...", expanded=False) as status:
        prediction = model.predict(scaled_data, verbose=0)
        status.update(
            label="✅ Analysis completed",
            state="complete"
        )

    probability = float(prediction[0][0])

    if probability >= 0.5:
        result = "Higher Risk"
    else:
        result = "Lower Risk"

    save_prediction(
        st.session_state.get("username", "User"),
        result,
        probability
    )

    # -----------------------------
    # Display Result
    # -----------------------------
    if probability >= 0.5:
        st.markdown(
            '<div style="padding:18px; border-radius:10px; background:#fff5f5; '
            'border:1px solid #ffd6d6; text-align:center; margin-top:20px;">'
            '<div style="font-size:22px; font-weight:600;">⚠️ Higher Risk of Heart Disease</div>'
            '<div style="font-size:14px; color:#777; margin-top:8px;">'
            'The model indicates a higher predicted risk.'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            '<div style="padding:18px; border-radius:10px; background:#f5fff8; '
            'border:1px solid #d6f5df; text-align:center; margin-top:20px;">'
            '<div style="font-size:22px; font-weight:600;">✅ Lower Risk of Heart Disease</div>'
            '<div style="font-size:14px; color:#777; margin-top:8px;">'
            'The model indicates a lower predicted risk.'
            '</div>'
            '</div>',
            unsafe_allow_html=True
    )

    if st.button("🔄 New Prediction", use_container_width=False):
        st.rerun()

# ----how it  works------
with st.expander("🧠 How does this system work?"):

    st.markdown(
        """
        **1. Enter Patient Details**  
        Provide the patient's health and medical test information.

        **2. Data Preprocessing**  
        The entered information is converted into the format
        expected by the trained model.

        **3. Federated Learning Model**  
        A 1D CNN model trained using Federated Learning analyzes
        the patient data.

        **4. Risk Prediction**  
        The system generates a predicted probability and classifies
        the result as **Higher Risk** or **Lower Risk**.
        """
    )

st.markdown(
    '<div style="text-align:center; color:#777; font-size:12px; margin-top:20px;">'
    '⚕️ This prediction is for educational purposes only and should not be used as a medical diagnosis.'
    '</div>',
    unsafe_allow_html=True
)