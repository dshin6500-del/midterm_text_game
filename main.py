import pickle


class Player:
    def __init__(self, location, hp, money, current_difficulty="보통"):
        self.location = location
        self.hp = hp
        self.money = money
        self.current_difficulty = current_difficulty
        self.bag = []
        self.missions = []

    def move(self, direction, campus_map):
        row = self.location[0]
        col = self.location[1]
        row_change, col_change = directions[direction]

        if location_check(campus_map, row + row_change, col + col_change) is None:
            print("그 방향은 막혔습니다.")
        else:
            self.location[0] += row_change
            self.location[1] += col_change

            self.hp -= difficulty[self.current_difficulty]

            new_location = campus_map[self.location[0]][self.location[1]]
            print(f"{new_location}에 도착했습니다.")

            if new_location in places:
                place = places[new_location]
                if place.buy:
                    print("[구매]")
                if place.sell:
                    print("[판매]")
                if place.quest:
                    print("[임무]")
                if place.event:
                    print(f"[사건관련정보] {place.event}")

    def print_status(self, campus_map):
        row = self.location[0]
        col = self.location[1]
        print(f"계좌의 잔액 = {self.money:,}원")
        print(f"HP = {self.hp}")
        print(f"현재위치 = {location_check(campus_map, row, col)}")
        north = location_check(campus_map, row-1, col) or "막힘"
        south = location_check(campus_map, row+1, col) or "막힘"
        east = location_check(campus_map, row, col+1) or "막힘"
        west = location_check(campus_map, row, col-1) or "막힘"
        print(f"동서남북 = {east}, {west}, {south}, {north}")

    def open_bag(self):
        if len(self.bag) == 0:
            print("가방이 비어있습니다")
        else:
            for i, item in enumerate(self.bag):
                print(f'{i+1}. {item}')
            while True:
                choice = input("사용할 아이템(취소[x]): ")
                if choice in self.bag:
                    self.hp += items[choice]['hp']
                    self.bag.remove(choice)
                    print(f"{choice}을(를) 사용했습니다. HP가 {items[choice]['hp']}만큼 증가했습니다.")
                    break
                elif choice == "x":
                    break
                else:
                    print("잘못된 입력입니다.")


class Quest:
    def __init__(self, description, answer=None):
        self.description = description
        self.answer = answer


class Place:
    def __init__(self, name, buy=None, sell=None, event=None, quest=None):
        self.name = name
        self.buy = buy
        self.sell = sell
        self.event = event
        self.quest = quest


def location_check(campus_map, row, col):
    if row < 0 or row >= len(campus_map) or col < 0 or col >= len(campus_map[0]) or campus_map[row][col] is None:
        return None
    else:
        return campus_map[row][col]


campus_map = [
    ["종합관", "본관", "경영관", "노천극장", "새천년관", "이윤재관"],
    ["백양관", "백양로5", "대강당", "음악관", "알렌관", "ABMRC"],
    ["중앙도서관", "독수리상", "학생회관", "루스채플", "재활병원", "치과대학"],
    ["체육관", "백양로3", "공터2", "광혜원", "어린이병원", "세브란스"],
    ["공학관", "백양로2", "백주년기념관", "안과병원", "제중관", None],
    ["공학원", "백양로1", "공터1", "암병원", "의과대학", None],
    ["연대앞 버스정류장", "정문", "스타벅스", "세브란스 버스정류장", None, None]
]

buy_shared_price = {"두쫀쿠": 4000, "카페라떼": 2000}
sell_shared_price1 = {"두쫀쿠": 7000, "카페라떼": 4000}
sell_shared_price2 = {"두쫀쿠": 6000, "카페라떼": 3000}

places = {
    "체육관": Place("체육관", sell=sell_shared_price1),
    "공학관": Place("공학관", sell=sell_shared_price1),
    "공학원": Place("공학원", sell=sell_shared_price1),
    "재활병원": Place("재활병원", sell=sell_shared_price1),
    "어린이병원": Place("어린이병원", sell=sell_shared_price1),
    "종합관": Place("종합관", sell=sell_shared_price1),
    "노천극장": Place("노천극장", sell=sell_shared_price1),
    "중앙도서관": Place("중앙도서관", sell=sell_shared_price2),
    "백양관": Place("백양관", sell=sell_shared_price2),
    "대강당": Place("대강당", sell=sell_shared_price2),
    "백주년기념관": Place("백주년기념관", sell=sell_shared_price2),
    "안과병원": Place("안과병원", sell=sell_shared_price2),
    "암병원": Place("암병원", sell=sell_shared_price2),
    "새천년관": Place("새천년관", sell=sell_shared_price2),
    "알렌관": Place("알렌관", sell=sell_shared_price2),
    "제중관": Place("제중관", sell=sell_shared_price2),
    "의과대학": Place("의과대학", sell=sell_shared_price2),
    "치과대학": Place("치과대학", sell=sell_shared_price2),
    "세브란스": Place("세브란스", sell=sell_shared_price2, quest=True),
    "본관": Place("본관", sell=sell_shared_price2, quest=True),
    "경영관": Place("경영관", sell=sell_shared_price2),
    "학생회관": Place("학생회관", buy={"두쫀쿠": 5000, "카페라떼": 3000}),
    "스타벅스": Place("스타벅스", buy=buy_shared_price),
    "ABMRC": Place("ABMRC", buy=buy_shared_price),
    "정문": Place("정문", quest=True),
    "독수리상": Place("독수리상", quest=True),
    "이윤재관": Place("이윤재관", quest=True),
}

with open("event.bin", "rb") as f:
    event_data = pickle.load(f)

for place_name, event_text in event_data["events"].items():
    if place_name in places:
        places[place_name].event = event_text
    else:
        places[place_name] = Place(place_name, event=event_text)


quest_go_to_eagle = Quest("독수리상에서 임무를 받아오자!")
quest_corruption = Quest(
    "교내 부조리 수사 - 교내 어딘가에서 부조리가 일어나고있다. 이동하고 상호작용을 해서 부조리를 찾아서 본관에 보고하라.",
    answer=event_data["answers"]["교내 부조리 수사"]
)
quest_hygiene = Quest(
    "교내 위생사건 수사 - 학생들이 단체로 식중독에 걸렸다. 이동하고 상호작용을 해서 위생사건의 원인을 찾아서 세브란스에 보고하라.",
    answer=event_data["answers"]["교내 위생사건 수사"]
)


directions = {
    "North": (-1, 0),
    "South": (1, 0),
    "East": (0, 1),
    "West": (0, -1)
}

items = {
    "두쫀쿠": {'price': 5000, 'hp': 10},
    "카페라떼": {'price': 2500, 'hp': 5}
}

difficulty = {
    "쉬움": 0.5,
    "보통": 1,
    "어려움": 2
}


player = Player([6, 0], 10, 10000)
print("송도 생활을 마치고 신촌에 처음 도착했다. 연대앞 버스정류장이다.")


while True:
    if player.hp <= 0:
        print("Game Over.")
        break

    user_input = input("입력: ")

    if user_input == "상태":
        player.print_status(campus_map)

    elif user_input == "북":
        player.move("North", campus_map)

    elif user_input == "남":
        player.move("South", campus_map)

    elif user_input == "동":
        player.move("East", campus_map)

    elif user_input == "서":
        player.move("West", campus_map)

    elif user_input == "가방":
        player.open_bag()

    elif user_input == "난이도":
        print(f"현재 난이도: {player.current_difficulty}")
        print("1. 쉬움  2. 보통  3. 어려움")
        choice = input("입력: ")
        if choice == "1":
            player.current_difficulty = "쉬움"
        elif choice == "2":
            player.current_difficulty = "보통"
        elif choice == "3":
            player.current_difficulty = "어려움"
        else:
            print("잘못된 입력입니다.")

    elif user_input == "임무목록":
        if len(player.missions) == 0:
            print("현재 임무가 없습니다.")
        else:
            for i, quest in enumerate(player.missions):
                print(f"{i+1}. {quest.description}")

    elif user_input == "임무":
        current_location = campus_map[player.location[0]][player.location[1]]
        if current_location == "독수리상":
            if quest_go_to_eagle in player.missions:
                player.missions.remove(quest_go_to_eagle)
            player.missions.append(quest_corruption)
            player.missions.append(quest_hygiene)
            print("교내 부조리 수사 임무를 받았습니다.")
            print("교내 위생사건 수사 임무를 받았습니다.")
            print("[임무목록]에 임무가 추가되었습니다.")

        elif current_location == "정문":
            if quest_go_to_eagle not in player.missions:
                player.missions.append(quest_go_to_eagle)
                print("학교에서 어떤 일들이 일어나고있는지 소식들이 모이는 독수리상에서 알아보자.")
                print("[임무목록]에 임무가 추가되었습니다.")
            else:
                print("이미 임무를 받았습니다.")

        elif current_location == "본관":
            if quest_corruption in player.missions:
                answer = input("교내 어디에 부조리가 있나? ")
                if answer == quest_corruption.answer:
                    player.missions.remove(quest_corruption)
                    print("정답입니다! 수업들으러 이윤재관 가야지!")
                else:
                    print("잘못된 답입니다. 더 조사해보세요.")
            else:
                print("관련 임무가 없습니다.")

        elif current_location == "세브란스":
            if quest_hygiene in player.missions:
                answer = input("교내 어디에 식중독 원인이 있나? ")
                if answer == quest_hygiene.answer:
                    player.missions.remove(quest_hygiene)
                    print("정답입니다! 수업들으러 이윤재관 가야지!")
                else:
                    print("잘못된 답입니다. 더 조사해보세요.")
            else:
                print("관련 임무가 없습니다.")

        elif current_location == "이윤재관":
            corruption_done = quest_corruption not in player.missions
            hygiene_done = quest_hygiene not in player.missions
            if corruption_done and hygiene_done:
                print("부조리와 식중독 수사를 완료했구나! 수업은 이걸로 끝입니다. 또 만나요~")
                break
            elif corruption_done:
                print("부조리 수사를 완료했구나! 식중독 원인도 찾아주세요~")
            elif hygiene_done:
                print("식중독 수사를 완료했구나! 부조리도 찾아주세요~")
            else:
                print("아직 임무를 완료하지 않았습니다. 독수리상에서 임무를 받아오세요.")
        else:
            print("여기서는 임무가 없습니다.")

    elif user_input == "구매":
        current_location = campus_map[player.location[0]][player.location[1]]
        place = places.get(current_location)

        if not place or not place.buy:
            print("여기서는 구매할 수 없습니다.")
        else:
            print("구매 가능한 물건:")
            item_list = list(place.buy.items())
            for i, (item_name, price) in enumerate(item_list):
                print(f"{i+1}. {item_name}: {price}원, HP가 {items[item_name]['hp']}만큼 증가한다.")
            print(f"{len(item_list)+1}. 종료")

            while True:
                choice = input("입력: ")
                if choice == str(len(item_list)+1):
                    break
                elif choice.isdigit() and 1 <= int(choice) <= len(item_list):
                    item_name, price = item_list[int(choice)-1]
                    if player.money < price:
                        print("잔액이 부족합니다.")
                    else:
                        player.money -= price
                        player.bag.append(item_name)
                        print(f"{item_name}을(를) 구매해서 가방에 넣었다. 계좌 잔액 = {player.money:,}원")
                        break
                else:
                    print("잘못된 입력입니다.")

    elif user_input == "판매":
        current_location = campus_map[player.location[0]][player.location[1]]
        place = places.get(current_location)


        if not place or not place.sell:
            print("여기서는 판매할 수 없습니다.")
        else:
            sellable = [item for item in player.bag if item in place.sell]
            if not sellable:
                print("판매할 수 있는 물건이 없습니다.")
            else:
                print("판매 가능한 물건:")
                for i, item_name in enumerate(sellable):
                    print(f"{i+1}. {item_name}: {place.sell[item_name]}원")
                print(f"{len(sellable)+1}. 종료")

                while True:
                    choice = input("입력: ")
                    if choice == str(len(sellable)+1):
                        break
                    elif choice.isdigit() and 1 <= int(choice) <= len(sellable):
                        item_name = sellable[int(choice)-1]
                        price = place.sell[item_name]
                        player.money += price
                        player.bag.remove(item_name)
                        print(f"{item_name}을(를) 판매했다. 계좌 잔액 = {player.money:,}원")
                        break
                    else:
                        print("잘못된 입력입니다.")