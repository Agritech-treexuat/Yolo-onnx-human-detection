from rtsp_processor import RTSPProcessor
from db_handler import MongoDBHandler
from dotenv import load_dotenv
import os

import hashlib
from datetime import datetime
import schedule
import time
from blockchain_handler import BlockchainHandler
from data_upload_blockchain_processer import DataProcessor

from web3 import Web3
from web3.auto import w3
from web3.middleware import geth_poa_middleware

load_dotenv()

def main():
    # Thay đổi thông tin kết nối MongoDB tùy thuộc vào cấu hình của bạn

    MONGO_USERNAME = os.getenv("MONGO_USERNAME")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
    MONGO_HOST = os.getenv("MONGO_HOST")
    MONGO_PORT = os.getenv("MONGO_PORT")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

    MONGO_URI = os.getenv("MONGO_URI")

    WASABI_ACCESS_KEY = os.getenv("WASABI_ACCESS_KEY")
    WASABI_SECRET_KEY = os.getenv("WASABI_SECRET_KEY")
    WASABI_REGION = os.getenv("WASABI_REGION")
    WASABI_ENDPOINT_URL = os.getenv("WASABI_ENDPOINT_URL")
    WASABI_BUCKET_NAME = os.getenv("WASABI_BUCKET_NAME")

    mongo_uri = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"
    if MONGO_URI:
        mongo_uri = MONGO_URI
    print(f"Connecting to MongoDB...")
    db_name = MONGO_DB_NAME
    frame_skip = 10

    mongo_uri = "mongodb://huy:12345678@localhost:27017"

    print(f"Mongo URI: {mongo_uri}")

    mongo_handler = MongoDBHandler(mongo_uri, db_name)

    # # 1. RTSP Processor
    # rtsp_processor = RTSPProcessor(frame_skip, mongo_uri, db_name, WASABI_ACCESS_KEY, WASABI_SECRET_KEY, WASABI_REGION, WASABI_ENDPOINT_URL, WASABI_BUCKET_NAME)
    # rtsp_processor.start_processing()

    # # 2. Capture and Upload Images
    # rtsp_processor.start_capture_and_upload_threads()

    # 3. Hash and upload to Blockchain
    # Khởi tạo provider của Ethereum (ví dụ: Infura)
    # provider = Web3(Web3.HTTPProvider('https://evmos-pokt.nodies.app'))

    # # Thêm middleware để xử lý vấn đề khi kết nối với mạng PoA (Proof of Authority)
    # provider.middleware_onion.inject(geth_poa_middleware, layer=0)

    # # Khởi tạo signer từ private key
    # wallet = provider.eth.account.privateKeyToAccount(os.getenv(WALLET_PRIVATE_KEY))

    # Kết nối với smart contract thông qua contract address và abi00000000
    contract_address = os.getenv("VIDEO_CONTRACT_ADDRESS")
    abi = [
        {
        "anonymous": False,
        "inputs": [
            {
            "indexed": True,
            "internalType": "uint256",
            "name": "cameraId",
            "type": "uint256"
            },
            {
            "indexed": True,
            "internalType": "address",
            "name": "owner",
            "type": "address"
            }
        ],
        "name": "CameraAdded",
        "type": "event"
        },
        {
        "inputs": [],
        "name": "addCamera",
        "outputs": [
            {
            "internalType": "uint256",
            "name": "",
            "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
        },
        {
        "inputs": [
            {
            "internalType": "uint256",
            "name": "cameraId",
            "type": "uint256"
            },
            {
            "internalType": "uint256",
            "name": "date",
            "type": "uint256"
            },
            {
            "internalType": "string",
            "name": "connectionLoss",
            "type": "string"
            },
            {
            "internalType": "uint256",
            "name": "totalLossPerDay",
            "type": "uint256"
            }
        ],
        "name": "addConnectionLoss",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
        },
        {
        "inputs": [
            {
            "internalType": "uint256",
            "name": "cameraId",
            "type": "uint256"
            },
            {
            "internalType": "string",
            "name": "videoHash",
            "type": "string"
            },
            {
            "internalType": "uint256",
            "name": "date",
            "type": "uint256"
            }
        ],
        "name": "addVideo",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
        },
        {
        "inputs": [],
        "name": "cameraCount",
        "outputs": [
            {
            "internalType": "uint256",
            "name": "",
            "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
        },
        {
        "inputs": [
            {
            "internalType": "uint256",
            "name": "",
            "type": "uint256"
            }
        ],
        "name": "cameras",
        "outputs": [
            {
            "internalType": "address",
            "name": "owner",
            "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
        },
        {
        "inputs": [
            {
            "internalType": "uint256",
            "name": "cameraId",
            "type": "uint256"
            }
        ],
        "name": "getCamera",
        "outputs": [
            {
            "internalType": "address",
            "name": "",
            "type": "address"
            },
            {
            "components": [
                {
                "internalType": "string",
                "name": "hash",
                "type": "string"
                },
                {
                "internalType": "uint256",
                "name": "date",
                "type": "uint256"
                }
            ],
            "internalType": "struct VideoHashContract.Video[]",
            "name": "",
            "type": "tuple[]"
            },
            {
            "components": [
                {
                "internalType": "uint256",
                "name": "date",
                "type": "uint256"
                },
                {
                "internalType": "string",
                "name": "connectionLoss",
                "type": "string"
                },
                {
                "internalType": "uint256",
                "name": "totalLossPerDay",
                "type": "uint256"
                }
            ],
            "internalType": "struct VideoHashContract.ConnectionLoss[]",
            "name": "",
            "type": "tuple[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
        },
        {
        "inputs": [
            {
            "internalType": "uint256",
            "name": "cameraId",
            "type": "uint256"
            }
        ],
        "name": "getConnectionLossByCamera",
        "outputs": [
            {
            "components": [
                {
                "internalType": "uint256",
                "name": "date",
                "type": "uint256"
                },
                {
                "internalType": "string",
                "name": "connectionLoss",
                "type": "string"
                },
                {
                "internalType": "uint256",
                "name": "totalLossPerDay",
                "type": "uint256"
                }
            ],
            "internalType": "struct VideoHashContract.ConnectionLoss[]",
            "name": "",
            "type": "tuple[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
        },
        {
        "inputs": [
            {
            "internalType": "uint256",
            "name": "cameraId",
            "type": "uint256"
            },
            {
            "internalType": "uint256",
            "name": "startTime",
            "type": "uint256"
            },
            {
            "internalType": "uint256",
            "name": "endTime",
            "type": "uint256"
            }
        ],
        "name": "getConnectionLossByDateRange",
        "outputs": [
            {
            "components": [
                {
                "internalType": "uint256",
                "name": "date",
                "type": "uint256"
                },
                {
                "internalType": "string",
                "name": "connectionLoss",
                "type": "string"
                },
                {
                "internalType": "uint256",
                "name": "totalLossPerDay",
                "type": "uint256"
                }
            ],
            "internalType": "struct VideoHashContract.ConnectionLoss[]",
            "name": "",
            "type": "tuple[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
        },
        {
        "inputs": [
            {
            "internalType": "uint256",
            "name": "cameraId",
            "type": "uint256"
            }
        ],
        "name": "getVideosByCamera",
        "outputs": [
            {
            "components": [
                {
                "internalType": "string",
                "name": "hash",
                "type": "string"
                },
                {
                "internalType": "uint256",
                "name": "date",
                "type": "uint256"
                }
            ],
            "internalType": "struct VideoHashContract.Video[]",
            "name": "",
            "type": "tuple[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
        },
        {
        "inputs": [
            {
            "internalType": "uint256",
            "name": "cameraId",
            "type": "uint256"
            },
            {
            "internalType": "uint256",
            "name": "startTime",
            "type": "uint256"
            },
            {
            "internalType": "uint256",
            "name": "endTime",
            "type": "uint256"
            }
        ],
        "name": "getVideosByDateRange",
        "outputs": [
            {
            "components": [
                {
                "internalType": "string",
                "name": "hash",
                "type": "string"
                },
                {
                "internalType": "uint256",
                "name": "date",
                "type": "uint256"
                }
            ],
            "internalType": "struct VideoHashContract.Video[]",
            "name": "",
            "type": "tuple[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
        }
    ]
    private_key = os.getenv("WALLET_PRIVATE_KEY")
    public_key = os.getenv("WALLET_PUBLIC_KEY")
    # contract_instance = provider.eth.contract(address=contract_address, abi=abi)
    provider_url = 'https://evmos-pokt.nodies.app'
    blockchain_handler = BlockchainHandler(contract_address, abi, public_key, private_key, provider_url)
    data_processor = DataProcessor(mongo_handler, blockchain_handler)

    print("Here")
    # Lập lịch cho công việc chạy vào 12h đêm mỗi ngày
    # schedule.every().day.at("18:25").do(data_processor.process_data_and_upload_to_blockchain)
    data_processor.process_data_and_upload_to_blockchain()

    # Vòng lặp chạy lập lịch
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
