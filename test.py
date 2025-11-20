""" from analysis_service import AnalysisService
english_message="I feel incredibly happy today!"
analysis_service = AnalysisService()
emotion = analysis_service.detect_emotion(english_message)
print(emotion)  """
import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('diags/mental_health_rag_1000.csv')

df.drop('id', axis=1, inplace=True) 

df.to_csv('diags/initial-screening.csv', index=False) 
# 'index=False' prevents writing the DataFrame index as a column in the CSV



'''
from keras.models import load_model

# Load your old Keras model
model = load_model("models/model.keras")   # change filename if needed

# Save as .h5 (universal format)
model.save("models/emotion_model.h5")

print("🔥 Conversion complete! Saved as emotion_model.h5")
'''
