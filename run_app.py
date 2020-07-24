#from caw_app import app
from caw_app import create_app, db ### run __init_.py file to load global variables

#### User Models ### Only User model isbeing loaded for test purpose
from caw_app.models import User

app = create_app()

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000, debug=True)