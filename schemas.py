from pydantic import BaseModel
from typing import Optional

# Request Model - Everything is made optional because of edit operation
class Department(BaseModel):
    data: Optional[str] = None
    department_id: Optional[int] = None
    
class Employee(BaseModel):
    employee_name: Optional[str] = None
    department: Optional[str] = None
    dob: Optional[str] = None
    employee_id: Optional[int] = None