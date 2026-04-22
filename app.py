import streamlit as st
import pickle

st.set_page_config(
    page_title='Car Price Predictor',
    page_icon='🚗',
    layout='centered',
)

page_style = """
<style>
    .stApp {
        background: linear-gradient(135deg, #0b3d91 0%, #14477d 50%, #10293d 100%);
        color: #f4f7fb;
    }

    .stButton>button {
        background-color: #ff7f50;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.7rem 1.2rem;
        font-weight: 600;
    }

    .stButton>button:hover {
        background-color: #ff9b6a;
    }

    .stTextInput>div>div>input {
        background: rgba(255, 255, 255, 0.95);
        color: #0f1b2d;
        border: 1px solid #aac8ff;
        border-radius: 12px;
        padding: 0.8rem;
    }

    .stTextInput>div>label {
        color: #e2ecff;
        font-weight: 600;
    }

    .css-1d391kg {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
    }

    .stMarkdown h1,
    .stMarkdown h2,
    .stMarkdown h3,
    .stMarkdown p {
        color: #f4f7fb;
    }
</style>
"""

st.markdown(page_style, unsafe_allow_html=True)

st.markdown('<div style="padding: 2rem; border-radius: 20px; background: rgba(255,255,255,0.08); margin-bottom: 1.5rem;">'
            '<h1 style="margin: 0; color: #ffde7a;">🚘 Car Price Predictor</h1>'
            '<p style="margin: 0.5rem 0 0; color: #d7e8ff; font-size: 1rem;">Enter details below and get a quick estimate.</p>'
            '</div>', unsafe_allow_html=True)

try:
    final_model = pickle.load(open('final_model.pkl', 'rb'))
except FileNotFoundError:
    st.error('The model file final_model.pkl was not found. Please make sure it is in the app folder.')
    st.stop()

insurance_options = [
    'Select insurance validity',
    'Comprehensive',
    'Third Party insurance',
    'Zero Dep',
    'Not Available',
    'Third Party',
]
fuel_options = ['Select fuel type', 'Petrol', 'Diesel', 'CNG']
transmission_options = ['Select transmission type', 'Manual', 'Automatic']
ownership_options = ['Select ownership', 'First Owner', 'Second Owner', 'Third Owner', 'Fourth Owner', 'Fifth Owner']

cols = st.columns(2)
insurance_validity = cols[0].selectbox('Insurance validity:', insurance_options, index=0)
fuel_type = cols[1].selectbox('Fuel Type:', fuel_options, index=0)
kms_driven = cols[0].text_input('KMs Driven:', '')
ownership = cols[1].selectbox('Ownership:', ownership_options, index=0)
transmission = cols[0].selectbox('Transmission Type:', transmission_options, index=0)

if st.button('Predict'):
    if insurance_validity == 'Select insurance validity' or fuel_type == 'Select fuel type' or ownership == 'Select ownership' or transmission == 'Select transmission type':
        st.error('Please select valid options for all dropdown fields.')
    elif not kms_driven.strip():
        st.error('Please enter the number of KMs driven.')
    else:
        try:
            d1 = {
                'Comprehensive': 0,
                'Third Party insurance': 1,
                'Zero Dep': 2,
                'Not Available': 3,
                'Third Party': 1,
            }
            d2 = {'Petrol': 0, 'Diesel': 1, 'CNG': 2}
            d3 = {'Manual': 0, 'Automatic': 1}
            d4 = {
                'First Owner': 1,
                'Second Owner': 2,
                'Third Owner': 3,
                'Fourth Owner': 4,
                'Fifth Owner': 5,
            }

            insurance_validity = d1[insurance_validity]
            fuel_type = d2[fuel_type]
            transmission = d3[transmission]
            ownership = d4[ownership]
            kms_driven = int(kms_driven)

            test = [[insurance_validity, fuel_type, kms_driven, ownership, transmission]]
            yp = int(final_model.predict(test)[0])
            st.success(f'Predicted Car Price: ₹{yp:,}')
        except ValueError:
            st.error('KMs Driven must be a valid number.')
        except Exception as e:
            st.error(f'Prediction error: {e}')
   