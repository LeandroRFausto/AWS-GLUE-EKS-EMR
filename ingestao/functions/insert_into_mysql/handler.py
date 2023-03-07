import os
import sys
import pymysql
from faker import Faker
from datetime import datetime
from faker_credit_score import CreditScore
from faker_music import MusicProvider

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_INSTANCE_ADDRESS")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")

try:
    conn = pymysql.connect(host=host, user=username, passwd=password, db=database, connect_timeout=5)
except pymysql.MySQLError as e:
    sys.exit()

def populate_mysql(event, context):

    faker = Faker()
    faker.add_provider(CreditScore)
    faker.add_provider(MusicProvider)

    with conn.cursor() as cur:
        cur.execute("""
         CREATE TABLE IF NOT EXISTS `customers` (
        `id` int NOT NULL AUTO_INCREMENT,
        `nome` text,
        `sexo` text,
        `endereco` text,
        `telefone` text,
        `email` text,
        `foto` text,
        `nascimento` date DEFAULT NULL,
        `profissao` text,
        `dt_update` timestamp NULL DEFAULT NULL,
        PRIMARY KEY (`id`)
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS `credit_score` (
        `id` int NOT NULL AUTO_INCREMENT,
        `customer_id` int NOT NULL,
        `nome` text,
        `provedor` text,
        `credit_score` text,
        `dt_update` timestamp NULL DEFAULT NULL,
        PRIMARY KEY (`id`)
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS `music` (
        `id` int NOT NULL AUTO_INCREMENT,
        `customer_id` int NOT NULL,
        `genero` text,
        `instrumento` text,
        `categoria` text,
        `dt_update` timestamp NULL DEFAULT NULL,
        PRIMARY KEY (`id`)
        )
        """)

        for i in range(10000):
            nome         = faker.name()
            customer_id  = faker.random_int()
            sexo         = faker.lexify(text='?', letters='MF')
            endereco     = faker.address() 
            telefone     = faker.phone_number() 
            email        = faker.safe_email() 
            foto         = faker.image_url() 
            nascimento   = faker.date_of_birth() 
            profissao    = faker.job() 
            provedor     = faker.credit_score_provider() 
            credit_score = faker.credit_score()
            genero       = faker.music_genre()
            instrumento  = faker.music_instrument()
            categoria    = faker.music_instrument_category()
            dt_update    = datetime.now() 

            customers_query = f"insert into customers ( nome, sexo, endereco, telefone, email, foto, nascimento, profissao, dt_update) values('{nome}', '{sexo}', '{endereco}', '{telefone}', '{email}', '{foto}', '{nascimento}', '{profissao}', '{dt_update}')"
            credit_query = f"insert into credit_score ( customer_id, nome, provedor, credit_score, dt_update) values('{customer_id}', '{nome}', '{provedor}', '{credit_score}', '{dt_update}')"
            music_query = f"insert into music ( customer_id, genero, instrumento, categoria, dt_update) values('{customer_id}', '{genero}', '{instrumento}', '{categoria}', '{dt_update}')"
            try:
                cur.execute(customers_query)
                conn.commit()
            except:
                print(f"Error writing customer row with the following values('{nome}', '{sexo}', '{endereco}', '{telefone}', '{email}', '{foto}', '{nascimento}', '{profissao}', '{dt_update}')")

            try:
                cur.execute(credit_query)
                conn.commit()
            except:
                print(f"Error writing credit row with the following values('{customer_id}', '{nome}', '{provedor}', '{credit_score}', '{dt_update}')")

            try:
                cur.execute(music_query)
                conn.commit()
            except:
                print(f"Error writing music row with the following values('{customer_id}', '{genero}', '{instrumento}', '{categoria}', '{dt_update}')")    
    return "Finished creating Databases and writing rows"
