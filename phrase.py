import random

phrase = [
    "삶이 있는 한 희망은 있다. - 키케로",
    "산다는 것 그것은 치열한 전투이다. - 로망로랑",
    "하루에 3시간을 걸으면 7년 후에 지구를 한 바퀴 돌 수 있다. - 사무엘존슨",
    "언제나 현재에 집중할 수 있다면 행복할 것이다. - 파울로 코엘료",
    "진저응로 웃으려면 고통을 참아야하며, 나아가 고통을 즐길 줄 알아야한다. - 찰리 채플린",
    "신은 용기있는 자를 결코 버리지 않는다. - 켄러",
    "피할 수 없으면 즐겨라. - 로버트 엘리엇",
    "행복한 삶을 살기 위해 필요한 것은 거의 없다. - 마르쿠스 아우렐리우스 안토니우스",
    "한번의 실패와 영원한 실패를 혼동하지 마라. - F.스콧 핏제랄드",
    "내일은 내일의 태양이 뜬다.",
    "오랫동안 꿈을 그리는 사람은 마침내 그 꿈을 닮아간다. - 앙드레 말로",
    "좋은 성과를 얻으려면 한 걸을 한 걸음이 힘차고 충실하지 않으면 안된다. - 단테",
    "행복은 습관이다. 그것을 몸에 지니라. - 허버드",
    "성공의 비결은 단 한가지, 잘할 수 있는 일에 광적으로 집중하는 것이다. - 톰 모나건",
    "자신감 있는 표정을 지으면 자신감이 생긴다. - 찰스 다윈",
    "평생 살 것처럼 꿈을 꾸어라. 그리고 내일 죽을 것처럼 오늘을 살아라. - 제임스 딘",
    "1퍼센트의 가능성, 그것이 나의 길이다. - 나폴레옹",
    "고통이 남기고 간 뒤를 보라. 고난이 지나면 반드시 기쁨이 스며든다. - 괴테",
    "꿈을 계속 간직하고 있으면 반드시 실현할 때가 온다. - 괴테",
    "마음만을 가지고 있어서는 안된다. 반드시 실천하여야 한다. - 이소룡",
    "만약 우리가 할 수 있는 일을 한다면 우리들은 우리 자신에 깜짝 놀랄 것이다. - 에디슨",
    "눈물과 더불어 빵을 먹어 보지 않은 자는 인생의 참다운 맛을 모른다. - 괴테",
    "진짜 문제는 사람들의 마음이다. 그것은 절대로 물리학이나 윤리학의 문제가 아니다. - 아인슈타인",
    "해야할 것을 하라. 모든 것은 타인의 행복을 위해서, 동시에 특히 나의 행복을 위해서이다. - 톨스토이",
    "사람이 여행을 하는 것은 도착하기 위해서가 아니라 여행하기 위해서이다. - 괴테",
    "재산을 잃은 사람은 많이 잃은 것이고, 친구를 잃은 사람은 더 많이 잃은 것이며, 용기르 잃은 사람은 모든 것을 잃은 것이다. - 세르반테스",
    "돈이란 바닷물과도 같다. 그것은 마시면 마실수록 목이 말라진다. - 쇼펜하우어",
    "사막이 아름다운 것은 어딘가에 샘이 숨겨져 있기 때문이다. - 생떽쥐베리",
    "고난의 시기에 동요하지 않는 것, 이것은 진정 칭찬받을 만한 뛰어난 인물의 증거다. - 베토벤",
    "만족할 줄 아는 사람은 진정한 부자이고, 탐욕스러운 사람은 진실로 가난한 사람이다. - 솔론",
    "성공해서 만족하는 것은 아니다. 만족하고 있었기 때문에 성공한 것이다. - 알랭",
    "곧 위에 비교하면 족하지 못한, 아래에 비교하면 남음이 있다. - 명심보감",
    "그대의 하루 하루를 그대의 마지막 날이라고 생각하라. - 호라티우스",
    "자신을 내보여라. 그러면 재능이 드러날 것이다. - 발타사르 그라시안",
    "당신이 할 수 있다고 믿든 할 수 없다고 믿든 믿는 대로 될 것이다. - 헬리 포드",
    "단순하게 살라. 쓸데없는 절차와 일 때문에 얼마나 복잡한 삶을 살아가는가? - 이드리스 샤흐",
    "자신을 내보여라. 그러면 재능이 드러날 것이다. - 발타사르 그라시안",
    "인생이란 학교에는 불행이란 훌륭한 스승이 있다. 그 스승 때문에 우리는 더욱 단련되는 것이다. - 프리체",
    "세상은 고통으로 가득하지만 그것을 극복하는 사람들로도 가득하다. - 헬렌켈러",
    "용기있는 자로 살아라. 운이 따라주지 않는다면 용기 있는 가슴으로 불행에 맞서라. - 키케로",
    "최고에 도달하려면 최저에서 시작하라. - P.시루스",
    "내 비장의 무기는 아직 손안에 있다. 그것은 희망이다. - 나폴레옹",
    "문제는 목적지에 얼마나 빨리 가느냐가 아니라 그 목적지가 어디냐는 것이다. - 메이벨 뉴컴버",
    "한 번 실패와 영원한 실패를 혼돈하지 마라. - F.스콧 핏제랄드",
    "인간의 삶 전체는 단지 한 순간에 불과하다. 인생을 즐기자. - 플루타르코스",
    "겨울이 오면 봄이 멀지 않으리. - 셸리",
    "일하여 얻으라. 그러면 운명의 바퀴를 붙들어 잡은 것이다. - 랄프 왈도 에머슨",
    "당신의 행복은 무엇이 당신의 영혼을 노래하게 하는가에 따라 결정된다. - 낸시 설리번",
    "자신이 해야할 일을 결정하는 사람은 세상에서 단 한사람, 오직 나 자신뿐이다. - 오손 웰스",
    "인생을 다시 산다면 다음번에는 더 많은 실수를 저지르리라. - 나딘 스테어",
    "절대 어제를 후회하지 마라. 인생은 오늘의 나 안에 있고 내일은 스스로 만드는 것이다. - L.론허바드",
    "인생에서 원하는 것을 얻기 위한 첫 번째 단계는 내가 무엇을 원하는 지 결정하는 것이다. - 벤스타인",
    "가난은 가난하다고 느끼는 곳에 존재한다. - 에머슨",
    "문제점을 찾지 말고 해결책을 찾으라. - 헨리포드",
    "우선 무엇이 되고자 하는가를 자신에게 말하라. 그리고 해야할 일을 하라. - 에픽토테스",
    "되찾을 수 없는게 세월이니 시시한 일에 시간을 낭비하지 말고 순간순간을 후회없이 잘 살아야한다. - 루소",
    "인생에 뜻을 세우는 데 있어 늦은 때라곤 없다. - 볼드윈",
    "도중에 포기하지 말라. 망설이지 말라. 최후의 성공을 거둘 때까지 밀고 나가자. - 헨리포드",
    "네 자신의 불행을 생각하지 않게 되는 가장 좋은 방법은 일에 몰두하는 것이다. - 베토벤",
    "우리는 두려움의 홍수에 버티기 위해서 끊임없이 용기의 둑을 쌓아야 한다. - 마틴 루터 킹",
    "이미 끝나버린 일을 후회하기 보다는 하고 싶었던 일을 하지 못한 것을 후회하라. - 탈무드",
    "실패는 잊어라 그러나 그것이 준 교훈은 절대 잊으면 안된다. - 하버트 개서",
    "길을 잃는다는 것은 곧 길을 알게 된다는 것이다."
]


def randomPhrase():
    return random.choice(phrase)