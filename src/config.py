import os

class Config:

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    #SECRET_KEY = "SECRET_KEY"

    # db Lau
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Odisea123@localhost:3306/gran_data_test'
    
    # db Naza 
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3308/gran_data_test'
    