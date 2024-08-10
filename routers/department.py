from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import Department
from database import SessionLocal
from department_crud import create_department, get_departments, edit_departments, delete_departments

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session


@router.get("/department/get-departments")
async def get_departments_endpoint(db: AsyncSession = Depends(get_db)):
    departments = await get_departments(db)
    return {"departments": departments}


@router.post("/department/create-department")
async def create_department_endpoint(department: Department, db: AsyncSession = Depends(get_db)):
    db_department = await create_department(db, department.data)
    return {"message": "Department created successfully", "department": db_department}

@router.patch("/department/edit-department")
async def edit_department_endpoint(department: Department, db: AsyncSession = Depends(get_db)):
    updated_department = await edit_departments(db, department.department_id, department.data)
    if updated_department is None:
        return {"error": "Department not found"}
    return {"message": "Department updated successfully", "department": updated_department}

@router.delete("/department/delete-department")
async def delete_department_endpoint(department: Department, db: AsyncSession = Depends(get_db)):
    deleted_department = await delete_departments(db, department.department_id)
    if deleted_department is None:
        return {"error": "Department not found"}
    return {"message": "Department deleted successfully"}
