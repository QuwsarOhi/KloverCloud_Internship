# Implemented using SQLalchemy

import sqlalchemy as sqla
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import date, timedelta

# Database ORM definition
Base = declarative_base()


class SellData(Base):
    """
        Table Name: selldata
        Columns:
            sell_id          = A unique token for each sell operation (primary key).
                               This was not defined in the question. However, adding this column is reasonable,
                               as every table requires a primary key.
                               DataType: VarChar(10).

            item_id          = The kacchi_id that was defined as "id" in the question.
                               This parameter has direct relation with "Kacchi" table.
                               Hence, adding ForeignKey relation is reasonable.
                               DataType: VarChar(10).

            number_of_plates = Defines the number of plates for each sell operation/batch.
                               DataType: Integer.

            total_price      = Defines the total price for each sell operation/batch.
                               DataType: Integer (this should be non-zero, but haven't implemented).

            date_time        = A DateTime column containing date and time of the sell operation/batch.
                               DataType: DateTime

        Relations:
            A foreign key relation with kacchi table. "item_id" is the ForeignKey of "id" in "Kacchi" table.

        Primary-Key:
            sell_id
    """
    __tablename__ = "selldata"

    sell_id = sqla.Column(sqla.String(length=10), primary_key=True)
    item_id = sqla.Column(sqla.String(length=10), sqla.ForeignKey("kacchi.id"))
    number_of_plates = sqla.Column(sqla.Integer)
    total_price = sqla.Column(sqla.Float)
    date_time = sqla.Column(sqla.DateTime)
    kacchi = relationship("Kacchi")

    def __repr__(self):
        return f"SID:{self.sell_id}, ID:{self.item_id} NOP:{self.number_of_plates}," + \
               f"Price:{self.total_price}, Time:{self.date_time}"


class Kacchi(Base):
    """
        Table Name: kacchi
        Columns:
            id          = A unique token for each type of kacchi (primary key).
                          DataType: VarChar(10).

            name        = Name of kacchi.
                          DataType: VarChar(20) (This should be unique. But haven't implemented).

            price       = Price per plate.
                          DaraType: Float.

        Relations:
            A foreign key relation with kacchi table. "item_id" is the ForeignKey of "id" in "Kacchi" table.

        Primary-Key:
            sell_id
    """
    __tablename__ = "kacchi"

    id = sqla.Column(sqla.String(length=10), primary_key=True)
    name = sqla.Column(sqla.String(length=20))
    price = sqla.Column(sqla.Float())

    sells = relationship("SellData")

    def __repr__(self):
        return f"ID:{self.id}, Name:{self.name}, Price:{self.price}"


# --------------- Implementing CRUD (in "Kacchi" table) ---------------

# Creating new data in the table
def createKacchi(n=4):
    for i in range(n):
        kacchi = Kacchi(id=str(i + 1), name=f"kacchi_{i}", price=(i + 1) * 100)
        session.add(kacchi)
    session.commit()


# Prints kacchi items
def readKacchi():
    for row in session.query(Kacchi).all():
        print(row)


# Update existing data in the table
def updateKacchi(kacchi_id, updated_price):
    if kacchi_id:
        session.query(Kacchi).filter(Kacchi.id == kacchi_id).update({"price": updated_price})
    else:
        print("No id provided")


# Delete rows from the sell
# delete less than or equal to a particular price
def deleteKacchis(price):
    session.query(Kacchi).filter(Kacchi.price > price).delete()
    session.commit()


# --------------- Implementing Create/Query (in "SellData" table) ---------------

# Create operation
def createSellData(n):
    for i in range(n):
        kacchi = session.query(Kacchi).get(str(i + 1))
        number_of_plates = i + i + 1
        total_price = kacchi.price * number_of_plates
        kacchi = SellData(sell_id=i + 1, number_of_plates=number_of_plates,
                          total_price=total_price, kacchi=kacchi,
                          date_time=date.today() - timedelta(days=i % 2))
        session.add(kacchi)
    session.commit()


# Query operation
def queryTodaySell():
    plates, sales = 0, 0
    for ret in session.query(SellData).filter(SellData.date_time == date.today()):
        plates += ret.number_of_plates
        sales += ret.total_price
    return plates, sales


if __name__ == '__main__':
    # Establish connection with mysql
    engine = sqla.create_engine("mysql://ohi:password@localhost/test", echo=False)

    # Table creation
    try:
        Kacchi.__table__.create(engine)
        SellData.__table__.create(engine)
    except:
        print('New table could not be created.')

    # Session binding for data manipulation
    Session = sessionmaker(bind=engine)
    session = Session()

    # CRUD operations on "Kacchi" table
    createKacchi(10)
    readKacchi()
    updateKacchi("7", "225")
    deleteKacchis(700)

    # Create, Query operation on "SellData" table
    createSellData(5)
    p, s = queryTodaySell()
    print()
    print(f"{p} plates were sold")
    print(f"Total sales amount : {s}")
