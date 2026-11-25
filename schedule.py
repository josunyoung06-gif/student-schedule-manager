from datetime import datetime


# 날짜 입력 및 형식 확인
def input_due_date():
    while True:
        due_date = input("마감일 (YYYY-MM-DD): ")

        try:
            date = datetime.strptime(due_date, "%Y-%m-%d")
            return date.strftime("%Y-%m-%d")
        except ValueError:
            print("올바른 날짜를 입력해 주세요.")


# 일정 등록
def add_schedule(schedules):
    title = input("일정 이름: ")

    while True:
        schedule_type = input("일정 유형 (assignment/exam): ")
        if schedule_type in ["assignment", "exam"]:
            break
        print("올바른 일정 유형을 입력해 주세요.")

    due_date = input_due_date()

    while True:
        priority = input("중요도 (high/medium/low): ")
        if priority in ["high", "medium", "low"]:
            break
        print("올바른 중요도를 입력해 주세요.")

    if len(schedules) == 0:
        schedule_id = 1
    else:
        schedule_id = max(s["id"] for s in schedules) + 1

    schedule = {
        "id": schedule_id,
        "title": title,
        "type": schedule_type,
        "due_date": due_date,
        "priority": priority,
        "completed": False
    }

    schedules.append(schedule)
    print("일정이 등록되었습니다.")

    return schedules


# 일정 목록 조회
def list_schedules(schedules):
    if len(schedules) == 0:
        print("등록된 일정이 없습니다.")
        return

    print("\n===== 일정 목록 =====")

    for schedule in schedules:
        if schedule["completed"]:
            status = "완료"
        else:
            status = "미완료"

        print(f'번호: {schedule["id"]}')
        print(f'이름: {schedule["title"]}')
        print(f'유형: {schedule["type"]}')
        print(f'마감일: {schedule["due_date"]}')
        print(f'중요도: {schedule["priority"]}')
        print(f'상태: {status}')
        print("--------------------")


# 일정 수정
def edit_schedule(schedules):
    list_schedules(schedules)

    if len(schedules) == 0:
        return schedules

    try:
        schedule_id = int(input("수정할 일정 번호: "))
    except ValueError:
        print("숫자를 입력해 주세요.")
        return schedules

    for schedule in schedules:
        if schedule["id"] == schedule_id:
            schedule["title"] = input("새로운 일정 이름: ")

            while True:
                schedule_type = input("새로운 유형 (assignment/exam): ")
                if schedule_type in ["assignment", "exam"]:
                    schedule["type"] = schedule_type
                    break
                print("올바른 유형을 입력해 주세요.")

            schedule["due_date"] = input_due_date()

            while True:
                priority = input("새로운 중요도 (high/medium/low): ")
                if priority in ["high", "medium", "low"]:
                    schedule["priority"] = priority
                    break
                print("올바른 중요도를 입력해 주세요.")

            print("일정이 수정되었습니다.")
            return schedules

    print("해당 일정이 존재하지 않습니다.")
    return schedules


# 일정 삭제
def delete_schedule(schedules):
    list_schedules(schedules)

    if len(schedules) == 0:
        return schedules

    try:
        schedule_id = int(input("삭제할 일정 번호: "))
    except ValueError:
        print("숫자를 입력해 주세요.")
        return schedules

    for schedule in schedules:
        if schedule["id"] == schedule_id:
            schedules.remove(schedule)
            print("일정이 삭제되었습니다.")
            return schedules

    print("해당 일정이 존재하지 않습니다.")
    return schedules
