from setup.adapters import task_queue


def test_queue_task(mocker):
    from fakeredis import FakeStrictRedis
    from rq import Queue

    task_queue.CdcQueue.queue = Queue(is_async=False, connection=FakeStrictRedis())

    def test_fuct(name: str):
        return f"hola {n}"

    job = task_queue.CdcQueue.enqueue(test_fuct, ("Pedro",))
    task_queue.CdcQueue.retrieve_result(job.id)
    assert job
