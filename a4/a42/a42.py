#!/usr/bin/env python3
'''Assignment 4 Part 2 template'''
print(__doc__)

from typing import IO
import random

class ArtConfig:
    '''ArtConfig class'''
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

class GenRandom:
    '''GenRandom class'''
    def __init__(self, art: ArtConfig):
        self.x = art.width
        self.y = art.height

    def create_shape(self) -> int:
        return random.randint(0, 2)
    
    def x_coord(self) -> int:
        return random.randint(0, self.x)

    def y_coord(self) -> int:
        return random.randint(0, self.y)

    def rad(self) -> int:
        return random.randint(0, 100)

    def rad_x(self) -> int:
        return random.randint(10, 30)

    def rad_y(self) -> int:
        return random.randint(10, 30)
    
    def width(self) -> int:
        return random.randint(0, 100)
    
    def height(self) -> int:
        return random.randint(0, 100)

    def red(self) -> int:
        return random.randint(0, 255)

    def green(self) -> int:
        return random.randint(0, 255)

    def blue(self) -> int:
        return random.randint(0, 255)

    def opacity(self) -> float:
        return random.uniform(0.0, 1.0)

def printTable() -> None:
    print('CNT SHA   X   Y RAD  RX  RY   W   H   R   G   B  OP')
    generator = GenRandom(ArtConfig(500, 300, 10))
    for i in range(10):
        print(f' {i:>2}', end=' ')
        print(f'  {generator.create_shape()}', end=' ')
        print(f'{generator.x_coord():>3}', end=' ')
        print(f'{generator.y_coord():>3}', end=' ')
        print(f'{generator.rad():>3}', end=' ')
        print(f'{generator.rad_x():>3}', end=' ')
        print(f'{generator.rad_y():>3}', end=' ')
        print(f'{generator.width():>3}', end=' ')
        print(f'{generator.height():>3}', end=' ')
        print(f'{generator.red():>3}', end=' ')
        print(f'{generator.green():>3}', end=' ')
        print(f'{generator.blue():>3}', end=' ')
        print(f'{generator.opacity():>3.1f}') 

def main() -> None:
    '''main method'''
    printTable()    

main()

