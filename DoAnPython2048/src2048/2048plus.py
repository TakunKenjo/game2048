# import thư viện
import pygame
import random

# Khai báo kích thước
SCREENWIDTH=960
SCREENHEIGHT=540

# Tạo biến point
point0=pygame.image.load(r'picture\0.png')
point2=pygame.image.load(r'picture\2.png')
point4=pygame.image.load(r'picture\4.png')
point8=pygame.image.load(r'picture\8.png')
point16=pygame.image.load(r'picture\16.png')
point32=pygame.image.load(r'picture\32.png')
point64=pygame.image.load(r'picture\64.png')
point128=pygame.image.load(r'picture\128.png')
point256=pygame.image.load(r'picture\256.png')
point512=pygame.image.load(r'picture\512.png')
point1024=pygame.image.load(r'picture\1024.png')
point2048=pygame.image.load(r'picture\2048.png')
# Khai báo class
class Button:
    # Constructor
    def __init__(self, image, x, y):
        self.image = pygame.transform.scale(image, image.get_size())
        self.rect = self.image.get_rect()
        self.rect.topleft = ((x - image.get_width() / 2), (y - image.get_height() / 2))
        self.clicked = False
        self.visible = False

    # Vẽ button lên màn hình
    def drawButton(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect.topleft)

    # Kiểm tra click button
    def clickButton(self, pos):
        if self.visible:
            if self.rect.collidepoint(pos):
                self.clicked = True
                self.visible = False
                pygame.mixer.music.load(merge_sound)
                pygame.mixer.music.play()

# Khai báo background
background=pygame.image.load(r'picture\mainbackground.png')
# Khai báo 3 button ở màn hình chính
play_button=Button(pygame.image.load(r'picture\playgame.png'), SCREENWIDTH / 2, SCREENHEIGHT / 2)
setting_button=Button(pygame.image.load(r'picture\settinggame.png'), SCREENWIDTH / 2, SCREENHEIGHT / 2 +80)
quit_button=Button(pygame.image.load(r'picture\quitgame.png'), SCREENWIDTH / 2, SCREENHEIGHT / 2 +80 +80)
# Khai báo màn hình chơi game
main_panel_game=pygame.image.load(r'picture\panelmaingame.png')
# Khai báo khung chơi game
BOARDSCREEN=pygame.image.load(r'picture\backgroundgame.png')
BOARD=[[(200,100),(305,100),(410,100),(515,100)],
       [(200,205),(305,205),(410,205),(515,205)],
       [(200,310),(305,310),(410,310),(515,310)],
       [(200,415),(305,415),(410,415),(515,415)]]
# Khởi tạo tọa độ cho bảng xếp hạng
HIGHSCORECHART=[[(229, 217, 242),(684,100,200,80)],
                [(245, 239, 255),(684,200,200,80)],
                 [(205, 193, 255),(684,300,200,80)],
                  [(165, 148, 249),(674,405,220,100)]]

# Khởi tạo biến restart
newgame_button=Button(pygame.image.load(r'picture\newgame.png'), 510, 45)
home_button=Button(pygame.image.load(r'picture\homeback.png'),90,50)

# Khởi tạo biến home
# Hàm lấy điểm ảnh
def get_point(point):
    if point==0:
        return point0
    elif point==2:
        return point2
    elif point==4:
        return point4
    elif point==8:
        return point8
    elif point==16:
        return point16
    elif point==32:
        return point32
    elif point==64:
        return point64
    elif point==128:
        return point128
    elif point==256:
        return point256
    elif point==512:
        return point512
    elif point==1024:
        return point1024
    elif point==2048:
        return point2048

# Hàm lấy điểm trong bảng xếp hạng
def getHighscore():
    with open("scorerank.txt", "r", encoding="utf-8") as file:
        data = file.readlines()

    scores = [(line.split("-")[0].strip(), int(line.split("-")[1])) for line in data]

    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True) 
    return sorted_scores

# Khai báo class Game
class Game:
    # Constructor
    def __init__(self, playername):
        self.playername=playername
        self.board = [[0] * 4 for _ in range(4)]
        self.game_over = False
        self.game_win = False  # Thêm biến game_win
        self.score=0
        for i in range(0,len(getHighscore())):
            if self.playername==getHighscore()[i][0]:
                self.best=getHighscore()[i][1]
                break
            else:
                self.best=0
        self.append_point()
        self.append_point()

    # Vẽ giao diện màn hình chơi game
    def draw_panel_game(self):
        screen.blit(main_panel_game,(0,0))
        screen.blit(BOARDSCREEN, (190,90))
        newgame_button.drawButton(screen)
        newgame_button.visible=True
        home_button.drawButton(screen)
        home_button.visible=True
        self.draw_chart()
        scoretext="Score: "+str(self.score)
        score = font.render(scoretext, True, (255, 255, 204))
        screen.blit(score,(200,10))
        besttext="Best: "+str(self.best)
        best=font.render(besttext,True,(255, 255, 204))
        screen.blit(best,(200,45))
        volume = font2.render("Volume: "+volume_text, True, (255, 251, 230))
        screen.blit(volume, (0, 0))
        for i in range(4):
            for j in range(4):
                screen.blit(get_point(self.board[i][j]),BOARD[i][j])

    # Vẽ giao diện bảng xếp hạng
    def draw_chart(self):
        exist = False
        with open("scorerank.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            file.close()
            
        with open("scorerank.txt", "w", encoding="utf-8") as file:
            file.seek(0)
            for line in lines:
                player_data = line.strip().split("-")
                playername = player_data[0]
                score = int(player_data[1])
                
                if self.playername == playername:
                    if self.score>score:
                        file.write(f"{self.playername}-{self.score}\n")
                    else :
                        file.write(f"{self.playername}-{score}\n")
                    exist = True
                else:
                    file.write(line)
            if not exist:
                file.write(f"{self.playername}-{self.score}\n")
        sorted_score = getHighscore()
        for i in range(0, 3):
            pygame.draw.rect(screen, HIGHSCORECHART[i][0], HIGHSCORECHART[i][1])
            if i < len(sorted_score):
                player_info ="RANK "+str(i+1)+": "+ sorted_score[i][0] + " - " + str(sorted_score[i][1]) 
                text_surface = font2.render(player_info, True, (0, 31, 63)) 
                text_rect = text_surface.get_rect()
                text_rect.center = HIGHSCORECHART[i][1][0] + HIGHSCORECHART[i][1][2] // 2, HIGHSCORECHART[i][1][1] + HIGHSCORECHART[i][1][3] // 2
                screen.blit(text_surface, text_rect) 
        
        pygame.draw.rect(screen, HIGHSCORECHART[3][0], HIGHSCORECHART[3][1])
        for i in range(0,len(sorted_score)):
            if self.playername==sorted_score[i][0]:
                index_of_player=i
                break
        player_info ="RANK "+str(index_of_player+1)+": "+ self.playername + " - " + str(self.score) 
        text_surface = font2.render(player_info, True, (255,255,255)) 
        text_rect = text_surface.get_rect()
        text_rect.center = HIGHSCORECHART[3][1][0] + HIGHSCORECHART[3][1][2] // 2, HIGHSCORECHART[3][1][1] + HIGHSCORECHART[3][1][3] // 2
        screen.blit(text_surface, text_rect)

    # Hàm random point
    def append_point(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_cells:
            row,col=random.choice(empty_cells)
            self.board[row][col] = random.choice([2,4])
            # Cập nhật ảnh tương đương với số(gtri)
            screen.blit(get_point(self.board[row][col]), BOARD[row][col])
    
    # Hàm hợp 2 phần tử
    def merge_cell(self, line):
        for i in range(len(line) - 1):
            if (line[i] == line[(i+1)]) and line[i] != 0:
                line[i] *= 2
                line[i + 1] = 0
                self.score+=line[i]
                if self.score>self.best:
                    self.best=self.score
                self.compact(line)
            elif (line[i] in  line[(i+1):]) and line[i] != 0:
                if line[i+2]==0:
                    line[i] *= 2
                    line[i + 3] = 0
                    self.score+=line[i]
                    if self.score>self.best:
                        self.best=self.score
                    self.compact(line)
                elif line[i+1]==0:
                    line[i] *= 2
                    line[i + 2] = 0
                    self.score+=line[i]
                    if self.score>self.best:
                        self.best=self.score
                    self.compact(line)

    # Compact - Cập nhật laị line (đẩy cell)
    def compact(self, line):
        zero_count = line.count(0)
        for _ in range(zero_count):
            line.remove(0)
            line.append(0)
        pygame.mixer.music.load(add_sound)
        pygame.mixer.music.play()

    # Move left
    def move_left(self):
        for row in self.board:
            self.merge_cell(row)
            empty_cells = row.count(0)
            for _ in range(empty_cells):
                row.remove(0)
                row.append(0)

    # Move right
    def move_right(self):
        for row in self.board:
            row.reverse()
            self.merge_cell(row)
            empty_cells = row.count(0)
            for _ in range(empty_cells):
                row.remove(0)
                row.append(0)
            row.reverse()

    # Move up
    def move_up(self):
        for col in range(4):
            column = [self.board[row][col] for row in range(4)]
            self.merge_cell(column)
            empty_cells = column.count(0)
            for _ in range(empty_cells):
                column.remove(0)
                column.append(0)
            for row in range(4):
                self.board[row][col] = column[row]

    # Move down
    def move_down(self):
         for col in range(4):
            column = [self.board[row][col] for row in range(3, -1, -1)]
            self.merge_cell(column)
            empty_cells = column.count(0)
            for _ in range(empty_cells):
                column.remove(0)
                column.append(0)
            for row in range(3, -1, -1):
                self.board[3 - row][col] = column[row]

    # draw game over
    def draw_over(self):
        pygame.draw.rect(screen, 'black', [205, 150, 400, 100], 0, 10)
        game_over_text1 = font.render('Game Over!', True, 'white')
        game_over_text2 = font.render('Click New Game To Restart!', True, 'white')
        screen.blit(game_over_text1, (320, 165))
        screen.blit(game_over_text2, (230, 205))

    # check game over
    def check_game_over(self):
        for row in self.board:
            if 0 in row:
                self.game_over = False
                return

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if j < len(self.board[i]) - 1 and self.board[i][j] == self.board[i][j + 1]:
                    self.game_over = False
                    return
                if i < len(self.board) - 1 and self.board[i][j] == self.board[i + 1][j]:
                    self.game_over = False
                    return
        self.game_over = True
        return
    
    # draw game win
    def draw_win(self):
        pygame.draw.rect(screen, 'green', [205, 150, 400, 100], 0, 10)
        game_over_text1 = font.render('You Win!', True, 'white')
        game_over_text2 = font.render('Click New Game To Restart!', True, 'white')
        screen.blit(game_over_text1, (320, 165))
        screen.blit(game_over_text2, (230, 205))

    # check game win
    def check_game_win(self):
        for row in self.board:
            if 2048 in row:
                self.game_win = True
                return
        self.game_win = False

    # Hàm nhận keydown
    def play(self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move_left()
                self.append_point()
            elif event.key == pygame.K_RIGHT:
                self.move_right()
                self.append_point()
            elif event.key == pygame.K_UP:
                self.move_up()
                self.append_point()
            elif event.key == pygame.K_DOWN:
                self.move_down()
                self.append_point()
            event.key="null"
        if self.game_over:
            self.draw_over()
        if self.game_win:  # Kiểm tra nếu thắng
            self.draw_win()

# Khai báo screen
pygame.init()
screen=pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
screen.blit(background,(0,0))

# Khai báo font chữ
font = pygame.font.Font(r'font\Cabin-VariableFont_wdth,wght.ttf', 30)
font2 = pygame.font.Font(r'font\Cabin-VariableFont_wdth,wght.ttf', 16)

# Khai báo âm thanh
merge_sound=r'sound\90s-game-ui-1-185094.mp3'
add_sound=r'sound\gameboy-pluck-41265.mp3'
panel_play=Game("")
# Khởi tạo giá trị âm lượng ở home
volume_text="Medium"
# Khởi tạo tên player
player_text=''
# Khởi tạo giao diện setting
backgroundsetting=pygame.image.load(r'picture\volumebackground.png')
# Khởi tạo button âm lượng
low_button=Button(pygame.image.load(r'picture\low.png'),360,400)
medium_button=Button(pygame.image.load(r'picture\medium.png'),480,400)
high_button=Button(pygame.image.load(r'picture\high.png'),600,400)

# Vẽ thêm giao diện bên home
def draw_home():
    screen.blit(background,(0,0))
    volume = font2.render("Volume: "+volume_text, True, (255, 251, 230))
    screen.blit(volume, (0, 0))
    play_button.drawButton(screen)
    play_button.visible=True
    setting_button.drawButton(screen)
    setting_button.visible=True
    quit_button.drawButton(screen)
    quit_button.visible=True
    text_surface = font.render("Enter your name: " + player_text, True, (255, 251, 230))
    panel_play.playername=player_text
    screen.blit(text_surface, (20, 500))

play=False
# MAIN
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.MOUSEBUTTONDOWN:
            play_button.clickButton(pygame.mouse.get_pos())
            newgame_button.clickButton(pygame.mouse.get_pos())
            home_button.clickButton(pygame.mouse.get_pos())
            quit_button.clickButton(pygame.mouse.get_pos())
            setting_button.clickButton(pygame.mouse.get_pos())
            low_button.clickButton(pygame.mouse.get_pos())
            medium_button.clickButton(pygame.mouse.get_pos())
            high_button.clickButton(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                active = False
            elif event.key == pygame.K_BACKSPACE:
                player_text = player_text[:-1]
                screen.blit(background, (0, 0))
            else:
                player_text += event.unicode

    if player_text!="":
        background=pygame.image.load(r'picture\mainbackground.png')
    # Nếu nút platext_rect)y_button được chọn
    if play_button.clicked==True:
        play_button.clicked=False
        if(player_text==""):
            text = font2.render("Bạn cần nhập tên trước khi chơi", True, (255,0,0))
            text_rect = text.get_rect(center=(130, 490))
            background.blit(text, text_rect)
        else:
            play=True
            panel_play=Game(player_text)

    # Kiểm tra nếu click restart
    if newgame_button.clicked:
        play=True
        panel_play=Game(player_text)
        panel_play.draw_panel_game()
        panel_play.play()
        newgame_button.clicked=False

    # Kiểm tra sự kiện click nút home
    if home_button.clicked:
        play=False
        draw_home()
        home_button.clicked=False

    # Nếu không được chơi
    if play==False:
        # Tạo sự kiện nút setting
        if setting_button.clicked==True:
            play_button.visible=False
            setting_button.visible=False
            quit_button.visible=False
            screen.blit(backgroundsetting,(0,0))
            low_button.drawButton(screen)
            low_button.visible=True
            medium_button.drawButton(screen)
            medium_button.visible=True
            high_button.drawButton(screen)
            high_button.visible=True
            if low_button.clicked==True:
                setting_button.clicked=False
                low_button.clicked=False
                volume_text="Low"
                pygame.mixer.music.set_volume(0.1)
            elif medium_button.clicked==True:
                setting_button.clicked=False
                medium_button.clicked=False
                volume_text="Medium"
                pygame.mixer.music.set_volume(0.5)
            elif high_button.clicked==True:   
                setting_button.clicked=False
                high_button.clicked=False
                volume_text="High"
                pygame.mixer.music.set_volume(1)
        else:
            draw_home()
    elif play==True:
        play_button.visible=False
        setting_button.visible=False
        quit_button.visible=False
        panel_play.draw_panel_game()
        panel_play.play()
        panel_play.check_game_over()
        panel_play.check_game_win()  # Gọi hàm kiểm tra thắng

    pygame.display.update() 

    # Tạo sự kiện nút quit
    if quit_button.clicked==True:
        running=False
    


pygame.quit()