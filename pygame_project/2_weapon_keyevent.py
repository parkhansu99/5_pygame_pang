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
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2) # 무기의 X축 위치
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

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


    ############
    # 4.충돌 처리
    

    #################
    # 5. 화면에 그리기

    # (위 아래에 있는) 위치에 따라 순서(z축 위치)가 결정됨
    screen.blit(background, (0, 0))
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    
    pygame.display.update()

# pygame 종료
pygame.quit()