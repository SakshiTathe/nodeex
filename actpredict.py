#diease,actpredict,actpredictem2, predict, predictem, emotionpred.py, diease

from predict import DisorderPredictor
predictor = DisorderPredictor(
    gru_model_path='models/gru_model.h5',
    tokenizer_path='models/tokenizer.pkl',
    label_encoder_path='models/label_encoder.pkl'
)
'''
sentence = "I feel anxious all the time."  # Example input

gru_prediction = predictor.predict(sentence, model_type='gru')
print(f"\n>>> GRU Prediction: ")
print(f"    Category: {gru_prediction.get('category', 'N/A')}, Confidence: {gru_prediction.get('confidence', 0):.4f}")
'''
