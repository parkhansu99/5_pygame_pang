# 그림판으로 배경 만들기

# frame_not working.py을 그대로 복사 붙여넣기하며 시작하기

import pygame
import os

##################################
# 기본 초기화 (반드시 해야 하는 것들)

pygame.init() # 초기화 (반드시 필요)


# 화면 크기 설정하기

screen_width = 640 # 가로 크기
screen_height = 480 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정

pygame.display.set_caption("게임 이름") # 게임 이름

# FPS

clock = pygame.time.Clock()

#######################################################
# 1. 사용자 게임 초기화 (배경화면, 게임 이미지, 좌표, 폰트 등)

current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
image_path = os.path.join(current_path, "images") # 현재의 경로에서 추가적으로 images라는 폴더로 가면 이미지 경로

# 배경 만들기 (하늘 부분)

background = pygame.image.load(os.path.join(image_path, "background.png")) # 이미지 경로에서 추가적으로 background.png로 가면 배경 이미지인데 배경으로 그것을 로드하겠다는 것 (단, 이러한 방법은 경로가 바뀌는 경우 치명적인 오류로 이어질 수 있음)

# 무대 만들기 (땅바닥 부분)

stage = pygame.image.load(os.path.join(image_path, "stage.png")) # 이미지 경로에서 추가적으로 stage.png로 가면 무대 이미지인데 무대로 그것을 로드하겠다는 것 (단, 이러한 방법은 경로가 바뀌는 경우 치명적인 오류로 이어질 수 있음)
stage_size = stage.get_rect().size
stage_height = stage_size[1] # 무대 높이 위에 캐릭터를 두기 위해 사용

# 캐릭터 만들기

character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width/2) - (character_width/2)
character_y_pos = screen_height - character_height - stage_height

# 캐릭터 이동 방향

character_to_x = 0

# 캐릭터 이동 속도

character_speed = 5

# 무기 만들기

weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한 번에 여러 발 발사 가능

weapons = []

# 무기 이동 속도

weapon_speed = 10

# 공 만들기 (4개 크기에 대해 따로 처리)

ball_images = [
    pygame.image.load(os.path.join(image_path, "ballon1.png")),
    pygame.image.load(os.path.join(image_path, "ballon2.png")),
    pygame.image.load(os.path.join(image_path, "ballon3.png")),
    pygame.image.load(os.path.join(image_path, "ballon4.png"))
]

# 공 크기에 따른 최초 스피드

ball_speed_y = [-18, -15, -12, -9]

# 공들

balls = []

# 최초 발생하는 큰 공 추가

balls.append({
    "pos_x" : 50, # 공의 x 좌표
    "pos_y" : 50, # 공의 y 좌표
    "img_idx" : 0, # 공의 이미지 인덱스
    "to_x" : 3, # x축 이동방향, -3이면 왼쪽, 3이면 오른쪽
    "to_y" : -6, # Y축 이동방향
    "init_spd_y" : ball_speed_y[0], # 최초 속도 (리스트의 첫번째 값으로 설정)
})

# 사라질 무기, 공 정보 저장 변수

weapon_to_remove = -1
ball_to_remove = -1


# 이벤트 루프 (게임창을 계속 띄워주는 역할)
running = True 
while running: # 게임이 진행중인 동안
    dt = clock.tick(60) # 게임화면의 초당 프레임 수를 설정
    # print("fps : " + str(clock.get_fps()))
    
    #################################
    # 2. 이벤트 처리 (키보드, 마우스 등)
    
    for event in pygame.event.get(): # 어떤 이벤트가 발생했는가
        if event.type == pygame.QUIT: # 창을 닫으면
            running = False # 파이썬 종료
        if event.type == pygame.KEYDOWN: # 키가 눌리면
            if event.key == pygame.K_LEFT: # 왼쪽 방향키를 누르면
                character_to_x -= character_speed # 캐릭터를 왼쪽으로 이동
            elif event.key == pygame.K_RIGHT: # 오른쪽 방향키를 누르면
                character_to_x += character_speed # 캐릭터를 오른쪽으로 이동
            elif event.key == pygame.K_SPACE: # 스페이스 방향키를 누르면
                weapon_pos_x = character_x_pos + (character_width / 2) - (weapon_width / 2) # 무기의 X축 위치
                weapon_pos_y = character_y_pos
                weapons.append([weapon_pos_x, weapon_pos_y])

        if event.type == pygame.KEYUP: # 키에서 손을 떼면
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: # 왼쪽 혹은 오른쪽 방향키에서 손을 떼면
                character_to_x = 0 # 더 이상 움직이지 않음
            

    ############################
    # 3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x
    if character_x_pos < 0 : # 캐릭터의 왼쪽 끝 영역보다 낮은 위치이면
        character_x_pos = 0 # 계속 왼쪽 끝 영역에 머무르도록 함
    elif character_x_pos > screen_width - character_width: # 캐릭터의 오른쪽 끝 영역보다 높은 위치이면
        character_x_pos = screen_width - character_width  # 계속 오른쪽 끝 영역에 머무르도록 함            

    # 무기 위치 조정

    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons] # 무기의 경우 x좌표는 그대로, y좌표만 변화하도록 함

    # 천장에 닿은 무기 없애기

    weapons =[[w[0], w[1]] for w in weapons if w[1] > 0]

    # 공 위치 정의

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size # 볼 이미지 순번에 해당하는 이미지를 가져옴
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # 가로 벽에 닿으면 공 이동 위치 변경 (튕기는 효과)

        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1 # 튕기는 x축 방향을 반대로 바꿈
        
        # 세로 위치
        # 처음 스테이지에 튕겨서 올라가는 처리
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else: # 그 외에 모든 경우에는 속도를 증가
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    ############
    # 4.충돌 처리
    
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        # 공 rect 정보 업데이트
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y
        # 공과 캐릭터 충돌
        if character_rect.colliderect(ball_rect):
            running = False
            break

        # 공과 무기 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # 무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # 충돌 체크
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx # 해당 무기 없애기 위한 값 설정
                ball_to_remove = ball_idx # 해당 공 없애기 위한 값 설정
                break

    # 충돌된 공 or 무기 없애기
    if ball_to_remove > -1: # 공이 충돌한 경우 (볼 인덱스 값으로 변경되어 -1보다 큰 상황임)
        del balls[ball_to_remove] # 무기 인덱스가 저장된 변수값 번째에 있는 볼을 제거함
        ball_to_remove = -1 # 다시 원래대로 안 없애기 설정

    if weapon_to_remove > -1: # 무기가 충돌한 경우 (무기 인덱스 값으로 변경되어 -1보다 큰 상황임)
        del weapons[weapon_to_remove]
        weapon_to_remove = -1 # 다시 원래대로 안 없애기 설정
    
    #################
    # 5. 화면에 그리기

    # (위 아래에 있는) 위치에 따라 순서(z축 위치)가 결정됨
    screen.blit(background, (0, 0))
    for weapon_pos_x, weapon_pos_y in weapons:
        screen.blit(weapon, (weapon_pos_x, weapon_pos_y))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    
    pygame.display.update()

# pygame 종료
pygame.quit()