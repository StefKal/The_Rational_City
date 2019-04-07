from random import randint
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
SIZE = 100
INDI_MONEY = 1000
CORP_MONEY = 10000
INDI_VISION = 10
CORP_VISION = 10
STATUS = 100

# construction of a corporation agent
class Corporation(object):
    def __init__(self, money, vision, optimal = False):
        self.money = money
        self.vision = vision
        self.optimal = optimal

    def run(self, add_amount, cost_amount):
        self.money += add_amount
        self.money -= cost_amount

    def __str__(self):
        return "corp"

    def __repr__(self):
        return "corp"


# constructor of an individual agent
class Individual(object):
    def __init__(self, money, vision, optimal = False):
        self.money = money
        self.vision = vision
        self.optimal = optimal

    def run(self, add_amount, cost_amount):
        self.money += add_amount
        self.money -= cost_amount


    def __str__(self):
        return "indi"

    def __repr__(self):
        return "indi"

# constructor of corporate cell
class CorpCell(object):
    def __init__(self, status, occupied = False, x = None, y = None, agent_inside = None ):
        self.rent = status * 100
        self.status = status
        self.occupied = occupied
        self.agent_inside = agent_inside
        self.x = x
        self.y = y

    def __str__(self):
        return "CORP"
    def __repr__(self):
        return "CORP"

    def __eq__(self, other):
        if isinstance(other, CorpCell):
            return True
# constructor of individual cell
class IndCell(object):

    def __init__(self, status, occupied = False, x=None, y=None, agent_inside = None ):
        self.rent = status * 10
        self.status = status
        self.occupied = occupied
        self.agent_inside = agent_inside
        self.x = x
        self.y = y

    def __str__(self):
        return "IND"

    def __repr__(self):
        return "IND"

# constructor of government cell
class GovCell(object):
    def __init__(self, status = 0 ,occupied = False, x = None, y = None, agent_inside = None,):
        self.rent = 10
        self.occupied = occupied
        self.agent_inside = agent_inside
        self.x = x
        self.y = y
        self.status = status


    def __str__(self):
        return "GOV"

    def __repr__(self):
        return "GOV"


# constructor of city
class City(object):
    def __init__(self, row_amount, col_amount):
        self.row_amount = row_amount
        self.col_amount = col_amount

        # dictionaries that contain all of the city cells, (x,y) --> instance of cell
        self.city_indCells = dict()
        self.city_corpCells = dict()
        self.city_govCells = dict()

        corp_count = int(row_amount*col_amount * 0.4)
        ind_count = int(row_amount*col_amount * 0.4)
        assist_count = int(row_amount*col_amount * 0.2)

        array1 = [GovCell() for i in range(assist_count)]

        array2 = [CorpCell(status=randint(1,STATUS)) for i in range(corp_count)]
        array3 =[IndCell(status=randint(1,STATUS)) for i in range(ind_count)]
        array23 = np.concatenate((array2, array3), axis=None)
        np.random.shuffle(array23)


        final_array = np.concatenate((array1, array23), axis=None)

        self.grid = np.array(final_array).reshape(row_amount, col_amount)
        for row in range(row_amount):
            for col in range(col_amount):
                self.grid[row][col].x = row
                self.grid[row][col].y = col
                if isinstance(self.grid[row][col],IndCell):
                    self.city_indCells[(row,col)] = self.grid[row][col]
                elif isinstance(self.grid[row][col], CorpCell):
                    self.city_corpCells[(row, col)] = self.grid[row][col]
                elif isinstance(self.grid[row][col], GovCell):
                    self.city_corpCells[(row, col)] = self.grid[row][col]


    def __iter__(self):
        self.col_amount = 0
        self.row_amount = 0
        return self

    def __next__(self):
        if self.row_amount < SIZE-1 and self.col_amount != SIZE-1:
            self.col_amount += 1
            return self.grid[self.row_amount, self.col_amount]

        if self.col_amount == SIZE-1 and self.row_amount < SIZE-1:
            self.row_amount += 1
            self.col_amount = 0
            return self.grid[self.row_amount, self.col_amount]

        else:
            raise StopIteration

    def __str__(self):
        return str(self.grid)

    def __repr__(self):
        return str(self.grid)



# first inhabitation of the city
def inhabit(city):
    individuals = list()
    corporations = list()

    # I N I T I A L  I N H A B I T A T I O N
    while len(individuals) < (SIZE*SIZE)/4:
        ind = Individual(randint(0, INDI_MONEY),INDI_VISION)
        for coord in city.city_indCells:
            cell = city.city_indCells[coord]
            if not cell.occupied:
                    if ind.money > cell.rent and cell != GovCell and cell.occupied == False and cell.agent_inside is None:
                        cell.agent_inside = ind
                        cell.occupied = True
                        individuals.append(ind)
                        break
                    # else:
                    #     for govcell in city.grid[0:10]:
                    #         if not govcell.occupied and isinstance(govcell, GovCell):
                    #             govcell.agent_inside = ind
                    #             break
                    #     break


    while len(corporations) < (SIZE * SIZE) / 4:
        corp = Corporation(randint(0, CORP_MONEY), CORP_VISION)
        for coord in city.city_corpCells:
            cell = city.city_corpCells[coord]
            if not cell.occupied:
                    if corp.money > cell.rent and cell.occupied == False and cell.agent_inside is None:
                        cell.agent_inside = corp
                        cell.occupied = True
                        corporations.append(corp)
                        break

def put_status(city):
    for row in range(1,SIZE-1):
        for col in range(1, SIZE-1):
            cell = city.grid[row][col]
            if not isinstance(cell , GovCell):

                avg_status = city.grid[row-1][col-1].status + city.grid[row][col-1].status + city.grid[row+1][col-1].status + \
                             city.grid[row-1][col].status   + city.grid[row][col].status   + city.grid[row+1][col].status + \
                             city.grid[row-1][col+1].status + city.grid[row][col+1].status + city.grid[row+1][col].status
                cell.status = avg_status/9

def update(city):
    # go through occupied cells
    for row in range(SIZE):
        for col in range(SIZE):
            cell = city.grid[row][col]

            if cell.occupied:

                agent_inside = cell.agent_inside
                best_status = cell.status
                current_cell = cell
                vision = agent_inside.vision
                best_cell = current_cell

                # for each occupied cell, find the best status cell within their vision
                for cells in city.grid[cell.x-vision:cell.x+vision, cell.y-vision:cell.y+vision]:
                    for item in cells:
                        if item.status > best_status and item.occupied == False:
                            best_status = item.status
                            best_cell = item

                cost = find_distance_cost(current_cell.x, best_cell.x, current_cell.y, best_cell.y)
                # if its not their current cell, and they can afford the movement cost and 2 times the rent of the place then move
                if best_cell != current_cell and agent_inside.money - cost > 0 and agent_inside.money > 2*best_cell.rent:
                    cell.occupied = False
                    agent_inside.money -= cost
                    cell.agent_inside = None
                    best_cell.occupied = True
                    best_cell.agent_inside = agent_inside
                    agent_inside.optimal = False


                elif isinstance(best_cell, GovCell):
                    agent_inside.optimal = False
                # if they cannot find a better cell that means that they are at their optimal cell
                else:
                    agent_inside.optimal = True




def test():
    # our city
    city = City(SIZE,SIZE)
    # makes each cell be the average status of its surrounding cells
    put_status(city)
    # inhabit city
    inhabit(city)

    ims = []
    fig = plt.figure()
    # G A M E  L O O P
    for period in range(100):
        # INCREASE UPDATE AGENTS INSIDE CITY BASED ON THE CELL THEY ARE IN
        for cell in city:
            agent_inside = cell.agent_inside
            if cell.occupied:
                # calculate their money by half as interest
                money_added = agent_inside.money* 1/2
                # increase their money by how much the status of their cell is
                money_added = money_added + agent_inside.money * cell.status
                # adds and subtracts money based on rent/status
                agent_inside.run(money_added, cell.rent)
                if cell.rent > agent_inside.money and isinstance(agent_inside, Individual):
                    for coord in city.city_govCells:
                        govcell = city.city_govCells[coord]
                        if not govcell.occupied:
                            govcell.agent_inside = agent_inside
                    cell.occupied = False
                    cell.agent_inside = None


        occupancy = city_occupancy(city)
        im = plt.imshow(occupancy, animated = True)
        ims.append([im])
        #display(city)
        update(city)
    ani = animation.ArtistAnimation(fig, ims, interval=100, blit=True, repeat_delay=100)
    plt.colorbar()
    plt.show()
# returns a city map with either 1 if cell is occupied or 0 if its not

def city_occupancy(city):
    occupancy = [[[] for x in range(SIZE)] for x in range(SIZE)]
    for i in range(SIZE):
        for j in range(SIZE):
            if city.grid[i][j].occupied and city.grid[i][j].agent_inside.optimal == True:
                occupancy[i][j] = 1
            elif city.grid[i][j].occupied and city.grid[i][j].agent_inside.optimal == False:
                occupancy[i][j] = 0.5
            else:
                occupancy[i][j] = 0
    return occupancy

def city_money(city):
    money = [[[] for x in range(SIZE)] for x in range(SIZE)]
    for i in range(SIZE):
        for j in range(SIZE):
            if city.grid[i][j].occupied:
                money[i][j] = city.grid[i][j].agent_inside.money
            else:
                money[i][j] = 0
    return money

def find_distance_cost(x1, x2, y1, y2):
    return np.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))

# Helper function that displays the city in the console
def display(city):
    for row in city.grid[0:SIZE-1,0:SIZE-1]:
        for cell in row:
            if cell.occupied and cell.agent_inside.optimal == True:
                print('*', end= ' ')
            elif cell.occupied and cell.agent_inside.optimal == False:
                print('0', end = ' ')
            else:
                print('-', end = ' ')
        print()
    print()

if __name__ == '__main__':
    test()
