from datetime import datetime
from dbhelper import db

class SitInSession(db.Model):
    __tablename__ = 'sit_in_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    computer_number = db.Column(db.String(10), nullable=False)
    purpose = db.Column(db.String(100), nullable=False)
    lab = db.Column(db.String(10))
    notes = db.Column(db.Text)
    start_time = db.Column(db.DateTime, default=datetime.now)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')
    
    # Define relationship with User model
    user = db.relationship('User', backref=db.backref('sit_in_sessions', lazy=True))
    
    def __init__(self, user_id, computer_number, purpose, lab=None, notes=None):
        self.user_id = user_id
        self.computer_number = computer_number
        self.purpose = purpose
        self.lab = lab
        self.notes = notes
        self.start_time = datetime.now()
        self.status = 'active'
    
    def end_session(self):
        """End the current sit-in session"""
        self.end_time = datetime.now()
        self.status = 'completed'
        return self
    
    def cancel_session(self):
        """Cancel this sit-in session"""
        self.status = 'cancelled'
        
    @staticmethod
    def get_session_by_id(session_id):
        """Get a sit-in session by ID"""
        return SitInSession.query.get(session_id)
    
    @staticmethod
    def get_active_sessions():
        """Get all active sit-in sessions"""
        return SitInSession.query.filter_by(status='active').order_by(SitInSession.start_time.desc()).all()
    
    @staticmethod
    def get_user_sessions(user_id):
        """Get all sit-in sessions for a specific user"""
        return SitInSession.query.filter_by(user_id=user_id).order_by(SitInSession.start_time.desc()).all()
    
    @staticmethod
    def get_active_sessions_count():
        """Get the count of active sit-in sessions"""
        return SitInSession.query.filter_by(status='active').count()
    
    @staticmethod
    def get_today_sessions():
        """Get all sit-in sessions for today"""
        today = datetime.now().date()
        return SitInSession.query.filter(
            db.func.date(SitInSession.start_time) == today
        ).order_by(SitInSession.start_time.desc()).all()
    
    @staticmethod
    def user_has_active_session(user_id):
        """Check if a user has any active sessions"""
        return SitInSession.query.filter_by(user_id=user_id, status='active').first() is not None
