from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Receptionist(db.Model):
    __tablename__ = 'receptionists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    checklists = db.relationship('Checklist', backref='receptionist', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'active': self.active
        }


class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=False, unique=True)
    building = db.Column(db.String(20), nullable=False)
    checklists = db.relationship('Checklist', backref='room', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'building': self.building
        }


class Checklist(db.Model):
    __tablename__ = 'checklists'
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    receptionist_id = db.Column(db.Integer, db.ForeignKey('receptionists.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Disponibilidad de cupos (p, v, v1)
    disponibilidad_cupos = db.Column(db.String(5), nullable=False)
    # Limpieza general (ok, x)
    limpieza_general = db.Column(db.String(5), nullable=False)
    # Limpieza baños (ok, x)
    limpieza_banos = db.Column(db.String(5), nullable=False)
    # Insumos básicos (ok, x)
    insumos_basicos = db.Column(db.String(5), nullable=False)
    # Iluminación (ok, x)
    iluminacion = db.Column(db.String(5), nullable=False)
    # Agua (ok, x)
    agua = db.Column(db.String(5), nullable=False)
    # Ventanas (ok, x)
    ventanas = db.Column(db.String(5), nullable=False)
    # Cortinas blackout/roller (ok, x)
    cortinas = db.Column(db.String(5), nullable=False)
    # Estufas (ok, x)
    estufas = db.Column(db.String(5), nullable=False)
    # Mobiliario (ok, x)
    mobiliario = db.Column(db.String(5), nullable=False)
    # Chapas de acceso (ok, x)
    chapas = db.Column(db.String(5), nullable=False)
    # Casilleros (p, v, ambos)
    casilleros = db.Column(db.String(10), nullable=False)
    # Observaciones
    observaciones = db.Column(db.Text, default='')

    def to_dict(self):
        return {
            'id': self.id,
            'room_code': self.room.code,
            'room_building': self.room.building,
            'receptionist_name': self.receptionist.name,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'disponibilidad_cupos': self.disponibilidad_cupos,
            'limpieza_general': self.limpieza_general,
            'limpieza_banos': self.limpieza_banos,
            'insumos_basicos': self.insumos_basicos,
            'iluminacion': self.iluminacion,
            'agua': self.agua,
            'ventanas': self.ventanas,
            'cortinas': self.cortinas,
            'estufas': self.estufas,
            'mobiliario': self.mobiliario,
            'chapas': self.chapas,
            'casilleros': self.casilleros,
            'observaciones': self.observaciones
        }

    @property
    def ok_count(self):
        fields = [self.limpieza_general, self.limpieza_banos, self.insumos_basicos,
                  self.iluminacion, self.agua, self.ventanas, self.cortinas,
                  self.estufas, self.mobiliario, self.chapas]
        return sum(1 for f in fields if f == 'ok')

    @property
    def issue_count(self):
        fields = [self.limpieza_general, self.limpieza_banos, self.insumos_basicos,
                  self.iluminacion, self.agua, self.ventanas, self.cortinas,
                  self.estufas, self.mobiliario, self.chapas]
        return sum(1 for f in fields if f == 'x')
