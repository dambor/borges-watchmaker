# setup_database.py
"""
Database setup script for the Watchmaker Repair Service
Run this script to initialize the database with sample data
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, WatchBrand, RepairType
from decouple import config
import uuid

def setup_database():
    # Get database URL from environment
    DATABASE_URL = config('DATABASE_URL', default='postgresql://user:password@localhost/watchmaker_db')
    
    # Create engine and session
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(WatchBrand).count() > 0:
            print("Database already has data. Skipping initial setup.")
            return
        
        print("Setting up initial data...")
        
        # Create common watch brands
        watch_brands = [
            WatchBrand(name="Rolex", is_active=True),
            WatchBrand(name="Omega", is_active=True),
            WatchBrand(name="Seiko", is_active=True),
            WatchBrand(name="Casio", is_active=True),
            WatchBrand(name="Citizen", is_active=True),
            WatchBrand(name="Orient", is_active=True),
            WatchBrand(name="Fossil", is_active=True),
            WatchBrand(name="Tissot", is_active=True),
            WatchBrand(name="TAG Heuer", is_active=True),
            WatchBrand(name="Breitling", is_active=True),
            WatchBrand(name="Cartier", is_active=True),
            WatchBrand(name="Invicta", is_active=True),
            WatchBrand(name="Apple Watch", is_active=True),
            WatchBrand(name="Samsung Galaxy Watch", is_active=True),
            WatchBrand(name="Garmin", is_active=True),
            WatchBrand(name="Outro (Especificar nos comentários)", is_active=True)
        ]
        
        for brand in watch_brands:
            db.add(brand)
        
        # Create common repair types
        repair_types = [
            RepairType(
                name="Troca de Bateria",
                description="Substituição da bateria do relógio",
                estimated_price=25.00,
                is_active=True
            ),
            RepairType(
                name="Conserto do Vidro",
                description="Reparo ou substituição do vidro/cristal",
                estimated_price=80.00,
                is_active=True
            ),
            RepairType(
                name="Conserto da Pulseira",
                description="Reparo ou substituição da pulseira",
                estimated_price=60.00,
                is_active=True
            ),
            RepairType(
                name="Não está funcionando",
                description="Relógio parou de funcionar completamente",
                estimated_price=100.00,
                is_active=True
            ),
            RepairType(
                name="Atrasando/Adiantando",
                description="Relógio não mantém o horário correto",
                estimated_price=75.00,
                is_active=True
            ),
            RepairType(
                name="Coroa não funciona",
                description="Problemas com a coroa de ajuste",
                estimated_price=90.00,
                is_active=True
            ),
            RepairType(
                name="Resistência à água",
                description="Teste e reparo da vedação",
                estimated_price=50.00,
                is_active=True
            ),
            RepairType(
                name="Limpeza e Lubrificação",
                description="Manutenção preventiva completa",
                estimated_price=120.00,
                is_active=True
            ),
            RepairType(
                name="Ponteiros soltos/danificados",
                description="Reparo ou substituição dos ponteiros",
                estimated_price=70.00,
                is_active=True
            ),
            RepairType(
                name="Mostrador danificado",
                description="Reparo ou substituição do mostrador",
                estimated_price=150.00,
                is_active=True
            ),
            RepairType(
                name="Mecanismo completo",
                description="Substituição completa do movimento",
                estimated_price=200.00,
                is_active=True
            ),
            RepairType(
                name="Orçamento personalizado",
                description="Avaliação específica necessária",
                estimated_price=None,
                is_active=True
            )
        ]
        
        for repair_type in repair_types:
            db.add(repair_type)
        
        # Commit the transaction
        db.commit()
        print(f"✅ Successfully created {len(watch_brands)} watch brands")
        print(f"✅ Successfully created {len(repair_types)} repair types")
        print("✅ Database setup completed!")
        
    except Exception as e:
        print(f"❌ Error setting up database: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup_database()