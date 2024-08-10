from sqlalchemy import Column, Integer, String, Date, ForeignKey, ARRAY, Text
from database import Base
from sqlalchemy.orm import relationship

class DepartmentModel(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    numberofemployees = Column(Integer, index=True, default=0)
    employees = relationship("EmployeeModel", back_populates="department_rel")

class EmployeeModel(Base):
    __tablename__ = "Employee"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(Text, index=True)
    dob = Column(Date, index=True)
    department = Column(Integer, ForeignKey('department.id'), index=True)
    
    department_rel = relationship("DepartmentModel", back_populates="employees")

