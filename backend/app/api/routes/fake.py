import random

from faker import Faker
from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep
from app.models import (
    CommercialCustomer,
    Competitor,
    Employee,
    PersonalCustomer,
    Project,
)

router = APIRouter()
fake = Faker()

# Commercial Customer CRUD
@router.post("/commercial_customers")
def create_commercial_customer(session: SessionDep):
    customer = CommercialCustomer(
        company_name=fake.company(),
        contact_person_first_name=fake.first_name(),
        contact_person_last_name=fake.last_name(),
        contact_person_position=fake.job(),
        address_street=fake.street_address(),
        address_city=fake.city(),
        address_state=fake.state_abbr(),
        address_zip_code=fake.zipcode(),
        address_country=fake.country(),
        phone_number=fake.phone_number(),
        email=fake.company_email(),
        website=fake.url(),
        tax_id=fake.ein(),
        business_type=fake.bs()
    )
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@router.get("/commercial_customers/{customer_id}")
def read_commercial_customer(customer_id: int, session: SessionDep):
    customer = session.get(CommercialCustomer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Commercial Customer not found")
    return customer

@router.put("/commercial_customers/{customer_id}")
def update_commercial_customer(customer_id: int, customer_info: CommercialCustomer, session: SessionDep):
    customer = session.get(CommercialCustomer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Commercial Customer not found")
    customer_data = customer_info.dict(exclude_unset=True)
    for key, value in customer_data.items():
        setattr(customer, key, value)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@router.delete("/commercial_customers/{customer_id}")
def delete_commercial_customer(customer_id: int, session: SessionDep):
    customer = session.get(CommercialCustomer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Commercial Customer not found")
    session.delete(customer)
    session.commit()
    return {"detail": "Commercial Customer deleted"}

# Personal Customer CRUD
@router.post("/personal_customers")
def create_personal_customer(session: SessionDep):
    customer = PersonalCustomer(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        address_street=fake.street_address(),
        address_city=fake.city(),
        address_state=fake.state_abbr(),
        address_zip_code=fake.zipcode(),
        address_country=fake.country(),
        phone_number=fake.phone_number(),
        email=fake.email(),
        date_of_birth=fake.date_of_birth().strftime('%Y-%m-%d'),
        gender=fake.random_element(elements=('Male', 'Female')),
        occupation=fake.job()
    )
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@router.get("/personal_customers/{customer_id}")
def read_personal_customer(customer_id: int, session: SessionDep):
    customer = session.get(PersonalCustomer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Personal Customer not found")
    return customer

@router.put("/personal_customers/{customer_id}")
def update_personal_customer(customer_id: int, customer_info: PersonalCustomer, session: SessionDep):
    customer = session.get(PersonalCustomer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Personal Customer not found")
    customer_data = customer_info.dict(exclude_unset=True)
    for key, value in customer_data.items():
        setattr(customer, key, value)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@router.delete("/personal_customers/{customer_id}")
def delete_personal_customer(customer_id: int, session: SessionDep):
    customer = session.get(PersonalCustomer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Personal Customer not found")
    session.delete(customer)
    session.commit()
    return {"detail": "Personal Customer deleted"}

# Project CRUD
@router.post("/projects")
def create_project(session: SessionDep):
    project = Project(
        project_name=fake.catch_phrase(),
        description=fake.text(),
        start_date=fake.date_this_decade().strftime('%Y-%m-%d'),
        end_date=fake.date_between(start_date='+1d', end_date='+2y').strftime('%Y-%m-%d'),
        budget=round(random.uniform(10000, 1000000), 2),
        client_company_name=fake.company(),
        client_contact_person_first_name=fake.first_name(),
        client_contact_person_last_name=fake.last_name(),
        client_contact_person_position=fake.job(),
        client_phone_number=fake.phone_number(),
        client_email=fake.company_email(),
        status=fake.random_element(elements=('Not Started', 'In Progress', 'Completed', 'On Hold'))
    )
    session.add(project)
    session.commit()
    session.refresh(project)
    return project

@router.get("/projects/{project_id}")
def read_project(project_id: int, session: SessionDep):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/projects/{project_id}")
def update_project(project_id: int, project_info: Project, session: SessionDep):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project_data = project_info.dict(exclude_unset=True)
    for key, value in project_data.items():
        setattr(project, key, value)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project

@router.delete("/projects/{project_id}")
def delete_project(project_id: int, session: SessionDep):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    session.delete(project)
    session.commit()
    return {"detail": "Project deleted"}

# Employee CRUD
@router.post("/employees")
def create_employee(session: SessionDep):
    employee = Employee(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        address_street=fake.street_address(),
        address_city=fake.city(),
        address_state=fake.state_abbr(),
        address_zip_code=fake.zipcode(),
        address_country=fake.country(),
        phone_number=fake.phone_number(),
        email=fake.email(),
        date_of_birth=fake.date_of_birth().strftime('%Y-%m-%d'),
        gender=fake.random_element(elements=('Male', 'Female')),
        position=fake.job(),
        department=fake.random_element(elements=('HR', 'IT', 'Finance', 'Marketing', 'Sales')),
        salary=round(random.uniform(30000, 120000), 2),
        date_hired=fake.date_this_decade().strftime('%Y-%m-%d')
    )
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee

@router.get("/employees/{employee_id}")
def read_employee(employee_id: int, session: SessionDep):
    employee = session.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee_info: Employee, session: SessionDep):
    employee = session.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee_data = employee_info.dict(exclude_unset=True)
    for key, value in employee_data.items():
        setattr(employee, key, value)
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee

@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, session: SessionDep):
    employee = session.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    session.delete(employee)
    session.commit()
    return {"detail": "Employee deleted"}

# Competitor CRUD
@router.post("/competitors")
def create_competitor(session: SessionDep):
    competitor = Competitor(
        company_name=fake.company(),
        address_street=fake.street_address(),
        address_city=fake.city(),
        address_state=fake.state_abbr(),
        address_zip_code=fake.zipcode(),
        address_country=fake.country(),
        phone_number=fake.phone_number(),
        email=fake.company_email(),
        website=fake.url(),
        industry=fake.random_element(elements=('Technology', 'Finance', 'Healthcare', 'Retail', 'Manufacturing')),
        number_of_employees=random.randint(50, 5000),
        annual_revenue=round(random.uniform(1000000, 50000000), 2)
    )
    session.add(competitor)
    session.commit()
    session.refresh(competitor)
    return competitor

@router.get("/competitors/{competitor_id}")
def read_competitor(competitor_id: int, session: SessionDep):
    competitor = session.get(Competitor, competitor_id)
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")
    return competitor

@router.put("/competitors/{competitor_id}")
def update_competitor(competitor_id: int, competitor_info: Competitor, session: SessionDep):
    competitor = session.get(Competitor, competitor_id)
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")
    competitor_data = competitor_info.dict(exclude_unset=True)
    for key, value in competitor_data.items():
        setattr(competitor, key, value)
    session.add(competitor)
    session.commit()
    session.refresh(competitor)
    return competitor

@router.delete("/competitors/{competitor_id}")
def delete_competitor(competitor_id: int, session: SessionDep):
    competitor = session.get(Competitor, competitor_id)
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")
    session.delete(competitor)
    session.commit()
    return {"detail": "Competitor deleted"}
