import pygame

# my imports
from ai.my_neat import MyNeat
from drawing.draw_wrapper import DrawWrapper
from entities.entity_enums import EntityType
from entities.survivor import Survivor
from map_creator.map_save import MapSave
from util.vector import Vector
from util.vector_pool import VectorPool
from world.game_tick_manager import GameTickManager
from util.util_enums import Direction as Dir
from world.collision_grid import CollisionGrid
from world.map_dto import MapDto
from world.overworld_map import OverworldMap
from world.waiting_map import WaitingMap

pygame.init()

VECTOR_POOL = VectorPool()

# Game setup
FPS_CAP = 10_000 #60

MAP: OverworldMap
WAITING_MAP: WaitingMap
NEAT: MyNeat = MyNeat()
WIN_SIZE = 900
WINDOW: pygame.surface = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
pygame.display.set_caption("SurvAIvor")

# Allow a playable character for debugging
PLAYABLE_CHAR = False
PLAYER_SPEED = 3
PLAYER_MAP = {
    pygame.K_UP: [0, -PLAYER_SPEED],
    pygame.K_DOWN: [0, PLAYER_SPEED],
    pygame.K_LEFT: [-PLAYER_SPEED, 0],
    pygame.K_RIGHT: [PLAYER_SPEED, 0]
}

# Map from pygame keys to my enum to keep layers seperate
MOVEMENT_MAP = {
    pygame.K_UP: Dir.UP,
    pygame.K_DOWN: Dir.DOWN,
    pygame.K_LEFT: Dir.LEFT,
    pygame.K_RIGHT: Dir.RIGHT
}


def draw(draw_wrapper, clicked_survivor):
    WINDOW.fill(pygame.Color(106, 148, 106))
    draw_wrapper.tree_painter.paint(draw_wrapper.survivor_painter.survivor_radius, False)
    draw_wrapper.survivor_painter.paint()
    draw_wrapper.grid_painter.paint(False, False)
    draw_wrapper.survivor_info_painter.paint(clicked_survivor)
    draw_wrapper.day_painter.paint()

    pygame.display.update()


def main():
    maps = ['HumbleBeginnings', 'LimitedTrees']
    init_map(maps[0], NEAT.population_size)

    # drawing objects
    tick_manager = GameTickManager(MAP, WAITING_MAP)
    draw_wrapper = DrawWrapper(WINDOW, MAP, tick_manager)

    # if PLAYABLE_CHAR:
    #     MAP.population.append(Survivor(Vector(400, 400)))

    # pygame stuff
    clock = pygame.time.Clock()
    should_run = True

    while should_run:
        winner = NEAT.neat_population.run(lambda genomes, config: run_neat(genomes, draw_wrapper, tick_manager, clock))

    for i in range(10_000):
        print('######################################### DONE ######################################')

    # Main loop and camera controls
    while should_run:
        clock.tick(FPS_CAP)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 4:
                    draw_wrapper.camera.set_zoom(True, *mouse_pos)
                elif event.button == 5:
                    draw_wrapper.camera.set_zoom(False, *mouse_pos)

        # Player and camera movement
        keys = pygame.key.get_pressed()
        for key in MOVEMENT_MAP.keys():
            if keys[key]:
                if PLAYABLE_CHAR:
                    player_dir = PLAYER_MAP[key]
                    player = MAP.population[0]
                    player.position.add(VECTOR_POOL.lend(player_dir[0], player_dir[1]))
                    draw_wrapper.camera.follow_position(player.position)
                else:
                    draw_wrapper.camera.move(MOVEMENT_MAP[key])

        # Handling the game world
        # Also handles the waiting queue, to allow new agents into the world
        # Actions before drawing
        tick_manager.tick()
        do_survivor_actions(MAP.population, MAP.collision_grid, MAP.dto)
        # Actions of survivors in waiting room
        do_survivor_actions(WAITING_MAP.population, WAITING_MAP.collision_grid, WAITING_MAP.dto)

        # Drawing
        #draw(draw_wrapper, clicked_survivor)

    pygame.quit()


def do_survivor_actions(population: [Survivor], grid: CollisionGrid, dto: MapDto):
    for survivor in population:
        # getting the inputs for the neural network and performing the chosen action
        tree = grid.get_closest_entity(survivor.position.x, survivor.position.y, EntityType.TREE)
        tree_x_dist = 1
        tree_y_dist = 1
        tree_fruit_count = 0

        # todo: make a nullable survivor and tree instead
        if tree is not None:
            tree_x_dist = (survivor.position.x - tree.position.x) / MAP.WIDTH
            tree_y_dist = (survivor.position.y - tree.position.y) / MAP.HEIGHT
            tree_fruit_count = tree.food_count / tree.max_food_count

        inputs = [
            survivor.fullness / 100,
            survivor.position.x / MAP.WIDTH,
            survivor.position.y / MAP.HEIGHT,
            tree_x_dist,
            tree_y_dist,
            tree_fruit_count
        ]

        action_index = NEAT.feed_forward(survivor, inputs)
        survivor.move(action_index, dto)
        if tree is not None:
            tree.try_forage_food(survivor)


def run_neat(genomes, draw_wrapper, tick_manager, clock):
    clicked_survivor = None
    is_first_gen = MAP.try_populate(genomes, NEAT)
    if not is_first_gen:
        WAITING_MAP.repopulate(genomes, NEAT)

    # While generation alive > threshold
    # Or time passed
    while WAITING_MAP.get_percent_alive() >= 0.3 or (is_first_gen and len(MAP.population) >= MAP.POPULATION_SIZE / 2):
        clock.tick(FPS_CAP)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 1 - left click, 2 - middle click, 3 - right click, 4 - scroll up, 5 - scroll down
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    mouse_world = VECTOR_POOL.lend(*draw_wrapper.camera.get_mouse_world_pos(*mouse_pos))
                    clicked_survivor = MAP.collision_grid.get_closest_entity(mouse_world.x, mouse_world.y, EntityType.SURVIVOR)
                elif event.button == 4:
                    draw_wrapper.camera.set_zoom(True, *mouse_pos)
                elif event.button == 5:
                    draw_wrapper.camera.set_zoom(False, *mouse_pos)

        # Camera movement
        keys = pygame.key.get_pressed()
        for key in MOVEMENT_MAP.keys():
            if keys[key]:
                draw_wrapper.camera.move(MOVEMENT_MAP[key])

        if clicked_survivor is not None:
            draw_wrapper.camera.follow_position(clicked_survivor.position)
        tick_manager.tick()
        MAP.collision_grid.rebuild()
        do_survivor_actions(MAP.population, MAP.collision_grid, MAP.dto)

        WAITING_MAP.collision_grid.rebuild()
        do_survivor_actions(WAITING_MAP.population, WAITING_MAP.collision_grid, WAITING_MAP.dto)
        draw(draw_wrapper, clicked_survivor)


def init_map(name, population_size):
    global WAITING_MAP, MAP
    save: MapSave = MapSave.load(name)
    cell_size = 200
    MAP = OverworldMap(save, population_size, cell_size)
    WAITING_MAP = WaitingMap(MapSave.load(name), population_size, cell_size)


if __name__ == "__main__":
    main()
