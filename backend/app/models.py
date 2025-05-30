# models.py
from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey, Table, Enum, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
import enum

Base = declarative_base()

class WatchType(enum.Enum):
    AUTOMATIC = "AUTOMATIC"
    BATTERY = "BATTERY"
    MANUAL = "MANUAL"

class RepairStatus(enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    DELIVERED = "DELIVERED"

# Many-to-many relationship table
repair_request_types = Table(
    'repair_request_types',
    Base.metadata,
    Column('repair_request_id', UUID(as_uuid=True), ForeignKey('repair_requests.id')),
    Column('repair_type_id', UUID(as_uuid=True), ForeignKey('repair_types.id'))
)

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    address = Column(Text, nullable=False)
    email = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    repair_requests = relationship("RepairRequest", back_populates="customer")

class WatchBrand(Base):
    __tablename__ = "watch_brands"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    repair_requests = relationship("RepairRequest", back_populates="watch_brand")

class RepairType(Base):
    __tablename__ = "repair_types"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    estimated_price = Column(Numeric(10, 2), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    repair_requests = relationship("RepairRequest", secondary=repair_request_types, back_populates="repair_types")

class RepairRequest(Base):
    __tablename__ = "repair_requests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reference_number = Column(String(20), unique=True, nullable=False, index=True)
    
    # Customer info (stored directly for non-registered customers)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=True)
    customer_name = Column(String(255), nullable=False)
    customer_cpf = Column(String(14), nullable=False)
    customer_phone = Column(String(20), nullable=False)
    customer_address = Column(Text, nullable=False)
    customer_email = Column(String(255), nullable=True)
    
    # Watch info
    watch_brand_id = Column(UUID(as_uuid=True), ForeignKey("watch_brands.id"), nullable=False)
    watch_type = Column(Enum(WatchType), nullable=False)
    
    # Repair info
    problem_description = Column(Text, nullable=False)
    status = Column(Enum(RepairStatus), default=RepairStatus.PENDING)
    estimated_completion = Column(DateTime, nullable=True)
    total_price = Column(Numeric(10, 2), nullable=True)
    internal_notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="repair_requests")
    watch_brand = relationship("WatchBrand", back_populates="repair_requests")
    repair_types = relationship("RepairType", secondary=repair_request_types, back_populates="repair_requests")
