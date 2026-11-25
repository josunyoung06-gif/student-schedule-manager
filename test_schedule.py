from schedule import add_schedule
from schedule import list_schedules
from schedule import edit_schedule
from schedule import delete_schedule

schedules = []

print("\n===== 일정 등록 테스트 =====")
schedules = add_schedule(schedules)

print("\n===== 일정 조회 테스트 =====")
list_schedules(schedules)

print("\n===== 일정 수정 테스트 =====")
schedules = edit_schedule(schedules)
list_schedules(schedules)

print("\n===== 일정 삭제 테스트 =====")
schedules = delete_schedule(schedules)
list_schedules(schedules)
