import json
import logging
from pathlib import Path

# 1. 配置日志：设定记录等级为 INFO，并定义统一的输出格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 2. 使用 pathlib 定义任务数据保存的 JSON 文件路径
DATA_FILE = Path("tasks.json")


def load_tasks() -> list:
    """从 JSON 文件加载任务列表"""
    if not DATA_FILE.exists():
        return []

    try:
        content = DATA_FILE.read_text(encoding="utf-8")
        return json.loads(content)
    except json.JSONDecodeError:
        logger.error("任务文件 JSON 格式错误，重置为空列表")
        return []
    except Exception as e:
        logger.error(f"读取文件时发生未知错误: {e}")
        return []


def save_tasks(tasks: list) -> None:
    """将任务列表保存到 JSON 文件"""
    try:
        content = json.dumps(tasks, ensure_ascii=False, indent=4)
        DATA_FILE.write_text(content, encoding="utf-8")
    except Exception as e:
        logger.error(f"保存任务文件失败: {e}")


def add_task(title: str) -> list:
    """添加新任务"""
    if not title.strip():
        logger.warning("任务标题不能为空！")
        return load_tasks()

    tasks = load_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "title": title,
        "completed": False
    }
    tasks.append(new_task)
    save_tasks(tasks)
    logger.info(f"成功添加任务: {title}")
    return tasks


def complete_task(task_id: int) -> bool:
    """将指定 ID 的任务标记为完成"""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            logger.info(f"任务 {task_id} 已标记为完成")
            return True

    logger.warning(f"未找到 ID 为 {task_id} 的任务")
    return False


def delete_task(task_id: int) -> bool:
    """删除指定 ID 的任务"""
    tasks = load_tasks()
    new_tasks = [task for task in tasks if task["id"] != task_id]

    if len(new_tasks) == len(tasks):
        logger.warning(f"未找到 ID 为 {task_id} 的任务，删除失败")
        return False

    for index, task in enumerate(new_tasks, start=1):
        task["id"] = index

    save_tasks(new_tasks)
    logger.info(f"成功删除 ID 为 {task_id} 的任务")
    return True


# ================= 华丽的分割线：下面是新增的交互与主函数部分 =================

def show_tasks():
    """查看并格式化打印所有任务"""
    tasks = load_tasks()
    if not tasks:
        print("\n📝 当前暂无任何任务！")
        return

    print("\n================ 任务列表 ================")
    for task in tasks:
        # 三元表达式：如果 completed 为 True 显示✅，否则显示⏳
        status = "✅ 已完成" if task["completed"] else "⏳ 未完成"
        print(f"[{task['id']}] {task['title']} --- {status}")
    print("==========================================")


def main():
    """程序的主入口：负责循环接收用户的键盘输入，并分发到不同的功能"""
    print("欢迎使用命令行任务管理器！")

    while True:
        print("\n请选择操作：")
        print("1. 查看所有任务")
        print("2. 添加新任务")
        print("3. 标记任务为完成")
        print("4. 删除任务")
        print("5. 退出程序")

        # 获取用户的键盘输入
        choice = input("请输入选项编号 (1-5): ").strip()

        if choice == "1":
            show_tasks()

        elif choice == "2":
            title = input("请输入任务内容: ").strip()
            add_task(title)
            print("✨ 添加成功！")

        elif choice == "3":
            try:
                task_id = int(input("请输入要标记为完成的任务 ID: ").strip())
                success = complete_task(task_id)
                if success:
                    print("🎉 任务已更新为完成状态！")
                else:
                    print("❌ 操作失败：未找到该 ID 的任务。")
            except ValueError:
                print("⚠️ 输入无效：请输入纯数字的 ID！")

        elif choice == "4":
            try:
                task_id = int(input("请输入要删除的任务 ID: ").strip())
                success = delete_task(task_id)
                if success:
                    print("🗑️ 任务已删除！")
                else:
                    print("❌ 操作失败：未找到该 ID 的任务。")
            except ValueError:
                print("⚠️ 输入无效：请输入纯数字的 ID！")

        elif choice == "5":
            print("👋 感谢使用，再见！")
            break  # 跳出 while 循环，程序安全退出
        else:
            print("⚠️ 无效的选项，请输入 1 到 5 之间的数字！")


# Python 的经典惯用法：只有直接运行这个文件时，才会执行 main()
if __name__ == "__main__":
    main()