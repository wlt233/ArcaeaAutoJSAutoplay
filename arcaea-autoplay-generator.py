# Arcaea AutoJS Autoplay Experimental v0.2.0

# Distributed with Apache License 2.0

import math

'''
Arguments
'''
screenWidth = 3120 # Screen Width
screenHeight = 1440 # Screen Height
refreshRate = 12  # Judgement Refresh Rate for Hold, Arc and ArcTap

tapIndexX = [2355, 1862, 1343, 863] # X-Coodinate for Track 1, 2, 3, 4

offset = 5560 # Input Offset

slot = [[100, 9, 0, 1557, 815], [300, 9, 1, 0, 0]] # Press the Restart Button by Default

arcPressed = [False, False, False] # Indicate if the Arcs are Pressed

startHeight = screenHeight * 0.81 # Y Coodinate with Height 0.00 in aff
startWidth = screenWidth * 0.33 # X Coodinate with Width 0.00 in aff
endHeight = screenHeight * 0.37 # Y Coodinate with Height 1.00 in aff
endWidth = screenWidth * 0.71 # X Coodinate with Width 1.00 in aff
height = startHeight - endHeight # Height for the Judgement Area
width = endWidth - startWidth # Width for the Judgement Area

'''
AFF --> TouchEvent List
'''

# Get Params in AFF
def getParams(str):
    paramStrings = str.split('(')[1].split(')')[0].split(',')
    params = []
    for i in paramStrings:
        try:
            if i.find('.') != -1:
                params.append(float(i))
            else:
                params.append(int(i))
        except BaseException:
            params.append(i)
    return params

# Get Timestamps for ArcTaps
# Output is a list with timestamps of all arctaps
def getArcTaps(str):
    arcTapList = str.split('[')[1].split(']')[0].split(',')
    for i in range(len(arcTapList)):
        arcTapList[i] = int(arcTapList[i].split('(')[1].split(')')[0])
    return arcTapList

# Generate the touchscreen coodinates for the moving Arcs
# arcNumber The ID of the arc (0: Blue, 1: Red, 2: Green)
# startX: Height at which the arc starts (Arc Argument, 取值-0.50~1.50)
# startY: Width  at which the arc starts (Arc Argument, 取值0.00~1.00)
# endX: Height at which the arc ends (Arc Argument, 取值0.00~1.00)
# endY: Width  at which the arc ends (Arc Argument, 取值0.00~1.00)
def generateArcTouchPoints(arcNumber, startX, endX, startY, endY, startTime, endTime, arcType):
    timePeriod = float(endTime - startTime)
    pointCount = 0
    slotId = arcNumber
    if startTime > 88190:
        slotId += 10
    while startTime < endTime:
        startTime += refreshRate
        pointCount += 1
        if arcType == 'b':
            currentPercentageX = (math.sin((pointCount * refreshRate / timePeriod) * 3 - 1.5708) + 1)/2
            currentPercentageY = (math.sin((pointCount * refreshRate / timePeriod) * 3 - 1.5708) + 1)/2
        elif arcType == 's':
            currentPercentageX = pointCount * refreshRate / timePeriod
            currentPercentageY = pointCount * refreshRate / timePeriod
        elif arcType == 'si':
            currentPercentageX = math.sqrt(pointCount * refreshRate / timePeriod)
            currentPercentageY = math.sqrt(pointCount * refreshRate / timePeriod)
        elif arcType == 'so':
            currentPercentageX = math.pow(pointCount * refreshRate / timePeriod, 2)
            currentPercentageY = math.pow(pointCount * refreshRate / timePeriod, 2)
        elif arcType == 'sisi':
            currentPercentageX = math.sqrt(pointCount * refreshRate / timePeriod)
            currentPercentageY = pointCount * refreshRate / timePeriod
        elif arcType == 'sosi': 
            currentPercentageX = math.pow(pointCount * refreshRate / timePeriod, 2)
            currentPercentageY = math.sqrt(pointCount * refreshRate / timePeriod)
        elif arcType == 'siso':
            currentPercentageX = math.sqrt(pointCount * refreshRate / timePeriod)
            currentPercentageY = math.pow(pointCount * refreshRate / timePeriod, 2)
        elif arcType == 'soso':
            currentPercentageX = math.pow(pointCount * refreshRate / timePeriod, 2)
            currentPercentageY = pointCount * refreshRate / timePeriod
        currentX = endWidth + currentPercentageX * (startX - endX) * width - startX * width
        currentY = endHeight + currentPercentageY * (startY - endY) * height + (1.00 - startY) * height
        if arcNumber == 0:
            slot.append([int(startTime+offset+15), slotId, 2, int(currentX), int(currentY)])
        elif arcNumber == 1:
            slot.append([int(startTime+offset-10), slotId, 2, int(currentX), int(currentY)])
        else:
            slot.append([int(startTime+offset-10), slotId, 2, int(currentX), int(currentY)])


# 获取ArcTap的坐标
# arcTapList: 当前Arc上的ArcTap列表
def generateArcTapTouchPoints(startX, endX, startY, endY, startTime, endTime, arcTapList):

    timePeriod = float(startTime - endTime)

    for arcTap in arcTapList:

        currentPercentage = (arcTap - startTime) / timePeriod
        currentX = endWidth - currentPercentage * (startX - endX) * width - startX * width
        currentY = currentPercentage * (endY - startY) * height + endHeight + (1.00 - startY) * height

        slotId = 3
        
        reCheck = True
        while reCheck:
            for event in slot:
                if (int(arcTap+offset) - 150) < event[0] < (int(arcTap+offset) + 150) and event[1] == slotId:
                    slotId += 1
                    break 
            reCheck = False
        if slotId > 4:
            print('Error: More than two ArcTaps appeared at very close time.')
            exit()

        slot.append([int(arcTap+offset), slotId, 0, int(currentX), int(currentY)])
        slot.append([int(arcTap+offset)+20, slotId, 2, 0, 0])

# Main Program
with open('0.aff','r') as aff:
    for line in aff:
        if line.startswith('AudioOffset'):
            offset = offset - float(line.split(':')[1])/1000
        elif line.startswith('(') or  line.startswith('  ('): # Tap
            params = getParams(line)
            slot.append([int(params[0]+offset), params[1]+4, 0, tapIndexX[params[1]-1], 1190])
            slot.append([int(params[0]+offset)+20, params[1]+4, 2, 0, 0])
        elif line.startswith('arc') or  line.startswith('  arc'): # Arc
            params = getParams(line)
            if params[9] == 'true': # Determine whether it is a black line
                if line.find('[') > -1: # Determine whether there are arctaps on it
                    generateArcTapTouchPoints(params[2], params[3], params[5], params[6], params[0], params[1], getArcTaps(line))
            else:
                if not arcPressed[params[7]]: # Press the Arc if not pressed
                    if params[7] == 0:
                        slot.append([int(params[0]+offset)-200, 0, 0, 2000, 200])
                    elif params[7] == 1:
                        slot.append([int(params[0]+offset)-300, 1, 0, 1000, 200])
                    else:
                        slot.append([int(params[0]+offset)-300, 2, 0, 1500, 200])
                    arcPressed[params[7]] = True
                generateArcTouchPoints(params[7], params[2], params[3], params[5], params[6], params[0], params[1], params[4])
                a = params[7]
                if params[0] > 104000:
                    a += 10
                if params[7] == 0:
                    slot.append([int(params[1]+offset+60), a, 2, 500, 300])
                elif params[7] == 1:
                    slot.append([int(params[1]+offset+60), a, 2, 3000, 300])
                else:
                    slot.append([int(params[1]+offset+60), a, 2, 1500, 300])
                
                    
        elif line.startswith('hold') or line.startswith('  hold'): # Hold
            params = getParams(line)
            slot.append([int(params[0]+offset)+20, params[2]+4, 0, tapIndexX[params[2]-1], 1190])
            startTime = params[0]
            while startTime < params[1]:
                startTime += refreshRate / 3
                slot.append([int(startTime+offset+20), params[2]+4, 2, tapIndexX[params[2]-1], 1190])

    
    # Release the Arc if it is pressed
    for i in range(3):
        if arcPressed[i]:
            slot.append([slot[-1][0]+1000, i, 1, 0, 0])
            print("ok")

    aff.close()

# sort

def takeFirst(elem):
    return elem[0]

slot.sort(key=takeFirst)

'''
Test
'''

#for line in slot:
#    print(str(line))

#print(str(slot))


'''
Output
'''


with open('arcaea-autoplay-script.js','r+') as js:
    lines = js.readlines()
    lines[7] = "var slot = " + str(slot) + "\n"
    js.close()

with open('arcaea-autoplay-script.js','w+') as js:
    js.writelines(lines)
    js.close()