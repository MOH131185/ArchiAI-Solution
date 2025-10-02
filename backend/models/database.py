"""
Database models and configuration for ArchiAI Solution
"""

from sqlalchemy import create_engine, Column, String, Float, DateTime, Text, JSON, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from typing import Optional
import os

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/archiai")

# Create database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

class Project(Base):
    """Project database model"""
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    surface_area = Column(Float, nullable=False)
    location = Column(JSON, nullable=False)
    requirements = Column(JSON, nullable=False)
    status = Column(String(50), nullable=False, default="created")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    designs = Column(JSON, nullable=True)
    portfolio = Column(JSON, nullable=True)
    
    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name}, type={self.type})>"

class Design(Base):
    """Design database model"""
    __tablename__ = "designs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), nullable=False)
    design_type = Column(String(50), nullable=False)  # 2d, 3d, structural, mep
    design_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Design(id={self.id}, project_id={self.project_id}, type={self.design_type})>"

class ClimateData(Base):
    """Climate data database model"""
    __tablename__ = "climate_data"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location = Column(String(255), nullable=False)
    coordinates = Column(JSON, nullable=False)
    climate_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ClimateData(id={self.id}, location={self.location})>"

class ArchitecturalStyle(Base):
    """Architectural style database model"""
    __tablename__ = "architectural_styles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location = Column(String(255), nullable=False)
    style_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ArchitecturalStyle(id={self.id}, location={self.location})>"

class Export(Base):
    """Export database model"""
    __tablename__ = "exports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), nullable=False)
    export_format = Column(String(50), nullable=False)
    software_type = Column(String(50), nullable=False)
    file_url = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Export(id={self.id}, project_id={self.project_id}, format={self.export_format})>"

class CostEstimate(Base):
    """Cost estimate database model"""
    __tablename__ = "cost_estimates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), nullable=False)
    cost_data = Column(JSON, nullable=False)
    excel_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<CostEstimate(id={self.id}, project_id={self.project_id})>"

class User(Base):
    """User database model"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"

class Portfolio(Base):
    """Portfolio database model"""
    __tablename__ = "portfolios"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    files = Column(JSON, nullable=False)
    analysis = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Portfolio(id={self.id}, user_id={self.user_id}, name={self.name})>"

class Modification(Base):
    """Modification database model"""
    __tablename__ = "modifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), nullable=False)
    design_type = Column(String(50), nullable=False)
    text_command = Column(Text, nullable=False)
    modification_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Modification(id={self.id}, project_id={self.project_id}, type={self.design_type})>"

class Analytics(Base):
    """Analytics database model"""
    __tablename__ = "analytics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), nullable=False)
    metric = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Analytics(id={self.id}, project_id={self.project_id}, metric={self.metric})>"

class Notification(Base):
    """Notification database model"""
    __tablename__ = "notifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    type = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, type={self.type})>"

# Database utility functions
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

def create_project(
    name: str,
    type: str,
    surface_area: float,
    location: dict,
    requirements: dict,
    db_session
) -> Project:
    """Create a new project"""
    project = Project(
        name=name,
        type=type,
        surface_area=surface_area,
        location=location,
        requirements=requirements
    )
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)
    return project

def get_project(project_id: str, db_session) -> Optional[Project]:
    """Get project by ID"""
    return db_session.query(Project).filter(Project.id == project_id).first()

def update_project(project_id: str, updates: dict, db_session) -> Optional[Project]:
    """Update project"""
    project = db_session.query(Project).filter(Project.id == project_id).first()
    if project:
        for key, value in updates.items():
            setattr(project, key, value)
        project.updated_at = datetime.utcnow()
        db_session.commit()
        db_session.refresh(project)
    return project

def delete_project(project_id: str, db_session) -> bool:
    """Delete project"""
    project = db_session.query(Project).filter(Project.id == project_id).first()
    if project:
        db_session.delete(project)
        db_session.commit()
        return True
    return False

def create_design(
    project_id: str,
    design_type: str,
    design_data: dict,
    db_session
) -> Design:
    """Create a new design"""
    design = Design(
        project_id=project_id,
        design_type=design_type,
        design_data=design_data
    )
    db_session.add(design)
    db_session.commit()
    db_session.refresh(design)
    return design

def get_design(design_id: str, db_session) -> Optional[Design]:
    """Get design by ID"""
    return db_session.query(Design).filter(Design.id == design_id).first()

def get_project_designs(project_id: str, db_session) -> list:
    """Get all designs for a project"""
    return db_session.query(Design).filter(Design.project_id == project_id).all()

def update_design(design_id: str, design_data: dict, db_session) -> Optional[Design]:
    """Update design"""
    design = db_session.query(Design).filter(Design.id == design_id).first()
    if design:
        design.design_data = design_data
        design.modified_at = datetime.utcnow()
        db_session.commit()
        db_session.refresh(design)
    return design

def create_climate_data(
    location: str,
    coordinates: dict,
    climate_data: dict,
    db_session
) -> ClimateData:
    """Create climate data record"""
    climate = ClimateData(
        location=location,
        coordinates=coordinates,
        climate_data=climate_data
    )
    db_session.add(climate)
    db_session.commit()
    db_session.refresh(climate)
    return climate

def get_climate_data(location: str, db_session) -> Optional[ClimateData]:
    """Get climate data by location"""
    return db_session.query(ClimateData).filter(ClimateData.location == location).first()

def create_architectural_style(
    location: str,
    style_data: dict,
    db_session
) -> ArchitecturalStyle:
    """Create architectural style record"""
    style = ArchitecturalStyle(
        location=location,
        style_data=style_data
    )
    db_session.add(style)
    db_session.commit()
    db_session.refresh(style)
    return style

def get_architectural_style(location: str, db_session) -> Optional[ArchitecturalStyle]:
    """Get architectural style by location"""
    return db_session.query(ArchitecturalStyle).filter(ArchitecturalStyle.location == location).first()

def create_export(
    project_id: str,
    export_format: str,
    software_type: str,
    file_url: str,
    db_session
) -> Export:
    """Create export record"""
    export = Export(
        project_id=project_id,
        export_format=export_format,
        software_type=software_type,
        file_url=file_url
    )
    db_session.add(export)
    db_session.commit()
    db_session.refresh(export)
    return export

def get_exports(project_id: str, db_session) -> list:
    """Get all exports for a project"""
    return db_session.query(Export).filter(Export.project_id == project_id).all()

def create_cost_estimate(
    project_id: str,
    cost_data: dict,
    excel_url: str = None,
    db_session
) -> CostEstimate:
    """Create cost estimate record"""
    cost_estimate = CostEstimate(
        project_id=project_id,
        cost_data=cost_data,
        excel_url=excel_url
    )
    db_session.add(cost_estimate)
    db_session.commit()
    db_session.refresh(cost_estimate)
    return cost_estimate

def get_cost_estimate(project_id: str, db_session) -> Optional[CostEstimate]:
    """Get cost estimate by project ID"""
    return db_session.query(CostEstimate).filter(CostEstimate.project_id == project_id).first()

def create_user(
    username: str,
    email: str,
    hashed_password: str,
    db_session
) -> User:
    """Create a new user"""
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

def get_user(username: str, db_session) -> Optional[User]:
    """Get user by username"""
    return db_session.query(User).filter(User.username == username).first()

def get_user_by_email(email: str, db_session) -> Optional[User]:
    """Get user by email"""
    return db_session.query(User).filter(User.email == email).first()

def create_portfolio(
    user_id: str,
    name: str,
    description: str,
    files: dict,
    analysis: dict = None,
    db_session
) -> Portfolio:
    """Create a new portfolio"""
    portfolio = Portfolio(
        user_id=user_id,
        name=name,
        description=description,
        files=files,
        analysis=analysis
    )
    db_session.add(portfolio)
    db_session.commit()
    db_session.refresh(portfolio)
    return portfolio

def get_portfolio(portfolio_id: str, db_session) -> Optional[Portfolio]:
    """Get portfolio by ID"""
    return db_session.query(Portfolio).filter(Portfolio.id == portfolio_id).first()

def get_user_portfolios(user_id: str, db_session) -> list:
    """Get all portfolios for a user"""
    return db_session.query(Portfolio).filter(Portfolio.user_id == user_id).all()

def create_modification(
    project_id: str,
    design_type: str,
    text_command: str,
    modification_data: dict,
    db_session
) -> Modification:
    """Create a new modification"""
    modification = Modification(
        project_id=project_id,
        design_type=design_type,
        text_command=text_command,
        modification_data=modification_data
    )
    db_session.add(modification)
    db_session.commit()
    db_session.refresh(modification)
    return modification

def get_modifications(project_id: str, db_session) -> list:
    """Get all modifications for a project"""
    return db_session.query(Modification).filter(Modification.project_id == project_id).all()

def create_analytics(
    project_id: str,
    metric: str,
    value: float,
    db_session
) -> Analytics:
    """Create analytics record"""
    analytics = Analytics(
        project_id=project_id,
        metric=metric,
        value=value
    )
    db_session.add(analytics)
    db_session.commit()
    db_session.refresh(analytics)
    return analytics

def get_analytics(project_id: str, db_session) -> list:
    """Get analytics for a project"""
    return db_session.query(Analytics).filter(Analytics.project_id == project_id).all()

def create_notification(
    user_id: str,
    type: str,
    message: str,
    db_session
) -> Notification:
    """Create a new notification"""
    notification = Notification(
        user_id=user_id,
        type=type,
        message=message
    )
    db_session.add(notification)
    db_session.commit()
    db_session.refresh(notification)
    return notification

def get_notifications(user_id: str, db_session) -> list:
    """Get all notifications for a user"""
    return db_session.query(Notification).filter(Notification.user_id == user_id).all()

def mark_notification_read(notification_id: str, db_session) -> bool:
    """Mark notification as read"""
    notification = db_session.query(Notification).filter(Notification.id == notification_id).first()
    if notification:
        notification.read = True
        db_session.commit()
        return True
    return False
