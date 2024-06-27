import luigi
import splunklib.client as splunk_client
import splunklib.results as splunk_results
from pymongo import MongoClient
import json
import time
import os
import logging.config
import configparser
from datetime import datetime

c_date = datetime.now().date()
time_for = datetime.now().strftime("%H%M%S")

configuration = configparser.ConfigParser()
configuration.read('/Users/muthamizh/PycharmProjects/datapipeline/config/config.ini')
script_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(script_dir, "logging.ini")
logging.config.fileConfig(log_path)

logger = logging.getLogger('luigi-interface')

class ExtractSplunkData(luigi.Task):
    splunk_host = luigi.Parameter()
    splunk_port = luigi.IntParameter()
    splunk_username = luigi.Parameter()
    splunk_password = luigi.Parameter()
    splunk_query = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(f"splunk_logs/splunk_data_fined_{time_for}.json")

    def run(self):
        try:
            logger.info("Connecting to Splunk")
            service = splunk_client.connect(
                host=self.splunk_host,
                port=self.splunk_port,
                username=self.splunk_username,
                password=self.splunk_password
            )

            logger.info("Running Splunk query")

            job = service.jobs.create(self.splunk_query)

            logger.info("Waiting for job to complete")
            while not job.is_done():
                logger.debug("Job not done yet, waiting...")
                time.sleep(1)

            logger.info("Retrieving results")
            results = job.results()
            data = splunk_results.ResultsReader(results)

            logger.info("Writing results to JSON file")
            with self.output().open("w") as f:
                json.dump([event for event in data], f, indent=4)

            logger.info("Successfully wrote results to JSON file")

        except Exception as e:
            logger.error(f"Failed to extract data from Splunk: {e}")

    def complete(self):
        return os.path.exists(self.output().path) and os.path.getsize(self.output().path) > 0


class LoadDataToMongoDB(luigi.Task):
    mongodb_host = luigi.Parameter()
    mongodb_port = luigi.IntParameter()
    mongodb_db = luigi.Parameter()
    mongodb_collection = luigi.Parameter()
    json_file = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(self.json_file)

    def run(self):
        logger.info("Connecting to MongoDB")
        client = MongoClient(self.mongodb_host, self.mongodb_port)
        db = client[self.mongodb_db]
        collection = db[self.mongodb_collection]

        logger.info("Reading data from JSON file")
        try:
            with open(self.json_file, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON: {e}")
            return

        if not data:
            logger.warning("No data to insert into MongoDB")
            return

        logger.info("Inserting data into MongoDB")
        collection.insert_many(data)

    def complete(self):
        return False  # Ensure this task runs every time


if __name__ == "__main__":
    luigi.run()
