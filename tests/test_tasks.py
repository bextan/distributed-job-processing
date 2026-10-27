from app.workers.tasks import process_data_task, send_notification_task


def test_process_data_task_eager():
    res = process_data_task.apply(args=[{"records": 25}]).get()
    assert res["status"] == "COMPLETED"
    assert res["processed_records"] == 50


def test_send_notification_task_eager():
    res = send_notification_task.apply(args=[{"recipient": "admin@test.org"}]).get()
    assert res["status"] == "SENT"
    assert res["recipient"] == "admin@test.org"
