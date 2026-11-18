
# 대학생 과제 및 시험 일정 관리 프로그램

## 1. 프로젝트 소개
대학생들이 과제와 시험 일정을 효율적으로 관리할 수 있도록 돕는 Python 기반 프로그램입니다.

## 2. 주요 기능
- 과제 및 시험 일정 등록·수정·삭제·조회
- 마감일까지 남은 날짜(D-Day) 자동 계산
- 마감일 및 중요도에 따른 일정 정렬
- 과제 완료 여부 체크
- 일정 데이터 저장 및 불러오기

## 3. 팀원별 역할 분담
- 팀장: main.py
  - 프로그램 실행 메뉴 구현
  - 전체 기능 연결 및 통합
  - GitHub 관리 및 README 작성

- 팀원 1: schedule.py
  - 일정 등록·수정·삭제·조회 기능

- 팀원 2: deadline.py
  - D-Day 계산
  - 마감일 및 중요도에 따른 일정 정렬

- 팀원 3: storage.py
  - 일정 완료 여부 관리
  - 일정 저장 및 불러오기

## 4. 공통 데이터 구조
모든 일정은 Python 딕셔너리 형태로 관리합니다.

```python
schedule = {
    "id": 1,
    "title": "Python Assignment",
    "type": "assignment",
    "due_date": "2026-12-01",
    "priority": "high",
    "completed": False
}
```

여러 일정은 `schedules`라는 리스트에 저장합니다.

## 5. 공통 데이터 규칙
- id: 일정마다 부여하는 고유 번호(정수)
- title: 과제 또는 시험 이름(문자열)
- type: assignment(과제), exam(시험)
- due_date: 마감일(YYYY-MM-DD)
- priority: high(높음), medium(보통), low(낮음)
- completed: True(완료), False(미완료)

## 6. 파일별 함수 구성

### main.py (팀장)
- main(): 프로그램 실행 및 메뉴 관리

### schedule.py (팀원 1)
- add_schedule(schedules): 일정 등록
- edit_schedule(schedules): 일정 수정
- delete_schedule(schedules): 일정 삭제
- list_schedules(schedules): 일정 목록 조회

### deadline.py (팀원 2)
- calculate_dday(due_date): D-Day 계산
- sort_by_deadline(schedules): 마감일순 정렬
- sort_by_priority(schedules): 중요도순 정렬

### storage.py (팀원 3)
- mark_completed(schedules, schedule_id): 완료 여부 변경
- save_schedules(schedules): 일정 파일 저장
- load_schedules(): 저장된 일정 불러오기

## 7. 개발 규칙
- 공통 데이터 구조와 변수명을 동일하게 사용합니다.
- 함수명과 파일명은 임의로 변경하지 않습니다.
- 각자 담당한 파일을 중심으로 개발합니다.
- 모든 팀원은 본인의 GitHub 계정으로 commit을 남깁니다.
- 개발한 기능은 Pull Request를 통해 통합합니다.
- 오류나 수정 사항은 팀원들과 공유합니다.

## 8. 개발 진행 순서
1. 공통 구조 및 역할 분담 확정
2. 팀원별 기능 개발
3. GitHub를 통한 코드 공유 및 통합
4. 프로그램 테스트 및 오류 수정
5. README 보완 및 최종 제출
