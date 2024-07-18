from datetime import datetime
import hashlib
import json

class Block():
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.create_hash()
    
    def create_hash(self):
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
        new_block.hash = new_block.create_hash()
        self.chain.append(new_block)


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