class IndividualProvider(db.Model):
    __tablename__ = 'individual_providers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    specialty = db.Column(db.String())
