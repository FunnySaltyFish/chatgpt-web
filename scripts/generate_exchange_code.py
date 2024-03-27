# cardno.string(),amount.int32(),redeemed.int32()

# 生成兑换码，并插入到 mongoimport --host=127.0.0.1 --port=27017 --username=xxxxx --password=xxxxx --authenticationDatabase=chatgpt --db=chatgpt --collection=giftcards --file=/home/ubuntu/giftcards/chatgpt-web-giftcards-20240213.csv --type=csv --columnsHaveTypes --fields="cardno.string(),amount.int32(),redeemed.int32()" --headerline  --ignoreBlanks 

from dotenv import load_dotenv
import os
import random
import pymongo
from pyparsing import Dict

load_dotenv("./service/.env")

MONGO_DB_URL = os.getenv("MONGODB_URL")

print("MONGO_DB_URL:", MONGO_DB_URL)

client = pymongo.MongoClient(MONGO_DB_URL)
db = client.chatgpt
collection = db.giftcards

collection.create_index("cardno", unique=True)

def random_code():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))


def generate_codes(amount: int = 10, count: int = 10):
    results = {}
    i = 0
    # 优化一下，改成返回插入语句
    while i < count:
        code = random_code()
        if code in results:
            continue
        results[code] = amount
        i += 1
    return results

def codes_to_insert_stat(codes: Dict):
    result = []
    for key, value in codes.items():
        result.append({"cardno": key, "amount": value, "redeemed": 0})
    return result

if __name__ == "__main__":
    n = int(input("请输入生成兑换码数量："))
    amount = int(input("请输入兑换码对应天速："))

    codes = generate_codes(amount, n)
    stat = codes_to_insert_stat(codes)
    # print(stat)

    insert_res = collection.insert_many(stat)
    print("Inserted:", len(insert_res.inserted_ids), "items.")
    print("\n".join(codes.keys()))
    print("兑换码已生成，请在数据库中查看。对应天数为", amount, "天。")



