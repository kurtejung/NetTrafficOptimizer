from __future__ import division
from visual import *


##  length units are to be in feet for ease of use in the USA ('Merica!)
light_rad=0.75
road_width = 24
stripe_length=10
stripe_width=1
stripe_spacing=30
block_length = 350 #center to center
temp_light = None
road_length = 350

##  set camera so that we are looking down onto streets
scene.forward = vector(0,-1,0)
scene.width=800
scene.height=800
#scene.autocenter = 1

#create a list of lights to compare...
ns_list_of_lights = []
ew_list_of_lights = []

##  set a global dictionary to associate direction names with vectors
##  to access them use directions['north'], directions['south'], etc.
directions = {'north':vector(0,0,-1), 'south':vector(0,0,1), 'east':vector(1,0,0), 'west':vector(-1,0,0)}

##  create a north, south, east, and west compass on map for ease of use
##  NOTE: North is -z, South is +z, East is +x, and West is -x
'''
comp_scale = 4
north_vec = arrow(pos=comp_scale*vector(10,0,10), axis=comp_scale*vector(0,0,-5), color=color.red)
north_text = text(text="North (-z)", pos = north_vec.pos+north_vec.axis, height=1*comp_scale, color=north_vec.color, up=vector(0,0,-1))
south_vec = arrow(pos=north_vec.pos, axis=comp_scale*vector(0,0,5), color=color.white)
south_text = text(text="South (+z)", pos = south_vec.pos+south_vec.axis + vector(0,0,1), height=1*comp_scale, color=south_vec.color, up=vector(0,0,-1))
east_vec = arrow(pos=north_vec.pos, axis=comp_scale*vector(5,0,0), color=color.green)
east_text = text(text="East (-x)", pos = east_vec.pos+east_vec.axis+vector(0,0,-1), height=1*comp_scale, color=east_vec.color, up=vector(0,0,-1))
west_vec = arrow(pos=north_vec.pos, axis=comp_scale*vector(-5,0,0), color=color.blue)
west_text = text(text="West (+x)", pos = west_vec.pos+west_vec.axis+vector(0,0,-1), height=1*comp_scale, color=west_vec.color, up=vector(0,0,-1))
'''

##  create a road class that will be the base of the others; use this to make easier position managment
class Road():
    def __init__(self, YorXpos, distance, direction):
    	xpos=0
    	ypos=0
    	if(dot(direction,vector(0,0,-1))):
    		xpos=YorXpos
    	if(dot(direction,vector(1,0,0))):
    		ypos=YorXpos
    	print "creating road with coordinates",vector(xpos,0,ypos)
        self.base=frame(pos=vector(0,0,0), up=vector(0,1,0), axis=direction)
        self.pave = box(frame=self.base,pos=vector(xpos,0,ypos), length=distance, width = road_width, height=0.25, color=(0.5,0.5,0.5), axis=vector(1,0,0)) #axis here points along axis of frame
        #lane stripes are 10 feet long and 30 feet spacing between them  (not sure about spacing...)
        self.stoplight_list=[]
        stripe_list=[]
        stripe_pos_list=[]
        stripe_zpos_list=range(int(-self.pave.length/2),int(self.pave.length/2+stripe_spacing),stripe_spacing)
        for z in stripe_zpos_list:
            stripe_pos_list.append(vector(z+xpos,0,ypos))
        for position in stripe_pos_list:
            stripe_list.append( box( frame=self.base, pos = position, length=stripe_length, width=stripe_width, height=0.3, color=color.yellow, axis=self.pave.axis))

    def change_dir(self, new_dir):
        self.base.axis=new_dir

    def move(self, new_pos):
        self.base.pos = new_pos
        self.pave.pos = new_pos

    def get_stoplights(self):
    	return self.stoplight_list

##  create a stoplight class that has member functions to change the color, change the position, etc.
class Stoplight():
    def __init__(self, road, position_on_road, direction):
        self.base = frame(pos=road.pave.pos)
        #   NOTE:::  All positions of objects witihin the frame are RELATIVE to the frame's position, not the world position
        if dot(direction,vector(0,0,1)) != 0:
            #if direction is in "z" direction, or north/south
            self.case=box(frame=self.base,pos=vector(-direction.z*(road.pave.width/4),20,-direction.z*position_on_road), length=4, width=4,height=2, color=color.white)
        else:
            #if direction is in "x" direciotn, or east/west
            self.case=box(frame=self.base,pos=vector(direction.x*position_on_road,20,direction.x*(road.pave.width/4)), length=4, width=4,height=2, color=color.white)
        self.yellow=sphere(frame=self.base,pos=self.case.pos+vector(0,self.case.height/2,0), radius=light_rad, color=color.yellow)
        self.green=sphere(frame=self.base,pos=self.case.pos+vector(0,self.case.height/2,0), radius=light_rad, color=color.green)
        self.red=sphere(frame=self.base,pos=self.case.pos+vector(0,self.case.height/2,0), radius=light_rad, color=color.red)
        self.direction = direction
        self.is_green = True
        self.is_yellow = False
        self.is_red = False
        self.green_light()
        self.attached_road = road
        road.get_stoplights().append(self)
        if dot(direction,vector(0,0,1)):
        	#ns_list_of_lights.append(self)
        	self.location = vector(-direction.z*(road.pave.width/4),20,-direction.z*position_on_road)
        else:
        	#ew_list_of_lights.append(self)
        	self.location = vector(direction.x*position_on_road,20,direction.x*(road.pave.width/4))

    def move(self, new_position):
        self.base.pos=new_position

    def green_light(self):
        self.red.visible=false
        self.yellow.visible=false
        self.green.visible=true
        self.is_green = True
        self.is_yellow = False
        self.is_red = False

    def yellow_light(self):
        self.red.visible=false
        self.yellow.visible=true
        self.green.visible=false
        self.is_green = False
        self.is_yellow = True
        self.is_red = False

    def red_light(self):
        self.red.visible=true
        self.yellow.visible=false
        self.green.visible=false
        self.is_green = False
        self.is_yellow = False
        self.is_red = True

    def toggle(self):
    	if(self.is_red):
    		self.red.visible=false
    		self.yellow.visible=false
    		self.green.visible=true
    		self.is_green = True
    		self.is_red = False
    		self.is_yellow = False
    		return
    	elif(self.is_green):
    		self.red.visible=true
    		self.yellow.visible=false
    		self.green.visible=false
    		self.is_green = False
    		self.is_red = True
    		self.is_yellow = False
    		return
    	else:
    		self.red.visible=true
    		self.yellow.visible=false
    		self.green.visible=false
    		self.is_green = False
    		self.is_red = True
    		self.is_yellow = False
    		return

    def get_state(self):
    	return vector(self.is_red,self.is_yellow,self.is_green)

class Car():
    def __init__(self, named, road, first_pos_on_road, v_direction):
        if dot(v_direction,vector(0,0,1)) != 0:
            #if direction is in "z" direction, or north/south
            self.body=box(pos=vector(-v_direction.z*(road_width/4),0,-v_direction.z*first_pos_on_road)+road.pave.pos, length=16, width=6,height=5, color=color.cyan, axis = v_direction)
        else:
            #if direction is in "x" direciotn, or east/west
            self.body=box(pos=vector(v_direction.x*first_pos_on_road,0,v_direction.x*(road_width/4))+road.pave.pos, length=16, width=6,height=5, color=color.cyan, axis = v_direction)
        
        ##  create velocity vector by using mag * dir
        self.v_mag = 37 # feet/second   ==  25 mph ;  rough speed of standard car
        self.v_hat = v_direction
        self.v = self.v_mag*self.v_hat
        self.a = vector(0,0,0)
        self.name = named
        self.attached_road = road
        self.next_light = self.find_nearest_light()
        self.seen_red_light = false

    #find nearest light in same direction as car is moving
    def find_nearest_light(self):
        #print("in find nearest light....")
        #print(list_of_lights)
        minLightDist=9999
        lightNo=0
        list_of_lights = self.attached_road.stoplight_list
        for i in range(len(list_of_lights)):
        	dist = dot((list_of_lights[i].location - self.body.pos),self.v_hat)
        	#print "car ",self.name," dist to light ", dist
        	#print dot(self.body.pos,self.v_hat)
        	if(dist>0):
        		#dist = dot((list_of_lights[i].location - self.body.pos),self.v_hat)
        		#if(dot(self.v_hat,vector(1,0,0))):
        		#print("dist to light = ", dist)
        		if (dist < minLightDist and dist>0):
        			minLightDist = dist
        			lightNo = i
        			#print "found nearest light at ", list_of_lights[i].location, "dist", dist
        self.next_light = list_of_lights[lightNo]
        if(minLightDist<9999):
        	return list_of_lights[lightNo]
        else:
        	return 0

    def is_offscreen(self):
    	if( dot(self.body.pos,self.v_hat)>200):
    		return true
    	else:
    		return false

    def slow_to_light(self):
        dist_to_light = dot((self.next_light.location - self.body.pos),self.v_hat) - 15 #15 feet is assumed distance from light that most traffic should stop...
        acc = (-dot(self.v,self.v)/(2*dist_to_light))*self.v_hat
        return acc

    def move(self, delta_position):
        self.body.pos = self.body.pos + delta_position

    def look_for_lights(self):
    	#refill lights associated to car
    	next_light = self.find_nearest_light()
    	if(next_light==0):
    		self.v = 37*self.v_hat
    		self.a_mag = 0
    		self.seen_red_light=false
    		return
    	#print next_light.location
    	dist = dot((next_light.location - self.body.pos),self.v_hat)
    	#print "for ", self.name
    	#print "next list dist",dist
    	if (next_light.is_red and dist>15 and self.seen_red_light==false):
    		
    		self.a = self.slow_to_light()
    		self.seen_red_light=true
    	if(next_light.is_green or dist<15):
    		self.v = 37*self.v_hat
    		self.a_mag = 0
    		self.seen_red_light=false

    def find_nearest_car(self):
    	minCarDist=9999
        carNo=-1
        for i in range(len(list_of_cars)):
        	#print list_of_lights[i].location
        	#print list_of_lights[i].direction
        	if(self==list_of_cars[i]):
        		continue
        	same_dir = dot(self.v_hat, list_of_cars[i].v_hat)
        	#print("same_dir = ", same_dir)
        	if(same_dir == 1 and dot(list_of_cars[i].body.pos,self.v_hat) > dot(self.body.pos,self.v_hat)):
        		dist = mag(self.body.pos - list_of_cars[i].body.pos) - (self.body.length*0.5)
        		#print("dist = ", dist)
        		if (dist < minCarDist):
        			minCarDist = dist
        			carNo = i
        			#print "found nearest car at ", list_of_cars[i].body.pos
        if(carNo>-1):
        	return list_of_cars[carNo]
        else:
        	return 0

    def look_for_cars(self):
    	next_car = self.find_nearest_car()
    	if(next_car):
    		dist = mag(next_car.body.pos - self.body.pos)
    		if (dist<self.body.length*4):
    			self.a = next_car.a
    			self.v = next_car.v
    		else:
    			self.a_mag = 0
    			self.v = 37*self.v_hat


def toggle_lights(light1, light2):
	state1 = light1.get_state()
	print "state 1", state1
	if(dot(state1,vector(1,0,0))==1):
		print "should toggle"
		light1.green_light
		light2.red_light
	elif(dot(state1,vector(0,0,1))==1):
		light1.red_light
		light2.green_light


########################################################################
########################################################################
##new_light = Stoplight(vector(0,10,0))
road1 = Road(0, int(road_length), directions['north'])
road2 = Road(-road1.pave.length/8, int(road_length), directions['west'])
#road2.move(road2.base.pos+vector(0,0,-road1.pave.length/8))
road3 = Road(road1.pave.length/8, int(road_length), directions['west'])
#road3.move(road3.base.pos+vector(0,0,+road1.pave.length/8))
##
##key=scene.kb.getkey()

light1 = Stoplight(road1,-road1.pave.length/8, directions['north'])
print "light1 created at location ", light1.location
light1.red_light()

light2 = Stoplight(road1,+road1.pave.length/8, directions['north'])
print "light2 created at location ", light2.location
light2.green_light()

light1_otherSide = Stoplight(road2,0,directions['east'])
light1_otherSide.green_light()
print "light1_otherSide created at location ", light1_otherSide.location

light2_otherSide = Stoplight(road3,0,directions['east'])
light2_otherSide.red_light()
print "light2_otherSide created at location ", light2_otherSide.location

light3 = Stoplight(road2,road2.pave.length/4, directions['east'])
light3.red_light()
print "road 2 size: ",road2.pave.pos, road2.pave.length
print "light3 created at location ", light3.location

##light2 = Stoplight(next_road.base.pos,-new_road.pave.length/4, directions['north'])
print "stoplight list size ", len(road1.stoplight_list), " ", len(road2.stoplight_list)," ",len(road3.stoplight_list)

list_of_cars = []
car1 = Car("ns primary car",road1, road1.pave.length/2, directions['south'])
print "car created at ",car1.body.pos
list_of_cars.append(car1)

car2 = Car("ew primary car", road2, -road2.pave.length/2, directions['east'])
print car2.name, " created at ",car2.body.pos
list_of_cars.append(car2)
#print(light1.case.pos)
#print(car1.next_light)



t=0
delta_t = 1/24
simtime = 50  #seconds
ithCar=0
carN = []
lastSpawnTime=0

while t < simtime:
    rate(1/delta_t)

    #Control rate of stoplight changes
    #stupid modulo workaround for float objects
    if((int)(t*(1/delta_t))%(int)(4*(1/delta_t))==0 and t>0.01):
    	light2.toggle()
    	light2_otherSide.toggle()

    if((int)(t*(1/delta_t))%(int)(5*(1/delta_t))==0 and t>0.01):
    	light1.toggle()
    	light1_otherSide.toggle()

    if((int)(t*(1/delta_t))%(int)(3*(1/delta_t))==0 and t>0.01):
    	light3.toggle()

    ##  check distance to closest light
    ## update speed
    ## and update position
    for carObj in list_of_cars:
    	if(carObj.find_nearest_car()):
    		if(carObj.find_nearest_light()==0):
    			carObj.look_for_cars()
    		elif(mag(carObj.find_nearest_car().body.pos - carObj.body.pos) < mag(carObj.find_nearest_light().location - carObj.body.pos)):
    			#print "nearest car: ",mag(carObj.find_nearest_car().body.pos - carObj.body.pos)
    			#print "nearest light: ",mag(carObj.find_nearest_light().location - carObj.body.pos)
    			#print "car position: ",mag(carObj.body.pos)
    			carObj.look_for_cars()
    		else:
    			carObj.look_for_lights()
    	else:
    		carObj.look_for_lights()
    	carObj.v = carObj.v + carObj.a*delta_t
    	if(dot(carObj.v,carObj.a)<=0):
    		deltaR1 = carObj.v*delta_t
    	else:
    		deltaR1 = vector(0,0,0)
    	carObj.move(deltaR1)

    if(len(list_of_cars)<5 and t-lastSpawnTime>1):
    	if(ithCar%3==2):
    		print "appending car",ithCar
    		carN.append(Car("car"+str(ithCar), road1, road1.pave.length/2, directions['south']))
    	elif(ithCar%3==1):
    		carN.append(Car("car"+str(ithCar), road2, -road2.pave.length/2, directions['east']))
    	else:
    		carN.append(Car("car"+str(ithCar), road3, -road3.pave.length/2, directions['east']))
    	list_of_cars.append(carN[ithCar])
    	lastSpawnTime=t
    	ithCar = ithCar+1

    ##cleanup cars once they leave the frame
    for carObj in list_of_cars:
    	if(carObj.is_offscreen()):
    		list_of_cars.remove(carObj)
    		carObj.visible=false
    		del carObj


    ##  update time
    t = t + delta_t

