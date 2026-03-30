import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import db, Room, Receptionist, Checklist
from rooms_data import get_buildings
from sqlalchemy import func, cast, Date

app = Flask(__name__)

# Database config
database_url = os.environ.get('DATABASE_URL', 'sqlite:///camp_checklist.db')
# Fix Render postgres URL (postgres:// -> postgresql://)
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

db.init_app(app)

with app.app_context():
    db.create_all()


# ── Pages ──────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    receptionists = Receptionist.query.filter_by(active=True).order_by(Receptionist.name).all()
    buildings = get_buildings()
    return render_template('index.html', receptionists=receptionists, buildings=buildings)


@app.route('/checklist/<building>')
def checklist_page(building):
    receptionist_id = request.args.get('receptionist_id', type=int)
    if not receptionist_id:
        return redirect(url_for('index'))
    receptionist = Receptionist.query.get_or_404(receptionist_id)
    rooms = Room.query.filter_by(building=building).order_by(Room.code).all()
    return render_template('checklist.html',
                           rooms=rooms,
                           building=building,
                           receptionist=receptionist)


@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')


@app.route('/receptionists')
def receptionists_page():
    receptionists = Receptionist.query.order_by(Receptionist.name).all()
    return render_template('receptionists.html', receptionists=receptionists)


@app.route('/history')
def history_page():
    return render_template('history.html')


# ── API Endpoints ──────────────────────────────────────────────────────────

@app.route('/api/receptionists', methods=['GET'])
def api_get_receptionists():
    recs = Receptionist.query.filter_by(active=True).order_by(Receptionist.name).all()
    return jsonify([r.to_dict() for r in recs])


@app.route('/api/receptionists', methods=['POST'])
def api_create_receptionist():
    data = request.json
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'error': 'El nombre es requerido'}), 400
    existing = Receptionist.query.filter_by(name=name).first()
    if existing:
        if not existing.active:
            existing.active = True
            db.session.commit()
            return jsonify(existing.to_dict()), 200
        return jsonify({'error': 'Ya existe un recepcionista con ese nombre'}), 400
    rec = Receptionist(name=name)
    db.session.add(rec)
    db.session.commit()
    return jsonify(rec.to_dict()), 201


@app.route('/api/receptionists/<int:rec_id>', methods=['PUT'])
def api_update_receptionist(rec_id):
    rec = Receptionist.query.get_or_404(rec_id)
    data = request.json
    if 'name' in data:
        rec.name = data['name'].strip()
    if 'active' in data:
        rec.active = data['active']
    db.session.commit()
    return jsonify(rec.to_dict())


@app.route('/api/receptionists/<int:rec_id>', methods=['DELETE'])
def api_delete_receptionist(rec_id):
    rec = Receptionist.query.get_or_404(rec_id)
    rec.active = False
    db.session.commit()
    return jsonify({'ok': True})


@app.route('/api/checklist', methods=['POST'])
def api_create_checklist():
    data = request.json
    room_id = data.get('room_id')
    receptionist_id = data.get('receptionist_id')

    if not room_id or not receptionist_id:
        return jsonify({'error': 'room_id y receptionist_id son requeridos'}), 400

    checklist = Checklist(
        room_id=room_id,
        receptionist_id=receptionist_id,
        disponibilidad_cupos=data.get('disponibilidad_cupos', ''),
        limpieza_general=data.get('limpieza_general', ''),
        limpieza_banos=data.get('limpieza_banos', ''),
        insumos_basicos=data.get('insumos_basicos', ''),
        iluminacion=data.get('iluminacion', ''),
        agua=data.get('agua', ''),
        ventanas=data.get('ventanas', ''),
        cortinas=data.get('cortinas', ''),
        estufas=data.get('estufas', ''),
        mobiliario=data.get('mobiliario', ''),
        chapas=data.get('chapas', ''),
        casilleros=data.get('casilleros', ''),
        observaciones=data.get('observaciones', '')
    )
    db.session.add(checklist)
    db.session.commit()
    return jsonify(checklist.to_dict()), 201


@app.route('/api/checklist/batch', methods=['POST'])
def api_create_checklist_batch():
    """Save multiple room checklists at once."""
    data = request.json
    items = data.get('items', [])
    receptionist_id = data.get('receptionist_id')

    if not items or not receptionist_id:
        return jsonify({'error': 'items y receptionist_id son requeridos'}), 400

    saved = []
    for item in items:
        checklist = Checklist(
            room_id=item['room_id'],
            receptionist_id=receptionist_id,
            disponibilidad_cupos=item.get('disponibilidad_cupos', ''),
            limpieza_general=item.get('limpieza_general', ''),
            limpieza_banos=item.get('limpieza_banos', ''),
            insumos_basicos=item.get('insumos_basicos', ''),
            iluminacion=item.get('iluminacion', ''),
            agua=item.get('agua', ''),
            ventanas=item.get('ventanas', ''),
            cortinas=item.get('cortinas', ''),
            estufas=item.get('estufas', ''),
            mobiliario=item.get('mobiliario', ''),
            chapas=item.get('chapas', ''),
            casilleros=item.get('casilleros', ''),
            observaciones=item.get('observaciones', '')
        )
        db.session.add(checklist)
        saved.append(checklist)

    db.session.commit()
    return jsonify({'saved': len(saved)}), 201


@app.route('/api/dashboard/stats')
def api_dashboard_stats():
    """Dashboard statistics."""
    days = request.args.get('days', 7, type=int)
    start_date = datetime.utcnow() - timedelta(days=days)

    # Checklists per day
    daily = db.session.query(
        cast(Checklist.created_at, Date).label('date'),
        func.count(Checklist.id).label('count')
    ).filter(
        Checklist.created_at >= start_date
    ).group_by(
        cast(Checklist.created_at, Date)
    ).order_by(
        cast(Checklist.created_at, Date)
    ).all()

    # Checklists per receptionist
    by_receptionist = db.session.query(
        Receptionist.name,
        func.count(Checklist.id).label('count')
    ).join(
        Checklist, Checklist.receptionist_id == Receptionist.id
    ).filter(
        Checklist.created_at >= start_date
    ).group_by(
        Receptionist.name
    ).order_by(
        func.count(Checklist.id).desc()
    ).all()

    # Issues summary (count of 'x' values across all fields)
    issue_fields = ['limpieza_general', 'limpieza_banos', 'insumos_basicos',
                    'iluminacion', 'agua', 'ventanas', 'cortinas',
                    'estufas', 'mobiliario', 'chapas']

    issues_data = {}
    field_labels = {
        'limpieza_general': 'Limpieza General',
        'limpieza_banos': 'Limpieza Baños',
        'insumos_basicos': 'Insumos Básicos',
        'iluminacion': 'Iluminación',
        'agua': 'Agua',
        'ventanas': 'Ventanas',
        'cortinas': 'Cortinas',
        'estufas': 'Estufas',
        'mobiliario': 'Mobiliario',
        'chapas': 'Chapas'
    }

    for field in issue_fields:
        count = Checklist.query.filter(
            Checklist.created_at >= start_date,
            getattr(Checklist, field) == 'x'
        ).count()
        issues_data[field_labels[field]] = count

    # Total stats
    total_checklists = Checklist.query.filter(
        Checklist.created_at >= start_date
    ).count()

    total_rooms = Room.query.count()
    rooms_checked = db.session.query(
        func.count(func.distinct(Checklist.room_id))
    ).filter(
        Checklist.created_at >= start_date
    ).scalar()

    # By building
    by_building = db.session.query(
        Room.building,
        func.count(Checklist.id).label('count')
    ).join(
        Checklist, Checklist.room_id == Room.id
    ).filter(
        Checklist.created_at >= start_date
    ).group_by(
        Room.building
    ).order_by(
        Room.building
    ).all()

    return jsonify({
        'daily': [{'date': str(d.date), 'count': d.count} for d in daily],
        'by_receptionist': [{'name': r.name, 'count': r.count} for r in by_receptionist],
        'issues': issues_data,
        'total_checklists': total_checklists,
        'total_rooms': total_rooms,
        'rooms_checked': rooms_checked or 0,
        'by_building': [{'building': b.building, 'count': b.count} for b in by_building]
    })


@app.route('/api/history')
def api_history():
    """Get checklist history with filters."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    building = request.args.get('building', '')
    receptionist_id = request.args.get('receptionist_id', type=int)
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')

    query = Checklist.query.join(Room).join(Receptionist)

    if building:
        query = query.filter(Room.building == building)
    if receptionist_id:
        query = query.filter(Checklist.receptionist_id == receptionist_id)
    if date_from:
        query = query.filter(Checklist.created_at >= datetime.strptime(date_from, '%Y-%m-%d'))
    if date_to:
        query = query.filter(Checklist.created_at <= datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1))

    total = query.count()
    checklists = query.order_by(Checklist.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()

    return jsonify({
        'items': [c.to_dict() for c in checklists],
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
