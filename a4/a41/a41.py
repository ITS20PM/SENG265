#!/usr/bin/env python3
'''Assignment 4 Part 1 template'''
print(__doc__)

from typing import IO

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
    def __init__(self, fnam: str, winTitle: str, svg: tuple):
        f: IO[str] = open(fnam, "w")
        writeHTMLHeader(f, winTitle)
        openSVGcanvas(f, 1, (svg[0], svg[1]))
        genArt(f, 2)
        closeSVGcanvas(f, 1)
        f.close()


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

def genArt(f: IO[str], t: int) -> None:
   '''genART method'''
   drawCircleLine(f, t, Circle((70,50,30), (155,60,60,0.70)))
   drawCircleLine(f, t, Circle((120,59,40), (55,0,110,0.90)))
   drawCircleLine(f, t, Circle((150,230,29), (255,0,80,0.92)))
   drawCircleLine(f, t, Circle((320,180,50), (104,21,20,0.46)))
   drawCircleLine(f, t, Circle((361,150,24), (61,29,180,0.77)))

   drawRectangle(f, t, Rectangle((0,110,80,80), (0,255,0,0.401)))
   drawRectangle(f, t, Rectangle((100,40,70,111), (0,255,255,0.32)))
   drawRectangle(f, t, Rectangle((200,92,85,50), (255,255,0,0.88)))
   drawRectangle(f, t, Rectangle((300,104,90,44), (100,155,0,0.66)))
   drawRectangle(f, t, Rectangle((400,128,32,94), (0,55,0,0.7)))

   drawEllipse(f, t, Ellipse((50,231,49,52), (102,0,255,0.42)))
   drawEllipse(f, t, Ellipse((107,250,61,31), (90,70,155,0.76)))
   drawEllipse(f, t, Ellipse((213,225,25,44), (40,0,144,0.80)))
   drawEllipse(f, t, Ellipse((102,250,30,50), (0,80,128,0.20)))
   drawEllipse(f, t, Ellipse((351,161,58,69), (10,190,0,0.32)))
        
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

def writeHTMLfile() -> None:
    '''writeHTMLfile method'''
    generator = ProEpilogue("a41.html", "My Art", (500, 300))
    
def main() -> None:
    '''main method'''
    writeHTMLfile()

main()

                                                                                                                                                                                                                                                                                                        
