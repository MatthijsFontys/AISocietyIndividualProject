import sys
from glob import glob
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
from world.map.map_checkpoint import MapCheckpoint
from world.time.game_tick_manager import GameTickManager
from util.util_enums import Direction as Dir
from world.map.collision_grid import CollisionGrid
from world.map.map_dto import MapDto
from world.map.overworld_map import OverworldMap
from world.map.waiting_map import WaitingMap

pygame.init()

VECTOR_POOL = VectorPool()

# Game setup
FPS_CAP = 10_000  # 60

MAP: OverworldMap
WAITING_MAP: WaitingMap
NEAT: MyNeat
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


def draw(draw_wrapper):
    WINDOW.fill(pygame.Color(106, 148, 106))
    draw_wrapper.tree_painter.paint(draw_wrapper.survivor_painter.survivor_radius, False)
    draw_wrapper.survivor_painter.paint(draw_wrapper.clicked_survivor)
    draw_wrapper.day_painter.paint()
    draw_wrapper.grid_painter.paint(should_paint=True)
    draw_wrapper.survivor_info_painter.paint(draw_wrapper.clicked_survivor)

    pygame.display.update()


def main():
    # World controllers
    tick_manager = GameTickManager()
    maps = ['HumbleBeginnings', 'LimitedTrees']
    #init_neat(maps[0], tick_manager, should_pygame=True)  # alternatively use load_neat to load an existing population
    # load_neat(tick_manager, start_from_gen=725, should_pygame=True)  # alternatively use init_neat to start from scratch
    load_latest_gen_neat(tick_manager, init_map_name=maps[0], should_pygame=True)
    init_map()
    data_collector = DataCollector(tick_manager.dto, NEAT.population_size)
    draw_wrapper = init_draw(tick_manager)
    MAP.set_data_collector(data_collector)
    WAITING_MAP.set_data_collector(MockCollector())
    tick_manager.set_world(MAP, WAITING_MAP)
    tick_manager.subscribe(data_collector)

    # pygame stuff
    clock = pygame.time.Clock()
    _ = NEAT.neat_population.run(lambda genomes, config: run_neat(genomes, draw_wrapper, tick_manager, clock))
    pygame.quit()


def do_survivor_actions(population: [Survivor], grid: CollisionGrid, dto: MapDto, clicked_survivor):
    # stats (fullness and cold)
    # self position (self x + self y)
    # inputs = 9 * 4 grid
    # closest entity position (tree / fire / seed) (x dist, y dist)
    # population count for each of the 9 cells in the grid

    # so for each of the 9 cells, we need:
    # population density + 4 pixel input + check entities for the closest record

    for survivor in population:
        grid_inputs, closest_entity = grid.get_inputs(survivor)
        # Todo: Figure out why the quantity of the entities match the situation, but the order is messed up somehow
        if survivor == clicked_survivor:
            # [inclusive:exclusive]
            print('### START ###')
            for i in range(0, 45, 5):
                print(grid_inputs[i: i+5])
            print('### END ###')
        closest_entity_inputs = [MAP.WIDTH, MAP.HEIGHT]
        if closest_entity is not None:
            closest_entity_inputs[0] = (survivor.position.x - closest_entity.position.x) / MAP.WIDTH
            closest_entity_inputs[1] = (survivor.position.y - closest_entity.position.y) / MAP.HEIGHT

        inputs = [
            # Low res pixel input
            *grid_inputs,
            # Stat inputs
            survivor.fullness / 100,
            # survivor.temperature / 100,
            # Own location input
            survivor.position.x / MAP.WIDTH,
            survivor.position.y / MAP.HEIGHT,
            # Nearby entity input
            *closest_entity_inputs

        ]
        tree = grid.get_closest_entity(survivor.position.x, survivor.position.y, EntityType.TREE)
        if tree is not None:
            tree.try_forage_food(survivor)
        action_index = NEAT.feed_forward(survivor, inputs)
        survivor.move(action_index, dto)


def run_pygame(draw_wrapper, clock):
    clock.tick(FPS_CAP)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 1 - left click, 2 - middle click, 3 - right click, 4 - scroll up, 5 - scroll down
            mouse_pos = pygame.mouse.get_pos()
            if event.button == 1:
                mouse_world = VECTOR_POOL.lend(*draw_wrapper.camera.get_mouse_world_pos(*mouse_pos))
                draw_wrapper.clicked_survivor = MAP.collision_grid.get_closest_entity(mouse_world.x, mouse_world.y,
                                                                                      EntityType.SURVIVOR)
            elif event.button == 4:
                draw_wrapper.camera.set_zoom(True, *mouse_pos)
            elif event.button == 5:
                draw_wrapper.camera.set_zoom(False, *mouse_pos)

    # Camera movement
    keys = pygame.key.get_pressed()
    for key in MOVEMENT_MAP.keys():
        if keys[key]:
            draw_wrapper.clicked_survivor = None
            draw_wrapper.camera.move(MOVEMENT_MAP[key])

    if draw_wrapper.clicked_survivor is not None:
        draw_wrapper.camera.follow_position(draw_wrapper.clicked_survivor.position)
        if draw_wrapper.clicked_survivor.is_dead():
            draw_wrapper.clicked_survivor = None


def run_neat(genomes, draw_wrapper, tick_manager, clock):
    is_first_gen = MAP.try_populate(genomes, NEAT)
    if not is_first_gen:
        WAITING_MAP.repopulate(genomes, NEAT)

    day_of_prev_gen = tick_manager.day
    day_threshold = 5
    # While generation alive > threshold # Or time passed
    while (WAITING_MAP.get_percent_alive() >= 0.10
            or (is_first_gen and len(MAP.population) >= MAP.POPULATION_SIZE / 2))\
            and tick_manager.day - day_of_prev_gen < day_threshold:
        if NEAT.should_run_pygame:
            run_pygame(draw_wrapper, clock)

        tick_manager.tick()
        MAP.collision_grid.rebuild()
        do_survivor_actions(MAP.population, MAP.collision_grid, MAP.dto, draw_wrapper.clicked_survivor)

        WAITING_MAP.collision_grid.rebuild()
        do_survivor_actions(WAITING_MAP.population, WAITING_MAP.collision_grid, WAITING_MAP.dto, draw_wrapper.clicked_survivor)

        if NEAT.should_run_pygame:
            draw(draw_wrapper)


def init_neat(map_name: str, tick_manager: GameTickManager, should_pygame=True):
    global NEAT
    map_checkpoint = MapCheckpoint(map_name, tick_manager.dto)
    NEAT = MyNeat(start_from_gen=0, run_pygame=should_pygame, map_checkpoint=map_checkpoint)


def load_neat(tick_manager: GameTickManager, start_from_gen: int, should_pygame=True):
    global NEAT
    NEAT = MyNeat(start_from_gen=start_from_gen, run_pygame=should_pygame)
    tick_manager.set_dto(NEAT.map_checkpoint.tick_dto)


def load_latest_gen_neat(tick_manager: GameTickManager, init_map_name, should_pygame=True):
    checkpoints = glob('./checkpoints/neat-checkpoint-*[0-9]')
    checkpoints.sort(key=lambda x: (len(x), x))
    if checkpoints:
        latest_gen = int(checkpoints[-1].split('-')[-1])
        load_neat(tick_manager, start_from_gen=latest_gen, should_pygame=should_pygame)
    else:
        init_neat(init_map_name, tick_manager, should_pygame)




def init_map():
    global WAITING_MAP, MAP
    save: MapSave = MapSave.load(NEAT.map_checkpoint.name)
    cell_size = 200
    MAP = OverworldMap(save, NEAT.population_size, cell_size)
    WAITING_MAP = WaitingMap(MapSave.load(NEAT.map_checkpoint.name), NEAT.population_size, cell_size)


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
