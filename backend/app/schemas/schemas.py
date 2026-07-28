from pydantic import BaseModel
from typing import List, Optional

class StudentBase(BaseModel):
    student_id: str
    name: str
    email: str
    department: str
    semester: int
    cgpa: float

class StudentResponse(StudentBase):
    id: int
    class Config:
        from_attributes = True

class FacultyBase(BaseModel):
    faculty_id: str
    faculty_name: str
    department_id: Optional[int] = None

class FacultyResponse(FacultyBase):
    id: int
    class Config:
        from_attributes = True

class ClassroomBase(BaseModel):
    room_name: str
    building: str
    capacity: int

class ClassroomResponse(ClassroomBase):
    id: int
    class Config:
        from_attributes = True

class CourseBase(BaseModel):
    course_id: str
    course_name: str
    department_id: Optional[int] = None
    semester: int
    faculty_id: int

class CourseResponse(CourseBase):
    id: int
    faculty: FacultyResponse
    class Config:
        from_attributes = True

class TimetableSlotResponse(BaseModel):
    id: int
    course: CourseBase
    classroom: ClassroomBase
    faculty: FacultyBase
    day_of_week: str
    start_time: str
    end_time: str
    semester: int
    academic_year: int
    section: str
    slot_type: str
    period_number: Optional[int] = None
    class Config:
        from_attributes = True

class SolveRequest(BaseModel):
    course_id: int
    section: str
    semester: int

class SolveResponse(BaseModel):
    success: bool
    classroom_id: Optional[int] = None
    classroom_name: Optional[str] = None
    building: Optional[str] = None
    day_of_week: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    academic_year: Optional[int] = None
    section: Optional[str] = None
    error: Optional[str] = None

class CourseAttendance(BaseModel):
    course_code: str
    course_name: str
    total_classes: int
    present_classes: int
    attendance_percentage: float

class StudentAttendanceSummary(BaseModel):
    student_id: str
    student_name: str
    overall_percentage: float
    courses: List[CourseAttendance]

class RiskStudent(BaseModel):
    student_id: str
    student_name: str
    department: str
    cgpa: float
    semester: int
    course_code: str
    course_name: str
    attendance_percentage: float
    risk_probability: float
    is_at_risk: bool
    prediction_note: str

class RiskAnalysisResponse(BaseModel):
    total_analyzed: int
    total_at_risk: int
    risk_students: List[RiskStudent]
