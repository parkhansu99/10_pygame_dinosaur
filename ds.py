import pygame
import os
import random
pygame.init()  # 초기화 (반드시 필요)

# Global Constants
SCREEN_HEIGHT = 600  # 화면 높이
SCREEN_WIDTH = 1100  # 화면 너비
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # 화면 설정

# 이미지 로딩 : 애니메이션으로 만들고자 리스트로 저장하는 것
RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),  # 달리기 이미지 1
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]  # 달리기 이미지 2
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))  # 점프 이미지
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),  # 앉기 이미지 1
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]  # 앉기 이미지 2
SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),  # 작은 선인장 이미지 1
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),  # 작은 선인장 이미지 2
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]  # 작은 선인장 이미지 3
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),  # 큰 선인장 이미지 1
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),  # 큰 선인장 이미지 2
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]  # 큰 선인장 이미지 3
BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),  # 새 이미지 1
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]  # 새 이미지 2
CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))  # 구름 이미지
BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))  # 배경 이미지


### Dinosaur 클래스 정의 (플레이어 캐릭터의 행동과 상태 관리)
class Dinosaur:
    X_POS = 80  # X 좌표
    Y_POS = 310  # Y 좌표 (달리기 상태)
    Y_POS_DUCK = 340  # Y 좌표 (앉기 상태)
    JUMP_VEL = 8.5  # 점프 속도

    def __init__(self):
        self.duck_img = DUCKING  # 앉기 이미지
        self.run_img = RUNNING  # 달리기 이미지
        self.jump_img = JUMPING  # 점프 이미지

        self.dino_duck = False  # 앉기 상태
        self.dino_run = True  # 달리기 상태
        self.dino_jump = False  # 점프 상태

        self.step_index = 0  # 이미지 전환 인덱스
        self.jump_vel = self.JUMP_VEL  # 점프 속도 초기화
        self.image = self.run_img[0]  # 기본 이미지 설정 (달리기)
        self.dino_rect = self.image.get_rect()  # 캐릭터의 사각형 구역 설정
        self.dino_rect.x = self.X_POS  # X 좌표 설정
        self.dino_rect.y = self.Y_POS  # Y 좌표 설정

    def update(self, userInput):
        if self.dino_duck:  # 앉기 상태일 때
            self.duck()
        if self.dino_run:  # 달리기 상태일 때
            self.run()
        if self.dino_jump:  # 점프 상태일 때
            self.jump()

        if self.step_index >= 10:  # 이미지 전환 인덱스 조정
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:  # 점프 입력 시
            self.dino_duck = False  # 앉기 상태 해제
            self.dino_run = False  # 달리기 상태 해제
            self.dino_jump = True  # 점프 상태 설정
        elif userInput[pygame.K_DOWN] and not self.dino_jump:  # 앉기 입력 시
            self.dino_duck = True  # 앉기 상태 설정
            self.dino_run = False  # 달리기 상태 해제
            self.dino_jump = False  # 점프 상태 해제
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):  # 점프와 앉기 상태가 아닐 때
            self.dino_duck = False  # 앉기 상태 해제
            self.dino_run = True  # 달리기 상태 설정
            self.dino_jump = False  # 점프 상태 해제

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]  # 앉기 이미지 설정
        self.dino_rect = self.image.get_rect()  # 캐릭터의 사각형 구역 설정
        self.dino_rect.x = self.X_POS  # X 좌표 설정
        self.dino_rect.y = self.Y_POS_DUCK  # Y 좌표 설정 (앉기 상태)
        self.step_index += 1  # 이미지 전환 인덱스 증가

    def run(self):
        self.image = self.run_img[self.step_index // 5]  # 달리기 이미지 설정
        self.dino_rect = self.image.get_rect()  # 캐릭터의 사각형 구역 설정
        self.dino_rect.x = self.X_POS  # X 좌표 설정
        self.dino_rect.y = self.Y_POS  # Y 좌표 설정 (달리기 상태)
        self.step_index += 1  # 이미지 전환 인덱스 증가

    def jump(self):
        self.image = self.jump_img  # 점프 이미지 설정
        if self.dino_jump:  # 점프 상태일 때
            self.dino_rect.y -= self.jump_vel * 4  # Y 좌표 감소 (점프)
            self.jump_vel -= 0.8  # 점프 속도 감소
        if self.jump_vel < - self.JUMP_VEL:  # 점프가 끝났을 때
            self.dino_jump = False  # 점프 상태 해제
            self.jump_vel = self.JUMP_VEL  # 점프 속도 초기화

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))  # 화면에 캐릭터 그리기


### Cloud 클래스 정의 (구름의 위치와 움직임 관리)
class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)  # 초기 X 좌표 설정
        self.y = random.randint(50, 100)  # 초기 Y 좌표 설정
        self.image = CLOUD  # 구름 이미지
        self.width = self.image.get_width()  # 구름의 너비

    def update(self):
        self.x -= game_speed  # X 좌표 감소 (움직임)
        if self.x < -self.width:  # 화면 밖으로 나가면
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)  # X 좌표 재설정
            self.y = random.randint(50, 100)  # Y 좌표 재설정

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))  # 화면에 구름 그리기


### Obstacle 클래스 정의 (장애물의 공통 속성 및 동작 관리)
class Obstacle:
    def __init__(self, image, type):
        self.image = image  # 이미지 리스트
        self.type = type  # 장애물 타입
        self.rect = self.image[self.type].get_rect()  # 장애물의 사각형 구역 설정
        self.rect.x = SCREEN_WIDTH  # X 좌표 설정

    def update(self):
        self.rect.x -= game_speed  # X 좌표 감소 (움직임)
        if self.rect.x < -self.rect.width:  # 화면 밖으로 나가면
            obstacles.pop()  # 장애물 제거

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)  # 화면에 장애물 그리기


### SmallCactus 클래스 정의 (작은 선인장의 속성 및 동작 관리)
class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)  # 장애물 타입 설정
        super().__init__(image, self.type)  # 부모 클래스 초기화
        self.rect.y = 325  # Y 좌표 설정


### LargeCactus 클래스 정의 (큰 선인장의 속성 및 동작 관리)
class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)  # 장애물 타입 설정
        super().__init__(image, self.type)  # 부모 클래스 초기화
        self.rect.y = 300  # Y 좌표 설정


### Bird 클래스 정의 (새의 속성 및 동작 관리)
class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0  # 새 타입 설정
        super().__init__(image, self.type)  # 부모 클래스 초기화
        self.rect.y = 250  # Y 좌표 설정
        self.index = 0  # 이미지 인덱스 초기화

    def draw(self, SCREEN):
        if self.index >= 9:  # 이미지 인덱스 범위 초과 시
            self.index = 0  # 인덱스 초기화
        SCREEN.blit(self.image[self.index//5], self.rect)  # 화면에 새 그리기
        self.index += 1  # 이미지 인덱스 증가


### 메인 함수 (게임의 주요 루프 및 로직 처리)
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles  # 전역 변수
    run = True  # 게임 실행 상태
    clock = pygame.time.Clock()  # FPS 설정
    player = Dinosaur()  # 플레이어 캐릭터 생성
    cloud = Cloud()  # 구름 생성
    game_speed = 20  # 초기 게임 속도
    x_pos_bg = 0  # 배경 X 좌표
    y_pos_bg = 380  # 배경 Y 좌표
    points = 0  # 점수 초기화
    font = pygame.font.Font('freesansbold.ttf', 20)  # 폰트 설정
    obstacles = []  # 장애물 리스트
    death_count = 0  # 사망 횟수 초기화

    ### 점수 함수 (점수 업데이트 및 표시)
    def score():
        global points, game_speed
        points += 1  # 점수 증가
        if points % 100 == 0:  # 점수가 100의 배수일 때
            game_speed += 1  # 게임 속도 증가

        text = font.render("Points: " + str(points), True, (0, 0, 0))  # 점수 텍스트 생성
        textRect = text.get_rect()  # 텍스트의 사각형 구역 설정
        textRect.center = (1000, 40)  # 텍스트 위치 설정
        SCREEN.blit(text, textRect)  # 화면에 점수 표시

    ### 배경 함수 (배경 이미지 업데이트 및 표시)
    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()  # 배경 이미지 너비
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))  # 배경 이미지 표시
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))  # 배경 이미지 반복 표시
        if x_pos_bg <= -image_width:  # 배경이 화면 밖으로 나가면
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))  # 배경 이미지 반복 표시
            x_pos_bg = 0  # 배경 X 좌표 재설정
        x_pos_bg -= game_speed  # 배경 X 좌표 감소 (움직임)

    while run:  # 게임 루프
        for event in pygame.event.get():  # 이벤트 처리
            if event.type == pygame.QUIT:  # 창을 닫으면
                run = False  # 게임 종료

        SCREEN.fill((255, 255, 255))  # 화면 배경색 설정
        userInput = pygame.key.get_pressed()  # 사용자 입력 처리

        player.draw(SCREEN)  # 캐릭터 그리기
        player.update(userInput)  # 캐릭터 업데이트

        if len(obstacles) == 0:  # 장애물이 없으면
            if random.randint(0, 2) == 0:  # 무작위로 장애물 생성
                obstacles.append(SmallCactus(SMALL_CACTUS))  # 작은 선인장 생성
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))  # 큰 선인장 생성
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))  # 새 생성

        for obstacle in obstacles:  # 모든 장애물 업데이트 및 그리기
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):  # 충돌 시
                pygame.time.delay(2000)  # 2초 대기
                death_count += 1  # 사망 횟수 증가
                menu(death_count)  # 메뉴 함수 호출

        background()  # 배경 업데이트

        cloud.draw(SCREEN)  # 구름 그리기
        cloud.update()  # 구름 업데이트

        score()  # 점수 표시

        clock.tick(30)  # FPS 설정
        pygame.display.update()  # 화면 업데이트


### 메뉴 함수 (게임 오버 시 표시 및 재시작 처리)
def menu(death_count):
    global points  # 전역 변수
    run = True  # 메뉴 실행 상태
    while run:
        SCREEN.fill((255, 255, 255))  # 화면 배경색 설정
        font = pygame.font.Font('freesansbold.ttf', 30)  # 폰트 설정

        if death_count == 0:  # 첫 번째 시작 시
            text = font.render("Press any Key to Start", True, (0, 0, 0))  # 시작 텍스트
        elif death_count > 0:  # 재시작 시
            text = font.render("Press any Key to Restart", True, (0, 0, 0))  # 재시작 텍스트
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))  # 점수 텍스트
            scoreRect = score.get_rect()  # 점수 텍스트의 사각형 구역 설정
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)  # 점수 위치 설정
            SCREEN.blit(score, scoreRect)  # 화면에 점수 표시
        textRect = text.get_rect()  # 텍스트의 사각형 구역 설정
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # 텍스트 위치 설정
        SCREEN.blit(text, textRect)  # 화면에 텍스트 표시
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))  # 캐릭터 이미지 표시
        pygame.display.update()  # 화면 업데이트
        for event in pygame.event.get():  # 이벤트 처리
            if event.type == pygame.QUIT:  # 창을 닫으면
                pygame.quit()  # Pygame 종료
                run = False  # 메뉴 종료
            if event.type == pygame.KEYDOWN:  # 키 입력 시
                main()  # 게임 재시작

menu(death_count=0)  # 게임 시작
