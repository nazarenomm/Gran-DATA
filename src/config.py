class Config:

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    #SECRET_KEY = "SECRET_KEY"

    # db Lau
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Odisea123@mysql-db:3307/gran_data_test'

    # db Naza 
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3308/gran_data_test'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@mysql-db:3306/gran_data_test'

    
    JWT_SECRET_KEY='bfd4832efa2bf3c934497cd9'