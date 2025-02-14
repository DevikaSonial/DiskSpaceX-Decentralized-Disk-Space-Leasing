

from flask import *
from public import public
from admin import admin
from user import users

app=Flask(__name__)

app.secret_key="sdfgh"


app.register_blueprint(public)
app.register_blueprint(admin)
app.register_blueprint(users)


app.run(debug=True,port=5011)


