from flask import Flask, jsonify
import random
import boto3
from upstash_redis import Redis
from datetime import datetime, timedelta
import json
import botocore
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

s3 = boto3.client(
    service_name="s3",
    endpoint_url=os.getenv("R2_ENDPOINT_URL"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name="auto"
)

redis = Redis(
    url=os.getenv("REDIS_ENDPOINT_URL"),
    token=os.getenv("REDIS_TOKEN")
)

synchro_words = [
    "cobalt", "swift", "nebula", "phantom", "sonic", 
    "crimson", "vortex", "pixel", "zenith", "lunar", 
    "amber", "mystic", "vector", "pulse", "glitch", 
    "frozen", "nomad", "cipher", "quartz", "echo", 
    "radiant", "rogue", "plasma", "static", "neon", 
    "silent", "titan", "matrix", "flux", "orbit", 
    "golden", "hunter", "carbon", "blaze", "prism", 
    "velvet", "shadow", "binary", "spark", "astral", 
    "silver", "viper", "omega", "cosmic", "fusion", 
    "bold", "knight", "logic", "storm", "turbo"
]

#Utility to create bucket on R2 and push metadata to redis
def create_synchro_bucket(bucket_id:str, expire_time:float):
    if type(bucket_id) is None:
        return jsonify({"message":"Invalid bucket id."})

    try:
        s3.create_bucket(
            Bucket=bucket_id,
        )

        s3.put_bucket_lifecycle_configuration(
            Bucket=bucket_id,
            LifecycleConfiguration={
                'Rules':[
                    {
                        'ID':'MediaAutoDelete',
                        'Status':'Enabled',
                        'Prefix': '',
                        'Expiration':{
                            'Days':1
                        }
                    }
                ]
            }
        )

        created_at = datetime.now()
        expires_on = created_at + timedelta(seconds=expire_time)
        metadata = {
            "created":created_at.isoformat(),
            "expires":expires_on.isoformat(),
            "gallery_id":bucket_id,
            "status":"active",
        }
        redis.setex(f"gallery:{bucket_id}", expire_time, json.dumps(metadata))
        return jsonify({"message":f"New bucket created:synchro-{bucket_id}", "pool_route":f"/pools/media/{bucket_id}"})
    except Exception as e:
        return jsonify({"message":"An error occured."})

def bucket_exists(bucket_id:str):
    try:
        s3.head_bucket(Bucket=bucket_id)
        return True
    except botocore.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            return False
        else:
            return False

def delete_entire_bucket(bucket_id:str):
    if bucket_exists(bucket_id):
        try:
            objects = s3.list_objects_v2(Bucket=bucket_id)
            if 'Contents' in objects:
                delete_keys = {'Objects': [{'Key':obj['Key']}] for obj in objects['Contents']}
                s3.delete_objects(
                    Bucket=bucket_id,
                    Delete=delete_keys,
                )
            s3.delete_bucket(Bucket=bucket_id)
            redis.delete(f"gallery:{bucket_id}")
            return jsonify({"message":f"Deleted bucket:{bucket_id}"})
        except Exception as e:
            return jsonify({"message":"An error occured."})
    else:
        return 404

#REMOVE AT PROD ***************************************************************
#TEST ROUTES
@app.route("/api/test", methods=["GET"])
def test_route():
    return jsonify({"message":"TEST PASSED FROM API."})

@app.route("/api/test/delete/<bucketId>", methods=["POST"])
def delete_all(bucketId):
    message = delete_entire_bucket(bucket_id=bucketId)
    return jsonify(message.json)
#KEEP AT PROD******************************************************************

@app.route("/api/create-bucket/media-pool", methods=["POST"])
def create_media_pool():
    pool_id = f"{random.choice(synchro_words)}-{random.choice(synchro_words)}-{random.choice(synchro_words)}"
    message = create_synchro_bucket(bucket_id=f"{pool_id}", expire_time=86400)

    return jsonify(message.json)

@app.route("/api/pools/media/<bucketId>", methods=["GET"])
def bucket_information(bucketId):
    try:
        metadata_raw = redis.get(f"gallery:{bucketId}")
        if metadata_raw is None:
            return jsonify({"message":"Pool not found or has expired."}), 400
        
        if isinstance(metadata_raw, str):
            metadata = json.loads(metadata_raw)
        else:
            metadata = metadata_raw

        return jsonify(metadata), 200
    except Exception as e:
        print(e)
        return jsonify({"message":"Unexpected error occured"}), 500

if __name__ == "__main__":
    app.run(port=5328, debug=True)