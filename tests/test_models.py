# test_models.py
import pytest
from app.models.class_a import ClassA  # Import ClassA
from app.models.class_b import ClassB  # Import ClassB

# Test case: Add ClassA with associated ClassB
def test_add_class_a_with_class_b(db_session):
    # Create an instance of ClassB
    class_b = ClassB(description="Test Description")
    db_session.add(class_b)
    db_session.commit()
    
    # Create an instance of ClassA and associate it with ClassB through the relationship
    class_a = ClassA(name="Test Name", model_details=[class_b])  # Use model_details to associate
    db_session.add(class_a)
    db_session.commit()
    
    # Query ClassA and check if the relationship works
    retrieved_class_a = db_session.query(ClassA).filter_by(name="Test Name").first()
    assert retrieved_class_a is not None
    assert retrieved_class_a.name == "Test Name"
    assert retrieved_class_a.model_details[0].description == "Test Description"  # Access through model_details


# Test case: Ensure ClassB relationship with ClassA is correctly established
def test_class_b_relationship_with_class_a(db_session):
    # Create instances of ClassB and ClassA
    class_b = ClassB(description="Another Test Description")
    db_session.add(class_b)
    db_session.commit()

    class_a = ClassA(name="Another Test Name", model_details=[class_b])  # Use model_details to associate
    db_session.add(class_a)
    db_session.commit()
    
    # Query ClassB and check the relationship
    retrieved_class_b = db_session.query(ClassB).filter_by(description="Another Test Description").first()
    assert retrieved_class_b is not None
    assert retrieved_class_b.description == "Another Test Description"
    assert retrieved_class_b.class_a.name == "Another Test Name"  # Access ClassA through class_a


# Test case: Ensure ClassA can exist without being associated with ClassB
def test_no_class_b_association_for_class_a(db_session):
    # Create an instance of ClassA without ClassB
    class_a = ClassA(name="No ClassB Association")
    db_session.add(class_a)
    db_session.commit()
    
    # Query ClassA and ensure model_details is an empty list or None
    retrieved_class_a = db_session.query(ClassA).filter_by(name="No ClassB Association").first()
    assert retrieved_class_a is not None
    print("Hi")
    print(retrieved_class_a.model_details)

    # Convert the model_details query to a list and check if it's empty
    model_details_list = list(retrieved_class_a.model_details)
    assert len(model_details_list) == 0  # Ensures model_details is an empty list