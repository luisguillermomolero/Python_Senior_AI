from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
from core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, comment="Id único del usuario")
    username = Column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
        comment="Nombre de usuario único"
    )
    
    hashed_password = Column(
        String(255),
        nullable=False,
        comment="Contraseña hasheable del usuario"
    )
    
    created_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Fecha y hora de la creación del usuario"
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Fecha y hora de la última actualización"
    )

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError("El nombre de usuario no puede estar vacio")
        if len(username) < 3:
            raise ValueError("El nombre de usuario debe tener al menos 3 caracteres")
        if len(username) > 50:
            raise ValueError("El nombre de usuario no puede tener más de 50 caracteres")
        # username: luis_molero2025, luis-molero2025, luismolero2025
        if not username.replace('_','').replace('-', '').isalnum(): # luismolero2025
            raise ValueError("El username solo puede tener caracteres alfabeticos, números, guiones, guiones bajos")
        return username.lower().strip()
    
    @validates('hashed_password')
    def validate_hashed_password(self, key, hashed_password):
        if not hashed_password:
            raise ValueError ("La contraseña hasheada no puede estar vacia")
        return hashed_password
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
    
    def to_dict(self):
        return{
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    