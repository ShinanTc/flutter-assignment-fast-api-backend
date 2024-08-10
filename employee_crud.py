from sqlalchemy.ext.asyncio import AsyncSession
from models import EmployeeModel, DepartmentModel
from sqlalchemy.future import select
from datetime import datetime
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.exc import NoResultFound

async def update_number_of_employees(db: AsyncSession, department_name: str, modification_type: str):
    try:
        # Fetch the department record
        result = await db.execute(
            select(DepartmentModel).where(DepartmentModel.name == department_name)
        )
        department = result.scalars().first()

        if department is None:
            raise ValueError(f"Department '{department_name}' not found")

        # Increment the number of employees if it is an employee creation
        if modification_type is 'increment':
            department.numberofemployees += 1
        else:
            department.numberofemployees -= 1

        # Commit the update
        await db.commit()

        return {"message": "Number of employees updated successfully"}

    except Exception as e:
        print(f"Error updating number of employees: {e}")

async def create_employee(db: AsyncSession, employee_name: str, department: str, dob: str):

    # Convert the dob string to a datetime object
    dob_datetime = datetime.strptime(dob, '%Y-%m-%d')

    try:

        # Fetch the department id based on department_name
        result = await db.execute(
            select(DepartmentModel.id).where(DepartmentModel.name == department)
        )
        department_id = result.scalar_one()  # Get the single result, which should be the id

        # getting that date value which is the appropriate 
        dob_datetime = dob_datetime.date()

    except NoResultFound:
        raise ValueError(f"Department not found")

    db_employee = EmployeeModel(name=employee_name, department=department_id, dob=dob_datetime)
    db.add(db_employee)
    await db.commit()
    await db.refresh(db_employee)

    # Increment the number of employees in the department
    await update_number_of_employees(db, department, 'increment')
    
    return db_employee

async def get_employees(db: AsyncSession):
    query = select(EmployeeModel).options(joinedload(EmployeeModel.department_rel))
    result = await db.execute(query)

    return result.scalars().all()

async def edit_employees(db: AsyncSession, employee_id: int, employee_name: str, department_name: str, dob: str):

    # Convert the dob string to a datetime object
    dob_datetime = datetime.strptime(dob, '%Y-%m-%d')

    dob_datetime = dob_datetime.date()
    
    try:
        # Fetch the department id based on department_name
        department = await db.execute(
            select(DepartmentModel.id).where(DepartmentModel.name == department_name)
        )

        department_id = department.scalar_one()

    # If no department is found, you might want to handle it
    except NoDepartmentFound:
        return None
        
    try:
        
        result = await db.execute(
            select(EmployeeModel)
            .options(selectinload(EmployeeModel.department_rel))
            .where(EmployeeModel.id == employee_id)
        )
        employee = result.scalars().one()

        current_department = employee.department_rel.name

        employee.name = employee_name
        employee.dob = dob_datetime
        employee.department = department_id

        await db.commit()
        await db.refresh(employee)

        # checking if the user tried to change the department of this employee
        if current_department != department:
            await update_number_of_employees(db, department_name, 'increment')
            await update_number_of_employees(db, current_department, 'decrement')

        return employee
    
    # If no employee is found, you might want to handle it
    except NoEmployeeFound:
        return None
    
async def delete_employees(db: AsyncSession, employee_id: int):
    
    try:
        # Load the related department
        query = (
        select(EmployeeModel)
        .options(selectinload(EmployeeModel.department_rel))
        .where(EmployeeModel.id == employee_id)
        )
        
        result = await db.execute(query)
        employee = result.scalars().first()

        department = employee.department_rel.name

        await db.delete(employee)
        await db.commit()
        
        await update_number_of_employees(db, department, 'decrement')
        
    except NoResultFound:
        return None