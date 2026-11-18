
def main():
    while True:
        print("\n===== 대학생 과제 및 시험 일정 관리 =====")
        print("1. 일정 등록")
        print("2. 일정 수정")
        print("3. 일정 삭제")
        print("4. 일정 목록 조회")
        print("5. D-Day 확인")
        print("6. 마감일순 정렬")
        print("7. 중요도순 정렬")
        print("8. 완료 여부 변경")
        print("9. 일정 저장")
        print("10. 일정 불러오기")
        print("0. 종료")

        choice = input("\n메뉴를 선택하세요: ")

        if choice == "0":
            print("프로그램을 종료합니다.")
            break
        elif choice in [str(i) for i in range(1, 11)]:
            print(f"{choice}번 기능은 개발 중입니다.")
        else:
            print("올바른 메뉴 번호를 입력해 주세요.")


if __name__ == "__main__":
    main()
