import tkinter
import random


class ShootGame:


    def __init__(self):

        # make an image
        self.image = tkinter.Canvas(bg='black', height=700, width=700)
        self.image.pack()

        # create a green line 
        self.image.create_line(0, int(self.image['height']) / 8, int(self.image['width']), int(self.image['height']) / 8,
                               fill='#25EC13', width=10)
        

        # right, left edge of a plane, and also the point of plane
        self.right_edge_plane = (int(self.image['width']) / 2) + 30
        self.left_edge_plane = (int(self.image['width']) / 2) - 30
        self.point_plane = int(self.image['width']) / 2


        # bullet tags, and number of bullets
        self.bullets = []
        self.n_bullet = 0
        
        # targets, key is the target's tag and values its moving direction, and number of targets
        self.targets = {}
        self.n_target = 0

        # targets and bullets to remove from the screen
        self.remove_targets = []
        self.remove_bullets = []
        

        # spawn rate of targets, target's speed and bullet travel speed, all in miliseconds
        self.spawn_time = 8000
        self.target_speed = 500
        self.bullet_speed = 10


        # so far haven't lost
        self.not_lost = True

        # score and hp
        self.score = 0
        self.hp = 7


        # first is 0 score
        self.score_text = self.image.create_text(int(self.image['width']) / 6, int(self.image['height']) / 15,
                                                 text='SCORE: ' + str(self.score), font='Arial 30', fill='white')
        

        # call methods and also bind some keyboard chars
        self.make_plane()
        self.make_target()
        
        self.move_bullet()
        self.move_targets()

        self.remove()

        self.hearts()


        self.image.bind_all('<Right>', self.operate_plane)
        self.image.bind_all('<Left>', self.operate_plane)
        self.image.bind_all('<Up>', self.operate_plane)



    # number of hearts displayed on the screen
    def hearts(self):

        for i in range(self.hp):
            self.image.delete('heart' + str(i))


        self.hp -= 1
        
        x_heart = int(self.image['width']) * 10 / 11
        y_heart = int(self.image['height']) / 10

        for i in range(self.hp):

            # HEART POLYGON
            self.image.create_polygon(x_heart, y_heart,
                                              
                                      x_heart - 30, y_heart - 30,
                                      x_heart - 30, y_heart - 40,
                                      x_heart - 15, y_heart - 50,
                                      
                                      x_heart, y_heart - 40,

                                      x_heart + 15, y_heart - 50,
                                      x_heart + 30, y_heart - 40,
                                      x_heart + 30, y_heart - 30,
                                      
                                      fill = 'red', outline='#fc8403', width=2, tag='heart' + str(i))

            x_heart -= 70


        # if 0 hp, stop game and type game over
        if self.hp <= 0:
            self.not_lost = False
            self.image.create_text(int(self.image['width']) / 2, int(self.image['height']) / 2, text='GAME OVER !!!', font='Arial 60', fill='#cf1f1f')


    # create a plane
    def make_plane(self):
        
        # draw a turret for plane
        self.image.create_rectangle(self.left_edge_plane + 22, (int(self.image['height'])) - (int(self.image['height']) / 10),
                                    self.right_edge_plane - 22, (int(self.image['height'])) - (int(self.image['height']) / 25),
                                    fill='#BCBCBC', outline='#07FFE7', width=2, tag='plane')
        
        # draw a plane
        self.image.create_polygon(self.point_plane, (int(self.image['height']) - (int(self.image['height']) / 15)),
                                  self.left_edge_plane, (int(self.image['height']) - (int(self.image['height']) / 15)) + 30,
                                  self.right_edge_plane, int(self.image['height']) - (int(self.image['height']) / 15) + 30,
                                  fill='#ECE929', outline='#6203C1', width=2, tag='plane')


    # create a bullet
    def create_bullet(self):

        # add specific bullet into the list of bullets
        self.bullets.append('bullet' + str(self.n_bullet))
        
        # make a bullet 
        self.image.create_oval(self.left_edge_plane + 22, (int(self.image['height'])) - (int(self.image['height']) / 8),
                               self.right_edge_plane - 22, (int(self.image['height'])) - (int(self.image['height']) / 10),
                               fill='white', outline='white', tag='bullet' + str(self.n_bullet))



    # create that target
    def make_target(self):

        # decide if spawns from left or right edge of screen
        which_side_spawn = random.choice(['right', 'left'])
        

        # make target and decide on which side it spawn, in what direction it move (from right edge = moving left, from left edge = moving right)
        if which_side_spawn == 'right':
            edge_coord = int(self.image['width'])
            
            self.image.create_rectangle(edge_coord, int(self.image['height']) / 7,
                                        edge_coord + 40, int(self.image['height']) / 5,
                                        fill='#F90000', outline='white', width=2, tag='target' + str(self.n_target))

            self.targets['target' + str(self.n_target)] = -30


        elif which_side_spawn == 'left':
            
            edge_coord = -40
            
            self.image.create_rectangle(edge_coord, int(self.image['height']) / 7,
                                        edge_coord + 40, int(self.image['height']) / 5,
                                        fill='#F90000', outline='white', width=2, tag='target' + str(self.n_target))
        
            self.targets['target' + str(self.n_target)] = 30


        self.n_target += 1

        if self.not_lost:
            self.image.after(self.spawn_time, self.make_target)

        

    def move_targets(self):

        # targets to remove, targets moving to the right and to the left, if they pass the screen edges
        remove_right_moving = [target for target, move_direction in self.targets.items() if self.targets[target] == 30 and self.image.coords(target)[0] >= int(self.image['width'])]
        remove_left_moving = [target for target, move_direction in self.targets.items() if self.targets[target] == -30 and self.image.coords(target)[2] <= 0]

        self.remove_targets = remove_right_moving + remove_left_moving

        
        # move targets
        for target in self.targets:
            self.image.move(target,  self.targets[target], 0)


        if self.not_lost:
            self.image.after(self.target_speed, self.move_targets)


    def move_bullet(self):

        # remove bullet when they pass green line, also when made a shot and didn't shoot the target, hp - 1
        for bullet in self.bullets:
            if self.image.coords(bullet)[1] <= int(self.image['height']) / 8:
                self.remove_bullets.append(bullet)
    
                self.hearts()
                

        # if you shoot a target score + 1
        for bullet in self.bullets:
            for target in self.targets:

                if self.image.coords(bullet)[2] >= self.image.coords(target)[0] and self.image.coords(bullet)[0] <= self.image.coords(target)[2]\
                   and self.image.coords(bullet)[1] <= self.image.coords(target)[3]:
                    
                    self.raise_score()
            
                    self.remove_bullets.append(bullet)
                    self.remove_targets.append(target)
                    

        # make bullets move
        for bullet in self.bullets:
            self.image.move(bullet, 0, -10)


        if self.not_lost:
            self.image.after(self.bullet_speed, self.move_bullet)
            
            
    # move plane with left and right arrows
    def operate_plane(self, event):
        
        self.event = event
        self.operation = self.event.keysym


        # move to the right
        if self.operation == 'Right':
            
            self.left_edge_plane += 10
            self.right_edge_plane += 10
            
            self.image.move('plane', 10, 0)

            # can move through the edges like in snake game
            if self.left_edge_plane >= int(self.image['width']):
                self.image.delete('plane')
                
                self.left_edge_plane = -60
                self.right_edge_plane = 0
                self.point_plane = - 30
                
                self.make_plane()
                

        # move to the left
        elif self.operation == 'Left':
            
            self.left_edge_plane -= 10
            self.right_edge_plane -= 10
            
            self.image.move('plane', -10, 0)

            # go through the edges like in snake
            if self.right_edge_plane <= 0:
                self.image.delete('plane')
                
                self.left_edge_plane = int(self.image['width'])
                self.right_edge_plane = int(self.image['width']) + 60
                self.point_plane = int(self.image['width']) + 30
                
                self.make_plane()


        # shoot a bullet
        elif self.operation == 'Up':
            self.create_bullet()
            self.n_bullet += 1


    # raise score, if target is shot
    def raise_score(self):

        self.score += 1

        # make it a little difficult, every 4th score
        if self.score % 4 == 0:
            self.spawn_time -= 1000
            self.target_speed -= 100
            self.bullet_speed += 10


        # type score, num of points
        self.image.delete(self.score_text)
        self.score_text = self.image.create_text(int(self.image['width']) / 6, int(self.image['height']) / 15,
                                                 text='SCORE: ' + str(self.score), font='Arial 30', fill='white')


    # remove all unnecessary bullets and targets
    def remove(self):

        # remove and delete from screen bullets
        for remove_bullet in self.remove_bullets:
            self.image.delete(remove_bullet)
                
            self.bullets.remove(remove_bullet)
            self.remove_bullets.remove(remove_bullet)

        # remove and delete from screen targets
        for remove_target in self.remove_targets:
            self.image.delete(remove_target)
            
            del self.targets[remove_target]
            self.remove_targets.remove(remove_target)


        if self.not_lost:
            self.image.after(10, self.remove)


p = ShootGame()
