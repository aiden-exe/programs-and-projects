def justLessThan(lis, x, lower, upper, key = lambda x:x):
    if upper - lower == 0:
        return None

    if x > key(lis[upper-1]):
        return upper

    if upper - lower == 1:
        return lower

    middle = (lower+upper-1)//2

    if x <= key(lis[middle]):
        return justLessThan(lis, x, lower, middle+1, key)

    else:
        return justLessThan(lis, x, middle+1, upper, key)


def searchRange(lis, q, d, key = lambda x: x):
    x1 = justLessThan(lis, q-d, 0, len(lis), key)

    nearbyPoints = []

    while x1 < len(lis) and key(lis[x1])<= q+d:
        nearbyPoints.append(lis[x1])
        x1 += 1
    
    return nearbyPoints


class PointDatabase:
    class PDNode:
        def __init__(self, key=None, LChild=None, RChild=None, yList = None) -> None:
            self.key = key
            self.LChild = LChild
            self.RChild = RChild
            self.yList = yList

        def hasChild(self):
            if self.LChild is None and self.RChild is None:
                return False

            return True 
  
               
    def buildPD(self, xSorted, ySorted):
        def buildRoot(xSorted, ySorted):            
            n = len(xSorted)
            
            if n == 0:
                return
            
            if n == 1:
                return PointDatabase.PDNode(key=xSorted[0], yList=xSorted)

            if n % 2 == 0:
                median = n//2 - 1

            else:
                median = n//2

            LySorted = []
            RySorted = []

            for i in ySorted:
                if i[0] <= xSorted[median][0]:
                    LySorted.append(i)
                else:
                    RySorted.append(i)

            root = PointDatabase.PDNode(key = xSorted[median], yList=ySorted)
            root.LChild = buildRoot(xSorted[:median+1], LySorted)
            root.RChild = buildRoot(xSorted[median+1:], RySorted)
            return root

        self.root = buildRoot(xSorted, ySorted)
    
    def __init__(self, pointlist: list) -> None:
        self.root = None
        xSorted = [i for i in pointlist]
        
        xSorted.sort(key = lambda x: x[0])
        

        ySorted = [i for i in pointlist]
        ySorted.sort(key = lambda x: x[1])

        self.buildPD(xSorted, ySorted)


    def searchNearby(self, q, d):
        nearbyPoints = []
        def contained(point, q, d):
            return q[0]-d <= point[0] <= q[0] + d and q[1]-d <= point[1] <= q[1]+d

        def searchRoot(root: PointDatabase.PDNode, q, d, nearbyPoints, key= lambda x: x.key):
            if root == None:
                return

            commonNode = root

            while True:
                if key(commonNode) >= q[0]+d:
                    if commonNode.LChild == None:
                        break
                    else:
                        commonNode = commonNode.LChild
                
                elif key(commonNode) < q[0]-d:
                    if commonNode.RChild == None:
                        break
                    else:
                        commonNode = commonNode.RChild
                else:
                    break
            
            # print("CommonNode = ", commonNode.key)
            if not commonNode.hasChild():
                # print("Common node is leaf")
                if contained(commonNode.key, q, d):
                    nearbyPoints.append(commonNode.key)
                return

            # For q-d
            # print("Searching for q-d")
            x1Node = commonNode.LChild

            while x1Node != None:
                # print("Current Node: ", x1Node.key)
                if not x1Node.hasChild():
                    # print("Node is a leaf")
                    if contained(x1Node.key, q, d):
                        # print("Leaf appended")
                        nearbyPoints.append(x1Node.key)
                    break

                if q[0]-d <= key(x1Node):
                    # print("Going left, searching in right")
                    rightsearch = searchRange(x1Node.RChild.yList, q[1], d, key=lambda x: x[1])
                    # print(f"Searched in {x1Node.RChild.yList}, returned {rightsearch}")
                    nearbyPoints.extend(rightsearch)

                    x1Node = x1Node.LChild
                
                else:
                    # print("Going right")
                    x1Node = x1Node.RChild


            # For q+d
            # print("Searching for q+d")
            x2Node = commonNode.RChild

            while x2Node != None:
                # print("Current Node: ", x2Node.key)
                if not x2Node.hasChild():
                    # print("Node is a leaf")
                    if contained(x2Node.key, q, d):
                        # print("Leaf appended")
                        nearbyPoints.append(x2Node.key)
                    break

                if q[0]+d > key(x2Node):
                    # print("Going right, searching in left")
                    leftsearch = searchRange(x2Node.LChild.yList, q[1], d, key=lambda x: x[1])
                    # print(f"Searched in {x2Node.LChild.yList}, returned {leftsearch}")
                    nearbyPoints.extend(leftsearch)

                    x2Node = x2Node.RChild
                
                else:
                    # print("Going left")
                    x2Node = x2Node.LChild
            
            return nearbyPoints

        
        searchRoot(self.root, q, d, nearbyPoints, key = lambda node: node.key[0])

        return nearbyPoints

    
    def inorder(self):
        def inorderRoot(root: PointDatabase.PDNode):
            if root == None:
                return

            inorderRoot(root.LChild)
            # print(f"Node {root.key}, sublist: {root.yList}")
            inorderRoot(root.RChild)

        inorderRoot(self.root)


if __name__ == "__main__":
    A = [(1,6), (2,4), (3,10), (4,9), (5,8), (6,3), (7,0), (8,1),(9,2), (10,5)]
    pointDbObject = PointDatabase(A)
    # pointDbObject.inorder()

    # print(searchRange(A, 6, 2, key=lambda x: x[0]))

    print(pointDbObject.searchNearby((5.5, 6), 3))