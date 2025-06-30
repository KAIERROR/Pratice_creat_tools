import json
from datetime import datetime, timedelta
import re

FILENAME = "toDo.json"

def loadTasks():
    try:
        with open(FILENAME,"r",encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def saveTasks(tasks):
    with open(FILENAME,"w",encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

def show_soon_tasks(tasks, days=3):
    today = datetime.today()
    soon = today + timedelta(days=days)
    found = False
    print(f"\n【即將在{days}天內到期的任務】")
    for i, task in enumerate(tasks, 1):
        try:
            deadline = datetime.strptime(task['deadline'], "%Y/%m/%d")
            if today <= deadline <= soon and not task.get("done"):
                status = "✅" if task.get("done") else "❌"
                print(f"{i}. {task['name']} (截止: {task['deadline']}) [{task['category']}] {status}")
                found = True
        except Exception:
            continue
    if not found:
        print("沒有即將到期的任務。")

def valid_date(date_str):
    # 簡單檢查 YYYY/MM/DD 格式
    return re.match(r"^\d{4}/\d{2}/\d{2}$", date_str) is not None

def main():
    tasks = loadTasks()
    print("\n歡迎回來任務清單！")

    while True:
        print("\n=====選單=====")
        print("1. 顯示任務清單")       
        print("2. 新增任務")
        print("3. 刪除任務")
        print("4. 切換任務完成狀態")
        print("5. 顯示即將到期任務")
        print("6. 離開")
        print("7. 修改任務")  # 新增選項
        choice = input("請輸入選項(1-7): ")

        if choice == "1":
            if not tasks:
                print("任務清單是空的。")
            else:
                print("\n任務清單 ")
                for i, task in enumerate(tasks, 1):
                    status = "✅" if task.get("done") else "❌"
                    print(f"{i}. {task['name']} (截止: {task['deadline']}) [{task['category']}] {status}")
        elif choice == "2":
            new_task = input("請輸入新的任務: ")
            # 日期格式防呆
            while True:
                new_taskDL = input("請輸入任務的截止日期(格式: YYYY/MM/DD): ")
                if valid_date(new_taskDL):
                    break
                else:
                    print("日期格式錯誤，請重新輸入（格式: YYYY/MM/DD）")
            task_category = input("請輸入任務分類（如 工作/學習/娛樂）: ")
            task = {
                "name": new_task,
                "deadline": new_taskDL,
                "category": task_category,
                "done": False
            }
            tasks.append(task)
            saveTasks(tasks)
            print(f"任務 '{new_task}' 已新增到清單中。")
        elif choice == "3":
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task['name']}")
            del_taskID = int(input("請輸入要刪除的任務編號: "))
            if 1 <= del_taskID <= len(tasks):
                remove_task = tasks.pop(del_taskID - 1)
                saveTasks(tasks)
                print(f"任務 '{remove_task['name']}' 已從清單中刪除。")
            else:
                print("無效的任務編號。")
        elif choice == "4":
            for i, task in enumerate(tasks, 1):
                status = "✅" if task.get("done") else "❌"
                print(f"{i}. {task['name']} {status}")
            idx = int(input("請輸入要切換完成狀態的任務編號: ")) - 1
            if 1 <= idx < len(tasks):
                tasks[idx]["done"] = not tasks[idx].get("done", False)
                saveTasks(tasks)
                print(f"任務 '{tasks[idx]['name']}' 狀態已切換。")
            else:
                print("無效的任務編號。")
        elif choice == "5":
            show_soon_tasks(tasks)
        elif choice == "6":
            print("感謝使用任務清單！再見！")
            break
        elif choice == "7":
            if not tasks:
                print("任務清單是空的，無法修改。")
                continue
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task['name']} (截止: {task['deadline']}) [{task['category']}]")
            try:
                idx = int(input("請輸入要修改的任務編號: ")) - 1
                if 0 <= idx < len(tasks):
                    print("你想修改什麼？")
                    print("1. 任務名稱")
                    print("2. 截止日期")
                    print("3. 任務分類")
                    field = input("請輸入選項(1-3): ")
                    if field == "1":
                        new_name = input("請輸入新的任務名稱: ")
                        tasks[idx]["name"] = new_name
                    elif field == "2":
                        # 日期格式防呆
                        while True:
                            new_deadline = input("請輸入新的截止日期(格式: YYYY/MM/DD): ")
                            if valid_date(new_deadline):
                                break
                            else:
                                print("日期格式錯誤，請重新輸入（格式: YYYY/MM/DD）")
                        tasks[idx]["deadline"] = new_deadline
                    elif field == "3":
                        new_category = input("請輸入新的任務分類: ")
                        tasks[idx]["category"] = new_category
                    else:
                        print("無效的選項。")
                        continue
                    saveTasks(tasks)
                    print("任務已修改完成。")
                else:
                    print("無效的任務編號。")
            except ValueError:
                print("請輸入有效的數字。")
        else:
            print("無效的選項，請重新輸入。")

if __name__ == "__main__":
    main()







