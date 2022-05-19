""" Imports """
import math


class Vehicle:
    def __init__(self, mode, position, c_sensor, c_translate, c_rotation):
        """ sensor values left and right """
        self.s_l = 0
        self.s_r = 0

        """ heading, wheel velocities and overall speed of the vehicle """
        self.heading = 0
        self.v_l = 0
        self.v_r = 0
        self.speed = 0

        """ behavior mode of the vehicle """
        self.mode = mode
        
        """ vehicle settings """
        self.c_sensor = c_sensor
        self.c_translate = c_translate
        self.c_rotation = c_rotation

        """ position of the vehicle and the left and right sensors """
        self.pos = position
        self.pos_l = [position[0] + (5 * math.cos(self.heading+30)), position[1] + (5 * math.sin(self.heading+30))]
        self.pos_r = [position[0] + (5 * math.cos(self.heading-30)), position[1] + (5 * math.sin(self.heading-30))]

    def sense(self, light_pos):
        """ determine the distances of each sensor to the light source """
        dx_l = light_pos[0] - self.pos_l[0]
        dy_l = light_pos[1] - self.pos_l[1]
        dx_r = light_pos[0] - self.pos_r[0]
        dy_r = light_pos[1] - self.pos_r[1]

        """ calculate the sensor values """
        self.s_l = self.c_sensor / math.sqrt((dx_l ** 2) + (dy_l ** 2))
        self.s_r = self.c_sensor / math.sqrt((dx_r ** 2) + (dy_r ** 2))

    def motor_control(self):
        """ changes the wheel velocity based on mode and sensor values """
        if self.mode == "flee":
            self.v_l = self.c_translate * self.s_l
            self.v_r = self.c_translate * self.s_r
        elif self.mode == "seek":
            self.v_l = self.c_translate * self.s_r
            self.v_r = self.c_translate * self.s_l

    def rotate(self):
        """ change the heading based on the difference of the wheel velocities """
        c_rotation = 0.1
        self.heading += min((c_rotation * (self.v_l - self.v_r)), 0.05)

    def translate(self):
        """ update the speed value of the vehicle """
        self.speed = min(max(((self.v_l + self.v_r) / 2), 1), 5)

        """ move into the direction of the heading with the speed value """
        delta_x = self.speed * math.cos(self.heading)
        delta_y = self.speed * math.sin(self.heading)
        self.pos = [self.pos[0] + delta_x, self.pos[1] + delta_y]
        self.pos_l = [self.pos[0] + (5 * math.cos(self.heading+30)), self.pos[1] + (5 * math.sin(self.heading+30))]
        self.pos_r = [self.pos[0] + (5 * math.cos(self.heading-30)), self.pos[1] + (5 * math.sin(self.heading-30))]

    def move(self, light_pos):
        """ bundle all four steps into one function """
        self.sense(light_pos)
        self.motor_control()
        self.rotate()
        self.translate()
