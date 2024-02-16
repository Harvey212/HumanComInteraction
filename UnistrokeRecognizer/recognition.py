import math
import template as tp


size =200

def transform(points):
    points = resample(points)
    points = move2zero(points)
    points = scaletosquare(points,size)
    points = translatetoorigin(points)
    return points


def resample(points):
    Interval= pathlength(points)/ 31
    ACCD = 0.0
    newpoints = [points[0]]
    
    for i in range(1, len(points)):
        d = distance(points[i-1],points[i])
        if (ACCD+d)>=Interval:
            if d==0:
                d=0.0000001
            x = points[i-1][0]+((Interval-ACCD)/d)*(points[i][0]-points[i-1][0])
            y = points[i-1][1]+((Interval-ACCD)/d)*(points[i][1]-points[i-1][1])
            newpt = (int(x),int(y))
            newpoints.append(newpt)
            points[i] = (x,y)
            ACCD=0.0
        else: 
            ACCD += d 
    return newpoints

def move2zero(points):
    c = centroid(points)
    theta = math.atan2(c[1]-points[0][1],c[0]-points[0][0])
    newpoints = rotateby(points, -theta)
    return newpoints



def rotateby(points, theta):
    c = centroid(points)
    cos = math.cos(theta)
    sin = math.sin(theta)
    newpoints=[]
    for i in range(0, len(points)-1):
        qx = (points[i][0]-c[0])*cos-(points[i][1]-c[1])*sin+c[0]
        qy = (points[i][0]-c[0])*sin+(points[i][1]-c[1])*cos+c[1]
        q=(int(qx),int(qy))
        newpoints.append(q)
    return newpoints

def scaletosquare(points, size):
    newpoints=[]
    B = boundingbox(points)
    b2=B[2]
    b3=B[3]
    for i  in range(0,len(points)-1):
        if b2==0:  
            b2=0.000000001
        if b3==0:
            b3=0.000000001
        x = points[i][0]*(size/b2)
        y = points[i][1]*(size/b3)
        pt= (int(x),int(y))
        newpoints.append(pt)
    return newpoints

def translatetoorigin(points):
    newpoints=[]
    c = centroid(points)
    for i in range(0,len(points)-1):
        x = points[i][0]-c[0]
        y = points[i][1]-c[1]
        pt = (x,y)
        newpoints.append(pt)
    return newpoints

def boundingbox(points):
    minX = float("+Inf")
    maxX = float("-Inf")
    minY = float("+Inf")
    maxY = float("-Inf")
    for i in range(0,len(points)-1):
        if points[i][0]<minX:
            minX = points[i][0]
        if points[i][0] > maxX:
            maxX = points[i][0]
        if points[i][1] < minY:
            minY = points[i][1]
        if points[i][1] > maxY:
            maxY = points[i][1]
    return (minX,minY,maxX-minX,maxY-minY)

def distanceatbestangle(points, data, thetaa,thetab,thetad):
    u = 1/2*(-1+math.sqrt(5))
    x1 = u*thetaa + (1-u)*thetab
    f1 = distanceatangle(points, data, x1)
    x2 = (1-u)*thetaa + u*thetab
    f2 = distanceatangle(points, data, x2)
    while abs(thetab-thetaa)>thetad:
        if f1<f2:
            thetab = x2
            x2=x1
            f2=f1
            x1=u*thetaa+(1-u)*thetab
            f1=distanceatangle(points,data,x1)
        else:
            thetaa=x1
            x1=x2
            f1=f2
            x2=(1-u)*thetaa+u*thetab
            f2=distanceatangle(points, data,x2)
    return min(f1,f2)
def distanceatangle(points,data,theta):
    newpoints = rotateby(points, theta)
    d= pathdistance(newpoints, data)
    return d





def recognize(points):
    mark =float("+inf")
    
    bestnumber="0"
    score=0.0
    bestcoo=[]
    points=transform(points)

    #print(points)

    numdic=tp.numdict

    for number in numdic:
        for data in numdic[number]:            
            d = distanceatbestangle(points,data,0.79,-0.79,0.03)
            if d<mark:
                mark=d
                bestcoo=data
                bestnumber=number
    score=1-mark/(0.5*math.sqrt(size**2+size**2))
    return(bestnumber,score)



def distance(p1, p2):
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]
    return math.sqrt(x*x + y*y)

def pathlength(pts):
    d = 0.0
    for i in range(1,len(pts)):
        d = d+distance(pts[i-1],pts[i])
    return d

def pathdistance(A,B):
    d=0.0
    lenA = len(A)
    for i in range(0, lenA-1):
        d=d+distance(A[i],B[i])
    return d/lenA


def centroid(points):
    x=0
    y=0
    for i in range(1,len(points)):
        x += points[i][0]
        y += points[i][1]
    x /= len(points)
    y /= len(points)
    return (int(x),int(y))






