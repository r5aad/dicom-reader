# from database import Base, db_session, engine
# from models import User


# def init_db():

#     Base.metadata.create_all(bind=engine)

#     db_session.add(
#         User(username="testuser", password_hash=b"", password_salt=b"", balance=1)
#     )
#     db_session.commit()

#     print("Initialized the db")