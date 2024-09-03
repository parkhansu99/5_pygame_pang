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

    ############################
    # 3. 게임 캐릭터 위치 정의

            
    ############
    # 4.충돌 처리


    #################
    # 5. 화면에 그리기
    screen.blit(background, (0, 0))
    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    pygame.display.update()

# pygame 종료
pygame.quit()