from datetime import datetime

from .app import db


def get_current_time():
    # This exists purely to be mocked in tests
    return datetime.utcnow().isoformat()


class Organization(db.Model):
    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    reports = db.relationship('Report')


class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    organization = db.relationship('Organization', back_populates='reports')
    reported = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    inventory = db.relationship('Item')

    def serialise(self):
        return {
            'id': self.id,
            'organization': self.organization.name,
            'reported': self.reported.isoformat(),
            'created': get_current_time(),  # We include the date this data exported
            'inventory': [item.serialise() for item in self.inventory]
        }


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'))
    report = db.relationship('Report', back_populates='inventory')
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer)

    def serialise(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
        }
