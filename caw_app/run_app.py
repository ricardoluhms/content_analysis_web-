from web import app

#### Config Modules
from web.config import Config_KEY, Config_DB
import os
#### User Models
from web.models import User

#### Start Config
app.config['SECRET_KEY']='060590Woofie'
app.config.from_object(Config_KEY)



if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000, debug=True)