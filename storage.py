# 일정 완료 처리, 저장 및 불러오기
# ChatGPT의 초기 코드와 수정안을 활용했으며, 가독성 개선에도 AI를 활용함.

import json
import os
import tempfile
from datetime import date
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent / "schedules.json"


# 일정 완료 처리 (완료 취소는 팀 합의 후 결정)
def mark_completed(schedules, schedule_id):
    if type(schedule_id) is not int:
        print("오류: 일정 번호는 정수여야 합니다.")
        return schedules
    for schedule in schedules:
        if schedule["id"] == schedule_id:
            schedule["completed"] = True
            return schedules
    print(f"오류: 일정 번호 {schedule_id}을(를) 찾을 수 없습니다.")
    return schedules


# 일정 데이터 형식 확인
def _validate_schedules(schedules):
    if not isinstance(schedules, list):
        raise ValueError("저장 파일의 데이터는 일정 리스트여야 합니다.")

    required = ("id", "title", "type", "due_date", "priority", "completed")
    ids = set()
    for index, schedule in enumerate(schedules, 1):
        if not isinstance(schedule, dict):
            raise ValueError(f"{index}번째 일정이 딕셔너리가 아닙니다.")

        for key in required:
            if key not in schedule:
                raise ValueError(f"{index}번째 일정에 필수 항목이 없습니다.")

        schedule_id = schedule["id"]
        if type(schedule_id) is not int or schedule_id in ids:
            raise ValueError(f"{index}번째 일정의 ID가 올바르지 않거나 중복됩니다.")
        ids.add(schedule_id)

        if not isinstance(schedule["title"], str):
            raise ValueError(f"{index}번째 일정 제목이 문자열이 아닙니다.")
        if schedule["type"] not in ("assignment", "exam"):
            raise ValueError(f"{index}번째 일정 종류가 올바르지 않습니다.")
        if schedule["priority"] not in ("high", "medium", "low"):
            raise ValueError(f"{index}번째 일정 중요도가 올바르지 않습니다.")
        if type(schedule["completed"]) is not bool:
            raise ValueError(f"{index}번째 일정 완료 여부가 True/False가 아닙니다.")

        due_date = schedule["due_date"]
        if not isinstance(due_date, str):
            raise ValueError(f"{index}번째 일정 날짜가 문자열이 아닙니다.")
        try:
            parsed = date.fromisoformat(due_date)
        except ValueError as exc:
            raise ValueError(f"{index}번째 일정 날짜가 잘못되었습니다.") from exc
        if parsed.isoformat() != due_date:
            raise ValueError(f"{index}번째 일정 날짜 형식이 YYYY-MM-DD가 아닙니다.")


# 일정 저장
def save_schedules(schedules):
    _validate_schedules(schedules)
    payload = json.dumps(schedules, ensure_ascii=False, indent=2, allow_nan=False)
    # 기존 파일은 임시 파일에 정상적으로 쓴 뒤에만 교체한다.
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=DATA_FILE.parent,
            prefix=".schedules-",
            suffix=".tmp",
            delete=False,
        ) as tmp:
            temp_path = Path(tmp.name)
            tmp.write(payload)
        os.replace(temp_path, DATA_FILE)
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


# 일정 불러오기
def load_schedules():
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            schedules = json.load(file)
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise ValueError("저장 파일을 읽을 수 없습니다. 원본 파일을 확인하세요.") from exc
    _validate_schedules(schedules)
    return schedules
