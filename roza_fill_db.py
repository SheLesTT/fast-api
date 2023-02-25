from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import sessionmaker
from roza_classes import Slope, Client, Instructor, Rent, SnowStructure,Lift,\
    LiftSlope, SkiPass,  SkiPassSlope, Rent, ClientRent, ClientInstructor, ClientBuySkiPass
from faker_classes import InstructorType, SlopeAtr, LiftAtr, SkiPassAtr, RentAtr
from faker import Faker
import random
from datetime import  datetime, timedelta
import numpy as np

f = Faker(["ru_RU"])
f.add_provider(InstructorType)
f.add_provider(SlopeAtr)
f.add_provider(LiftAtr)
f.add_provider(SkiPassAtr)
f.add_provider(RentAtr)

db_config_local_bind = {
    'user': 'postgres',  # имя пользователя
    'pwd': 'F_7d3fd73',  # пароль
    'host': 'localhost',
    'port': 5432,  # порт подключения
    'db': 'postgres',  # название базы данных
}
conn_addr = 'postgresql://{}:{}@{}:{}/{}'.format(
    db_config_local_bind['user'],
    db_config_local_bind['pwd'],
    db_config_local_bind['host'],
    db_config_local_bind['port'],
    db_config_local_bind['db']
)
print("[SQL] Trying to connect to " + conn_addr)
engine = create_engine(conn_addr, pool_recycle=280,  echo=True)
print('[SQL] Connexion established on ' + conn_addr)

session = sessionmaker(bind=engine)


# Fill instructor database
def fill_instructors():
    s = session()
    for inst in range(50):
        a = Instructor(in_first_name=f.first_name(),in_last_name=f.last_name(),
                       in_price= np.random.randint(800,2000), in_type=f.instructor_type(),
                        in_description = f.text(),
                       in_phone = f.phone_number())

        s.add(a)
    s.commit()

# Fill user database
def fill_user():
    s =session()
    for user in range(1000):

        a = Client(cl_first_name =f.first_name(), cl_second_name = f.last_name(),
                cl_birthday_date =  f.date_between_dates(date_start = datetime(1950,1,1), date_end = datetime(2010,1,1)),
                 cl_phone =f.phone_number(), cl_email = f.email())
        s.add(a)
    s.commit()

# Fill Slope
def fill_slope():
    s = session()
    for slope in range(30):
        a = Slope(sl_length = np.random.randint(1000, 5000),
                  difficulty = f.slope_difficulty(),
                  title=f.sentence(nb_words=1)[:-1],
                  height_difference= np.random.randint(100,1500),
                  artificial_snow = random.choice([True,False]),
                  description = f.text(), open =random.choice([True,False]))

        s.add(a)
    s.commit()

#Fill lifts
def fill_lifts():
    s = session()
    for lift in range(10):
        a = Lift(title=f.sentence(nb_words=1)[:-1],
                     lif_length = np.random.randint(1000,10000),
                    lif_open_time = f.lift_open_time(),
                     lif_close_time = f.lift_close_time())
        s.add(a)
    s.commit()

# Fill SkiPass
def fill_ski_pass():
    s = session()
    for skipass in range(10):
        pass_type = random.choice(["period", "passes"])
        if pass_type == "period":
             pass_period = f.ski_pass_period()
             passes = None
        else:
            pass_period = None
            passes = f.ski_pass_passes()

        gen_price = random.randint(1000,50000)
        a = SkiPass(type=pass_type, title=f.sentence(nb_words=1)[:-1],
                    period=pass_period,
                     number_of_passes = passes, beneficiaries=f.text(),
                     beneficiary_price = gen_price/2,
                     price = gen_price)
        s.add(a)
    s.commit()

#Fill Rent
def fill_rent():
    s =session()

    for rent in range(1000):
        a = Rent(rent_type = f.rent_type(),
                 rent_status = f.rent_status(),
                 rent_price = np.random.randint(100,1000))
        s.add(a)
    s.commit()
# Fill lift slope

def fill_lift_slope():
    s = session()

    slope_ids = []
    for slope in s.query(Slope):
        slope_ids.append(slope.slope_id)

    for lift in s.query(Lift):
        con_slopes = np.random.randint(1,5)
        for i in range(con_slopes):
            sl_id = random.choice(slope_ids)
            slope = s.query(Slope).filter(Slope.slope_id == sl_id).first()
            a = LiftSlope(lift_id = lift.lift_id, slope_id = sl_id)
            s.add(a)

    s.commit()

# FIll ski pass slape
def fill_ski_pass_slope():
    s = session()

    slope_ids = []
    for slope in s.query(Slope):
        slope_ids.append(slope.slope_id)

    for ski_pass in s.query(SkiPass):
        pas_slopes = random.choice([5,len(slope_ids)])
        if pas_slopes == 5:
            for i in range(pas_slopes):

                sl_id = random.choice(slope_ids)
                slope = s.query(Slope).filter(Slope.slope_id == sl_id).first()
                a = SkiPassSlope(ski_pass_id = ski_pass.ski_pass_id, slope_id = sl_id)
                s.add(a)
        else:
            for sl_id in slope_ids:
                slope = s.query(Slope).filter(Slope.slope_id == sl_id).first()
                a = SkiPassSlope(ski_pass_id = ski_pass.ski_pass_id, slope_id = sl_id)
                s.add(a)

    s.commit()
# Fill client instructor
def fill_client_instructor():
    s = session()

    instructor_ids = []
    for instructor in s.query(Instructor):
        instructor_ids.append(instructor.instructor_id)

    client_ids = []
    for client in s.query(Client):
        client_ids.append(client.client_id)

    for client in random.choices(client_ids, k = round(len(client_ids)/5)):
        amount_inst = np.random.randint(1,10)

        for i in range(amount_inst):
            inst_id = random.choice(instructor_ids)
            time =f.date_time_this_decade()
            a = ClientInstructor(client_id = client, instructor_id = inst_id,
                                 start_rent = time, end_rent = time + timedelta(hours = 2))
            s.add(a)

    s.commit()

# Fill client_rent
def fill_client_rent():
    s = session()

    rent_ids = []
    for rent in s.query(Rent):
        rent_ids.append(rent.rent_id)
    print(len(rent_ids))
    client_ids = []
    for client in s.query(Client):
        client_ids.append(client.client_id)
    print(len(client_ids))
    for client in random.choices(client_ids, k = round(len(client_ids)/4)):
        amount_inst = np.random.randint(1,8)

        for i in range(amount_inst):
            rent_id = random.choice(rent_ids)
            time =f.date_time_this_decade()
            a = ClientRent(client_id = client, rent_id = rent_id,
                                 start_rent = time, end_rent = time + timedelta(hours = 2),
                                 us_r_damage = random.choice([True,False]),
                                 back_in_time = random.choice([True,False]))
            s.add(a)
    s.commit()

# Fill user ski pass
def fill_client_ski_pass():
    s = session()

    ski_pass_ids = []
    for ski_pass in s.query(SkiPass):
        ski_pass_ids.append(ski_pass.ski_pass_id)

    client_ids = []
    for client in s.query(Client):
        client_ids.append(client.client_id)

    for client in client_ids:
        amount_inst = np.random.randint(1,3)

        for i in range(amount_inst):
            pass_id = random.choice(ski_pass_ids)
            time =f.date_time_this_decade()
            a = ClientBuySkiPass(client_id = client, ski_pass_id = pass_id,
                                 buy_date = f.date_time_this_decade())

            s.add(a)
    s.commit()

# Fill snow structure:
def fill_snow_structure():
    s = session()
    slope_ids = []
    for slope in s.query(Slope):
        slope_ids.append(slope.slope_id)

    for slope in slope_ids:
        for i in range(365):
            data = datetime(2021,1,1,1,1,1)
            a = SnowStructure(slope_id = slope, description = f.text(),
                              temperature = np.random.randint(-25,0),
                              sn_st_data = data + timedelta(days=i))
            s.add(a)
    s.commit()


#-------------------------------------------------------------------

# HERE MAGIC BEGINS

# fill_lifts()
# fill_user()
# fill_rent()
# fill_slope()
# fill_instructors()
fill_ski_pass()
# fill_snow_structure()
# fill_client_instructor()
# fill_client_rent()
# fill_lift_slope()
fill_ski_pass_slope()
fill_client_ski_pass()


#-------------------------------------------------------------------------

# BLACK MAGIC BEGINS HERE
s = session()

# SnowStructure.__table__.drop(engine)
# ClientRent.__table__.drop(engine)
# ClientInstructor.__table__.drop(engine)
# LiftSlope.__table__.drop(engine)
# SkiPassSlope.__table__.drop(engine)
# ClientBuySkiPass.__table__.drop(engine)

# Test.__table__.drop(engine)
# Client.__table__.drop(engine)
# Rent.__table__.drop(engine)
# SkiPass.__table__.drop(engine)
# Lift.__table__.drop(engine)
# Slope.__table__.drop(engine)
# Instructor.__table__.drop(engine)


s.commit()