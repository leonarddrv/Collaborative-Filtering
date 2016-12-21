from math import sqrt
import codecs

def loadMovieLens(path=''):
	data = {}
	i = 0
	f = codecs.open(path + 'u5.base', 'r', 'ascii')
	for line in f:
		fields = line.split('\t')
		user = fields[0]
		movie = fields[1]
		rating = int(fields[2].strip().strip('"'))
		#print(fields[0] + '\t' + fields[1] + '\t' + fields[2])
		if user in data:
			currentRatings = data[user]
		else:
			currentRatings = {}
		currentRatings[movie] = rating
		data[user] = currentRatings
	f.close()
	#print('loaded')
	return data

def normalizeData( data ):
	normalised = {}

	for user in data:
		userSum = 0
		userAvg = 0
		ratingCount = 0
		userNormalised = {}
		for rating in data[user].itervalues():
			ratingCount += 1
			userSum += rating
		userAvg = userSum/ratingCount
		for (movie,rating) in data[user].iteritems():
			userNormalised[movie] = (rating - userAvg)
		normalised[user] = userNormalised

	return normalised        

def calcSim (user, userOther, data):
	sum_xy = 0
	sum_x2 = 0
	sum_y2 = 0
	n = 0
	rating1 = data[user]
	rating2 = data[userOther]

	for key in rating1:
		if key in rating2:
			n += 1
			sum_xy += rating1[key]*rating2[key]
			

	if n == 0:
		return 0
	else:

		for value in rating1.itervalues():
			sum_x2 += value**2
		for value in rating2.itervalues():
			sum_y2 += value**2

		denominator = sqrt(sum_x2) * sqrt(sum_y2)

		if denominator == 0:
			return 0
		else:
			return sum_xy/denominator

def createSimMatrix(data):

	normalizedMatrix = normalizeData(data) 

	simMatrix = {}
	sumNum = 0
	sumUser = 0
	sumOtherUser = 0

	for user in normalizedMatrix:
		#print ("for user " + user)
		sim = {}

		for userOther in normalizedMatrix:
			k = calcSim (user, userOther, normalizedMatrix)
			sim[userOther] = k			
			#print ("sim("+user+","+userOther+") ="+str(k))


		simMatrix[user] = sim

	return simMatrix

def computeNearestNeighbor(username, movie, data, simMatrix, i):
	simUser = simMatrix.get(username)
	sorted_simUser = sorted(simUser.items(), key=lambda x: -x[1])
	#print sorted_simUser
	simArray = []
	cnt1 = 0
	cnt2 = 0
	for u in sorted_simUser:
		cnt1 = cnt1 + 1
		
		if cnt1 is not 1:
			if data.get(u[0]).get(movie) is not None:
				temp = (u[0], u[1])
				simArray.append(temp)
				cnt2 = cnt2 + 1
				#print u[0]
				#print data.get(u[0]).get(movie)
		if cnt2 is i:
			break
	
	return simArray

def calculateRating(username, movie, data, simMatrix, i):
	currentUser = data.get(username)
	simArray = computeNearestNeighbor(username, movie, data, simMatrix, i)
	denominator_sum = 0
	total = 0
	length = len(simArray)
	for el in simArray:
		total = total + el[1]*data[el[0]][movie]
		denominator_sum = denominator_sum + el[1]
	div = 0
	if denominator_sum > 0.00000000000001:
		div = total/denominator_sum
	#print simArray
	return div

def mainFunction(path=''):
	data = loadMovieLens(path)
	simMatrix = createSimMatrix(data)
	for i in range (1,51):
		f = codecs.open(path + 'u5.test', 'r', 'ascii')
		cnt = 0
		dif = 0
		sum = 0
		for line in f:
			fields = line.split('\t')
			user = fields[0]
			movie = fields[1]
			rating = int(fields[2].strip().strip('"'))
			calculated = calculateRating(user, movie, data, simMatrix, i)		
			if calculated is not 0:
				dif = (calculated - rating) ** 2
				sum = sum + dif
				cnt = cnt + 1
			#print cnt
		f.close()
		rmse = sqrt(sum/cnt)
		print i,rmse


mainFunction('ml-100k/')