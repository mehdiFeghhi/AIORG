import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import pytest
from sklearn.tree import DecisionTreeClassifier
from app.models.AI.decision_tree import DecisionTreeModel

def test_decision_tree_initialization():
    """بررسی مقداردهی اولیه مدل در کلاس DecisionTreeModel"""
    model = DecisionTreeModel(max_depth=5, criterion="gini")

    assert isinstance(model.model, DecisionTreeClassifier)  # مدل باید از نوع DecisionTreeClassifier باشد
    assert model.model.max_depth == 5  # مقدار max_depth باید ۵ باشد
    assert model.model.criterion == "gini"  # معیار باید gini باشد
    assert model.model.__class__.__name__ == "DecisionTree"  # نام کلاس سفارشی‌شده بررسی شود

def test_decision_tree_default_params():
    """بررسی مقداردهی اولیه مدل با پارامترهای پیش‌فرض"""
    model = DecisionTreeModel()

    assert model.param_grid is not None  # پارامترهای جستجو نباید خالی باشند
    assert "max_depth" in model.param_grid  # باید شامل max_depth باشد
    assert "criterion" in model.param_grid  # باید شامل criterion باشد

@pytest.mark.parametrize(
    "kwargs, expected_depth, expected_criterion",
    [
        ({"max_depth": 3, "criterion": "entropy"}, 3, "entropy"),
        ({"max_depth": None, "criterion": "gini"}, None, "gini"),
    ]
)
def test_decision_tree_with_params(kwargs, expected_depth, expected_criterion):
    """بررسی مقداردهی مدل با مجموعه‌ای از پارامترهای مختلف"""
    model = DecisionTreeModel(**kwargs)
    
    assert model.model.max_depth == expected_depth
    assert model.model.criterion == expected_criterion
