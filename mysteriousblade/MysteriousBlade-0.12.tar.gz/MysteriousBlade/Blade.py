import pygame, random, math, time, os

from pygame.locals import *

pygame.init()
pygame.mixer.init()
pygame.mouse.set_visible(False)

Cursor = pygame.image.load('BladeCursor.png')
BladeBlade = pygame.image.load('BladeBlade.png')
Back = pygame.image.load('BladeField.png')
FakeScreen = pygame.image.load('FakeScreen.png')
MoonScreen = pygame.image.load('MoonScreen.png')
RangeLines = pygame.image.load('RangeLines.png')
StartLines = pygame.image.load('StartLines.png')
EdithBlade = pygame.image.load('EdithBlade.png')
EdithShout = pygame.mixer.Sound('Shout.ogg')
ForkClick = pygame.mixer.Sound('ForkClick.ogg')
EdithScreen = pygame.image.load('EdithScreen.png')
EdithBossIntro = pygame.image.load('EdithBossIntro.png')
VirtualCounterpoint = pygame.mixer.Sound('Virtual_Counterpoint_2.ogg')
EdithBossMusic = pygame.mixer.Sound('Your_Best_Friend_[First_Draft_.ogg')
Hit = pygame.mixer.Sound('Hit.ogg')
FireBase = pygame.image.load('FireBase.png')
Fireball = pygame.image.load('Fireball.png')
Clap = pygame.mixer.Sound('Clap.ogg')
Firesound = pygame.mixer.Sound('Whoosh.ogg')
Whoosh = pygame.mixer.Sound('Shoop.ogg')


Field = pygame.display.set_mode((320,300),DOUBLEBUF)

X = 0
Y = 0

Reach = 40

Attacks = []
Blade = []
BladeHold = []
BladeRot = []
Active = False
DState = None
TReach = 0
LastAng = 0
Pos = 400
White = (255,255,255)
Grey = (150,150,150)
LGrey = (200,200,200)
HBlue = (0,75,255)
Black = (0,0,0)
EMag = (255,30,255)
Red = (255,30,30)
PositTrans = 300.0/1000.0
Blade = []
NPos = 2000

def Dist(x,y):
    return math.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)
def Angle(x,y):
    rads = math.atan2((y[0]-x[0]),(y[1]-x[1]))
    degs = math.degrees(rads)        
    return (degs+90.0)
def Sigmoid(x):
  return ((1.0 / (1.0 + math.exp(-x)))-0.5)*2
    
def DrawBlade(Blade,Cursori,Sprit):
    global LastAng
    if len(Blade) == 0:
        return
    BladeHold = []
    BladeRot = []
    P1 = Cursori
    P2 = Blade[0]
    if P1 == P2:
        Ang = LastAng
    else:
        Ang = Angle(P1,P2)
        LastAng = Ang
    #print(Ang)
    Rot = pygame.transform.rotate(Sprit,Ang)
    BladeRot.append(Rot)
    BladeHold.append(Field.blit(BladeRot[0],(P2[0]-7,P2[1]-4)))
    for i in range(1,len(Blade)):
        P1 = Blade[i-1]
        P2 = Blade[i]
        Ang = Angle(P1,P2)
        Rot = pygame.transform.rotate(Sprit,Ang)
        BladeRot.append(Rot)
        BladeHold.append(Field.blit(BladeRot[i],(P2[0]-7,P2[1]-4)))
    return BladeHold

def DrawCursor(Cursori):
    Field.blit(Cursor,Cursori)
    return

def Clear():
    pygame.draw.rect(Field,Black,(0,0,320,300),0)
    Field.blit(Back,(0,0))
    pygame.draw.line(Field,White,(0,0),(150,150),2)
    pygame.draw.line(Field,White,(300,0),(150,150),2)
    pygame.draw.line(Field,White,(0,300),(150,150),2)
    pygame.draw.line(Field,White,(300,300),(150,150),2)
    pygame.draw.line(Field,White,(300,0),(300,300),2)
    pygame.draw.line(Field,Grey,(300,150),(320,150),1)
    pygame.draw.line(Field,Grey,(300,165),(320,165),1)
    pygame.draw.line(Field,Grey,(300,135),(320,135),1)
    return

def Posit(Pos,Color):
    NPos = Pos*PositTrans
    pygame.draw.line(Field,Color,(300,300-NPos),(320,300-NPos),2)

def Text(Text,Speak,Char):
    print('*'+str(Speak)+': '+str(Text))
    if Char != None:
        Field.blit(Char,(260,260))
    pygame.draw.circle(Field,EMag,(10,10),10,2)
    pygame.display.flip()
    while(True):
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            break
def Tex(Text,Speak,Char):
    print('*'+str(Speak)+': '+str(Text))

def Cull(Blade,Reach):
    TReach = 0
    DeadBlade = Blade
    Blade = []
    if len(DeadBlade) < Reach:
        TReach = len(DeadBlade)
    else:
        TReach = Reach
    for i in range(TReach):
        Blade.append(DeadBlade[i])
    return Blade

def Bladex(Blade, Active):
    Blade = Cull(Blade,Reach)
    (X,Y) = pygame.mouse.get_pos()
    #print(X,Y)
    if Active == True:
        Point = [(X,Y)]
        #print(Point)
        if len(Blade) == 0:
            #print("Hoy!")
            Blade = Point
        else:
            #print("Hi!")
            #print(Point)
            #print(Blade)
            Blade.insert(0,(X,Y))
            #print(Blade)
    #print(Blade)
    DrawCursor((X,Y))
    #print(Blade)
    BladeHold = DrawBlade(Blade,(X,Y),BladeBlade)
    pygame.display.flip()
    #print("All Done!")
    #print(Active)
    return Blade, Active

def Move(Pos,DState,Active):
    event = pygame.event.poll()
    if event.type == pygame.MOUSEBUTTONDOWN and Active == False:
        Active = True
    elif event.type == pygame.MOUSEBUTTONUP and Active == True:
        Active = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            DState = 'Up'
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            DState = 'Down'
    elif event.type == pygame.KEYUP:
        DState = None
    if DState == 'Up' and Pos < 1000 and Pos+5 < NPos:
        Pos += 5
    elif DState == 'Down' and Pos > 0:
        Pos -= 5
    return Pos, DState, Active
    

def Flit(Sprite, (x,y), EPos, IPos):
    if IPos > EPos:
        #print('Lets Go!')
        #print(IPos-EPos)
        Dist = IPos-EPos
        Dist = 1000-Dist
        Dist = Dist/1000.0
##        Dist = Dist/50.0
##        if Dist != 0:
##            Shift = 1.0/Dist
##        else:
##            Shift = 1000
        #print(Dist)
        Shift = Dist**2
        #print(Dist)
        Push = (300-int(Shift*300))/2
        (w,h) = Sprite.get_size()
        #print(Shift)
        Sprit = pygame.transform.scale(Sprite,(int(w*Shift),int(h*Shift)))
        Field.blit(Sprit,(int(int(x*Shift)+Push),int((y*Shift)+Push)))
def DrawStart(Pos):
    Flit(StartLines,(0,0),Pos, 450)
    Flit(StartLines,(0,0),Pos, 500)
    Flit(StartLines,(0,0),Pos, 550)
    return
Pos = 450
os.system('clear')
Name = raw_input(str("What is your name?:"))
#while(True):
NFriend = raw_input(str("What is the name of your best friend?:"))
    #LFriend = raw_input(str("What is the name of a friend you will never mmet again?:"))
    #if NFriend != LFriend:
#        break
#    else:
#        print("The present is as a bucket, so how do you hope to bound the ocean in this fragileq vessel?")
Text("Hey! Hey! Are you alright? Wake up!","???",None)
Text("(...What? There's someone here. I can feel a cold wind and smell salt. How did I get here?...)",Name,None)
Text("Hello! It's a pleasure to meet you. I'm "+NFriend+". What's your name?",NFriend,None)
if Name == NFriend:
    Text("Very funny. Let's get back to work.",NFriend+' [Exasperated]',None)
if Name == 'Henry':
    Text("Really? I've always thought of Henry as such a refined name!",NFriend+' [In Admiration]',None)
if Name == 'Chandler':
    Text("WOW. SO DANK.",'Otherworldly Voice',None)
    Text("Did you hear something odd just then?",NFriend+' [Perplexed]', None)
Text(Name+", then? That's a nice name. Anyways, you look pretty haggarded, so I figured I'd take you to Nishar. And if we're going to make it home you'll need to learn how to protect yourself.",NFriend,None)
Text("That's quite a fine sword you brought - much better than anything we could make - so let's start there.",NFriend,None)
Text("Now, you see, here it's very hard to - hurt - someone the way you might imagine.",NFriend,None)
Text("Of all that we lost, I suppose that was fortunate.",NFriend,None)
Text("However, the very essence of our being is corrupt. I suppose that what Nishar means when she says we've 'fallen'.",NFriend,None)    
Text("Therefore, if you wish to vanquish someone, you must approach their being and break their mortal screen.",NFriend,None)
Text("You look terrified! No, people don't die, and screens reform very quickly. It just means that in that moment, someone is open, exposed.",NFriend,None)
VirtualCounterpoint.play(loops=-1)
Clear()
pygame.display.flip()
Text("This is the area where this duel will occur, the FIELD.",NFriend,None)
Text("There's nothing on it right now, so how about you try walking to the end?",NFriend,None)
while(Pos != 1000):
    Clear()
    Pos, DState, Active = Move(Pos,DState,Active)
    Posit(Pos,HBlue)
    pygame.display.flip()
Text("How about you go back to where you started? Notice you don't turn around - to turn your back on an opponent would be quite dishonorable, after all!",NFriend,None)
while(Pos != 450):
    Clear()
    Pos, DState, Active = Move(Pos,DState,Active)
    Posit(Pos,HBlue)
    pygame.display.flip()
Text("Now, let's see what you can do with that sword. The blue dot represents the tip of your blade, and you can try cutting with it.",NFriend,None)
Text("|EQUIPPED| - Mysterious Blade.",'',None)
Text("Now I'm going to put up a fake screen. Walk to it and attack it.",NFriend,None)
while(True):
    Clear()
    DrawStart(Pos)
    Pos, DState, Active = Move(Pos,DState,Active)
    Flit(FakeScreen,(0,0),Pos, 750)
    Posit(Pos,HBlue)
    Blade, Active = Bladex(Blade, Active)
    pygame.display.flip()
    if abs(Pos-750) < 25 and Active == True:
        break
Clear()
Text("In a duel, that would have scored a point over your opponent. However, you would not expect your opponent to take such an offense passively.",NFriend,None)
Text("But let's call it a day.",NFriend,None)
Text("Hello! You came back!",NFriend,None)
Text("You might not be too surprised to hear this, but there have been unseen forces at work.",NFriend,None)
Text("Specifically, you actually have two screens: your TRUE SCREEN (the one that protects your soul) and your GUARD SCREEN, which is your first screen's means of protection.",NFriend,None)
Text("Don't get to thinking you're safe, though, because your guard screen can also be used to score for your opponent, and only advances beyond your true screen when your honor is expressed.",NFriend,None)
Text("What do I mean? In a duel, you either have gained the honor of the duel, or your opponent has gained it and you wish to reclaim it.",NFriend,None)
Text("We call this honor the RIGHT OF WAY, and while you have your GUARD SCREEN will protect you from all but an extraordinarily nimble opponent.",NFriend,None)
Text("Your 'perspective' is actually placed on your guard screen, which you thus can't see.",NFriend,None)
Text("However you can see two blue lines that represents your range, and your opponent's guard - it's almost always plain and white.",NFriend,None)
Text("Make sure you are in range, and then attack - you'll notice a blue and a white circle homing in on the tip of your blade.",NFriend,None)
Text("The blue represents how far your attack has progressed, the white how close you are to making contact. You will lose right of way if you start an attack without striking your opponent.",NFriend,None)
Text("I'm going to put up that fake screen again, and my own guard screen. When you move forward and it does not, you will gain right of way, and then you should attack!",NFriend,None)
Text("Don't worry! It's not my own true screen, and you can only hurt someone's guard screen if they try to attack.",NFriend,None)
NPos = 750
TGPos = -25
GPos = -25
GNPos = 25
TGNPos = 25
AProg = 0
ADist = 0
ASpeed = 2
Range = 50
ATime = 30
ASet = 20
Row = False
Score = False
State = "Start"
Pos = 450
def BoringAI(Pos, NPos, State):
    return "Stay"
def MoveAI(NPos, State):
    if State == "Stay":
        return NPos, State
    if State == "Guarding":
        return NPos, State
    if State == "Parry":
        return NPos, State
    if State == "Guard":
        return NPos, State
    if State == "Parrying":
        return NPos, State
def SimpleRow(Row, DState, State):
    if DState == 'Up' and State == 'Stay' and Row == False:
        Row = True
        #print('Caught!')
        return Row
    else:
        return Row
def AdjGuard(GPos,GNPos,Row):
    if Row == True and GPos > TGPos:
        GPos -= 5
    if Row == False and GPos < 0:
        GPos += 5
    if Row == True and GNPos > 0:
        GNPos -= 5
    if Row == False and GNPos < TGNPos:
        GNPos += 5
    #print(GPos,GNPos)
    return GPos, GNPos
def DrawCircles(Prog,Time,Set,Pos,Dist,Targ,Row,X,Y,Col):
    if (Time - Prog) > 0 and Row == True:
        pygame.draw.circle(Field, Col, (X,Y), (Time - Prog),1)
    if (Set - Prog) > 0 and Row == True:
        pygame.draw.circle(Field, Col, (X,Y), (Set - Prog),1)
    if (Targ-(Pos+Dist)) > 0 and Active == True and Row == True:
        pygame.draw.circle(Field,LGrey, (X,Y), (Targ-(Pos+Dist)),1)
    return
def DDrawCircles(Prog,Time,Set,Pos,Dist,Targ,Row,X,Y,Col):
    X = int(X)
    Y = int(Y)
    if (Time - Prog) > 0 and Row == False:
        pygame.draw.circle(Field, Col, (X,Y), (Time - Prog),1)
    if (Set - Prog) > 0 and Row == False:
        pygame.draw.circle(Field, Col, (X,Y), (Set - Prog),1)
    if (Targ-(Pos+Dist)) > 0 and DActive == True and Row == False:
        pygame.draw.circle(Field,LGrey, (X,Y), (Targ-(Pos+Dist)),1)
    return
def Bladey(Blade,Active,AProg,ADist,ASpeed,Range,ATime,ASet,Pos,GPos,Row):
    Blade = Cull(Blade,Reach)
    (X,Y) = pygame.mouse.get_pos()
    #print(X,Y)
    if Active == True and AProg > ATime and Row == True:
        Active = False
    if Active == False:
        AProg = 0
        ADist = 0
        Blade = []
    if Active == True:
        Point = [(X,Y)]
        #print(Point)
        if len(Blade) == 0:
            #print("Hoy!")
            Blade = Point
        else:
            #print("Hi!")
            #print(Point)
            #print(Blade)
            Blade.insert(0,(X,Y))
            #print(Blade)
        if ADist < Range:
            ADist += ASpeed
        AProg += 1
    DrawCircles(AProg,ATime,ASet,Pos,ADist,GPos,Row,X,Y,HBlue)
    #print(Blade)
    DrawCursor((X,Y))
    #print(Blade)
    BladeHold = DrawBlade(Blade,(X,Y),BladeBlade)
    pygame.display.flip()
    #print("All Done!")
    #print(Active)
    return Blade, Active, AProg, ADist
def DetCut(Active,Pos,ADist,GPos,Row):
    if Active == True and Row == True and (NPos - Pos) <= ADist and AProg >= ASet:
        return True
    else:
        return False

Active = False
Row = False
while(True):
    Clear()
    DrawStart(Pos)
    Pos, DState, Active = Move(Pos,DState,Active)
    State = BoringAI(Pos, NPos, State)
    NPos, State = MoveAI(NPos, State)
    #print(DState,State,Row)
    Row = SimpleRow(Row, DState, State)
    GPos, GNPos = AdjGuard(GPos,GNPos,Row)
    Flit(RangeLines,(0,0),Pos,(Pos+Range))
    Flit(FakeScreen,(0,0),Pos,(750+GNPos))
    Flit(MoonScreen,(0,0),Pos,750)
    Posit(Pos,HBlue)
    Blade, Active, AProg, ADist = Bladey(Blade,Active,AProg,ADist,ASpeed,Range,ATime,ASet,Pos,NPos,Row)
    Score = DetCut(Active, Pos, ADist, GPos,Row)
    if Score == True:
        Hit.play()
        break
Text("Nice work! That was a bit more complicated, wasn't it? Don't worry, Nishar and I will keep you safe until you've learned enough to get by on your own.",NFriend,None)
Text("Well, uh...Nishar will take care of you. I'll try my best.",NFriend,None)
Text("Now, this has all been a bit slow, hasn't it? You scoring points without any resistance.",NFriend,None)
Text("So how about I ATTACK YOU!?!?",NFriend,None)
Text("Oh dear, that wasn't quite how I meant it. How about I attack you in a totally safe, controlled, non-aggressive manner?",NFriend,None)
Text("1) That sounds alright!  2) Are you sure about this?  3) Who are you?  4) You talk too much.",Name,None)    
while(True):
    event = pygame.event.poll()
    if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
        Text("Great! Sorry if I've kinda been freaking you out.",NFriend,None)
        Text("Although I suppose you might need to get used to that feeling here...",NFriend,None)
        break
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
        Text("Trust me! I've practiced A LOT with Nishar.",NFriend,None)
        Text("Although I couldn't hurt her even if I tried...she's *pretty* good.",NFriend,None)
        break
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
        Text("I'm "+NFriend+", your best friend!",NFriend+'[Flustered]',None)
        Text("You'll let me be your best friend, right?",NFriend,None)
        break
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
        Text("...I guess I do. I'm sorry.",NFriend,None)
        Text("There aren't a lot of people here, and just chatting with Nishar can get pretty boring after a while.",NFriend,None)
        break
Text("Anyways! I'm going to try to try to slash you while not actually slashing you!",NFriend,None)
Text("I'm going to take the right of way, so you'll see the same circles you get when you attack.",NFriend,None)
Text("When I cut, try to draw your blade STRAIGHT and PERPENDICULAR to mine. For this it's okay to be a bit sloppy, but for tougher opponents you might need to up your game!",NFriend,None)
Text("Okay! Let's do this! I'll give you a shout before I attack. How about we aim for you to parry four out of five?",NFriend,None)
Text("|EQUIPPED| - Mirror-Edge Sabre",NFriend,None)
CutLim = 25
ParryLim = 15
StraightSens = 36
ParryClose = 15
DSpeed = 2
DRange = 100
DTime = 60
DSet = 50
DProg = 0
DDist = 0
AccParry = 0.85
DStart = (0,0)
DGoal = (0,0)
DBlade = []
DActive = False
DReach = 30
DSteps = 0
Parry = False
ParryPoints = 0
DWait = 0
DHits = 0
DX = 0
DY = 0
NPos = 550
Pos = 450
StepMin = 1
State = 'Stay'
    
def ParryCheck(ABlade,DBlade,CutLim,ParryLim,StraightSens,AccParry):
    #print(ABlade)
    #print(DBlade)
    AEnd = len(ABlade)-1
    DEnd = len(DBlade)-1
    if len(ABlade) < 5:
        return None
    elif len(DBlade) < 5:
        return False
    if Dist(ABlade[0],ABlade[AEnd]) < CutLim:
        return None
    elif Dist(DBlade[0],DBlade[DEnd]) < ParryLim:
        return False
    A1 = 0
    A2 = int(math.floor((len(ABlade)*(1.0/4.0)))-1)
    A3 = int(math.floor((len(ABlade)*(2.0/4.0)))-1)
    A4 = int(math.floor((len(ABlade)*(3.0/4.0)))-1)
    A5 = AEnd
    D1 = 0
    D2 = int(math.floor((len(DBlade)*(1.0/4.0)))-1)
    D3 = int(math.floor((len(DBlade)*(2.0/4.0)))-1)
    D4 = int(math.floor((len(DBlade)*(3.0/4.0)))-1)
    D5 = DEnd
    #print('//////////////////////////////////////////')
    #print(D1,D2,D3,D4,D5)
    GA1 = Angle(ABlade[A1],ABlade[A2])
    GA2 = Angle(ABlade[A2],ABlade[A3])
    GA3 = Angle(ABlade[A3],ABlade[A4])
    GA4 = Angle(ABlade[A4],ABlade[A5])
    GD1 = Angle(DBlade[D1],DBlade[D2])
    GD2 = Angle(DBlade[D2],DBlade[D3])
    GD3 = Angle(DBlade[D3],DBlade[D4])
    GD4 = Angle(DBlade[D4],DBlade[D5])
    GTA = Angle(ABlade[A1],ABlade[A5])
    GTD = Angle(DBlade[D1],DBlade[D5])
    AStraightCheck = 0
    DStraightCheck = 0
    for i in [GA1, GA2, GA3, GA4]:
        AStraightCheck += min(abs(GTA-i),abs(((GTA+180)%360)-i))**2
    #print([GD1, GD2, GD3, GD4])
    for i in [GD1, GD2, GD3, GD4]:
        #print('/////')
        #print(i)
        #print(GTD)
        DStraightCheck += min(abs(GTD-i),abs(((GTD+180)%360)-i))**2
        #print(min(abs(GTD-i),abs(((GTD+180)%360)-i))**2)
    #print('/////////////////////////')
    #print(AStraightCheck)
    #print(DStraightCheck)
    ASC = 1-Sigmoid(AStraightCheck/((StraightSens)**2))
    DSC = 1-Sigmoid(DStraightCheck/((StraightSens)**2))
    #print(GTA)
    #print(GTD)
    AngDiff = 1-(abs(90-min(abs(GTA-GTD),abs(((GTA+180)%360)-GTD))))/180.0
    #print(AngDiff)
    #print(DSC)
    FinalComp = AngDiff + DSC
    #print(FinalComp)
    if FinalComp >= AccParry:
        return True
    else:
        return False
def DBladey(DBlade,DActive,DProg,DDist,DSpeed,DRange,DTime,DSet,NPos,GNPos,Row,DX,DY,DStart,DGoal,DSteps,State):
    DBlade = Cull(DBlade,DReach)
    if State == 'Stay' or 'Attack':
        if DSteps < 60:
            Vec = (DGoal[0]-DStart[0],DGoal[1]-DStart[1])
            Vec = (Vec[0]/30.0,Vec[1]/30.0)
            DX += Vec[0]
            DY += Vec[1]
    if State == 'Parry' or 'Parrying':
        if DSteps < 15:
            Vec = (DGoal[0]-DStart[0],DGoal[1]-DStart[1])
            Vec = (Vec[0]/15.0,Vec[1]/15.0)
            DX += Vec[0]
            DY += Vec[1]
    if DActive == True and DProg > DTime and Row == False:
        DActive = False
        DSteps = 0
    if DActive == False:
        DProg = 0
        DDist = 0
    if DActive == True:
        Point = [(DX,DY)]
        #print(Point)
        if len(DBlade) == 0:
            #print("Hoy!")
            DBlade = Point
        else:
            #print("Hi!")
            #print(Point)
            #print(Blade)
            DBlade.insert(0,(DX,DY))
            #print(Blade)
    if DActive == True:
        if DDist < DRange:
            DDist += DSpeed
        DProg += 1
    DDrawCircles(DProg,DTime,DSet,NPos,DDist,GNPos,Row,DX,DY,EMag)
    #print(Blade)
    #DrawCursor((X,Y))
    #print(Blade)
    BladeHold = DrawBlade(DBlade,(DX,DY),EdithBlade)
    pygame.display.flip()
    #print("All Done!")
    #print(Active)
    return DBlade, DActive, DProg, DDist, DSteps, DX, DY
def DDetCut(DActive,NPos,DDist,Pos,Row,DProg):
    if DActive == True and Row == False and (NPos - Pos) <= DDist and DProg >= DSet:
        return True
    else:
        return False
while(True):
    #print(ParryPoints)
    #print(DSteps)
    #print(DWait)
    #print(DActive)
    #print(DProg)
    if DSteps == 60 or DSteps == 0 and DWait == 100:
        DActive = True
        DSteps = 0
        DProg = 0
        DWait = -1
        EdithShout.play()
        while(True):
            DStart = (random.randint(0,299),random.randint(0,299))
            DGoal = (random.randint(100,200),random.randint(100,200))
            if Dist(DStart,DGoal) > 75:
                break
        DX = DStart[0]
        DY = DStart[1]
    elif DWait == -1 and DActive == True:
        DSteps += 1
    if DWait >= 0 and DActive == False:
        DWait += 1
    Clear()
    DrawStart(Pos)
    Pos, DState, Active = Move(Pos,DState,Active)
    Pos = 450
    State = BoringAI(Pos, NPos, State)
    NPos, State = MoveAI(NPos, State)
    GPos, GNPos = AdjGuard(GPos,GNPos,Row)
    Row = False
    Flit(RangeLines,(0,0),Pos,(Pos+Range))
    Flit(FakeScreen,(0,0),Pos,(550+GNPos))
    Flit(MoonScreen,(0,0),Pos,550)
    Posit(Pos,HBlue)
    Posit(NPos,EMag)
    Blade, Active, AProg, ADist = Bladey(Blade,Active,AProg,ADist,ASpeed,Range,ATime,ASet,Pos,NPos,Row)
    if DActive == True:
        #print("Blading!")
        DBlade, DActive, DProg, DDist, DSteps, DX, DY = DBladey(DBlade,DActive,DProg,DDist,DSpeed,DRange,DTime,DSet,NPos,GNPos,Row,DX,DY,DStart,DGoal,DSteps,State)
    if Blade != [] and DActive == True:
        for sprit in DBlade:
            if Dist(Blade[0],sprit) < ParryClose:
                Parry = ParryCheck(DBlade,Blade,CutLim,ParryLim,StraightSens,AccParry)
                if Parry == True:
                    ForkClick.play()
                    DSteps = 0
                    DActive = False
                    ParryPoints += 1
                    DWait = 0
                    break
    Score = DDetCut(DActive,NPos,DDist,Pos,Row,DProg)
    if Score == True:
        Hit.play()
        DHits += 1
        DActive = False
        DWait = 0
        DSteps = 0
    if DHits == 5:
        Text("Oh dear. Let's try that again! Don't give up! I believe in you! "+NFriend+" realizes they are using too many exclamation points and puts on their best apologetic smile.",NFriend,None)
        DHits = 0
        ParryScore = 0
    if ParryPoints == 4:
        Text("Nice work! That wasn't too bad, was it? Now, there's just a few more things you need to know and you'll be JUST FINE here.",NFriend,None)
        break
Text("You know, I...",NFriend,None)
Text("I probably shouldn't be teaching you. Fencing...isn't really my thing.",NFriend,None)
Text("That was what Nishar first told me, when she found me. She...told me I wasn't meant for this age.",NFriend,None)
Text("I still have no clue what she meant by that. What do you think?",NFriend,None)
Text("(...I still have no idea who this person is, much less what they're talking about...)",Name,None)
Text("(...But it seems to really matter to them, so maybe I should try to come up with something...)",Name,None)
Text("1) Honestly, I have no idea.  2) Who's Nishar?  3) What does it matter? You have a friend here.  4) How did you find me?",Name,None)
while(True):
    event = pygame.event.poll()
    if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
        Text("...Yeah, I suppose you wouldn't.",NFriend,None)
        Text("I'm sorry. Maybe that's what she means - that I worry about silly things that other people don't waste time thinking about.",NFriend,None)
        break
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
        Text("Nishar? She's the guardian of this city. She taught me to read and write and do math.",NFriend,None)
        Text("She never talks about herself, but once, she took me to a broken-down observatory and got the telescope working - just like that!.",NFriend,None)
        Text("She pointed it into deep space, and showed me on a computer how to find radiation trails, relics of the Creation.",NFriend,None)
        Text("Some of them were moving and twisting like fractals, and she said those were angels, undiluted conciousnesses that were bound to the moral fabric of the universe.",NFriend,None)
        Text("I think she's an angel. It's the only explanation for what I've seen her do.",NFriend,None)
        Text("And now she's my mom, I suppose. The best one I could have asked for.",NFriend,None)
        break
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
        Text("What do you mean?",NFriend,None)
        Text("Oh! You'll be...my friend?",NFriend+'[Dawning Realization]',None)
        Text("You really don't have any reason to be friends with the first scatterbrained apprentice sorceror you meet, you know.",NFriend+'[Blushing]',None)
        break
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
        Text("I found you on the beach out there. You were out cold! I took you back here and gave you some fresh water while you were unconcious.",NFriend,None)
        Text("You weren't wet or sandy at all, though, so I wonder?...No, Nishar told me it's pointless to interrogate people until they feel safe.",NFriend,None)
        break
Text("But I could use some parry practice as well. So I was thinking you would attack and I would try to parry it?",NFriend,None)
Text("Oh? Don't worry, I don't think you're anywhere near proficient enough to hurt me.",NFriend,None)
Text("Plus, I'll add one more catch. We're both using SABRE-like weapons, which means we slash. So if you keep your attack in one place, you won't make forward progress.",NFriend,None)

def Bladeq(Blade,Active,AProg,ADist,ASpeed,Range,ATime,ASet,Pos,GPos,Row):
    Blade = Cull(Blade,Reach)
    (X,Y) = pygame.mouse.get_pos()
    #print(X,Y)
    if Active == True and AProg > ATime and Row == True:
        Active = False
    if Active == False:
        AProg = 0
        ADist = 0
        Blade = []
    if Active == True:
        Point = [(X,Y)]
        #print(Point)
        if len(Blade) == 0:
            #print("Hoy!")
            Blade = Point
        elif Dist((X,Y),Blade[0]) > StepMin:
            #print("Hi!")
            #print(Point)
            #print(Blade)
            Blade.insert(0,(X,Y))
            #print(Blade)
            if ADist < Range:
                ADist += ASpeed
                AProg += 1
    DrawCircles(AProg,ATime,ASet,Pos,ADist,GPos,Row,X,Y,HBlue)
    #print(Blade)
    DrawCursor((X,Y))
    #print(Blade)
    BladeHold = DrawBlade(Blade,(X,Y),BladeBlade)
    pygame.display.flip()
    #print("All Done!")
    #print(Active)
    return Blade, Active, AProg, ADist
def ParryLoc(Blade):
     if len(Blade) <= 6:
         return None
     else:
         Spot = random.randint(2,3)
         S1 = Spot - 2
         S2 = Spot + 2
         P = Blade[Spot]
         #print("P:"+str(P))
         P1 = Blade[S1]
         P2 = Blade[S2]
         Vec = (P1[0]-P2[0],P1[1]-P2[1])
         IVec = (Vec[0],Vec[1])
         #print("IVec:"+str(IVec))
         Scale = random.randint(25,50) * 1.0
         if Dist(IVec,(0,0)) == 0:
             return 0, 0, 0
         SIVec = ((IVec[0]*1.0/Dist(IVec,(0,0)))*Scale,(IVec[1]*1.0/Dist(IVec,(0,0)))*Scale)
         #print("SIVec:"+str(SIVec))
         Flip = random.randint(0,1)
         #print("Flip:"+str(Flip))
         if Flip == 0:
             FVec = (SIVec[1]*-1.0,SIVec[0])
         if Flip == 1:
             FVec = (SIVec[1],SIVec[0]*-1.0)
         #print("FVec:"+str(FVec))
         FPoint = (P[0] + FVec[0]+random.randint(-10,10),P[1] + FVec[1]+random.randint(-10,10))
         #print("FPoint:"+str(FPoint))
         return FPoint, P, 1
     
def DefendState(State, Active):
     if State == 'Guard':
         State = 'Guarding'
         #print('Trigger 1')
     elif State == 'Guarding' and Active == True:
         State = 'Parry'
         #print('Trigger 2')
     elif State == 'Parry' and Active == False:
         State = 'Guard'
         #print('Trigger 3')
     elif State == 'Parrying' and Active == False:
         State = 'Guard'
     return State

DProg = 0
DDist = 0
DStart = (0,0)
DGoal = (0,0)
DBlade = []
Blade = []
DActive = False
Row = True
State = 'Guarding'
Active = True
DReach = 30
DSteps = 0
Parry = False
ParryPoints = 0
DWait = 0
DHits = 0
DX = 0
DY = 0
NPos = 550
Pos = 500
Sure = 0
                

while(True):
    if State == 'Guard':
        DActive = True
        while(True):
            DStart = (random.randint(0,299),random.randint(0,299))
            DGoal = (random.randint(0,299),random.randint(0,299))
            if Dist(DStart,DGoal) > 200:
                break
        DX = DStart[0]
        DY = DStart[1]
    if State == 'Parry':
        DActive = True
        if len(Blade) > 7:
            DSt, DGo, Sure = ParryLoc(Blade)
            if Sure == 1:
                DStart = DSt
                DGoal = DGo
                DX = DStart[0]
                DY = DStart[1]
                State = 'Parrying'
    Clear()
    DrawStart(Pos)
    Pos, DState, Active = Move(Pos,DState,Active)
    Pos = 500
    State = DefendState(State, Active)
    if DX > 300 or DX < 0 or DY > 300 or DY < 0:
        State = 'Guard'
    #print(NPos, State, Active)
    NPos, State = MoveAI(NPos, State)
    GPos, GNPos = AdjGuard(GPos,GNPos,Row)
    Row = True
    Flit(RangeLines,(0,0),Pos,(Pos+Range))
    Flit(FakeScreen,(0,0),Pos,(550+GNPos))
    Flit(MoonScreen,(0,0),Pos,550)
    Posit(Pos,HBlue)
    Posit(NPos,EMag)
    Blade, Active, AProg, ADist = Bladeq(Blade,Active,AProg,ADist,ASpeed,Range,ATime,ASet,Pos,NPos,Row)
    if DActive == True:
        #print("Blading!")
        DBlade, DActive, DProg, DDist, DSteps, DX, DY = DBladey(DBlade,DActive,DProg,DDist,DSpeed,DRange,DTime,DSet,NPos,GNPos,Row,DX,DY,DStart,DGoal,DSteps,State)
    if DBlade != [] and Active == True:
        for sprit in Blade:
            if Dist(DBlade[0],sprit) < ParryClose:
                Parry = ParryCheck(Blade,DBlade,CutLim,ParryLim,StraightSens,AccParry)
                if Parry == True:
                    ForkClick.play()
                    Active = False
                    ParryPoints += 1
                    break
    Score = DetCut(Active, Pos, ADist, GPos,Row)
    if Score == True:
        DHits += 1
        Hit.play()
        Active = False
        DWait = 0
    if DHits == 5:
        Text("Oh dear. You aren't good, so I must be pretty bad, huh? Well, it's good to have some to practice with who isn't absolutely perfect.",NFriend,None)
        DHits = 0
        ParryScore = 0
    if ParryPoints == 5:
        Text("See? We can both parry, so we'll be alright here together...Whew. I wasn't sure I was going to make that.",NFriend,None)
        break
Text("You know, you look a lot better than when I found you. And I'm really glad you're fine after all that.",NFriend,None)
Text("You look like a good person, so I think this next part will make sense to you.",NFriend,None)
Text("When you break someone's barrier, you can just walk away, and leave them as they were.",NFriend,None)
Text("Or...Oh great, how do I explain this? You can see inside their soul. You can change things for better or worse.",NFriend,None)
Text("You can HURT them.",NFriend,None)
Text("Listen, I think the only way you're going to understand is if...well...you see...I need to know...",NFriend,None)
Text("Here, people go by two names. One we get when we're born, one we choose ourselves.",NFriend,None)
Text(NFriend+" is my birthname. I like it, but you should know my choice name too.",NFriend,None)
Text("It's Edith.",NFriend,None)
Text("Do you think it's a nice name?",NFriend,None)
VirtualCounterpoint.stop()
Clear()
pygame.display.flip()
Flit(EdithScreen,(0,0),Pos,Pos+1)
pygame.display.flip()
time.sleep(1)
Flit(EdithBossIntro,(0,0),Pos,Pos+1)
pygame.display.flip()
time.sleep(2)
EdithBossMusic.play(loops=-1)
time.sleep(3)

DProg = 0
DDist = 0
DStart = (0,0)
DGoal = (0,0)
DBlade = []
Blade = []
DActive = False
LastAc = False
Active = False
LastDAc = False
Row = None
State = 'Start'
Active = False
DReach = 30
DSteps = 0
Parry = False
ParryPoints = 0
DWait = 0
DHits = 0
DX = 0
DY = 0
NPos = 600
LNPos = 600
Pos = 400
LPos = 400
Sure = 0
Points = 0
NPoints = 0
GoOn = False

def DuelAI(State,Active,Pos,NPos,Row):
    if State == 'Start':
        StartR = random.randint(1,3)
        if StartR != 3:
            return 'Go'
        else:
            return 'Back'
    elif State == 'Go' and Active == False and abs(Pos-NPos) < 90:
        return 'Attack'
    elif State == 'Go' and Active == True and abs(Pos-NPos) < 90:
        return 'Parry'
    elif State == 'Parry':
        return 'Parrying'
    elif State == 'Attack':
        return 'Attacking'
    elif State == 'Parrying' and Active == False:
        return 'Guarding'
    elif State == 'Guard':
        return 'Guarding'
    elif State == 'Guarding' and Active == True:
        return 'Parry'
    elif State == 'Parry' and Row == False:
        return 'Go'
    elif State == 'Attack' and Row == True:
        return 'Back'
    elif State == 'Back' and Active == True:
        return 'Parry'
    elif State == 'Back' and random.randint(1,40) == 40:
        return 'Tricky'
    elif State == 'Tricky':
        return 'Tricking'
    elif State == 'Tricking':
        return 'Back'
    elif State == 'Back' and (random.randint(1,50) == 50 or NPos <= 900):
        return 'Guard'
    elif State == 'Attacking' and DActive == False:
        return 'Go'
    if Row == False and State != 'Go' and State != 'Attack' and State != 'Attacking':
        return 'Go'
    else:
        return State

def DuelMoveAI(State,NPos,Pos):
    if State == 'Go':
        NPos -= 3
    if State == 'Attack' or 'Attacking':
        NPos -= 3
    if State == 'Back':
        NPos += 3
    if NPos < 0:
        NPos = 0
    if NPos > 1000:
        NPos = 0
    if NPos <= Pos:
        NPos = Pos + 3
    if Pos >= NPos:
        Pos = NPos - 3
    return NPos, Pos

def DuelRow(Row,Pos,LPos,NPos,LNPos,LastAc,LastDAc,Active,DActive):
    if Row == None and Pos > LPos and NPos >= LNPos:
        Row = True
    if Row == None and Pos >= LPos and NPos < LNPos:
        Row = False
    if Row == True and Pos >= LPos and NPos < LNPos:
        Row = False
    if Row == False and Pos > LPos and NPos >= LNPos:
        Row = True
    if Active == False and LastAc == True:
        Row = False
    if DActive == False and LastDAc == True:
        Row = True
    return Row,Pos,NPos,Active,DActive
while(True):
##    Text("Make it interesting faster? y/n",Name,None)
##    while(True):
##        event = pygame.event.poll()
##        if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
##            GoOn = True
##            break
##        if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
##            GoOn = False
##            break
##    if GoOn == True:
##        break
    if NPoints > 4:
        Text("Oh dear! Let's start that over.",NFriend,None)
        NPoints = 0
        Points = 0
    if Points > 4:
        Text("Hahaha! You're doing great! But let's make this a little more interesting!",NFriend,None)
        break
    Row = None
    DProg = 0
    DDist = 0
    DStart = (0,0)
    DGoal = (0,0)
    DBlade = []
    Blade = []
    DActive = False
    LastAc = False
    Active = False
    LastDAc = False
    Row = None
    State = 'Start'
    DX = 0
    DY = 0
    NPos = 600
    LNPos = 600
    Pos = 400
    LPos = 400
    Sure = 0
    Tex("En Garde!",'DUEL',None)
    time.sleep(1)
    Tex("Allez!",'DUEL',None)
    Clap.play()
    while(True):
        print(str(State))
        if State == 'Guard':
            DActive = True
            while(True):
                DStart = (random.randint(0,299),random.randint(0,299))
                DGoal = (random.randint(0,299),random.randint(0,299))
                if Dist(DStart,DGoal) > 200:
                    break
            DX = DStart[0]
            DY = DStart[1]
        if State == 'Parry':
            DActive = True
            if len(Blade) > 7:
                DSt, DGo, Sure = ParryLoc(Blade)
                if Sure == 1:
                    DStart = DSt
                    DGoal = DGo
                    DX = DStart[0]
                    DY = DStart[1]
                    State = 'Parrying'
        if State == 'Attack':
            DActive = True
            while(True):
                DStart = (random.randint(0,299),random.randint(0,299))
                DGoal = (random.randint(100,200),random.randint(100,200))
                if Dist(DStart,DGoal) > 75:
                    break
            DX = DStart[0]
            DY = DStart[1]
        Clear()
        DrawStart(Pos)
        Pos, DState, Active = Move(Pos,DState,Active)
        State = DuelAI(State,Active,Pos,NPos,Row)
        NPos, Pos = DuelMoveAI(State,NPos,Pos)
        Row,LPos,LNPos,LastAc,LastDac = DuelRow(Row,Pos,LPos,NPos,LNPos,LastAc,LastDAc,Active,DActive)
        if DX > 300 or DX < 0 or DY > 300 or DY < 0:
            if State == 'Parrying':
                State = 'Guard'
            if State == 'Attacking':
                Row = True
                State = 'Back'
        GPos, GNPos = AdjGuard(GPos,GNPos,Row)
        Flit(RangeLines,(0,0),Pos,(Pos+Range))
        Flit(EdithScreen,(0,0),Pos,(NPos+GNPos))
        Flit(MoonScreen,(0,0),Pos,NPos)
        Posit(Pos,HBlue)
        Posit(NPos,EMag)
        Blade, Active, AProg, ADist = Bladeq(Blade,Active,AProg,ADist,ASpeed,Range,ATime,ASet,Pos,NPos,Row)
        if DActive == True:
            DBlade, DActive, DProg, DDist, DSteps, DX, DY = DBladey(DBlade,DActive,DProg,DDist,DSpeed,DRange,DTime,DSet,NPos,GNPos,Row,DX,DY,DStart,DGoal,DSteps,State)
        if DBlade != [] and Active == True and Row == True:
            for sprit in Blade:
                if Dist(DBlade[0],sprit) < ParryClose:
                    Parry = ParryCheck(Blade,DBlade,CutLim,ParryLim,StraightSens,AccParry)
                    if Parry == True:
                        ForkClick.play()
                        Active = False
                        Row = False
                        break
        if Blade != [] and DActive == True and Row == False:
            for sprit in DBlade:
                if Dist(Blade[0],sprit) < ParryClose:
                    Parry = ParryCheck(DBlade,Blade,CutLim,ParryLim,StraightSens,AccParry)
                    if Parry == True:
                        ForkClick.play()
                        DActive = False
                        State = 'Back'
                        Row = True
                        break
        Score = DetCut(Active, Pos, ADist, GPos,Row)
        DScore = DDetCut(DActive,NPos,DDist,NPos,Row,DProg)
        if Score == True and Row == True:
            Points += 1
            Hit.play()
            Tex("Point to "+Name,'DUEL',None)
            time.sleep(1)
            break
        if DScore == True and Row == False:
            NPoints += 1
            Hit.play()
            Tex("Point to "+NFriend,'DUEL',None)
            time.sleep(1)
            break
Fires = []
Pos = 450
NPos = 800
for i in range(4):
    Fires = []
    for j in range(i):
        Fires.append([random.randint(50,250),random.randint(50,250),800+random.randint(-50,50)])
    Firesound.play()
    while(True):
        Clear()
        DrawStart(Pos)
        Pos, DState, Active = Move(Pos,DState,Active)
        if Pos > 600:
            Pos = 600
        Flit(RangeLines,(0,0),Pos,(Pos+Range))
        Flit(EdithScreen,(0,0),Pos,(NPos+GNPos))
        Flit(MoonScreen,(0,0),Pos,NPos)
        Flit(FireBase,(0,0),Pos,600)
        Posit(Pos,HBlue)
        Posit(NPos,EMag)
        Row = False
        Blade, Active, AProg, ADist = Bladeq(Blade,Active,AProg,ADist,ASpeed,Range,ATime,ASet,Pos,NPos,Row)
        if len(Fires) == 0:
            break
        print(Fires)
        for q in range(len(Fires)):
            if q >= len(Fires):
                break
            print(q)
            Fire = Fires[q]
            Fire[2] -= 7
            Flit(Fireball,(Fire[0]-15,Fire[1]-15),Pos,Fire[2])
            if Fire[2]-Pos > 0:
                    pygame.draw.circle(Field, Red, (Fire[0]-15,Fire[1]-15), Fire[2]-Pos,1)
            if abs(Fire[2]-Pos) < 10:
                i = 0
                break
            if len(Blade) > 0:
                if Dist((Fire[0],Fire[1]),Blade[0]) < 25 and abs(Pos-Fire[2]) < 75:
                    del Fires[q]
                    Firesound.play()
        pygame.display.flip()
Text("Nice! But I wonder if you can handle this? ;)",NFriend,None)
Points = 0
NPoints = 0
while(True):
    if NPoints > 2:
        Text("Don't give up!",NFriend,None)
        NPoints = 0
        Points = 0
    if Points > 2:
        Text("You're doing fantastic! So let's GET REAL.",NFriend,None)
        break
    Row = None
    DProg = 0
    DDist = 0
    DStart = (0,0)
    DGoal = (0,0)
    DBlade = []
    Blade = []
    DActive = False
    LastAc = False
    Active = False
    LastDAc = False
    Row = None
    State = 'Start'
    DX = 0
    DY = 0
    NPos = 600
    LNPos = 600
    Pos = 400
    LPos = 400
    Sure = 0
    Tex("En Garde!",'DUEL',None)
    time.sleep(1)
    Tex("Allez!",'DUEL',None)
    Clap.play()
    while(True):
        if State == 'Guard':
            DActive = True
            while(True):
                DStart = (random.randint(0,299),random.randint(0,299))
                DGoal = (random.randint(0,299),random.randint(0,299))
                if Dist(DStart,DGoal) > 200:
                    break
            DX = DStart[0]
            DY = DStart[1]
        if State == 'Parry':
            DActive = True
            if len(Blade) > 7:
                DSt, DGo, Sure = ParryLoc(Blade)
                if Sure == 1:
                    DStart = DSt
                    DGoal = DGo
                    DX = DStart[0]
                    DY = DStart[1]
                    State = 'Parrying'
        if State == 'Attack':
            DActive = True
            while(True):
                DStart = (random.randint(0,299),random.randint(0,299))
                DGoal = (random.randint(100,200),random.randint(100,200))
                if Dist(DStart,DGoal) > 75:
                    break
            DX = DStart[0]
            DY = DStart[1]
        if State == 'Attack' and NPos > Pos + 50 and random.randint(1,20) == 20:
            NPos = Pos + 50
            Whoosh.play()
        if State == 'Back' and random.randint(1,10) == 10:
            NPos += 200
            State = 'Guard'
            Whoosh.play()
        if State == 'Guarding' and random.randint(1,15) == 15:
            if random.randint(1,2) == 1:
                NPos += 50
                Whoosh.play()
            else:
                NPos -= 50
                Whoosh.play()
        Clear()
        DrawStart(Pos)
        Pos, DState, Active = Move(Pos,DState,Active)
        State = DuelAI(State,Active,Pos,NPos,Row)
        NPos, Pos = DuelMoveAI(State,NPos,Pos)
        Row,LPos,LNPos,LastAc,LastDac = DuelRow(Row,Pos,LPos,NPos,LNPos,LastAc,LastDAc,Active,DActive)
        if DX > 300 or DX < 0 or DY > 300 or DY < 0:
            State = 'Guard'
        GPos, GNPos = AdjGuard(GPos,GNPos,Row)
        Flit(RangeLines,(0,0),Pos,(Pos+Range))
        Flit(EdithScreen,(0,0),Pos,(NPos+GNPos))
        Flit(MoonScreen,(0,0),Pos,NPos)
        Posit(Pos,HBlue)
        Posit(NPos,EMag)
        Blade, Active, AProg, ADist = Bladeq(Blade,Active,AProg,ADist,ASpeed,Range,ATime,ASet,Pos,NPos,Row)
        if DActive == True:
            DBlade, DActive, DProg, DDist, DSteps, DX, DY = DBladey(DBlade,DActive,DProg,DDist,DSpeed,DRange,DTime,DSet,NPos,GNPos,Row,DX,DY,DStart,DGoal,DSteps,State)
        if DBlade != [] and Active == True and Row == True:
            for sprit in Blade:
                if Dist(DBlade[0],sprit) < ParryClose:
                    Parry = ParryCheck(Blade,DBlade,CutLim,ParryLim,StraightSens,AccParry)
                    if Parry == True:
                        ForkClick.play()
                        Active = False
                        Row = False
                        break
        if Blade != [] and DActive == True and Row == False:
            for sprit in DBlade:
                if Dist(Blade[0],sprit) < ParryClose:
                    Parry = ParryCheck(DBlade,Blade,CutLim,ParryLim,StraightSens,AccParry)
                    if Parry == True:
                        ForkClick.play()
                        DActive = False
                        Row = True
                        break
        Score = DetCut(Active, Pos, ADist, GPos,Row)
        DScore = DDetCut(DActive,NPos,DDist,NPos,Row,DProg)
        if Score == True and Row == True:
            Points += 1
            Hit.play()
            Tex("Point to "+Name,'DUEL',None)
            time.sleep(1)
            break
        if DScore == True and Row == False:
            NPoints += 1
            Hit.play()
            Tex("Point to "+NFriend,'DUEL',None)
            time.sleep(1)
            break
for i in range(6):
    Fires = []
    for j in range(i):
        Fires.append([random.randint(50,250),random.randint(50,250),800+random.randint(-50,50)])
    while(True):
        Clear()
        DrawStart(Pos)
        Pos, DState, Active = Move(Pos,DState,Active)
        if Pos > 600:
            Pos = 600
        Flit(RangeLines,(0,0),Pos,(Pos+Range))
        Flit(EdithScreen,(0,0),Pos,(NPos+GNPos))
        Flit(MoonScreen,(0,0),Pos,NPos)
        Flit(FireBase,(0,0),Pos,600)
        Posit(Pos,HBlue)
        Posit(NPos,EMag)
        Row = False
        Blade, Active, AProg, ADist = Bladeq(Blade,Active,AProg,ADist,ASpeed,Range,ATime,ASet,Pos,NPos,Row)
        if len(Fires) == 0:
            break
        for q in range(len(Fires)):
            if q >= len(Fires):
                break
            print(q)
            Fire = Fires[q]
            Fire[2] -= 7
            Flit(Fireball,(Fire[0]-15,Fire[1]-15),Pos,Fire[2])
            if Fire[2]-Pos > 0:
                    pygame.draw.circle(Field, Red, (Fire[0]-15,Fire[1]-15), Fire[2]-Pos,1)
            if abs(Fire[2]-Pos) < 10:
                i = 0
                break
            if len(Blade) > 0:
                if Dist((Fire[0],Fire[1]),Blade[0]) < 25 and abs(Pos-Fire[2]) < 75:
                    del Fires[q]
                    Firesound.play()
        pygame.display.flip()
Text("Isn't this FUN?!?!?!?!",NFriend,None)
Points = 0
NPoints = 0
while(True):
    if NPoints > 1:
        Text("Don't give up!",NFriend,None)
        NPoints = 0
        Points = 0
    if Points > 1:
        Text("Woah...you...beat...me...fair and square...nice...work...",NFriend+'[Panting]',None)
        break
    Row = None
    DProg = 0
    DDist = 0
    DStart = (0,0)
    DGoal = (0,0)
    DBlade = []
    Blade = []
    DActive = False
    LastAc = False
    Active = False
    LastDAc = False
    Row = None
    State = 'Start'
    DX = 0
    DY = 0
    NPos = 550
    LNPos = 550
    Pos = 450
    LPos = 450
    Sure = 0
    Fires = []
    Tex("En Garde!",'DUEL',None)
    time.sleep(1)
    Tex("Allez!",'DUEL',None)
    Clap.play()
    while(True):
        if State == 'Guard':
            DActive = True
            while(True):
                DStart = (random.randint(0,299),random.randint(0,299))
                DGoal = (random.randint(0,299),random.randint(0,299))
                if Dist(DStart,DGoal) > 200:
                    break
            DX = DStart[0]
            DY = DStart[1]
        if State == 'Parry':
            DActive = True
            if len(Blade) > 7:
                DSt, DGo, Sure = ParryLoc(Blade)
                if Sure == 1:
                    DStart = DSt
                    DGoal = DGo
                    DX = DStart[0]
                    DY = DStart[1]
                    State = 'Parrying'
        if State == 'Attack':
            DActive = True
            while(True):
                DStart = (random.randint(0,299),random.randint(0,299))
                DGoal = (random.randint(100,200),random.randint(100,200))
                if Dist(DStart,DGoal) > 75:
                    break
            DX = DStart[0]
            DY = DStart[1]
        if State == 'Attack' and NPos > Pos + 50 and random.randint(1,20) == 20:
            NPos = Pos + 50
            Whoosh.play()
        if State == 'Back' and random.randint(1,10) == 10:
            NPos += 200
            State = 'Guard'
            Whoosh.play()
        if State == 'Guarding' and random.randint(1,15) == 15:
            if random.randint(1,2) == 1:
                NPos += 50
                Whoosh.play()
            else:
                NPos -= 50
                Whoosh.play()
        if random.randint(1,75) == 75:
            Fires.append([random.randint(50,250),random.randint(50,250),800+random.randint(-50,50)])
            Firesound.play()
        Fires
        Clear()
        DrawStart(Pos)
        Pos, DState, Active = Move(Pos,DState,Active)
        State = DuelAI(State,Active,Pos,NPos,Row)
        NPos, Pos = DuelMoveAI(State,NPos,Pos)
        Row,LPos,LNPos,LastAc,LastDac = DuelRow(Row,Pos,LPos,NPos,LNPos,LastAc,LastDAc,Active,DActive)
        if DX > 300 or DX < 0 or DY > 300 or DY < 0:
            State = 'Guard'
        GPos, GNPos = AdjGuard(GPos,GNPos,Row)
        Flit(RangeLines,(0,0),Pos,(Pos+Range))
        Flit(EdithScreen,(0,0),Pos,(NPos+GNPos))
        Flit(MoonScreen,(0,0),Pos,NPos)
        Posit(Pos,HBlue)
        Posit(NPos,EMag)
        Blade, Active, AProg, ADist = Bladeq(Blade,Active,AProg,ADist,ASpeed,Range,ATime,ASet,Pos,NPos,Row)
        if DActive == True:
            DBlade, DActive, DProg, DDist, DSteps, DX, DY = DBladey(DBlade,DActive,DProg,DDist,DSpeed,DRange,DTime,DSet,NPos,GNPos,Row,DX,DY,DStart,DGoal,DSteps,State)
        if DBlade != [] and Active == True and Row == True:
            for sprit in Blade:
                if Dist(DBlade[0],sprit) < ParryClose:
                    Parry = ParryCheck(Blade,DBlade,CutLim,ParryLim,StraightSens,AccParry)
                    if Parry == True:
                        ForkClick.play()
                        Active = False
                        Row = False
                        break
        if Blade != [] and DActive == True and Row == False:
            for sprit in DBlade:
                if Dist(Blade[0],sprit) < ParryClose:
                    Parry = ParryCheck(DBlade,Blade,CutLim,ParryLim,StraightSens,AccParry)
                    if Parry == True:
                        ForkClick.play()
                        DActive = False
                        Row = True
                        break
        if len(Fires) > 0:
            if q >= len(Fires):
                break
            print(q)
            Fire = Fires[q]
            Fire[2] -= 7
            Flit(Fireball,(Fire[0]-15,Fire[1]-15),Pos,Fire[2])
            if Fire[2]-Pos > 0:
                    pygame.draw.circle(Field, Red, (Fire[0]-15,Fire[1]-15), Fire[2]-Pos,1)
            if abs(Fire[2]-Pos) < 10:
                DPoints += 1
                Hit.play()
                Text("Point to "+NFriend,'DUEL',None)
                time.sleep(2)
                break
            if len(Blade) > 0:
                if Dist((Fire[0],Fire[1]),Blade[0]) < 25 and abs(Pos-Fire[2]) < 75:
                    del Fires[q]
                    Firesound.play()
                    
        pygame.display.flip()
        Score = DetCut(Active, Pos, ADist, GPos,Row)
        DScore = DDetCut(DActive,NPos,DDist,NPos,Row,DProg)
        if Score == True and Row == True:
            Points += 1
            Hit.play()
            Tex("Point to "+Name,'DUEL',None)
            time.sleep(1)
            break
        if DScore == True and Row == False:
            DPoints += 1
            Hit.play()
            Tex("Point to "+NFriend,'DUEL',None)
            time.sleep(1)
            break
Text("That was...so much fun. Thank you. I'm so sorry I got a bit carried away.",NFriend,None)
Clear()
Flit(EdithScreen,(0,0),1000)
display.flip()
Text("Now, there's one more thing. Walk to one end of the field.",NFriend,None)
while(Pos != 1000 or Pos != 0):
    Clear()
    Flit(EdithScreen,(0,0),1000)
    Pos, DState, Active = Move(Pos,DState,Active)
    Posit(Pos,HBlue)
    pygame.display.flip()
if Pos == 0:
    Text("So you chose to let me be. Great, let's go find Nishar.",NFriend,None)
    Text("I think...we're going to be great friends.",NFriend,None)
    Text("THANKS FOR PLAYING!","HENRY",None)
    time.sleep(3)
    pygame.quit()
elif Pos == 1000:
    Clear()
    Flit(EdithScreen,(0,0),1000)
    pygame.display.flip()
    Text("(...It's dark in here...and unexpectedly chilly...there's an icy breeze from somewhere...)",Name,None)
    Text("You're inside my soul. Why don't you EXIT? It's not a nice place to be, trust me.",NFriend,None)
    while(True):
        Phrase = str(input('}'))
        if Phrase == 'EXIT':
            Clear()
            pygame.display.flip()
            Text("Sorry you had to see that. Let's go find Nishar.",NFriend,None)
            Text("I think...we're going to be great friends.",NFriend,None)
            Text("THANKS FOR PLAYING!","HENRY",None)
            time.sleep(3)
            pygame.quit()
            break
        elif Phrase == 'HURT':
            Text("(...The darkness is dissolving...)",Name,None)
            Text("I'm sorry. I didn't want things to end this way.",NFriend,None)
            Text(NFriend+" snaps her fingers. You are engulfed in flame.","",None)
            Firesound.play()
            time.sleep(3)
            pygame.quit()

                

            
        






         



    
                    

                     

                                                                        
    
