from world.time.game_tick_dto import GameTickDto


class MapCheckpoint:
    def __init__(self, name: str, tick_dto: GameTickDto):
        self.name = name
        self.tick_dto = tick_dto

    def get_day(self) -> int:
        return self.tick_dto.day
