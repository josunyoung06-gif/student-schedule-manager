"""일정 완료 상태 및 JSON 파일 저장/불러오기 (1차 수정 검토안).

README에 명시된 공개 함수명과 입출력 규칙을 유지합니다.
AI가 작성한 검토용 코드이며, 팀의 합의와 통합 테스트 전 단계입니다.
"""

import json
import os
import tempfile
from datetime import date
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent / "schedules.json"


def mark_completed(schedules, schedule_id):
    """해당 ID의 completed를 True로 표시하고 목록을 반환합니다."""
    for schedule in schedules:
        if schedule["id"] == schedule_id:
            schedule["completed"] = True
            return schedules
    print(f"오류: 일정 번호 {schedule_id}을(를) 찾을 수 없습니다.")
    return schedules


def _validate_schedules(schedules):
    """README의 공통 데이터 형식과 고유 ID 규칙을 확인합니다."""
    if not isinstance(schedules, list):
        raise ValueError("저장 파일의 데이터는 일정 리스트여야 합니다.")

    ids = set()
    for index, schedule in enumerate(schedules, 1):
        if not isinstance(schedule, dict):
            raise ValueError(f"{index}번째 일정이 딕셔너리가 아닙니다.")

        required = {"id", "title", "type", "due_date", "priority", "completed"}
        if not required.issubset(schedule):
            raise ValueError(f"{index}번째 일정에 필수 항목이 없습니다.")
        if type(schedule["id"]) is not int or schedule["id"] in ids:
            raise ValueError(f"{index}번째 일정의 ID가 올바르지 않거나 중복됩니다.")
        ids.add(schedule["id"])
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


def save_schedules(schedules):
    """정상적인 일정 목록을 임시 파일에 저장한 다음 본 파일로 교체합니다."""
    _validate_schedules(schedules)
    payload = json.dumps(schedules, ensure_ascii=False, indent=2)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=DATA_FILE.parent,
            prefix=".schedules-", suffix=".tmp", delete=False,
        ) as tmp:
            temp_path = Path(tmp.name)
            tmp.write(payload)
        os.replace(temp_path, DATA_FILE)
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def load_schedules():
    """저장된 일정 목록을 읽고 검증합니다. 파일이 없다면 []을 반환합니다."""
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            schedules = json.load(file)
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise ValueError("저장 파일을 읽을 수 없습니다. 원본 파일을 확인하세요.") from exc
    _validate_schedules(schedules)
    return schedules
