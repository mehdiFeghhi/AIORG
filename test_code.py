# test_code.py
import pytest
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy import create_engine

# Model Definitions
Base = declarative_base()


class ClassA(Base):
    __tablename__ = "class_a"
    
    id = Column(Integer, primary_key=True)
    class_b_id = Column(Integer, ForeignKey("class_b.id"))
    class_b = relationship("ClassB", back_populates="class_as")

# ClassB.class_as = relationship("ClassA", order_by=ClassA.id, back_populates="class_b")
class ClassB(Base):
    __tablename__ = "class_b"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    class_as = relationship("ClassA", order_by=ClassA.id, back_populates="class_b")
        

# Test Setup
@pytest.fixture(scope="session")
def engine():
    # Use an in-memory SQLite database for testing
    return create_engine("sqlite:///:memory:")

@pytest.fixture(scope="function")
def tables(engine):
    # ایجاد جداول در دیتابیس
    Base.metadata.create_all(engine)
    yield
    # پاکسازی دیتابیس بعد از هر تست
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def session(engine, tables):
    connection = engine.connect()
    Session = sessionmaker(bind=connection)
    session = Session()
    yield session
    session.close()
    connection.close()

# Test Cases
def test_add_class_a_with_class_b(session):
    # اضافه کردن ClassB
    class_b_instance = ClassB(name="Test B")
    session.add(class_b_instance)
    session.commit()

    # اضافه کردن ClassA که به ClassB مرتبط است
    class_a_instance = ClassA(class_b=class_b_instance)
    session.add(class_a_instance)
    session.commit()

    # بررسی اینکه ارتباط بین ClassA و ClassB به درستی برقرار است
    assert class_a_instance.class_b.id == class_b_instance.id

def test_class_b_relationship_with_class_a(session):
    # اضافه کردن ClassB
    class_b_instance = ClassB(name="Test B")
    session.add(class_b_instance)
    session.commit()

    # اضافه کردن ClassA که به ClassB مرتبط است
    class_a_instance = ClassA(class_b=class_b_instance)
    session.add(class_a_instance)
    session.commit()

    # بازیابی ClassB از دیتابیس
    retrieved_class_b = session.query(ClassB).first()

    # چاپ طول و ID های ClassA های مرتبط
    print(f"Number of related ClassA instances: {len(retrieved_class_b.class_as)}")
    print(f"Related ClassA instance IDs: {[a.id for a in retrieved_class_b.class_as]}")

    # بازیابی دوباره ClassA از دیتابیس
    retrieved_class_a_instance = session.query(ClassA).get(class_a_instance.id)

    # بررسی اینکه ClassB دقیقا یک ClassA مرتبط دارد
    assert len(retrieved_class_b.class_as) == 1  # بررسی اینکه ClassB یک ClassA مرتبط دارد
    assert retrieved_class_b.class_as[0].id == retrieved_class_a_instance.id  # بررسی مطابقت ID

def test_no_class_b_association_for_class_a(session):
    # ایجاد ClassA بدون ارتباط به ClassB
    class_a_instance = ClassA()
    session.add(class_a_instance)
    session.commit()

    # بررسی اینکه ClassA به هیچ ClassB ای مرتبط نیست
    assert class_a_instance.class_b is None
