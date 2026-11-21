"""일정 완료 상태 및 JSON 파일 저장/불러오기.

팀 README에 명시된 세 함수의 인터페이스를 유지한 검토용 초안.
"""

import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent / "schedules.json"


def mark_completed(schedules, schedule_id):
    """지정한 ID의 일정을 완료(True)로 표시하고 목록을 반환한다."""
    for schedule in schedules:
        if schedule["id"] == schedule_id:
            schedule["completed"] = True
            return schedules

    print(f"오류: 일정 번호 {schedule_id}을(를) 찾을 수 없습니다.")
    return schedules


def save_schedules(schedules):
    """일정 목록을 storage.py와 같은 폴더의 schedules.json에 저장한다."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(schedules, file, ensure_ascii=False, indent=2)


def load_schedules():
    """저장된 일정 목록을 읽는다. 파일이 없으면 빈 목록을 반환한다."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            schedules = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError("저장 파일의 JSON 형식이 잘못되었습니다. 원본 파일을 확인하세요.") from exc

    if not isinstance(schedules, list):
        raise ValueError("저장 파일의 데이터는 일정 리스트여야 합니다.")
    return schedules
