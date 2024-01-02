
def build_job_payload(
    event_type: str,
    source: str,
    response_body: dict,
    response_tube: str = None,
    job_id: str = None,
    response_status: str = None,
):
    return {
        "eventType": event_type,
        "source": source,
        "version": 0,
        "job_id": job_id,
        "response_tube": response_tube,
        "response_status": response_status,
        "body": response_body
    }
