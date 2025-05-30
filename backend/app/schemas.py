# schemas.py
from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
import re

class WatchBrandBase(BaseModel):
    name: str
    is_active: bool = True

class WatchBrandCreate(WatchBrandBase):
    pass

class WatchBrand(WatchBrandBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class RepairTypeBase(BaseModel):
    name: str
    description: Optional[str] = None
    estimated_price: Optional[Decimal] = None
    is_active: bool = True

class RepairTypeCreate(RepairTypeBase):
    pass

class RepairType(RepairTypeBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class CustomerData(BaseModel):
    name: str
    cpf: str
    phone: str
    address: str
    email: Optional[str] = None
    
    @field_validator('cpf')
    @classmethod
    def validate_cpf(cls, v):
        # Remove non-digits
        cpf = re.sub(r'\D', '', v)
        
        # Check if CPF has 11 digits
        if len(cpf) != 11:
            raise ValueError('CPF must have 11 digits')
        
        # Check if all digits are the same
        if cpf == cpf[0] * 11:
            raise ValueError('Invalid CPF')
        
        # Calculate verification digits
        def calculate_digit(cpf_partial):
            sum_val = sum(int(digit) * weight for digit, weight in zip(cpf_partial, range(len(cpf_partial) + 1, 1, -1)))
            remainder = sum_val % 11
            return 0 if remainder < 2 else 11 - remainder
        
        # Validate first digit
        if int(cpf[9]) != calculate_digit(cpf[:9]):
            raise ValueError('Invalid CPF')
        
        # Validate second digit
        if int(cpf[10]) != calculate_digit(cpf[:10]):
            raise ValueError('Invalid CPF')
        
        # Format CPF
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

class WatchData(BaseModel):
    brand_id: str
    type: str  # AUTOMATIC, BATTERY, MANUAL

class RepairData(BaseModel):
    repair_type_ids: List[str]
    problem_description: str

class RepairRequestCreate(BaseModel):
    customer_data: CustomerData
    watch_data: WatchData
    repair_data: RepairData
    create_customer_account: bool = False

class RepairRequestResponse(BaseModel):
    id: str
    reference_number: str
    customer_name: str
    customer_phone: str
    watch_brand_name: str
    watch_type: str
    repair_type_names: List[str]
    problem_description: str
    status: str
    estimated_completion: Optional[datetime] = None
    total_price: Optional[Decimal] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class RepairRequestUpdate(BaseModel):
    status: Optional[str] = None
    estimated_completion: Optional[datetime] = None
    total_price: Optional[Decimal] = None
    internal_notes: Optional[str] = None

class FormData(BaseModel):
    watch_brands: List[WatchBrand]
    repair_types: List[RepairType]

class CustomerCheck(BaseModel):
    exists: bool
    customer: Optional[CustomerData] = None