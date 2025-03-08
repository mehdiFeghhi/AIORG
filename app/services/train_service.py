import os
import json
import joblib
import numpy as np
from datetime import datetime
from fastapi import Depends
from sqlalchemy.orm import Session
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from scipy.stats import ttest_rel
from app.database import get_db
from .enhance_training_data_service import enhance_dataset
from app.models.AI.ModelDetails import ModelDetails  # Assuming ModelDetails is in app.models
from app.utils.train_helper_method import calculate_confidence_level, manage_model_directory



def tune_hyperparameters(model, X_train, Y_train, param_grid):
    """
    Tune hyperparameters using GridSearchCV.
    """
    if not param_grid:
        print("No hyperparameter grid provided. Skipping hyperparameter tuning.")
        return {}
    
    grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy')
    grid_search.fit(X_train, Y_train)
    return grid_search.best_params_


def train_and_evaluate(model_class, best_params, X_train, Y_train, X_test, Y_test):
    """
    Train the model with the best parameters and evaluate it.
    """
    model = model_class(**best_params) if best_params else model_class()
    model.fit(X_train, Y_train)
    Y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(Y_test, Y_pred)
    f1 = f1_score(Y_test, Y_pred, average='macro')
    precision = precision_score(Y_test, Y_pred, average='macro')
    recall = recall_score(Y_test, Y_pred, average='macro')
    
    return accuracy, f1, precision, recall


def train_model(
    model_class, X, Y, job_id, exam_id, base_directory_model,
    num_classes,name_object_predict,n_iterations=5,test_size=0.2, param_grid=None,
    db: Session = Depends(get_db), name_position=None
):
    """
    Train the model, evaluate it, and save details to the database.
    """
    np.random.seed(42)
    best_params_list = []
    accuracies, f1_scores, precisions, recalls = [], [], [], []
    
    for i in range(n_iterations):
        np.random.seed(42 + i)
        X_train, X_test, Y_train, Y_test,feature_engineering_details = enhance_dataset(X,Y,num_classes,test_size)
        
        best_params = tune_hyperparameters(model_class, X_train, Y_train, param_grid)
        best_params_list.append(best_params)
        
        accuracy, f1, precision, recall = train_and_evaluate(
            model_class, best_params, X_train, Y_train, X_test, Y_test
        )
        
        accuracies.append(accuracy)
        f1_scores.append(f1)
        precisions.append(precision)
        recalls.append(recall)
        
        print(f"Iteration {i+1}: Accuracy = {accuracy:.4f}, F1 = {f1:.4f}")
    
    t_stat_acc, p_value_acc = ttest_rel(accuracies, f1_scores)
    t_stat_f1, p_value_f1 = ttest_rel(f1_scores, precisions)
    
    avg_accuracy_per_param = []
    unique_params = list(set(tuple(p.items()) for p in best_params_list))
    for param in unique_params:
        param_dict = dict(param)
        indices = [i for i, p in enumerate(best_params_list) if p == param_dict]
        mean_acc = np.mean([accuracies[i] for i in indices])
        avg_accuracy_per_param.append((param_dict, mean_acc))
    
    best_final_params = max(avg_accuracy_per_param, key=lambda x: x[1])[0]
    final_model = model_class(**best_final_params)
    X_train, X_test, Y_train, Y_test,feature_engineering_details = enhance_dataset(X,Y,num_classes,test_size)
    final_model.fit(X_train, X_test)
    
    model_directory, model_filename, card_filename, feature_engg_filename, next_version = manage_model_directory(
        base_directory_model, name_position, model_class.__name__
    )
    
    save_place = os.path.join(model_directory, model_filename)
    joblib.dump(final_model, save_place)
    
    feature_engg_path = os.path.join(model_directory, feature_engg_filename)
    with open(feature_engg_path, 'w') as fe_file:
        json.dump(feature_engineering_details, fe_file, indent=4)
    
        
    # Calculate confidence levels
    confidence_level_accuracy = calculate_confidence_level(p_value_acc)
    confidence_level_f1_score = calculate_confidence_level(p_value_f1)
   
    card_info = {
        'name_object_predict': name_object_predict,
        'address': save_place,
        'feature_engineering_details_address': feature_engg_path,
        'architecture': model_class.__name__,
        'accuracy_results': {'mean': np.mean(accuracies), 'std': np.std(accuracies)},
        'f1_score_results': {'mean': np.mean(f1_scores), 'std': np.std(f1_scores)},
        'precision_results': {'mean': np.mean(precisions), 'std': np.std(precisions)},
        'recall_results': {'mean': np.mean(recalls), 'std': np.std(recalls)},
        't_test_results_accuracy': {'t_stat': t_stat_acc, 'p_value': p_value_acc},
        't_test_results_f1_score': {'t_stat': t_stat_f1, 'p_value': p_value_f1},
        'confidence_level_accuracy': confidence_level_accuracy,
        'confidence_level_f1_score': confidence_level_f1_score,
        'num_all_samples': len(X),
        'num_features': X.shape[1],
        'split_test': len(X_test),
        'n_splits_t_test': n_iterations,
        'number_of_labels': num_classes,
        'model_evaluation_date': datetime.now(),
        'version': f"v{next_version}",
        'exam_id': exam_id,
        'job_id': job_id
    }
    
    card_path = os.path.join(model_directory, card_filename)
    with open(card_path, 'w') as f:
        json.dump(card_info, f, indent=4)
    
    ModelDetails.add_record(db, card_info)
    print(f"Final model and metadata saved to {model_directory}")


