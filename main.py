from datetime import datetime
import hashlib
import json

class Block():
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        sha = hashlib.sha256()
        data_str = json.dumps(self.data, sort_keys=True)
        to_hash = str(self.index) + str(self.timestamp) + data_str + self.previous_hash
        sha.update(to_hash.encode('utf-8'))
        return sha.hexdigest()
    
class Blockchain():
    def __init__(self):
        self.chain = [self.create_genesis_block()]
    
    def create_genesis_block(self):
        return Block(0, datetime.now(), {"message": "This is the genesis block"}, "0")
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def check_chain_valid(self):
        for i in range(1, len(self.chain)):
            curr_block = self.chain[i]
            prev_block = self.chain[i-1]

            if curr_block.hash != curr_block.calculate_hash():
                return False
            if curr_block.previous_hash != prev_block.hash:
                return False

        return True


# Test creating blockchain and add some blocks
MyBlockchain = Blockchain()
MyBlockchain.add_block(Block(1, datetime.now(), {"message": "This is block 1"}, MyBlockchain.get_latest_block().hash))
MyBlockchain.add_block(Block(2, datetime.now(), {"message": "This is block 2"}, MyBlockchain.get_latest_block().hash))


for block in MyBlockchain.chain:
    print("index", block.index)
    print("timestamp", block.timestamp)
    print("data", block.data)
    print("prev hash", block.previous_hash)
    print("hash:", block.hash)


#check if chain is valid
print(MyBlockchain.check_chain_valid())
#try changing data 
MyBlockchain.chain[-1].data = {"message": "Hello world"}
MyBlockchain.chain[-1].hash = MyBlockchain.chain[-1].calculate_hash
print("data modified")
#check if chain is valid after changing block's data
print(MyBlockchain.check_chain_valid())
