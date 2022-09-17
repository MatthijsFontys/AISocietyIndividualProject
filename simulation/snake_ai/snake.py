from util.vector import Vector


class Snake:

    def __init__(self, start_x, start_y):
        self.SPEED = 1
        # 0 = up, 1 = down, 2 = left, 3 = right
        self.MOVEMENT = [Vector(0, -self.SPEED), Vector(0, self.SPEED), Vector(-self.SPEED, 0), Vector(self.SPEED, 0)]
        # starting at invalid index so i don't get bothered by not being able to move in a certain direction 1st frame
        self.movement_index = -1
        self.pos = Vector(start_x, start_y)  # head position
        self.segments = []  # position of all other snake segments

    def size(self):
        return len(self.segments) + 1

    def eat(self):
        self.segments.append(Vector(-1, -1))

    def get_segment(self, index):
        if index == 0:
            return self.pos
        else:
            return self.segments[index - 1]

    def move(self, next_index: int):
        if self.can_move_in_dir(next_index):
            self.movement_index = next_index

        for i, segment in reversed(list(enumerate(self.segments))):
            if i == 0:
                self.segments[i] = self.pos.copy()
                break
            else:
                self.segments[i] = self.segments[i - 1]

        self.pos.add(self.MOVEMENT[self.movement_index])

    def can_move_in_dir(self, next_index: int):
        # snake_ai can't move in the opposite direction that it is currently moving
        is_allowed = True
        prev_index = self.movement_index
        if self.MOVEMENT[next_index].x == 0 and self.MOVEMENT[prev_index].x == 0:
            if self.MOVEMENT[next_index].y != self.MOVEMENT[prev_index].y:
                is_allowed = False
        elif self.MOVEMENT[next_index].y == 0 and self.MOVEMENT[prev_index].y == 0:
            if self.MOVEMENT[next_index].x != self.MOVEMENT[prev_index].x:
                is_allowed = False

        return True
       # return is_allowed
