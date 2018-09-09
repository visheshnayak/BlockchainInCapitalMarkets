import threading
import logging
import Blockchain
import socket
import sqlite3
import datetime
import json

tempTrans ={}

'''
    configure the logger
'''
logging.basicConfig(filename='MatchingEngineLogs.log', level=logging.DEBUG)

'''
    function to save the data to DB
'''
def save_to_db(data):
    #get the data from data
    dbconn = sqlite3.connect('test.db')

    dbconn.execute(
        """
            INSERT INTO POOL_OF_AWESOMENESS (
                BUYER_ID, FLAG, QUANTITY, PRICE, MOD_DATE_TIME
            )
            VALUES(
                {}, {}, {}, {}, {}
            )
        """.format(data['buyerId'] , data['sellerId'] , data['price'], data['quantity'], data['saletype'], str(datetime.datetime.now()))
    )
    cursor = dbconn.cursor()
    cursor.execute(
        """
            SELECT
                max(id)
            FROM
                POOL_OF_AWESOMENESS

        """.format(data['price'], data['quantity'])
    )
    saleType='buyerId'
    if(data['saletype'] == 'S'):
        saleType = 'sellerId'
    data[saleType] = cursor.fetchone()[0];

    dbconn.close

'''
    function to match the requests
'''
def match_req(data):
    dbconn = sqlite3.connect('test.db')
    cursor = dbconn.cursor()
    blockoffer
    if data['saletype'] == 'S' :
        cursor.execute(
            """
                SELECT
                    *
                FROM
                    POOL_OF_AWESOMENESS
                WHERE
                    price <= {}
                    AND quantity <= {}
                    AND status = 'P'
                ORDER BY
                    MOD_DATE_TIME
                LIMIT 1
                    """.format(data['price'], data['quantity'])
        )



    else:
        cursor.execute(
            """
                SELECT
                    *
                FROM
                    POOL_OF_AWESOMENESS
                WHERE
                    price >= {}
                    AND quantity <= {}
                    AND status = 'O'
                ORDER BY
                    MOD_DATE_TIME
                LIMIT 1
            """.format(data['price'], data['quantity'])
        )

    #if the cursor doesn't get any rows, then open transaction
    if cursor.rowcount == 0 :
        return False

    saleType = 'buyerId'

    if data['saletype'] == 'S' :
        saleType = 'sellerId'

    #Vishesh: should work
    data[saleType] = cursor.fetchone()[0];

    #if the cursor did get values, change the status of that specific row
    dbconn.execute(
        """
            UPDATE POOL_OF_AWESOMENESS
            SET
                Status = {}
            WHERE
                OID in ({},{})
        """.format('S', data['sellerId'], data['buyerId'])
    )

    dbconn.close()

'''
    function to read from the Blockchain and send it to the buyer
'''
def buyer_block():
    logging.info('Buyer block generation has started')

'''
    function to read from the blockChain and send it to the seller
'''
def seller_block():
    logging.info('Seller block generation has started.')

'''
    Matching Engine starts from here
'''
logging.info('Matching Engine starts here.')

#create THE BLOCKCHAIN
blockchain = Blockchain.Blockchain()

#define the IP addr and the ports
TCP_IP = '127.0.0.1'
TCP_PORT = 5005

#create the socket for data transfer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind the socket to the IP addr and thje port
s.bind((TCP_IP, TCP_PORT))

#listen to the port
s.listen(1)

while True:
    conn, addr = s.accept()

    print ('Recieved data from: {}'.format(addr))

    while True:
        data = conn.recv(BUFFER_SIZE)

        if not data:
            break;

        identity, price, quantity, saletype = data.decode('UTF-8').split(',')

        if identity == 'Trade' and tempTrans[price] == None :
            newVal = tempTrans[price]
            tempTrans.pop(price, None)

            data_string = json.dumps(newVal)
            data_loaded = json.loads(newVal)

            s.send(data_loaded)
        else :
            order = {
                'price' : price,
                'quantity' : quantity,
                'sellerId' : identity if saletype == 'S' else '',
                'buyerId' : identity if saletype == 'B' else '',
                'saleType' : saletype,
                'sellerOfferId' : '',
                'buyerOfferId' : ''
            }

            #put into database
            save_to_db(order)

            #match with the transactions
            if match_req(order):

                #add to the blockchain
                blockchain.new_transaction(data[buyerId], data[sellerId], data[quantity], data[price])

                blockchain.new_block(blockchain.hash(blockchain.last_block()))

                if order['saleType'] == 'S' :
                    tempTrans['buyerId'] = blockchain.last_block()
                else:
                    tempTrans['sellerId'] = blockchain.last_block()

                s.send(blockchain.last_block())

            else:
                s.send('Order Inserted Successfully')
