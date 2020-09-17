from faceRec import app
from faceRec.models import db

db.create_all()

app.run(host='0.0.0.0', debug=True)
