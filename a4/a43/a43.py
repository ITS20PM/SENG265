#!/usr/bin/env python3
'''Assignment 4 Part 3 template'''
print(__doc__)

from typing import IO
import random

class Circle:
    '''Circle class'''
    def __init__(self, cir: tuple, col: tuple):
        self.cx: int = cir[0]
        self.cy: int = cir[1]
        self.rad: int = cir[2]
        self.red: int = col[0]
        self.green: int = col[1]
        self.blue: int = col[2]
        self.op: float = col[3]

class Rectangle:
    '''Rectangle class'''
    def __init__(self, rect: tuple, col: tuple):
        self.x: int = rect[0]
        self.y: int = rect[1]
        self.width: int = rect[2]
        self.height: int = rect[3]
        self.red: int = col[0]
        self.green: int = col[1]
        self.blue: int = col[2]
        self.op: int = col[3]

class Ellipse:
    '''Ellipse class'''
    def __init__(self, elli: tuple, col: tuple):
        self.cx: int = elli[0]
        self.cy: int = elli[1]
        self.rx: int = elli[2]
        self.ry: int = elli[3]
        self.red: int = col[0]
        self.green: int = col[1]
        self.blue: int = col[2]
        self.op: float = col[3]

class ProEpilogue:
    '''ProEpilogue class'''
    def __init__(self, fnam: str, winTitle: str, numShape: int, svg: tuple, 
                shape: tuple, rad: tuple, rwh: tuple, col: tuple):
        f: IO[str] = open(fnam, "w")
        writeHTMLHeader(f, winTitle)
        openSVGcanvas(f, 1, (svg[0], svg[1]))
        genArt(f, 2, numShape, svg, shape, rad, rwh, col)
        closeSVGcanvas(f, 1)
        f.close()

    
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

    def create_shape(self, shape: tuple)->int:
        return random.randint(shape[0], shape[1])
    
    def x_coord(self)->int:
        return random.randint(0, self.x)

    def y_coord(self)->int:
        return random.randint(0, self.y)

    def rad(self, rad: tuple)->int:
        return random.randint(rad[0], rad[1])

    def rad_x(self, rwh: tuple)->int:
        return random.randint(rwh[0], rwh[1])

    def rad_y(self, rwh: tuple)->int:
        return random.randint(rwh[2], rwh[3])
    
    def width(self, rwh: tuple)->int:
        return random.randint(rwh[4], rwh[5])
    
    def height(self, rwh: tuple)->int:
        return random.randint(rwh[6], rwh[7])

    def red(self, col: tuple)->int:
        return random.randint(col[0], col[1])

    def green(self, col: tuple)->int:
        return random.randint(col[2], col[3])

    def blue(self, col: tuple)->int:
        return random.randint(col[4], col[5])

    def opacity(self, col: tuple)->float:
        return random.uniform(col[6], col[7])

def writeHTMLcomment(f: IO[str], t: int, com: str) -> None:
    '''writeHTMLcomment method'''
    ts: str = "   " * t
    f.write(f'{ts}<!--{com}-->\n')
        
def drawCircleLine(f: IO[str], t: int, c: Circle) -> None:
    '''drawCircle method'''
    ts: str = "   " * t
    line: str = f'<circle cx="{c.cx}" cy="{c.cy}" r="{c.rad}" fill="rgb({c.red}, {c.green}, {c.blue})" fill-opacity="{c.op}"></circle>'
    f.write(f"{ts}{line}\n")

def drawRectangle(f: IO[str], t: int, r: Rectangle) -> None:
    '''drawRectangle method'''
    ts: str = "   " * t
    line: str = f'<rect x="{r.x}" y="{r.y}" width="{r.width}" height="{r.height}" fill="rgb({r.red}, {r.green}, {r.blue})" fill-opacity="{r.op}"></rect>'
    f.write(f"{ts}{line}\n")

def drawEllipse(f: IO[str], t: int, e: Ellipse) -> None:
    '''drawEllipse method'''
    ts: str = "   " * t
    line: str = f'<ellipse cx="{e.cx}" cy="{e.cy}" rx="{e.rx}" ry="{e.ry}" fill="rgb({e.red}, {e.green}, {e.blue})" fill-opacity="{e.op}"></ellipse>'
    f.write(f"{ts}{line}\n")

def genArt(f: IO[str], t: int, numShape: int, svg: tuple, shape: tuple, rad: tuple, rwh: tuple, col: tuple) -> None:
    generator: GenRandom = GenRandom(ArtConfig(svg[0], svg[1]))
    for i in range(numShape):
        sha = generator.create_shape(shape=shape)
        if sha == 0:
            drawCircleLine(f, t, Circle((generator.x_coord(),generator.y_coord(),generator.rad(rad=rad)), 
            (generator.red(col=col),generator.green(col=col),generator.blue(col=col),generator.opacity(col=col))))
        if sha == 1:
            drawRectangle(f, t, Rectangle((generator.x_coord(),generator.y_coord(),generator.width(rwh=rwh),generator.height(rwh=rwh)), 
            (generator.red(col=col),generator.green(col=col),generator.blue(col=col),generator.opacity(col=col))))
        if sha == 2:
            drawEllipse(f, t, Ellipse((generator.x_coord(),generator.y_coord(),generator.rad_x(rwh=rwh),generator.rad_y(rwh=rwh)), 
            (generator.red(col=col),generator.green(col=col),generator.blue(col=col),generator.opacity(col=col))))

def openSVGcanvas(f: IO[str], t: int, canvas: tuple) -> None:
    '''openSVGcanvas method'''
    ts: str = "   " * t
    writeHTMLcomment(f, t, "Define SVG drawing box")
    f.write(f'{ts}<svg width="{canvas[0]}" height="{canvas[1]}">\n')

def closeSVGcanvas(f: IO[str], t: int) -> None:
    '''closeSVGcanvas method'''
    ts: str = "   " * t
    f.write(f'{ts}</svg>\n')
    f.write(f'</body>\n')
    f.write(f'</html>\n')

def writeHTMLline(f: IO[str], t: int, line: str) -> None:
    '''writeLineHTML method'''
    ts = "   " * t
    f.write(f"{ts}{line}\n")

def writeHTMLHeader(f: IO[str], winTitle: str) -> None:
    '''writeHeadHTML method'''
    writeHTMLline(f, 0, "<html>")
    writeHTMLline(f, 0, "<head>")
    writeHTMLline(f, 1, f"<title>{winTitle}</title>")
    writeHTMLline(f, 0, "</head>")
    writeHTMLline(f, 0, "<body>")

def writeHTMLfile(fnam: str, winTitle: str, numShape: int, svg: tuple, shape: tuple, rad: tuple, rwh: tuple, col: tuple) -> None:
    '''writeHTMLfile method'''
    ProEpilogue(fnam, winTitle, numShape, svg, shape, rad, rwh, col)
    
class PyArt:
    '''PyArt class'''
    def __init__(self, fnam: str, winTitle: str, numShape: int, svg: tuple, shape: tuple, rad: tuple, rwh: tuple, col: tuple) -> None:
        writeHTMLfile(fnam, winTitle, numShape, svg, shape, rad, rwh, col)

def main() -> None:
    '''main method'''
    python_Art: PyArt = PyArt(fnam="a43.html", winTitle="Python art", numShape=1000, svg=(600, 400), shape=(1, 2), rad=(0, 40), 
                        rwh=(10, 30, 10, 30, 0, 50, 0, 30), col=(100, 255, 100, 255, 0, 155, 0.8, 1.0))

main()
