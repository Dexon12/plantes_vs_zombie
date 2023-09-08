import arcade
from random import *
from time import *
class Window(arcade.Window):
    def __init__(self):
        super().__init__(1000, 600, "Plants vs zombies")
        self.BG = arcade.load_texture("background.jpg")
        self.BG_2 = arcade.load_texture("menu_vertical.png")
        self.plant = None
        self.plant_list = arcade.SpriteList()
        self.my_lawns = []
        self.my_money = 300
        self.seed_sound = arcade.load_sound("seed.mp3")
        self.music = arcade.load_sound("sunspawn.mp3")
        self.pea_sound = arcade.load_sound("peaspawn.mp3")
        self.grasswalk_1 = arcade.load_sound("grasswalk.mp3")
        arcade.play_sound(self.grasswalk_1)
        self.sun_list = arcade.SpriteList()
        self.time_down = time()
        self.pea_list = arcade.SpriteList()
        self.zombi_list = arcade.SpriteList()                
        self.zombi_time = time()
        self.zombi_2_time = time()
        self.zombi_3_time = time()
        self.stop_game = False
        self.stop_screen = arcade.load_texture("end.png")
        self.score = 0
    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(500, 300, 1000, 600, self.BG)
        arcade.draw_texture_rectangle(60, 300, 130, 600, self.BG_2)
        if self.plant != None:
            self.plant.draw()
        self.plant_list.draw()
        arcade.draw_text(f"{self.my_money}", 30, 490, arcade.color.BROWN, 30)
        self.sun_list.draw()
        self.pea_list.draw()
        self.zombi_list.draw()
        if self.stop_game:
            arcade.draw_texture_rectangle(500,300,1000,600,self.stop_screen )
        
            
    def on_mouse_press(self,x,y,button,modifiers):
        if 10 <x<110 and 370<y<480:
            print("sunflower")
            self.plant = Sunflower()
            arcade.play_sound(self.seed_sound)
            if self.plant.cost > self.my_money:
                self.plant = None
            
        if 10<x<110 and 255<y<365:
            print("peashooter")
            self.plant = Pea()
            arcade.play_sound(self.seed_sound)
            if self.plant.cost > self.my_money:
                self.plant = None
            

        if 10<x<110 and 140<y<250:
            self.plant = Nut()
            arcade.play_sound(self.seed_sound)
            print("Wallnut")
            if self.plant.cost > self.my_money:
                self.plant = None
            
        if 10<x<110 and 25<y<135:
            self.plant = Tree()
            arcade.play_sound(self.seed_sound)
            print("torchwood")
            if self.plant.cost > self.my_money:
                self.plant = None

        for sun in self.sun_list:
            if sun.right>x>sun.left and sun.bottom<y<sun.top:
                sun.kill()
                self.my_money += 25
        if self.plant != None:
            self.plant.center_x = x
            self.plant.center_y = y
            self.plant.alpha = 100
    def on_mouse_release(self,x,y,button,modifiers):
        if self.plant != None and 250<x<960 and 30<y<526:
            center_x,column = Lawn_x(x)
            center_y,line = Lawn_y(y)
            if (line,column) not in self.my_lawns and self.plant.cost <= self.my_money:
                self.my_money -= self.plant.cost
                self.plant.planting(center_x,center_y,line,column)
                self.my_lawns.append((line,column))
                                                                    
                self.plant.alpha = 255
                self.plant_list.append(self.plant)
                self.plant = None
        elif self.plant != None and 0<x<250:
            self.plant = None
    def on_mouse_motion(self,x,y,dx,dy):
        if self.plant != None:
            self.plant.center_x = x
            self.plant.center_y = y
    def update(self,delta_time):
        if self.stop_game:
            quit()
        if self.stop_game == False:
            if self.plant != None:
                self.plant.update()
                self.plant.update_animation()
            self.plant_list.update()
            self.plant_list.update_animation()
            self.sun_list.update()
            if time() - self.time_down > 20:
                self.sun_1 = Down_sun()
                self.sun_list.append(self.sun_1)
                self.time_down = time()
            self.pea_list.update()
            self.zombi_list.update()
            self.zombi_list.update_animation()
            if time() - self.zombi_time > 10:
                center_y,line = Lawn_y(randint(30,520))
                self.zombi_1 = Difficult_zombi(line)
                self.zombi_1.center_y = center_y
                self.zombi_list.append(self.zombi_1)
                self.zombi_time = time()
            if time() - self.zombi_2_time > 15:
                center_y,line = Lawn_y(randint(30,520))
                self.zombi_2 = Conus_zombi(line)
                self.zombi_2.center_y = center_y
                self.zombi_list.append(self.zombi_2)
                self.zombi_2_time = time()
            if time() - self.zombi_3_time > 30:
                center_y,line = Lawn_y(randint(30,520))
                self.zombi_3 = Buck_zombi(line)
                self.zombi_3.center_y = center_y
                self.zombi_list.append(self.zombi_3)
                self.zombi_3_time = time()
            if self.score >= 1:
                self.stop_game = True
                self.stop_screen = arcade.load_texture("logo.png")
            
class Plants(arcade.AnimatedTimeBasedSprite):
    def __init__(self,health,cost):
        super().__init__()
        self.scale = 0.12
        self.health = health
        self.cost = cost
        self.line = 0
        self.column = 0
    def update(self):
        if self.health <= 0:
            self.kill()
            window.my_lawns.remove((self.line,self.column))
    def planting(self,x,y,line,column):
        self.center_x = x
        self.center_y = y
        self.line = line
        self.column = column
        
class Sunflower(Plants):
    def __init__(self):
        super().__init__(80,50)
        cadr_1 = arcade.AnimationKeyframe(0,300,arcade.load_texture("sun1.png"))
        self.frames.append(cadr_1)
        cadr_2 = arcade.AnimationKeyframe(1,300,arcade.load_texture("sun2.png"))
        self.frames.append(cadr_2)
        self.now_time = time()
        

        
        
    def update(self):
        super().update()
        if time() - self.now_time > 15:
            self.sun_2 = Sun(self.center_x + 20,self.center_y + 30)
            window.sun_list.append(self.sun_2)
            self.now_time = time()
            arcade.play_sound(window.music)
            
        
class Down_sun(arcade.Sprite):
    def __init__(self):
        super().__init__("sun.png",0.12)
        self.center_x = randint(250,960)
        self.center_y = 600
        self.change_y = -1
    def update(self):
        self.angle += 1
        self.center_y += self.change_y
        if self.center_y <= 0:
            self.kill()
        
class Sun(arcade.Sprite):
    def __init__(self,x,y):
        super().__init__("sun.png",0.12)
        self.center_x = x
        self.center_y = y
        self.sun_time = time()
    def update(self):
        self.angle += 1
        if time() - self.sun_time > 3:
            self.kill()

class Pea(Plants):
    def __init__(self):
       super().__init__(100,100)
       cadr_1 = arcade.AnimationKeyframe(0,250,arcade.load_texture("pea1.png"))
       self.frames.append(cadr_1)
       cadr_2 = arcade.AnimationKeyframe(1,250,arcade.load_texture("pea2.png"))
       self.frames.append(cadr_2)
       cadr_3 = arcade.AnimationKeyframe(2,250,arcade.load_texture("pea3.png"))
       self.frames.append(cadr_3)
       self.pea_time = time()
    def update(self):
        super().update()
        zombi_line = False
        for zombi in window.zombi_list:
            if zombi.line == self.line:
                zombi_line = True
                
        if time() - self.pea_time > 2 and zombi_line == True:
            self.pea = Pea_bullet(self.center_x + 10,self.center_y + 10)
            window.pea_list.append(self.pea)
            self.pea_time = time()
        

class Pea_bullet(arcade.Sprite):
    def __init__(self,x,y):
        super().__init__("bul.png",0.12)
        self.center_x = x
        self.center_y = y
        self.damage = 15
        self.change_x = 5
    def update(self):
        self.center_x += self.change_x
        if self.center_x >= 1000:
            self.kill()
        hit_list = arcade.check_for_collision_with_list(self,window.zombi_list)
        for zombi in hit_list:
            zombi.health -= self.damage
            self.kill()
            
        
class Nut(Plants):
    def __init__(self):
        super().__init__(500,50)
        cadr_1 = arcade.AnimationKeyframe(0,1,arcade.load_texture("nut1.png"))
        self.frames.append(cadr_1)
        cadr_5 = arcade.AnimationKeyframe(1,3000,arcade.load_texture("nut1.png"))
        self.frames.append(cadr_5)
        cadr_2 = arcade.AnimationKeyframe(2,300,arcade.load_texture("nut2.png"))
        self.frames.append(cadr_2)
        cadr_3 = arcade.AnimationKeyframe(3,200,arcade.load_texture("nut3.png"))
        self.frames.append(cadr_3)
    
class Tree(Plants):
    def __init__(self):
        super().__init__(125,150)
        cadr_1 = arcade.AnimationKeyframe(0,150,arcade.load_texture("tree1.png"))
        self.frames.append(cadr_1)
        cadr_2 = arcade.AnimationKeyframe(1,150,arcade.load_texture("tree2.png"))
        self.frames.append(cadr_2)
        cadr_3 = arcade.AnimationKeyframe(2,150,arcade.load_texture("tree3.png"))
        self.frames.append(cadr_3)

    def update(self):
        super().update()
        tree_hit = arcade.check_for_collision_with_list(self, window.pea_list)
        for pea in tree_hit:
            pea.damage = 30
            pea.texture = arcade.load_texture("firebul.png")

class Zombi(arcade.AnimatedTimeBasedSprite):
    def __init__(self,health,lines):
        super().__init__()
        self.scale = 0.1
        self.health = health
        self.line = lines
        self.center_x = 1000
        self.change_x = - 0.2
        
    def update(self):
        self.center_x += self.change_x
        if self.health <= 0:
            self.kill()
            window.score += 1
        eating = False
        zombi_hit = arcade.check_for_collision_with_list(self,window.plant_list)
        for plant in zombi_hit:
            if plant.line == self.line:
                plant.health -= 1
                eating = True
        if eating == True:
            self.change_x = 0
            self.angle = 15
        else:
            self.change_x = -0.2
            self.angle = 0
        if self.center_x < 200:
            window.stop_game = True
            
            
                
class Difficult_zombi(Zombi):
    def __init__(self,line):
        super().__init__(75,line)
        cadr_1 = arcade.AnimationKeyframe(0,1,arcade.load_texture("zom1.png"))
        self.frames.append(cadr_1)
        cadr_2 = arcade.AnimationKeyframe(1,600,arcade.load_texture("zom1.png"))
        self.frames.append(cadr_2)
        cadr_3 = arcade.AnimationKeyframe(2,600,arcade.load_texture("zom2.png"))
        self.frames.append(cadr_3)
        
class Conus_zombi(Zombi):
    def __init__(self,line):
        super().__init__(150,line)
        cadr_1 = arcade.AnimationKeyframe(0,1,arcade.load_texture("cone1.png"))
        self.frames.append(cadr_1)
        cadr_2 = arcade.AnimationKeyframe(1,600,arcade.load_texture("cone1.png"))
        self.frames.append(cadr_2)
        cadr_3 = arcade.AnimationKeyframe(2,600,arcade.load_texture("cone2.png"))
        self.frames.append(cadr_3)
class Buck_zombi(Zombi):
    def __init__(self,line):
        super().__init__(300,line)
        cadr_1 = arcade.AnimationKeyframe(0,1,arcade.load_texture("buck1.png"))
        self.frames.append(cadr_1)
        cadr_2 = arcade.AnimationKeyframe(1,600,arcade.load_texture("buck1.png"))
        self.frames.append(cadr_2)
        cadr_3 = arcade.AnimationKeyframe(2,600,arcade.load_texture("buck2.png"))
        self.frames.append(cadr_3)
                                          
    

def Lawn_x(x):
    if 250<x<=326:
        center_x = 290
        column = 1
    if 326<x<=400:
        center_x = 360
        column = 2
    if 400<x<485:
        center_x = 440
        column = 3
    if 485<x<560:
        center_x = 520
        column = 4
    if 560<=x<640:
        center_x = 600
        column = 5
    if 640<=x<715:
        center_x = 690
        column = 6
    if 715<=x<785:
        center_x = 740
        column = 7
    if 785<=x<870:
        center_x = 820
        column = 8
    if 870<=x<960:
        center_x = 920
        column = 9
    return center_x, column
def Lawn_y(y):
    if 29<y<130:
        center_y = 70
        line = 1
    if 130<=y<220:
        center_y = 180
        line = 2
    if 220<=y<320:
        center_y = 270
        line = 3
    if 320<=y<425:
        center_y = 375
        line = 4
    if 425<=y<530:
        center_y = 480
        line = 5
    return center_y,line
        
        
window = Window()
arcade.run()
