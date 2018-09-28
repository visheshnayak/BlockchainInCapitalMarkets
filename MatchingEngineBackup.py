import threading
import logging
import Blockchain
import socket
import sqlite3
import datetime
import json

orders = []
order_index = 0

'''
    configure the logger
'''
logging.basicConfig(filename='MatchingEngineLogs.log', level=logging.DEBUG)

'''
    function to save the data to DB
'''
def save_to_db(identity, price, quantity, saleType):
  global order_index
  order_index += 1

  print ('a')

  if saleType == 'B' :
    identity = 1001
  else :
    identity = 1002  

  #get the data from database
  order = {
    'index' : order_index,
    'id' : identity,
    'price' : price,
    'quantity' : quantity,
    'saleType' : saleType
  }

  #append to the collection of the orders
  orders.append(order)

  #clear order
  order = {}

'''
    function to match the requests
'''
def match_req():
  #matches the closest transaction
  if order_index % 2 == 0 :
    return True
  return False

'''
    function to read from the Blockchain and send it to the buyer
'''
def buyer_block():
    logging.info('Buyer block generation has started')

    block = blockchain.last_block

    bossHash = blockchain.hash(blockchain.chain[0])

    jsonblock = str(block)  + 'security_hash: ' +  str(bossHash)

    #write to buyer.json
    with open('buyer.json', 'w') as f:
      json.dump(jsonblock, f)

'''
    function to read from the blockChain and send it to the seller
'''
def seller_block():
    logging.info('Seller block generation has started.')

    block = blockchain.last_block

    bossHash = blockchain.hash(blockchain.chain[0])
    
    jsonblock = str(block) + 'security_hash: ' + str(bossHash)

    with open('seller.json', 'w') as f:
      json.dump(jsonblock, f)

'''
    Matching Engine starts from here
'''
logging.info('Matching Engine starts here.')

#create THE BLOCKCHAIN
blockchain = Blockchain.Blockchain()

# #assigning
# order_index = 0

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
        #get the data that is geing sent     
        data = conn.recv(2048)

        if not data:
            print('No data recieved, hence, skipping the iteration.')
  
            break

        #get the values of the data
        identity, price, quantity, saleType = data.decode('UTF-8').split(',')

        #put the order in the DB
        save_to_db(identity, price, quantity, saleType)

        #search for if any transaction requests get processed
        if match_req():
          #if some transactions do get completed, add into the main blockchain
          #create new transaction
          blockchain.new_transaction(1001, 1002, quantity, price)

          #add to block
          blockchain.new_block(blockchain.hash(blockchain.last_block))

          #to send the block of confirmation to buyer and seller
          #create new threads
          buyerThread = threading.Thread(target=buyer_block)
          sellerThread = threading.Thread(target=seller_block)

          buyerThread.start()
          sellerThread.start()

          buyerThread.join()
          sellerThread.join()

          with open ('MyBlockchain.json', 'w') as f:
            print(blockchain.chain)
            json.dump(blockchain.chain, f)
          conn.send(bytes('Offer added successfully', 'utf-8'))
          break
        
        else:
          conn.send(bytes('Offer added successfully', 'utf-8'))
          break

    