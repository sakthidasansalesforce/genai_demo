from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date
from backend.database import Base, engine, SessionLocal

app = FastAPI(title="Employee Leave Management API")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    role = Column(String)
    department = Column(String)


class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer)
    employee_name = Column(String)
    leave_type = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    reason = Column(String)
    status = Column(String, default="Pending")


Base.metadata.create_all(bind=engine)


class EmployeeCreate(BaseModel):
    name: str
    email: str
    role: str
    department: str


class LeaveCreate(BaseModel):
    employee_id: int
    employee_name: str
    leave_type: str
    start_date: date
    end_date: date
    reason: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Employee Leave Management API running"}


@app.post("/employees")
def add_employee(emp: EmployeeCreate, db: Session = Depends(get_db)):
    employee = Employee(**emp.dict())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


@app.get("/employees")
def get_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()


@app.post("/leave/apply")
def apply_leave(leave: LeaveCreate, db: Session = Depends(get_db)):
    new_leave = LeaveRequest(**leave.dict(), status="Pending")
    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)
    return new_leave


@app.get("/leave/all")
def get_all_leaves(db: Session = Depends(get_db)):
    return db.query(LeaveRequest).order_by(LeaveRequest.id.desc()).all()


@app.get("/leave/employee/{employee_id}")
def get_employee_leaves(employee_id: int, db: Session = Depends(get_db)):
    return db.query(LeaveRequest).filter(
        LeaveRequest.employee_id == employee_id
    ).order_by(LeaveRequest.id.desc()).all()


@app.put("/leave/{leave_id}/approve")
def approve_leave(leave_id: int, db: Session = Depends(get_db)):
    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")

    leave.status = "Approved"
    db.commit()
    db.refresh(leave)
    return leave


@app.put("/leave/{leave_id}/reject")
def reject_leave(leave_id: int, db: Session = Depends(get_db)):
    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")

    leave.status = "Rejected"
    db.commit()
    db.refresh(leave)
    return leave


@app.get("/statistics")
def statistics(db: Session = Depends(get_db)):
    leaves = db.query(LeaveRequest).all()

    return {
        "total": len(leaves),
        "approved": len([l for l in leaves if l.status == "Approved"]),
        "rejected": len([l for l in leaves if l.status == "Rejected"]),
        "pending": len([l for l in leaves if l.status == "Pending"])
    }