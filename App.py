import sys
import pygame
from settings import *
import queue


class Node:
    def __init__(self,parent = None,position = None):
        self.parent = parent
        self.position = position
        self.gcost = 0
        self.hcost = 0
        self.fcost = 0
class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode([WIDTH,HEIGHT])
        self.running = True
        self.selected = []
        self.mousePos = None
        self.start = None
        self.end = None
        self.path = []
        self.closed = []
        self.noPath = False
        self.shortestPath = []
        self.failed = pygame.font.SysFont("arial", 40,)
        self.font = pygame.font.SysFont("arial", 23)
        self.title = pygame.font.SysFont("arial",50)
    def run(self):
        pygame.display.set_caption("PATHFINDER")
        
        while self.running:
            
            self.update()
            
            self.events()
            self.draw(self.window)
        pygame.quit()
        sys.exit()
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    pos=self.mousePos
                    x = pos[0] //20
                    y = pos[1] //20
                    if y < 35 and y >= 5 and (x,y) not in self.selected:
                        self.start = (x,y)
                if event.key == pygame.K_e:
                    pos=self.mousePos
                    x = pos[0] //20
                    y = pos[1] //20
                    if y < 35 and y >= 5 and (x,y) not in self.selected:
                        self.end = (x,y)
                if event.key == pygame.K_BACKSPACE:
                    pos = self.mousePos
                    x = pos[0]//20
                    y = pos[1]//20
                    if (x,y) in self.selected:
                        self.selected.remove((x,y))
                if event.key == pygame.K_c:
                    self.__init__()
                    
                if event.key == pygame.K_RETURN:
     
                    self.solver()
            elif pygame.mouse.get_pressed()[0]:
                pos = self.mousePos
                x = pos[0]//20
                y = pos[1]//20
                if y < 35 and y >= 5 and (x,y) not in self.selected:
                    self.selected.append((x,y))
            elif pygame.mouse.get_pressed()[2]:
           
                pos = self.mousePos
                x = pos[0]//20
                y = pos[1]//20
                if (x,y) in self.selected:
                    self.selected.remove((x,y))
            
    def update(self):
        self.mousePos =pygame.mouse.get_pos()  
    def draw(self,window):
        window.fill(BLACK)

        for pos in self.selected:
            self.highlightBox(pos,window)
        for pos in self.closed:
            self.checkedCells(pos,window)
        for pos in self.path:
            self.passed(pos,window)
        
        if self.start:
            self.drawStart(self.start,window)
        if self.end:
            self.drawEnd(self.end,window)
        
        self.drawGrid(window)
        if self.noPath:
            self.noSolution()
        self.drawInfo(window)
        
        pygame.display.update()

### SOLVING FUNCTIONS ###
    def solver(self):
        startNode = Node(None,self.start)
        endNode = Node(None,self.end)
        #print("START", self.start)
        #print("END:", self.end)
        openList = []
        closedList = []
      
        openList.append(startNode)
        
        while openList != []:
        
            currentNode = openList[0]
           
            
            for node in openList[1:]:
                if node.fcost < currentNode.fcost or (node.fcost == currentNode.fcost and node.hcost < currentNode.hcost):
                    currentNode = node

                 
            openList.remove(currentNode)
            closedList.append(currentNode)
            #print([x.position  for x in openList]) 
            #print([x.position for x in closedList]) 
            if currentNode.position == endNode.position:
                current = currentNode
                
                while current is not None:
                    self.path.insert(0,current.position)
                    current = current.parent
                    
                return
            
             
            for new_pos in [(0,1),(0,-1),(1,1),(1,0),(-1,0),(-1,-1),(-1,1),(1,-1)]:
                node_position = (currentNode.position[0]+new_pos[0],currentNode.position[1]+new_pos[1])
                
                if node_position in self.selected:
                    continue
                if node_position[1] > 34 or node_position[1] < 5 or node_position[0] < 0 or node_position[0] >  29:
                    continue
                if node_position in [x.position for x in closedList] :
                    
                    continue
                
                if node_position != currentNode:
                    
                    new_node = Node(currentNode,node_position)
                    
                    child = new_node
                    movementCost = currentNode.gcost + self.getDistance(currentNode,child)
                    if  movementCost < child.gcost or child.position not in [x.position for x in openList]:
                        child.gcost = movementCost
                        child.hcost =self.getDistance(child,endNode)
                        child.fcost = child.gcost+child.hcost
                        child.parent = currentNode
                        if (child.parent,child.position) not in [(x.parent,x.position) for x in openList]:
                            openList.append(child)
                            self.closed.append(child.position)
                            self.checkedCells(child.position,self.window)
                            self.drawStart(self.start,self.window)
                            self.drawEnd(self.end,self.window)
                            self.drawGrid(self.window)
                            pygame.display.update()
                 
                    
      
       
        self.noPath = True 
### HELPER FUNCTIONS FOR GRID###
    def drawGrid(self,window):
        for i in range(31):
            pygame.draw.line(window, WHITE,(i*cellSize,100), (i*cellSize,HEIGHT-100))
            pygame.draw.line(window, WHITE,(0,i*cellSize+100), (WIDTH,i*cellSize+100))
    
    def passed(self,pos,window):
        pygame.draw.rect(window,RED , (pos[0]*cellSize,pos[1]*cellSize,cellSize,cellSize))
    
    def checkedCells(self,pos,window):
        pygame.draw.rect(window, BLUE , (pos[0]*cellSize,pos[1]*cellSize,cellSize,cellSize))
    
    def highlightBox(self,pos,window):
        pygame.draw.rect(window, WHITE, (pos[0]*cellSize,pos[1]*cellSize,cellSize,cellSize))
        
    def drawStart(self,pos,window):
        
        pygame.draw.rect(window,GREEN,(pos[0]*cellSize,pos[1]*cellSize,cellSize,cellSize))  
    
    def drawEnd(self,pos,window):
        
        pygame.draw.rect(window,YELLOW,(pos[0]*cellSize,pos[1]*cellSize,cellSize,cellSize)) 
            
    def drawInfo(self,window):
        start = self.font.render("Click 's' to set a start.", True, WHITE)
        end = self.font.render("Click 'e' to set an end.", True,WHITE)
        clear = self.font.render("Click 'c' to clear grid.", True,WHITE)
        delete = self.font.render("Left click to select, right click to unselect.",True,WHITE)
        solve = self.font.render("Click enter to find shortest path.",True,WHITE)
        title = self.title.render("PATHFINDER",True,WHITE)
        titlePos = title.get_size()
        Spos = start.get_size()
        window.blit(start,(0,725))
        window.blit(end,(0,725+Spos[1]))
        window.blit(clear,(0,725+Spos[1]*2))
        window.blit(delete,(WIDTH//2,725))
        window.blit(solve,(WIDTH//2,725+Spos[1]))
        window.blit(title,((WIDTH//2)-(titlePos[0]//2),50-titlePos[1]//2))
### HELPER FOR SOLVING FUNCTION###    
    def getDistance(self,NodeA,NodeB):
        distX = abs(NodeA.position[0] - NodeB.position[0])
        distY = abs(NodeA.position[1] - NodeB.position[1])
        if distX > distY:
            return (14*distY + 10*(distX-distY))
        return (14*distX + 10*(distY-distX))
    def noSolution(self):
        font = self.failed.render("NO PATH FOUND",True,BLACK,WHITE)
        pos = font.get_size()
        posX = pos[0]//2
        posY = pos[1]//2
        self.window.blit(font,(WIDTH//2-posX,HEIGHT//2-posY))