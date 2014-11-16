class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.tiles = {}
        for x in range(0, self.width+1):
            for y in range(0, self.height+1):
                self.tiles[x,y] = "dirty"
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        self.tiles[int(pos.getX()),int(pos.getY())]="clean"
           
        
    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        if self.tiles[int(m),int(n)]=="clean":
            return True
        return False
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return  int(self.width*self.height)

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        numClean = 0
        for x in range(0, self.width+1):
            for y in range(0, self.height+1):
                if self.tiles[x, y] == "clean":
                    numClean = numClean + 1
        return numClean

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        x = random.randrange(self.width)
        y = random.randrange(self.height)
        position = Position(x,y)
        return position
    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        if 0 <= pos.getX() < self.width and 0 <= pos.getY() < self.height:
            return True
        return False
class Robot(RectangularRoom):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.speed = speed
        self.room = room
        self.direc = random.randrange(360)
        self.pos = Position(random.randrange(room.width),random.randrange(room.height))
    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.pos
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direc

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.pos = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direc = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError # don't change this!
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        newPosition = self.getRobotPosition().getNewPosition(self.direc, self.speed)
        if self.room.isPositionInRoom(newPosition):
            self.room.cleanTileAtPosition(newPosition)
            self.setRobotPosition(newPosition)
        else:
            self.setRobotDirection(random.uniform(0,360))
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials, robot_type, animate=False):
    total_steps = 0
    for __ in range(num_trials):
        if animate:
            anim = ps7_visualize.RobotVisualization(num_robots, width, height)
        room = RectangularRoom(width, height)
        robots = []
        for r in range(num_robots):
            robots.append(robot_type(room, speed))
        while room.getNumCleanedTiles() / float(room.getNumTiles()) < min_coverage:
            if animate:
                anim.update(room, robots)
            for robot in robots:
                robot.updatePositionAndClean()
            total_steps += 1
        if animate:
            anim.update(room, robots)
            anim.done()
    return total_steps / float(num_trials)   

#Problem 4
class Robot(object):
    def __init__(self, room, speed):
        self.dir = int(360 * random.random())
        self.pos = Position(room.width * random.random(),room.height * random.random())
        self.room = room
        self.room.cleanTileAtPosition(self.pos)
        if speed > 0:
            self.speed = speed
        else:
            raise ValueError("Zero is not a speed.")

    def getRobotPosition(self):
        return self.pos
    
    def getRobotDirection(self):
        return self.dir

    def setRobotPosition(self, position):
        self.pos = position

    def setRobotDirection(self, direction):
        self.dir = direction

    def updatePositionAndClean(self):
        raise NotImplementedError # don't change this!

class RandomWalkRobot(Robot):
    def updatePositionAndClean(self):
        self.dir = int(360 * random.random())
        while not self.room.isPositionInRoom(self.pos.getNewPosition(self.dir, self.speed)):
            self.dir = int(360 * random.random())
        self.pos = self.pos.getNewPosition(self.dir, self.speed)
        self.room.cleanTileAtPosition(self.pos)