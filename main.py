import sys
import pygame
import math
import os
pygame.init()

BACKGROUND = (21, 39, 54)
LINE_COLOR = (56, 136, 201)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


screen = pygame.display.set_mode([800, 800])
pygame.display.set_caption("Tic Tac Toe")
icon = pygame.image.load(resource_path("tictactoe.png"))
pygame.display.set_icon(icon)
screen.fill(BACKGROUND)

# GRID DRAWING
pygame.draw.line(screen, LINE_COLOR, (325, 175), (325, 625), 6)
pygame.draw.line(screen, LINE_COLOR, (475, 175), (475, 625), 6)
pygame.draw.line(screen, LINE_COLOR, (175, 325), (625, 325), 6)
pygame.draw.line(screen, LINE_COLOR, (175, 475), (625, 475), 6)

pygame.draw.circle(screen, LINE_COLOR, (326, 175), 3)
pygame.draw.circle(screen, LINE_COLOR, (326, 625), 3)
pygame.draw.circle(screen, LINE_COLOR, (476, 175), 3)
pygame.draw.circle(screen, LINE_COLOR, (476, 625), 3)
pygame.draw.circle(screen, LINE_COLOR, (175, 326), 3)
pygame.draw.circle(screen, LINE_COLOR, (625, 326), 3)
pygame.draw.circle(screen, LINE_COLOR, (175, 476), 3)
pygame.draw.circle(screen, LINE_COLOR, (625, 476), 3)

# 9 meaning blank unused spot
tttArray = [[9, 9, 9], [9, 9, 9], [9, 9, 9]]
boxCenters = [[244, 244], [400, 244], [556, 244], [244, 400], [400, 400], [556, 400], [244, 556], [400, 556], [556, 556]]
won = False
players = ['O', 'X']
crossOffset = 55


def drawPlayers(turnC, coords, greenBool):
    if greenBool:
        color = (0, 255, 0)
    else:
        color = (255, 255, 255)
    if turnC:
        pygame.draw.line(screen, color, (coords[0]+crossOffset, coords[1]-crossOffset), (coords[0]-crossOffset, coords[1]+crossOffset), 10)
        pygame.draw.line(screen, color, (coords[0]-crossOffset, coords[1]-crossOffset), (coords[0]+crossOffset, coords[1]+crossOffset), 10)
    elif not turnC:
        pygame.draw.circle(screen, color, (coords[0], coords[1]), 60, 7)


def winCheck(turnCr):
    for i in range(3):
        if tttArray[i][0] != 9 and tttArray[i][0] == tttArray[i][1] and tttArray[i][1] == tttArray[i][2]:
            drawPlayers(turnCr, boxCenters[3*i], True)
            drawPlayers(turnCr, boxCenters[3*i+1], True)
            drawPlayers(turnCr, boxCenters[3*i+2], True)
            return True, tttArray[i][0]
        elif tttArray[0][i] != 9 and tttArray[0][i] == tttArray[1][i] and tttArray[1][i] == tttArray[2][i]:
            drawPlayers(turnCr, boxCenters[i], True)
            drawPlayers(turnCr, boxCenters[2+i+1], True)
            drawPlayers(turnCr, boxCenters[5+i+1], True)
            return True, tttArray[0][i]
    if tttArray[0][0] != 9 and tttArray[0][0] == tttArray[1][1] and tttArray[1][1] == tttArray[2][2]:
        drawPlayers(turnCr, boxCenters[0], True)
        drawPlayers(turnCr, boxCenters[4], True)
        drawPlayers(turnCr, boxCenters[8], True)
        return True, tttArray[0][0]
    elif tttArray[2][0] != 9 and tttArray[2][0] == tttArray[1][1] and tttArray[1][1] == tttArray[0][2]:
        drawPlayers(turnCr, boxCenters[2], True)
        drawPlayers(turnCr, boxCenters[4], True)
        drawPlayers(turnCr, boxCenters[6], True)
        return True, tttArray[2][0]
    return False, tttArray[0][0]


def boxFinder(pos):
    distance = 400
    clickedBox = []
    nTemp = 0
    n = 0
    for box in boxCenters:
        nTemp += 1
        dx = pos[0]-box[0]
        dy = pos[1]-box[1]
        currDist = math.sqrt(dx*dx + dy*dy)
        if currDist < distance:
            distance = currDist
            clickedBox = box
            n = nTemp
    if tttArray[math.ceil(n / 3) - 1][n - 1 - 3 * (math.ceil(n / 3) - 1)] != 9:
        return
    return clickedBox, n


pygame.display.flip()
turnCross = True
running = True
turns = 0
fontVar = pygame.font.SysFont('Comic Sans MS', 30)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and 175 <= event.pos[0] <= 625 and 175 <= event.pos[1] <= 625:
                clicked = boxFinder(event.pos)
                if clicked is not None:
                    turns += 1
                    drawPlayers(turnCross, clicked[0], False)
                    if turnCross:
                        tttArray[math.ceil(clicked[1] / 3) - 1][clicked[1] - 1 - 3 * (math.ceil(clicked[1] / 3) - 1)] = 1
                    elif not turnCross:
                        tttArray[math.ceil(clicked[1] / 3) - 1][clicked[1] - 1 - 3 * (math.ceil(clicked[1] / 3) - 1)] = 0
                    winCheckOutput = winCheck(turnCross)
                    turnCross = not turnCross
                    if winCheckOutput[0]:
                        print("nice work Buddy. the winner is", players[winCheckOutput[1]])
                        winnerString = players[winCheckOutput[1]].upper() + " is the winner!"
                        fontObj = fontVar.render(winnerString, True, (255, 255, 255), BACKGROUND)
                        screen.blit(fontObj, (293, 50))
                        won = True
                        running = False
                    elif turns == 9:
                        drawStr = "Draw - nobody wins."
                        print(drawStr)
                        fontObj = fontVar.render(drawStr, True, (255, 255, 255), BACKGROUND)
                        screen.blit(fontObj, (260, 50))
                        won = True
                        running = False
                    pygame.display.flip()

while won:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            won = False
