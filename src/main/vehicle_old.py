import math


class Vehicle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("vehicle.png")
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_HEIGHT/2, SCREEN_WIDTH/2)
        self.bearing = 0
        self.velocity = [0,0]
        self.base_v = 10

    def move(self, light):
        """ determine the velocity based on the light source """

        """ determine the position of the light source relative to the vehicle in polar coordinates """
        x = light.rect.center[0] - self.rect.center[0]
        y = light.rect.center[1] - self.rect.center[0]
        r = math.sqrt(x**2+y**2)
        if y >= 0:
            alpha = math.degrees(math.acos(x/(r)))
        else:
            alpha = 360 - math.degrees(math.acos(x/r))

        """ calculate the difference in angle between the heading and alpha """
        diff_angle = self.bearing - alpha
        if diff_angle > 180:
            diff_angle = 360 - diff_angle
        elif diff_angle <= -180:
            diff_angle = 360 + diff_angle

        """ calculate the velocity in x and y using the heading augmented by alpha """
        self.bearing += diff_angle / 5

        x_vel = math.ceil((self.base_v / (r+1)) * math.cos(self.bearing))
        y_vel = math.ceil((self.base_v / (r+1)) * math.sin(self.bearing))
        self.rect.move_ip(x_vel, y_vel)

        """ if the vehicle leaves the screen, jump to the opposite side"""
        if self.rect.center[0] > SCREEN_HEIGHT:
            self.rect.center = (0, self.rect.center[1])
        elif self.rect.center[0] < 0:
            self.rect.center = (SCREEN_HEIGHT, self.rect.center[1])
        elif self.rect.center[1] > SCREEN_WIDTH:
            self.rect.center = (self.rect.center[0], 0)
        elif self.rect.center[1] < 0:
            self.rect.center = (self.rect.center[0], SCREEN_WIDTH)

    def draw(self, surface):
        """ rotate image to reflect heading and draw it """
        self.image = pygame.transform.rotate(self.image, self.bearing)
        surface.blit(self.image, self.rect)