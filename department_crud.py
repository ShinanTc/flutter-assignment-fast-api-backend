from sqlalchemy.ext.asyncio import AsyncSession
from models import DepartmentModel
from sqlalchemy.future import select

async def create_department(db: AsyncSession, department_data: str):
    db_department = DepartmentModel(name=department_data)
    db.add(db_department)
    await db.commit()
    await db.refresh(db_department)
    return db_department

async def get_departments(db: AsyncSession):
    result = await db.execute(select(DepartmentModel))
    return result.scalars().all()

async def edit_departments(db: AsyncSession, department_id: int, department_data: str):

    try:
        result = await db.execute(
            select(DepartmentModel).where(DepartmentModel.id == department_id)
        )
        department = result.scalars().one()
        department.name = department_data

        await db.commit()
        await db.refresh(department)

        return department
    
    # If no department is found, you might want to handle it (e.g., raise an HTTPException)
    except NoResultFound:
        return None
    
    
async def delete_departments(db: AsyncSession, department_id: int):

    try:
        result = await db.execute(
            select(DepartmentModel).where(DepartmentModel.id == department_id)
        )

        department = result.scalars().one()

        await db.delete(department)
        await db.commit()
        
    except NoResultFound:
        return None