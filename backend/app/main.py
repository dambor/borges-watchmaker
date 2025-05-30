# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
import uuid
from datetime import datetime

from database import get_db
from models import Customer, WatchBrand, RepairType, RepairRequest, WatchType, RepairStatus
import schemas
from utils import generate_reference_number, format_cpf_for_display

app = FastAPI(title="Watchmaker Repair Service API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== CUSTOMER ENDPOINTS =====

@app.get("/api/repair-form/data", response_model=schemas.FormData)
async def get_form_data(db: Session = Depends(get_db)):
    """Get watch brands and repair types for the form"""
    watch_brands = db.query(WatchBrand).filter(WatchBrand.is_active == True).all()
    repair_types = db.query(RepairType).filter(RepairType.is_active == True).all()
    
    return schemas.FormData(
        watch_brands=watch_brands,
        repair_types=repair_types
    )

@app.get("/api/customers/check", response_model=schemas.CustomerCheck)
async def check_customer(cpf: str, db: Session = Depends(get_db)):
    """Check if customer exists by CPF"""
    # Clean CPF
    cpf_digits = ''.join(filter(str.isdigit, cpf))
    
    # Look for customer with this CPF (try both formatted and unformatted)
    customer = db.query(Customer).filter(
        or_(
            Customer.cpf == cpf,
            Customer.cpf == format_cpf_for_display(cpf_digits)
        )
    ).first()
    
    if customer:
        return schemas.CustomerCheck(
            exists=True,
            customer=schemas.CustomerData(
                name=customer.name,
                cpf=customer.cpf,
                phone=customer.phone,
                address=customer.address,
                email=customer.email
            )
        )
    
    return schemas.CustomerCheck(exists=False)

@app.post("/api/repair-requests")
async def create_repair_request(request: schemas.RepairRequestCreate, db: Session = Depends(get_db)):
    """Create a new repair request"""
    
    # Validate watch brand exists
    watch_brand = db.query(WatchBrand).filter(
        and_(WatchBrand.id == request.watch_data.brand_id, WatchBrand.is_active == True)
    ).first()
    if not watch_brand:
        raise HTTPException(status_code=400, detail="Invalid watch brand")
    
    # Validate repair types exist
    repair_types = db.query(RepairType).filter(
        and_(RepairType.id.in_(request.repair_data.repair_type_ids), RepairType.is_active == True)
    ).all()
    if len(repair_types) != len(request.repair_data.repair_type_ids):
        raise HTTPException(status_code=400, detail="Invalid repair types")
    
    customer_id = None
    customer_account_created = False
    
    # Check if customer wants to create an account
    if request.create_customer_account:
        # Check if customer already exists
        existing_customer = db.query(Customer).filter(Customer.cpf == request.customer_data.cpf).first()
        
        if existing_customer:
            customer_id = existing_customer.id
        else:
            # Create new customer
            new_customer = Customer(
                name=request.customer_data.name,
                cpf=request.customer_data.cpf,
                phone=request.customer_data.phone,
                address=request.customer_data.address,
                email=request.customer_data.email
            )
            db.add(new_customer)
            db.flush()  # Get the ID
            customer_id = new_customer.id
            customer_account_created = True
    
    # Generate unique reference number
    reference_number = generate_reference_number()
    while db.query(RepairRequest).filter(RepairRequest.reference_number == reference_number).first():
        reference_number = generate_reference_number()
    
    # Create repair request
    repair_request = RepairRequest(
        reference_number=reference_number,
        customer_id=customer_id,
        customer_name=request.customer_data.name,
        customer_cpf=request.customer_data.cpf,
        customer_phone=request.customer_data.phone,
        customer_address=request.customer_data.address,
        customer_email=request.customer_data.email,
        watch_brand_id=request.watch_data.brand_id,
        watch_type=WatchType(request.watch_data.type),
        problem_description=request.repair_data.problem_description,
        repair_types=repair_types
    )
    
    db.add(repair_request)
    db.commit()
    
    return {
        "success": True,
        "repair_request": {
            "id": str(repair_request.id),
            "reference_number": repair_request.reference_number,
            "status": repair_request.status.value,
            "created_at": repair_request.created_at
        },
        "customer_account_created": customer_account_created,
        "message": "Repair request submitted successfully!"
    }

@app.get("/api/repair-requests/{repair_id}/status")
async def get_repair_status(repair_id: str, db: Session = Depends(get_db)):
    """Get repair request status"""
    try:
        repair_uuid = uuid.UUID(repair_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid repair ID format")
    
    repair = db.query(RepairRequest).filter(RepairRequest.id == repair_uuid).first()
    if not repair:
        raise HTTPException(status_code=404, detail="Repair request not found")
    
    return {
        "id": str(repair.id),
        "reference_number": repair.reference_number,
        "status": repair.status.value,
        "estimated_completion": repair.estimated_completion,
        "customer_name": repair.customer_name,
        "watch_brand": repair.watch_brand.name,
        "repair_types": [rt.name for rt in repair.repair_types],
        "created_at": repair.created_at,
        "notes": repair.internal_notes if repair.status != RepairStatus.PENDING else None
    }

@app.get("/api/repair-requests/reference/{reference_number}/status")
async def get_repair_status_by_reference(reference_number: str, db: Session = Depends(get_db)):
    """Get repair request status by reference number"""
    repair = db.query(RepairRequest).filter(RepairRequest.reference_number == reference_number).first()
    if not repair:
        raise HTTPException(status_code=404, detail="Repair request not found")
    
    return {
        "id": str(repair.id),
        "reference_number": repair.reference_number,
        "status": repair.status.value,
        "estimated_completion": repair.estimated_completion,
        "customer_name": repair.customer_name,
        "watch_brand": repair.watch_brand.name,
        "repair_types": [rt.name for rt in repair.repair_types],
        "created_at": repair.created_at,
        "notes": repair.internal_notes if repair.status != RepairStatus.PENDING else None
    }

# ===== ADMIN ENDPOINTS =====

@app.get("/api/admin/repair-requests")
async def list_repair_requests(
    status: Optional[str] = None,
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """List all repair requests with pagination"""
    query = db.query(RepairRequest)
    
    if status:
        try:
            status_enum = RepairStatus(status.upper())
            query = query.filter(RepairRequest.status == status_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid status")
    
    total_items = query.count()
    total_pages = (total_items + limit - 1) // limit
    
    repairs = query.offset((page - 1) * limit).limit(limit).all()
    
    repair_list = []
    for repair in repairs:
        repair_list.append({
            "id": str(repair.id),
            "reference_number": repair.reference_number,
            "customer_name": repair.customer_name,
            "customer_phone": repair.customer_phone,
            "watch_brand": repair.watch_brand.name,
            "watch_type": repair.watch_type.value,
            "repair_types": [rt.name for rt in repair.repair_types],
            "status": repair.status.value,
            "total_price": repair.total_price,
            "created_at": repair.created_at
        })
    
    return {
        "repair_requests": repair_list,
        "pagination": {
            "current_page": page,
            "total_pages": total_pages,
            "total_items": total_items
        }
    }

@app.get("/api/admin/repair-requests/{repair_id}")
async def get_repair_request_details(repair_id: str, db: Session = Depends(get_db)):
    """Get detailed repair request information"""
    try:
        repair_uuid = uuid.UUID(repair_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid repair ID format")
    
    repair = db.query(RepairRequest).filter(RepairRequest.id == repair_uuid).first()
    if not repair:
        raise HTTPException(status_code=404, detail="Repair request not found")
    
    return {
        "id": str(repair.id),
        "reference_number": repair.reference_number,
        "customer_name": repair.customer_name,
        "customer_cpf": repair.customer_cpf,
        "customer_phone": repair.customer_phone,
        "customer_address": repair.customer_address,
        "customer_email": repair.customer_email,
        "watch_brand": repair.watch_brand.name,
        "watch_type": repair.watch_type.value,
        "repair_types": [{"id": str(rt.id), "name": rt.name, "description": rt.description} for rt in repair.repair_types],
        "problem_description": repair.problem_description,
        "status": repair.status.value,
        "estimated_completion": repair.estimated_completion,
        "total_price": repair.total_price,
        "internal_notes": repair.internal_notes,
        "created_at": repair.created_at,
        "updated_at": repair.updated_at
    }

@app.put("/api/admin/repair-requests/{repair_id}")
async def update_repair_request(
    repair_id: str,
    update_data: schemas.RepairRequestUpdate,
    db: Session = Depends(get_db)
):
    """Update repair request"""
    try:
        repair_uuid = uuid.UUID(repair_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid repair ID format")
    
    repair = db.query(RepairRequest).filter(RepairRequest.id == repair_uuid).first()
    if not repair:
        raise HTTPException(status_code=404, detail="Repair request not found")
    
    # Update fields
    if update_data.status:
        try:
            repair.status = RepairStatus(update_data.status.upper())
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid status")
    
    if update_data.estimated_completion is not None:
        repair.estimated_completion = update_data.estimated_completion
    
    if update_data.total_price is not None:
        repair.total_price = update_data.total_price
    
    if update_data.internal_notes is not None:
        repair.internal_notes = update_data.internal_notes
    
    repair.updated_at = datetime.utcnow()
    db.commit()
    
    return {"success": True, "message": "Repair request updated successfully"}

# ===== ADMIN BRAND MANAGEMENT =====

@app.get("/api/admin/watch-brands", response_model=List[schemas.WatchBrand])
async def list_watch_brands(db: Session = Depends(get_db)):
    """List all watch brands"""
    return db.query(WatchBrand).all()

@app.post("/api/admin/watch-brands", response_model=schemas.WatchBrand)
async def create_watch_brand(brand: schemas.WatchBrandCreate, db: Session = Depends(get_db)):
    """Create new watch brand"""
    # Check if brand already exists
    existing = db.query(WatchBrand).filter(WatchBrand.name == brand.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Watch brand already exists")
    
    db_brand = WatchBrand(**brand.dict())
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand

@app.put("/api/admin/watch-brands/{brand_id}")
async def update_watch_brand(
    brand_id: str, 
    brand: schemas.WatchBrandCreate, 
    db: Session = Depends(get_db)
):
    """Update watch brand"""
    try:
        brand_uuid = uuid.UUID(brand_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid brand ID format")
    
    db_brand = db.query(WatchBrand).filter(WatchBrand.id == brand_uuid).first()
    if not db_brand:
        raise HTTPException(status_code=404, detail="Watch brand not found")
    
    for field, value in brand.dict().items():
        setattr(db_brand, field, value)
    
    db.commit()
    return {"success": True, "message": "Watch brand updated successfully"}

@app.delete("/api/admin/watch-brands/{brand_id}")
async def delete_watch_brand(brand_id: str, db: Session = Depends(get_db)):
    """Delete watch brand (soft delete by setting is_active=False)"""
    try:
        brand_uuid = uuid.UUID(brand_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid brand ID format")
    
    db_brand = db.query(WatchBrand).filter(WatchBrand.id == brand_uuid).first()
    if not db_brand:
        raise HTTPException(status_code=404, detail="Watch brand not found")
    
    db_brand.is_active = False
    db.commit()
    return {"success": True, "message": "Watch brand deactivated successfully"}

# ===== ADMIN REPAIR TYPE MANAGEMENT =====

@app.get("/api/admin/repair-types", response_model=List[schemas.RepairType])
async def list_repair_types(db: Session = Depends(get_db)):
    """List all repair types"""
    return db.query(RepairType).all()

@app.post("/api/admin/repair-types", response_model=schemas.RepairType)
async def create_repair_type(repair_type: schemas.RepairTypeCreate, db: Session = Depends(get_db)):
    """Create new repair type"""
    db_repair_type = RepairType(**repair_type.dict())
    db.add(db_repair_type)
    db.commit()
    db.refresh(db_repair_type)
    return db_repair_type

@app.put("/api/admin/repair-types/{repair_type_id}")
async def update_repair_type(
    repair_type_id: str,
    repair_type: schemas.RepairTypeCreate,
    db: Session = Depends(get_db)
):
    """Update repair type"""
    try:
        repair_type_uuid = uuid.UUID(repair_type_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid repair type ID format")
    
    db_repair_type = db.query(RepairType).filter(RepairType.id == repair_type_uuid).first()
    if not db_repair_type:
        raise HTTPException(status_code=404, detail="Repair type not found")
    
    for field, value in repair_type.dict().items():
        setattr(db_repair_type, field, value)
    
    db.commit()
    return {"success": True, "message": "Repair type updated successfully"}

@app.delete("/api/admin/repair-types/{repair_type_id}")
async def delete_repair_type(repair_type_id: str, db: Session = Depends(get_db)):
    """Delete repair type (soft delete)"""
    try:
        repair_type_uuid = uuid.UUID(repair_type_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid repair type ID format")
    
    db_repair_type = db.query(RepairType).filter(RepairType.id == repair_type_uuid).first()
    if not db_repair_type:
        raise HTTPException(status_code=404, detail="Repair type not found")
    
    db_repair_type.is_active = False
    db.commit()
    return {"success": True, "message": "Repair type deactivated successfully"}

# ===== HEALTH CHECK =====
@app.get("/")
async def root():
    return {"message": "Watchmaker Repair Service API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)