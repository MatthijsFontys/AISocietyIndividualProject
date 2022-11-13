import pygame

# my imports
from ai.my_neat import MyNeat
from world.data.data_collector import DataCollector
from drawing.draw_wrapper import DrawWrapper
from entities.entity_enums import EntityType
from entities.survivor import Survivor
from map_creator.map_save import MapSave
from util.vector_pool import VectorPool
from world.data.mock_collector import MockCollector
from world.time.game_tick_manager import GameTickManager
from util.util_enums import Direction as Dir
from world.map.collision_grid import CollisionGrid
from world.map.map_dto import MapDto
from world.map.overworld_map import OverworldMap
from world.map.waiting_map import WaitingMap

pygame.init()

VECTOR_POOL = VectorPool()

# Game setup
FPS_CAP = 10_000

MAP: OverworldMap
WAITING_MAP: WaitingMap
NEAT: MyNeat = MyNeat(start_from_gen=0, run_pygame=True)
WIN_SIZE = 900
# WINDOW = pygame.Surface((WIN_SIZE, WIN_SIZE))
WINDOW: pygame.surface
pygame.display.set_caption("SurvAIvor")

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
    draw_wrapper.survivor_painter.paint(clicked_survivor)
    draw_wrapper.grid_painter.paint(False, False)
    draw_wrapper.survivor_info_painter.paint(clicked_survivor)
    draw_wrapper.day_painter.paint()

    pygame.display.update()


def main():
    # World controllers
    tick_manager = GameTickManager()
    data_collector = DataCollector(tick_manager.dto)
    maps = ['HumbleBeginnings', 'LimitedTrees']
    init_map(maps[0], NEAT.population_size)
    draw_wrapper = init_draw(tick_manager)
    MAP.set_data_collector(data_collector)
    WAITING_MAP.set_data_collector(MockCollector())
    tick_manager.set_world(MAP, WAITING_MAP)
    tick_manager.subscribe(data_collector)

    # pygame stuff
    clock = pygame.time.Clock()
    winner = NEAT.neat_population.run(lambda genomes, config: run_neat(genomes, draw_wrapper, tick_manager, clock))
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


def run_pygame(draw_wrapper, clock, clicked_survivor):
    clock.tick(FPS_CAP)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 1 - left click, 2 - middle click, 3 - right click, 4 - scroll up, 5 - scroll down
            mouse_pos = pygame.mouse.get_pos()
            if event.button == 1:
                mouse_world = VECTOR_POOL.lend(*draw_wrapper.camera.get_mouse_world_pos(*mouse_pos))
                clicked_survivor = MAP.collision_grid.get_closest_entity(mouse_world.x, mouse_world.y,
                                                                         EntityType.SURVIVOR)
            elif event.button == 4:
                draw_wrapper.camera.set_zoom(True, *mouse_pos)
            elif event.button == 5:
                draw_wrapper.camera.set_zoom(False, *mouse_pos)

    # Camera movement
    keys = pygame.key.get_pressed()
    for key in MOVEMENT_MAP.keys():
        if keys[key]:
            clicked_survivor = None
            draw_wrapper.camera.move(MOVEMENT_MAP[key])

    if clicked_survivor is not None:
        draw_wrapper.camera.follow_position(clicked_survivor.position)
        if clicked_survivor.is_dead():
            clicked_survivor = None
    return clicked_survivor


def run_neat(genomes, draw_wrapper, tick_manager, clock):
    clicked_survivor = None
    is_first_gen = MAP.try_populate(genomes, NEAT)
    if not is_first_gen:
        WAITING_MAP.repopulate(genomes, NEAT)

    # While generation alive > threshold # Or time passed
    while WAITING_MAP.get_percent_alive() >= 0.3 or (is_first_gen and len(MAP.population) >= MAP.POPULATION_SIZE / 2):
        if NEAT.should_run_pygame:
            clicked_survivor = run_pygame(draw_wrapper, clock, clicked_survivor)

        tick_manager.tick()
        MAP.collision_grid.rebuild()
        do_survivor_actions(MAP.population, MAP.collision_grid, MAP.dto)

        WAITING_MAP.collision_grid.rebuild()
        do_survivor_actions(WAITING_MAP.population, WAITING_MAP.collision_grid, WAITING_MAP.dto)

        if NEAT.should_run_pygame:
            draw(draw_wrapper, clicked_survivor)


def init_map(name, population_size):
    global WAITING_MAP, MAP
    save: MapSave = MapSave.load(name)
    cell_size = 200
    MAP = OverworldMap(save, population_size, cell_size)
    WAITING_MAP = WaitingMap(MapSave.load(name), population_size, cell_size)


def init_draw(tick_manager):
    to_return = None
    if NEAT.should_run_pygame:
        global WINDOW
        WINDOW = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
        to_return = DrawWrapper(WINDOW, MAP, tick_manager.dto)
        tick_manager.subscribe(to_return.day_painter)
    return to_return


if __name__ == "__main__":
    main()
