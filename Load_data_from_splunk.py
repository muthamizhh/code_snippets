import splunklib.client as splunk_client

def extract_data_from_splunk(splunk_host, splunk_port, splunk_username, splunk_password, splunk_query):
    try:
        service = splunk_client.connect(
            host=splunk_host,
            port=splunk_port,
            username=splunk_username,
            password=splunk_password
        )

        job = service.jobs.create(splunk_query)
        while not job.is_done():
            pass  # Simulate waiting for job completion

        results = job.results()
        data = [event for event in results]
        
        return data

    except Exception as e:
        print(f"Failed to extract data from Splunk: {e}")
        return None
