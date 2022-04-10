import time
import random
import time
import uuid

from opentelemetry import metrics
from opentelemetry.exporter.prometheus_remote_write import (
    PrometheusRemoteWriteMetricsExporter,
)
from opentelemetry.sdk.metrics import MeterProvider

# configure the Logz.io listener endpoint and Prometheus metrics account token
exporter = PrometheusRemoteWriteMetricsExporter(
    endpoint="https://listener.logz.io:8053",
    headers={
        "Authorization": "Bearer XXXX",
    }
)

push_interval = 1

metrics.set_meter_provider(MeterProvider())
meter = metrics.get_meter(__name__)
metrics.get_meter_provider().start_pipeline(meter, exporter, push_interval)

steps_names = ["DPModeling", "Alignment", "PopulateDB"]
clusters = ["swarm-test"]
maps_names = ["Europe"]
jobs_status = ["FAILED", "SUCCESS", "SUCCESS_UPON_RETRY"]
# provide the first data point

cores_number_ctr = meter.create_counter(
    name="step_exec_time_ctr",
    description="size of requests",
    unit="1",
    value_type=int,
)

jobs_status_ctr = meter.create_counter(
    name="job_status_ctr",
    description="size of requests",
    unit="1",
    value_type=int,
)

values_map = dict()

while True:
    job_id = str(uuid.uuid1())
    map_name = random.choice(maps_names)
    cluster = random.choice(clusters)
    # add labels
    jobs_status_labels = {
        "job_status": "STARTED",
        "env_name": cluster,
        "map": map_name,
        "job_id": job_id,
    }
    jobs_status_ctr.add(0, jobs_status_labels)
    total_steps_duration = 0
    last_step = None
    for step in steps_names:
        last_step = step
        for i in range(1,2):
            labels = {
                "env_name": cluster,
                "map": map_name,
                "job_id": job_id,
                "step_name": step
            }


            def populate_dict():
                print("labels: " + str(labels))


            populate_dict()
            cores_number_ctr.add(30, labels)
            total_steps_duration += 30
            print("sleeping...")

            time.sleep(30)
    jobs_status = random.choice(jobs_status)
    jobs_status_labels = {
        "job_status": jobs_status,
        "env_name": cluster,
        "map": map_name,
        "job_id": job_id,
    }
    print("jobs_status_labels: " + str(jobs_status_labels))
    jobs_status_ctr.add(total_steps_duration,jobs_status_labels)
