from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import Employee
from database import SessionLocal
from employee_crud import create_employee, get_employees, edit_employees, delete_employees

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session


@router.get("/employee/get-employees")
async def get_employees_endpoint(db: AsyncSession = Depends(get_db)):
    employees = await get_employees(db)
    return {"employees": employees}

@router.post("/employee/create-employee")
async def create_employee_endpoint(employee: Employee, db: AsyncSession = Depends(get_db)):
    db_employee = await create_employee(db, employee.employee_name, employee.department, employee.dob)
    return {"message": "Employee created successfully", "employee": db_employee}

@router.patch("/employee/edit-employee")
async def edit_employee_endpoint(employee: Employee, db: AsyncSession = Depends(get_db)):
    updated_employee = await edit_employees(db, employee.employee_id, employee.employee_name, employee.department, employee.dob)
    if updated_employee is None:
        return {"error": "Employee not found"}
    return {"message": "Employee updated successfully", "employee": updated_employee}

@router.delete("/employee/delete-employee")
async def delete_employee_endpoint(employee: Employee, db: AsyncSession = Depends(get_db)):
    deleted_employee = await delete_employees(db, employee.employee_id)
    if deleted_employee is None:
        return {"error": "Employee or Department data not found"}
    return {"message": "Employee deleted successfully"}
