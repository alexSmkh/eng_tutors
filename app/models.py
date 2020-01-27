from app import db


teachers_goals_association = db.Table(
    'teachers_goals',
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id')),
    db.Column('goal_id', db.Integer, db.ForeignKey('goals.id')),
)


class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    requests = db.relationship('Request', back_populates='goal')
    teachers = db.relationship(
       'Teacher',
       secondary=teachers_goals_association,
       back_populates='goals'
    )


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), nullable=False)
    about = db.Column(db.String(2000), nullable=False)
    rating = db.Column(db.Float, default=0.0)
    picture = db.Column(db.String(1000))
    price = db.Column(db.Integer, nullable=False)
    schedule = db.Column(db.String(5000), nullable=False)
    bookings = db.relationship('Booking', back_populates='teacher')
    goals = db.relationship(
        'Goal',
        secondary=teachers_goals_association, 
        back_populates='teachers'
    )


class Booking(db.Model):
    __tablename__ = 'booking'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    weekday = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(6), nullable=False)
    teacher = db.relationship('Teacher', back_populates='bookings')
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))


class Request(db.Model):
    __tablename__ = 'request'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    goal = db.relationship('Goal', back_populates='requests')
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'))
    time = db.Column(db.String(6), nullable=False)
