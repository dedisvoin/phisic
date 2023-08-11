from library.lib import *

win = Window(size=[1200,750])

class Rect(Vector2):
    @overload
    def __init__(self, x: float, y: float, w: float, h: float) -> "Rect":
        ...

    @overload
    def __init__(self, pos: Tuple[float, float], size: Tuple[float, float]) -> "Rect":
        ...

    def __init__(self, *args):
        self.__args_wrapper(*args)
        self.colliding = True
        self.id = random.randint(0,99999999999999)

    def __args_wrapper(self, *args):
        if len(args) == 4:
            _x = args[0]
            _y = args[1]
            self._w = args[2]
            self._h = args[3]
        elif len(args) == 2:
            _x = args[0][0]
            _y = args[0][1]
            self._w = args[1][0]
            self._h = args[1][1]
        super().__init__(_x, _y)

    def draw(self, win: Window):
        Draw.draw_rect(win, self.xy, self.wh, "red", 1)

    def collide_point(self, point: Tuple[float, float] | Vector2) -> bool:
        px, py = 0, 0
        if isinstance(point, Vector2):
            px = point.x
            py = point.y
        if isinstance(point, (list, tuple)):
            px = point[0]
            py = point[1]

        if (
            self.x < px
            and px < self.x + self.w
            and self.y < py
            and py < self.y + self.h
        ):
            return True

        return False

    def collide_rect(self, rect: "Rect", win: None = None):
        if self.colliding:
            min_x = min(self._x, rect._x)
            min_y = min(self._y, rect._y)

            max_x = max(self._x + self._w, rect._x + rect._w)
            max_y = max(self._y + self._h, rect._y + rect._h)

            if win is not None:
                Draw.draw_rect(
                    win,
                    [min_x - 2, min_y - 2],
                    [max_x - min_x + 4, max_y - min_y + 4],
                    "Blue",
                    2,
                )

            dist_w = distance([min_x, min_y], [max_x, min_y])
            dist_h = distance([min_x, min_y], [min_x, max_y])
            if dist_w < self._w + rect._w and dist_h < self._h + rect._h:
                return True
        return False

    @property
    def wh(self) -> Tuple[float, float]:
        return [self._w, self._h]
    
    @wh.setter
    def wh(self, size_: Tuple[float,float]):
        self._w = int(size_[0])
        self._h = int(size_[1])

    @property
    def w(self) -> float:
        return self._w

    @w.setter
    def w(self, w: float):
        self._w = w

    @property
    def h(self) -> float:
        return self._h

    @h.setter
    def h(self, h: float):
        self._h = h

    @property
    def y_up(self) -> float:
        return self._y

    @y_up.setter
    def y_up(self, y: float):
        self._y = y

    @property
    def y_down(self) -> float:
        return self._y + self._h

    @y_down.setter
    def y_down(self, y: float):
        self._y = y - self._h

    @property
    def x_left(self) -> float:
        return self._x

    @x_left.setter
    def x_left(self, x: float):
        self._x = x

    @property
    def x_right(self) -> float:
        return self._x + self._w

    @x_right.setter
    def x_right(self, x: float):
        self._x = x - self._w
        
    @property
    def center(self):
        return [self._x+self._w/2, self._y+self._h/2]
    
    @property
    def center_x(self):
        return self._x+self._w/2
    
    @property
    def center_y(self):
        return self._y+self._h/2
    
    @center_x.setter
    def center_x(self, _x:int):
        self._x = _x-self._w/2
    
    @center_y.setter
    def center_y(self, _y:int):
        self._y = _y-self._h/2
    
    @center.setter
    def center(self, pos):
        self._x = pos[0]-self._w/2
        self._y = pos[1]-self._h/2
        

class Collider():
    def __init__(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        speed: Vector2 = Vector2(0, 0),
        resistance: Vector2 = Vector2(1,1),
        id:None = None,
        is_simulating: bool = False
    ):
        self._rect = Rect(x,y,w,h)
        self._speed = speed
        self.is_simulating = is_simulating
        if id is not None:
            self._id = id
        else:
            self._id = id_generate(7)
        
        self._resistance = resistance
        self.collides = {"left": False, "right": False, "up": False, "down": False}

    def __collides_return__(self):
        self.collides = {"left": False, "right": False, "up": False, "down": False}

    def collide_list_form(self, rects):
        collide_list: Tuple[Rect, ...] = []
        for rect in rects:
            if rect._id!=self._id:
                if self._rect.collide_rect(rect._rect):
                    
                    collide_list.append(rect)
        return collide_list
    

    @property
    def collide_up(self) -> bool:
        return self.collides["up"]

    @property
    def collide_down(self) -> bool:
        return self.collides["down"]

    @property
    def collide_left(self) -> bool:
        return self.collides["left"]

    @property
    def collide_right(self) -> bool:
        return self.collides["right"]

    @property
    def sx(self):
        return self._speed.x

    @property
    def sy(self):
        return self._speed.y

    @sx.setter
    def sx(self, sx: float):
        self._speed.x = sx

    @sy.setter
    def sy(self, sy: float):
        self._speed.y = sy

class CollidesSpace:
    def __init__(self, gravity_: Vector2, air_resistance_: Vector2) -> None:
        self._colliders: Tuple[Collider, ...] = []
        self._gravity = gravity_
        self._air_resistance = air_resistance_
    
    def add(self, collide_item_: Collider | Rect):
        self._colliders.append(collide_item_)
       
        
    def simulate(self):
        for simulating_item_ in self._colliders:
            
            if simulating_item_.is_simulating:
                simulating_item_._speed+=self._gravity
                simulating_item_._speed.x*=self._air_resistance.x
                simulating_item_._speed.y*=self._air_resistance.y
                simulating_item_.__collides_return__()
                
                simulating_item_._rect.y+=simulating_item_._speed.y
            
                collide_list = simulating_item_.collide_list_form(self._colliders)
                    
                for c_rect in collide_list:
                    
                    if simulating_item_._speed.y > 0:

                            simulating_item_._speed.y *= -simulating_item_._resistance.y

                            simulating_item_._speed.x *= simulating_item_._resistance.x
                            simulating_item_._rect.y_down = copy(c_rect._rect.y_up)
                            simulating_item_.collides["down"] = True

                    elif simulating_item_._speed.y <= 0:

                            simulating_item_._speed.y *= -simulating_item_._resistance.y
                            simulating_item_._speed.x *= simulating_item_._resistance.x
                            simulating_item_._rect.y_up = copy(c_rect._rect.y_down)
                            simulating_item_.collides["up"] = True
                            
                simulating_item_._rect.x += simulating_item_._speed.x
        
                collide_list = simulating_item_.collide_list_form(self._colliders)
                    
                for c_rect in collide_list:

                    if simulating_item_._speed.x > 0:
                                simulating_item_._speed.x *= -simulating_item_._resistance.x
                                # self.speed_.y *= self._trenie.y
                                simulating_item_._rect.x_right = c_rect._rect.x_left
                                simulating_item_.collides["right"] = True

                    elif simulating_item_._speed.x < 0:
                                simulating_item_._speed.x *= -simulating_item_._resistance.x
                                # self.speed_.y *= self._trenie.y
                                simulating_item_._rect.x_left = c_rect._rect.x_right
                                simulating_item_.collides["left"] = True
              
    def draw(self,win_surf_:pygame.Surface):
        for block in self._colliders:
            Draw.draw_rect_fast(win_surf_, block._rect.xy, block._rect.wh,(255,0,0))
              
            
        
space = CollidesSpace(Vector2(0,0.5),Vector2(0.99,0.99))


space.add(Collider(0,700,1200,60))
space.add(Collider(400,200,50,50,is_simulating=True))
space.add(Collider(400,000,50,50,is_simulating=True))
space.add(Collider(500,000,50,50,is_simulating=True))

while win.update(fps=60, fps_view=1, base_color='white'):
    space.draw(win())
    space.simulate()