"""
Database configuration and connection management
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import asyncpg
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import redis.asyncio as redis
import logging

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class MongoDB:
    client: AsyncIOMotorClient = None
    database = None

mongodb = MongoDB()

engine = create_engine(settings.POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

redis_client = None

async def init_db():
    """Initialize all database connections"""
    try:
        await init_mongodb()
    except Exception as e:
        logger.warning(f"MongoDB initialization failed: {e}")
    
    try:
        await init_redis()
    except Exception as e:
        logger.warning(f"Redis initialization failed: {e}")
    
    try:
        init_postgresql()
    except Exception as e:
        logger.warning(f"PostgreSQL initialization failed: {e}")
    
    logger.info("Database initialization completed (some services may be unavailable)")

async def init_mongodb():
    """Initialize MongoDB connection"""
    try:
        mongodb.client = AsyncIOMotorClient(settings.MONGODB_URL)
        mongodb.database = mongodb.client[settings.MONGODB_DB_NAME]
        
        await mongodb.client.admin.command('ping')
        logger.info("MongoDB connected successfully")
        
        await create_mongodb_indexes()
        
    except Exception as e:
        logger.warning(f"MongoDB connection failed: {e}")
        logger.warning("Running in development mode without MongoDB")

async def create_mongodb_indexes():
    """Create MongoDB indexes for optimal performance"""
    try:
        await mongodb.database.patients.create_index("patient_id")
        await mongodb.database.patients.create_index("created_at")
        
        await mongodb.database.medical_documents.create_index("patient_id")
        await mongodb.database.medical_documents.create_index("document_type")
        await mongodb.database.medical_documents.create_index("upload_date")
        
        await mongodb.database.provider_matches.create_index("patient_id")
        await mongodb.database.provider_matches.create_index("match_score")
        
        await mongodb.database.insurance_claims.create_index("patient_id")
        await mongodb.database.insurance_claims.create_index("claim_status")
        
        logger.info("MongoDB indexes created successfully")
        
    except Exception as e:
        logger.error(f"Failed to create MongoDB indexes: {e}")

def init_postgresql():
    """Initialize PostgreSQL connection for FHIR resources"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("PostgreSQL connected and tables created")
        
    except Exception as e:
        logger.warning(f"PostgreSQL connection failed: {e}")
        logger.warning("Running in development mode without PostgreSQL")

async def init_redis():
    """Initialize Redis connection"""
    global redis_client
    try:
        redis_client = redis.from_url(settings.REDIS_URL)
        await redis_client.ping()
        logger.info("Redis connected successfully")
        
    except Exception as e:
        logger.warning(f"Redis connection failed: {e}")
        logger.warning("Running in development mode without Redis")

def get_db():
    """Get PostgreSQL database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_mongodb():
    """Get MongoDB database instance"""
    return mongodb.database

async def get_redis():
    """Get Redis client instance"""
    return redis_client

async def close_db_connections():
    """Close all database connections"""
    if mongodb.client:
        mongodb.client.close()
    
    if redis_client:
        await redis_client.close()
    
    logger.info("Database connections closed")
