import pytest
from task_manager import add_task, complete_task, delete_task, load_tasks, DATA_FILE


@pytest.fixture(autouse=True)
def clean_env():
    """测试夹具（Fixture）：在每个测试运行前和运行后，自动清空测试用的 json 文件，保证测试环境干净"""
    if DATA_FILE.exists():
        DATA_FILE.unlink()
    yield
    if DATA_FILE.exists():
        DATA_FILE.unlink()


def test_add_task():
    """测试添加任务功能"""
    tasks = add_task("学习 Python")
    assert len(tasks) == 1
    assert tasks[0]["title"] == "学习 Python"
    assert tasks[0]["completed"] is False


def test_complete_task():
    """测试完成任务功能"""
    add_task("写作业")
    success = complete_task(1)
    assert success is True

    tasks = load_tasks()
    assert tasks[0]["completed"] is True


def test_delete_task():
    """测试删除任务并自动重排 ID 的功能"""
    add_task("任务1")
    add_task("任务2")

    success = delete_task(1)
    assert success is True

    tasks = load_tasks()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "任务2"
    assert tasks[0]["id"] == 1  # 验证 ID 是否成功重置为 1