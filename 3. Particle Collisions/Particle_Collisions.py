def listCollisions(M, x, v, m, t):
    if len(M) <= 1:
        return []
    n = len(M)
    last_update = [0]*n     # Keeps track of the time at which position
                            # of particle i was stored
    class Particle:
        '''
        Every node in the heap will be a object of class
        Particle, containing information about the ith particle and
        the time at which it would collide with particle i+1'''

        def __init__(self, index):
            self.index = index

            if index == n-1:
                self.next_coll = t+1

            else:
                if v[index]-v[index+1] <= 0 or x[index] == x[index+1]:
                    # Such collisions never happen, so put it as infinity, which is
                    # modelled as t+1
                    self.next_coll = t+1
                else:
                    self.next_coll = (x[index+1]-x[index])/(v[index]-v[index+1])

        # Defining comparison operators for particle class:
        def __eq__(self, obj):
            if self.index == obj.index:
                return True

            return False
        
        def __lt__(self, obj):
            if self.next_coll == obj.next_coll:
                return self.index < obj.index
            
            return self.next_coll < obj.next_coll

        def __le__(self, obj):
            return (self == obj or self < obj)

        def __ge__(self, obj):
            return not(self<obj)

        def __gt__(self, obj):
            return self >= obj and not (self == obj)

        def update_time(self):
            # Updates the time till next collision of particle i using
            # the updated data of x and time of last update
            if self.index < n-1:
                if v[self.index] <= v[self.index+1]:
                    self.next_coll = t+1
                else:
                    x_next = x[self.index+1] + v[self.index+1]*(last_update[self.index]-last_update[self.index+1])
                    self.next_coll = last_update[self.index]+(x_next-x[self.index])/(v[self.index]-v[self.index+1])

    class CollisionsHeap:
        def __init__(self, data = None):
            # _pointers list keeps track where Particle i is located in heap
            # So if particle 2 is at heap index 3, self._pointers[2] = 3
            if data == None:
                self._pointers = []
                self._data = []

            else:
                self._pointers = [i for i in range(n)]
                self.BuildHeap(data)

        def key(self, index):
            return self._data[index]

        def swap(self, index1, index2):
            # Swaps nodes at heap indices index1 and index, 
            # and also updates their corresponding pointers
            particle1 = self.key(index1).index
            particle2 = self.key(index2).index
            self._data[index1], self._data[index2] = self._data[index2], self._data[index1]
            self._pointers[particle1], self._pointers[particle2] = self._pointers[particle2], self._pointers[particle1]
            
        def __len__(self):
            return len(self._data)

        
        def HeapDown(self, index):
            if 2*index + 1 >= len(self):
                return

            if 2*index + 2 == len(self._data):
                if self.key(index) > self.key(2*index+1):
                    self.swap(index, 2*index+1)
                return

            min_child = 2*index + 1
            if self.key(2*index+2) < self.key(min_child):
                min_child = 2*index+2

            if self.key(index) > self.key(min_child):
                self.swap(index, min_child)
                self.HeapDown(min_child)


        def HeapUp(self, index):
            if index == 0:
                return

            parent = (index - 1)//2

            if self.key(index) < self.key(parent):
                self.swap(index, parent)
                self.HeapUp(parent)

        def changeKey(self, index):
            if index != 0 and self.key(index) < self.key((index-1)//2):
                self.HeapUp(index)
                return
            self.HeapDown(index)

            
        def BuildHeap(self, data):
            # Initializes the heap given a list without the heap order property
            n = len(data)
            self._data = data

            for i in range(n//2, -1, -1):
                self.HeapDown(i)

    # ------------------------------Definition of classes end--------------------------

    particlesHeap = CollisionsHeap([Particle(i) for i in range(n)])
    current_time = 0
    collisions = []

    def velocityAfterColl(i):
        # Given particle i, calculates new velocities i and i+1th particle
        # would gain on colliding

        return (((M[i]-M[i+1])*v[i]+2*M[i+1]*v[i+1])/(M[i]+M[i+1]),
                        ((M[i+1]-M[i])*v[i+1]+2*M[i]*v[i])/(M[i]+M[i+1]))

    rootParticle = particlesHeap.key(0)     # The particle which will collide soonest, say particle i
    next = rootParticle.next_coll           # Time at which the collision happens
    while next <= t and m > 0:
        current_time = next     # Set current time to the time of this collision

        # Update position of particle i and i+1 to match current time
        x[rootParticle.index] += v[rootParticle.index] * (current_time - last_update[rootParticle.index])
        x[rootParticle.index+1] = x[rootParticle.index]
        
        # Add the collision data to final list
        collisions.append((round(current_time, 4), rootParticle.index, round(x[rootParticle.index], 4)))

        # Update velocities of particle i and i+1
        v[rootParticle.index], v[rootParticle.index+1] = velocityAfterColl(rootParticle.index)

        # Since position has been updated to current time, last_update values is updated
        last_update[rootParticle.index] = current_time
        rootParticle.update_time()

        # Root particle's time till next call is now infinity, so push it down
        particlesHeap.HeapDown(0)
        
        if rootParticle.index == 0:
            # In collision of i and i+1, time till next collision of i+1 is changed
            # so it is updated in heap
            next_particle_pointer = particlesHeap._pointers[rootParticle.index+1]
            last_update[rootParticle.index+1] = current_time
            particlesHeap.key(next_particle_pointer).update_time()
            
            # Since time till next collision of i+1 can only decrease, we only call heapup
            particlesHeap.HeapUp(next_particle_pointer)

        else:
            # In collision of i and i+1, time till next collision of i+1 and i-1
            # is changed so it is updated in heap
            next_particle_pointer = particlesHeap._pointers[rootParticle.index+1]
            last_update[rootParticle.index+1] = current_time
            particlesHeap.key(next_particle_pointer).update_time()
            # Since time till next collision of i+1 can only decrease, we only call heapup
            particlesHeap.HeapUp(next_particle_pointer)
            
            previous_particle_pointer = particlesHeap._pointers[rootParticle.index-1]
            particlesHeap.key(previous_particle_pointer).update_time()
            # Since time till next collision of i-1 can only decrease, we only call heapup
            particlesHeap.HeapUp(previous_particle_pointer)

        m -= 1
        rootParticle = particlesHeap.key(0)
        next = rootParticle.next_coll


    return collisions


if __name__ == "__main__":
    pass
