class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Alish%40123@localhost/Intern'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    JWT_SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    JWT_TOKEN_LOCATION = ['headers'] 
    JWT_HEADER_NAME = 'Authorization'  
    JWT_HEADER_TYPE = 'Bearer' 
    JWT_ACCESS_TOKEN_EXPIRES = 3600 
    Debug = True