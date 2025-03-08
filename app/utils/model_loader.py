from app.models.AI import decision_tree,LSTM,MLP,svm,xgboost_model
from app.utils.public_method import load_json


def find_model(model_address:str):

        json_card_model = load_json(model_address)
        if json_card_model is None:

            raise "There is no model card."

        type_model = json_card_model.get("architecture",None)
        main_address = json_card_model.get('address',None)
        number_of_label = json_card_model.get("number_of_labels",None)
        num_features = json_card_model.get("num_features",None)
        if type_model is None or main_address is None or number_of_label is None or num_features is None:

            raise "The information about this model is not complete!"
        
        elif type_model == "DecisionTree":
             
            model = decision_tree.DecisionTreeModel()
            model.load_model(main_address)
        
        elif type_model == "SVM":
            
            model = svm.SVMModel()
            model.load_model(main_address)
             
        
        elif type_model == "XGB":
            model =  xgboost_model.XGBoostModel()
            model.load_model(main_address)


        elif type_model == "LSTM":
            model = LSTM.LSTMModel(
                        model=LSTM.LSTM,       # Pass the LSTM class
                        input_size=num_features,    # Number of features per timestep
                        output_size=number_of_label,  # Number of output classes
                    )
            model.load_model(main_address)

            
        elif type_model == "MLP":
            model = MLP.MLPModel()
            model.load_model(main_address)
            
        else: 

            raise f"The architecture name {type_model} is unfifamiliar"
        

        return model,number_of_label


def get_prediction_range(num_classes: int, prediction: int) -> str:
    """
    دریافت تعداد کلاس‌ها و پیش‌بینی مدل و برگشت تناسب درصدی مطابق با قوانین مشخص‌شده.
    """
    # محاسبه فاصله‌ی بین هر کلاس
    range_percentage = 100 / (num_classes - 1)  # مثلا برای 5 کلاس، فاصله بین هر دو کلاس 25 درصد است.

    # محاسبه محدوده درصدی
    lower_bound = prediction * range_percentage
    upper_bound = (prediction + 1) * range_percentage
    
    # بازگشت نتیجه به صورت رشته
    return f"{lower_bound:.0f} تا {upper_bound:.0f}"