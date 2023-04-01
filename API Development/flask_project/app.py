from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ta.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JWT_SECRET_KEY'] = 'jwt-secret-key'

db = SQLAlchemy(app)
jwt = JWTManager(app)

class TA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    native_english_speaker = db.Column(db.Boolean, nullable=False)
    course_instructor = db.Column(db.String(50), nullable=False)
    course = db.Column(db.String(50), nullable=False)
    semester = db.Column(db.String(10), nullable=False)
    class_size = db.Column(db.Integer, nullable=False)
    performance_score = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"TA(id={self.id}, native_english_speaker={self.native_english_speaker}, course_instructor='{self.course_instructor}', course='{self.course}', semester='{self.semester}', class_size={self.class_size}, performance_score={self.performance_score})"
    
    def to_dict(self):
        return {
            'id': self.id,
            'native_english_speaker': self.native_english_speaker,
            'course_instructor': self.course_instructor,
            'course': self.course,
            'semester': self.semester,
            'class_size': self.class_size,
            'performance_score': self.performance_score,
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}')"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', None)
    password = data.get('password', None)
    if not username:
        return jsonify({'message': 'Missing username parameter'}), 400
    if not password:
        return jsonify({'message': 'Missing password parameter'}), 400
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'message': 'Username already exists'}), 409
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', None)
    password = data.get('password', None)
    if not username:
        return jsonify({'message': 'Missing username parameter'}), 400
    if not password:
        return jsonify({'message': 'Missing password parameter'}), 400
    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return jsonify({'message': 'Invalid username or password'}), 401
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/api/tas', methods=['POST'])
@jwt_required()
def create_ta():
    ta = TA(**request.get_json())
    db.session.add(ta)
    db.session.commit()
    return jsonify({'message': 'TA created successfully'}), 201

@app.route('/api/tas/<int:id>', methods=['GET'])
@jwt_required()
def get_ta(id):
    ta = TA.query.get(id)
    if ta is None:
        return jsonify({'message': 'TA not found'}), 404
    return jsonify(ta.to_dict())

@app.route('/api/tas', methods=['GET'])
@jwt_required()
def get_tas():
    tas = TA.query.all()
    return jsonify([ta.to_dict() for ta in tas])

@app.route('/api/tas/<int:id>', methods=['PUT'])
@jwt_required()
def update_ta(id):
    ta = db.session.get(TA, id)
    if ta is None:
        return jsonify({'message': 'TA not found'}), 404
    ta.native_english_speaker = request.get_json().get('native_english_speaker')
    ta.course_instructor = request.get_json().get('course_instructor')
    ta.course = request.get_json().get('course')
    ta.semester = request.get_json().get('semester')
    ta.class_size = request.get_json().get('class_size')
    ta.performance_score = request.get_json().get('performance_score')
    db.session.commit()
    return jsonify({'message': 'TA updated successfully'})

@jwt_required()
def delete_ta(id):
    ta = TA.query.get(id)
    if ta is None:
        return jsonify({'message': 'TA not found'}), 404
    db.session.delete(ta)
    db.session.commit()
    return jsonify({'message': 'TA deleted successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
