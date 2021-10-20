import asyncio
import functools
import json
import os
import sys
import traceback
from time import sleep
from typing import Any, Dict

import boto3
from datasets.arrow_dataset import Dataset
from jetpack import job
from transformers.trainer_utils import TrainOutput
from transformers import (
    AutoModelForSequenceClassification,
    BertTokenizer,
    Trainer,
    TrainingArguments
)
from redis import StrictRedis, exceptions as rexc

# Turn off buffering for print statement
print = functools.partial(print, flush=True)

TEST_BUCKET = 'lago-test-bucket'

def redis_conn() -> StrictRedis:
    host = os.environ.get("REDIS_HOST")
    port = os.environ.get("REDIS_PORT")
    if host is None or port is None:
        raise ValueError("REDIS_HOST environment variable not set")
    return StrictRedis(host=host, port=int(port), password="secretpassword")


def download_model() -> bool:
    bucket = boto3.resource("s3").Bucket(TEST_BUCKET)
    os.makedirs("./model_tmp")
    bucket.download_file('config.json', './model_tmp/config.json')
    bucket.download_file('pytorch_model.bin', './model_tmp/pytorch_model.bin')
    return True


def upload_model() -> bool:
   bucket = boto3.resource("s3").Bucket(TEST_BUCKET)
   bucket.upload_file('./model_tmp/config.json', 'config.json')
   bucket.upload_file('./model_tmp/pytorch_model.bin', 'pytorch_model.bin')
   return True

@job
async def train_model(datadict: Dict[str, Any], model_name: str) -> Dict[str, float]:
    r = redis_conn()
    data = Dataset.from_dict(datadict)

    print("==Downloading Tokenizer==")
    tokenizer = BertTokenizer.from_pretrained(model_name)
    
    print("==Tokenizing Dataset==")
    tdataset: Dataset = data.map(
        lambda example: tokenizer(
            example["text"], truncation=True, padding='max_length'
        )
    )

    print("==Downloading and configuring model==")
    # model_bucket.download_folder("")
    download_model()
    model = AutoModelForSequenceClassification.from_pretrained('./model_tmp', num_labels=2)
    training_args = TrainingArguments("test_trainer", eval_accumulation_steps=2)
    
    print("==Training Now==")
    trainer: Trainer = Trainer(model=model, args=training_args, train_dataset=tdataset)
    result: TrainOutput = trainer.train()
    
    print("==Saving Trained Model==")
    r.set(model_name, json.dumps(result.metrics))
    model.save_pretrained('./model_tmp')
    upload_model()
    return result.metrics


async def main():
    conn = redis_conn()
    p = conn.pubsub(ignore_subscribe_messages=True)

    p.psubscribe('newReviews')

    while True:
        try:
            message = p.get_message()
            sleep(1)
        except (rexc.ConnectionError, rexc.TimeoutError):
            message = None
            print(f'Connection error:\n{traceback.format_exc()}')
            sleep(1)
        except Exception as e:
            message = None
            print(f'Unexpected error:\n{traceback.format_exc()}')
            sleep(1)

        if message == None:
            sleep(2)
            continue

        msg = json.loads(message['data'])
        print(f"Message Recieved {msg}")
        try:
            result = await train_model(datadict=msg, model_name="bert-base-uncased")
        except Exception as e:
            result = f"Unexpected error:\n{traceback.format_exc()}"
        print(result)
        sleep(1)

if __name__ == "__main__":
    asyncio.run(main())