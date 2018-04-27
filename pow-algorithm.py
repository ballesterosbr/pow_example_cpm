from hashlib import sha256
import time

# Function to swap transaction bytes
def swapTX(tx):
	return tx.decode('hex')[::-1].encode('hex')

def swapAll(allTX):
	for i in range(len(allTX)):
		allTX[i] = swapTX(allTX[i])
	return allTX

# Function to calculate Merkle root (only works for Power of Two numbers)
def merkle_root_func(myTX):
	swapAll(myTX)
	while (len(myTX)>2):
		for i in xrange(0,len(myTX),2):
			myTX[i/2] = sha256(sha256(myTX[i].decode('hex') + myTX[i+1].decode('hex')).digest()).digest().encode('hex')
		myTX = myTX[:(len(myTX)/2)]
	merkle_root = sha256(sha256(myTX[0].decode('hex')+myTX[1].decode('hex')).digest()).digest()
	return merkle_root.encode('hex')

#Transactions
myTX = [
	'9c7ab5a8c9ee62fd6a8b2ea0d83eba45cd92fa8fd950a9616d93bb6bd5f6c94e',
	'8792106e4ed2fe7ae0f7e737f3652dcf555a8cb4ed652eee568d5be3174c81b0']

#Header data
version = '00000001'
prev_hash = '56d52878eb8600c7a4c585af9f45a3511a7e1db425fe921001924f11643de4b6'
merkle_root = merkle_root_func(myTX)
bits = '1e0fffff'
student_hash = '016c9ecee0cc3d695835e928fd084d1c9d278cd7aff9570d54247f576355194f'

start = int('00000000', 16)
end = int('ffffffff', 16)
real_nonce = 0

#Target
coefficient = int(bits[:2],16)
exponent = int(bits[-6:],16)
target_form = exponent * 2**(8*(coefficient - 3))
new_target = hex(target_form)[2:].rstrip("L").zfill(64)

#Save time
temp = time.time()

for nonce in xrange(start, end+1):
	timestamp = hex(int(time.time()))[2:].zfill(8)
	nonce = hex(real_nonce)[2:].zfill(8)
	hash_header = swapTX(version) + swapTX(prev_hash) + merkle_root + swapTX(timestamp) + swapTX(bits) + swapTX(student_hash) + swapTX(nonce)
	header = sha256(sha256(hash_header.decode('hex')).digest()).digest().encode('hex')
	real_nonce = real_nonce+1
	if (int(long(swapTX(header),16)) < int(long(new_target,16))):
		print 'Target: ' + str(int(long(new_target,16))) + '\nDifficulty bits: ' + new_target
		print 'Merkle root: ' + swapTX(merkle_root) + '\nStudent hash: ' + student_hash
		print 'Seconds: ' + str(time.time() - temp) + '\nBlock hash: ' + swapTX(header) + '\nNonce: ' + nonce + ' ('+str(long(nonce,16))+')'
		print time.ctime(int(timestamp,16)) + ' (' + str(int(timestamp,16)) + ')\n'

		temp = time.time()
		real_nonce = 0
