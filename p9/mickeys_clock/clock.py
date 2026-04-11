from datetime import datetime
import pygame


def get_current_time():
    now = datetime.now()
    return now.minute, now.second


def rotate_image(image, angle, center):
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_rect = rotated_image.get_rect(center=center)
    return rotated_image, rotated_rect


def draw_clock(screen, left_arm, right_arm, center, minutes, seconds):
    # 60 секунд = 360 градус => 1 секунд = 6 градус
    second_angle = -(seconds * 6)

    # минут қолы секундқа да тәуелді болса, әдемірек қозғалады
    minute_angle = -((minutes + seconds / 60) * 6)

    rotated_left, left_rect = rotate_image(left_arm, second_angle, center)
    rotated_right, right_rect = rotate_image(right_arm, minute_angle, center)

    screen.blit(rotated_right, right_rect)  # минут
    screen.blit(rotated_left, left_rect)    # секунд