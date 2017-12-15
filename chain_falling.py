from pylab import *

def get_next_status(current_position, current_speed, acceleration, t):
	next_speed = current_speed + acceleration*t
	average_speed = (current_speed + next_speed)/2
	next_position = current_position + average_speed*t
	return next_position, next_speed

n = 5 #total number of balls
starting_height = 10 #starting height of the lowest ball
t = 0.01 #time period that next frame updates
h = 1 #length between two balls when the spring is still
m = 1 #weight of one ball, unit kg
k = 100 #k of one spring between two balls
g = 10

floor_boundary = 1e-6

spring_limit = 0.2 #the shortest a spring can go
spring_limit_long = 1.8

#BEGINNING：The whole chain hanging in the air, still

initial_speed = zeros(n)
initial_position = empty(n)
still_stretch = m*g/k

initial_position[0] = starting_height

for i in range(1,n):
	initial_position[i] = initial_position[i-1] + h + i*still_stretch #start in a hanging position
	# initial_position[i] = initial_position[i-1] + h #start with equal spaced

A_falling = zeros(shape=(n,n)) #accelerate matrix for falling
A_falling[0][0] = -1
A_falling[0][1] = 1
A_falling[-1][-1] = -1
A_falling[-1][-2] = 1

ends = zeros(n)
ends[0] = -k*h
ends[-1] = k*h

for i in range(1,n-1):
	A_falling[i][i] = -2
	A_falling[i][i-1] = 1
	A_falling[i][i+1] = 1


current_position = initial_position
current_speed = initial_speed
current_acceleration = -g + k/m * dot(A_falling, current_position) + ends
current_time = 0

total_time = 2
plot([0,total_time], [0,0], '-b')


while (current_time <= total_time):

	plot(zeros(n) + current_time, current_position, 'ro')

	if (current_position[0] < floor_boundary):
		current_speed[0] = -current_speed[0]
		print("bouncing!!")

	#save the data from last frame in case in the next frame the first ball position goes under zero
	last_acceleration = current_acceleration
	last_position = current_position
	last_speed = current_speed
	last_time = current_time

	current_acceleration = -g + k/m * dot(A_falling, current_position) + ends
	current_position, current_speed = get_next_status(current_position, current_speed, current_acceleration, t)
	current_time += t

	while (current_position[0] < 0): #try to approach zero, but above zero

		print("inside approaching zero ", current_position[0])

		temp_t = last_position[0]/(last_position[0] - current_position[0])*t
		current_acceleration = -g + k/m * dot(A_falling, last_position) + ends
		current_position, current_speed = get_next_status(last_position, last_speed, last_acceleration, temp_t)
		current_time = last_time + temp_t	

	print("current_time: ", current_time)
	print("current last ball position: ",current_position[0])
	print("----------------")

show()





























