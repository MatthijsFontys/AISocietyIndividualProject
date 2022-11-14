from glob import glob


def get_asset_path():
    return 'drawing/assets/'


def sprite_glob(sprite_pattern):
    return glob(f'{get_asset_path()}images/{sprite_pattern}')
