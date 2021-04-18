// import * as PIXI from '../lib/pixi';
"use strict";

const app = new PIXI.Application();

// CONSTANTS
const TILESIZE = 16;
const GLOBAL_SCALE = TILESIZE / 32;
const ASH_OFFSET = { 
    x: 16 * GLOBAL_SCALE,
    y: 8 * GLOBAL_SCALE
};
const ASH_SPEED = 0.5;

document.body.appendChild(app.view);

function setTilePlacement(current_tile, i, j) {
    current_tile.x = TILESIZE * j;
    current_tile.y = TILESIZE * i;
}

function generateMap(input_map, free_path_textures, forest_texture, d_forest_texture) {
    let start_i, start_j;

    for (let i = 0; i < input_map.length; i++) {
        for (let j = 0; j < input_map[0].length; j++) {
            let current_tile;
            switch (input_map[i][j]) {
                case 'M': // tile should be deep forest
                    current_tile = new PIXI.Sprite(d_forest_texture);
                    break;
                case 'R': // tile should be forest
                    current_tile = new PIXI.Sprite(forest_texture);
                    break;
                case '.': // tile should be free path
                    let rnd = Math.floor(Math.random() * 3);
                    current_tile = new PIXI.Sprite(free_path_textures[rnd]);
                    break;
                case 'B': // tile should be base
                    current_tile = new PIXI.Sprite(free_path_textures[0]);
                    break;
                case 'I': // tile should be start
                    start_i = i;
                    start_j = j;
                    current_tile = new PIXI.Sprite(free_path_textures[0]);
                    break;
                case 'F': // tile should be end
                    current_tile = new PIXI.Sprite(free_path_textures[0]);
                    break;
                default:
                    console.log(input_map[i][j]);
                    return;
            }
            setTilePlacement(current_tile, i, j);
            current_tile.scale.set(GLOBAL_SCALE)
            
            app.stage.addChild(current_tile);
        }
    }

    return { i: start_i, j: start_j };
}


/*
    walkToTile: moves ash's sprite towards target tile.

    Returns true if sprite is in the target tile already
        and false otherwise.
*/
function walkToTile(ash_sprite, ash_sheet, tile) {
    let target_x = (tile[1] * TILESIZE) + ASH_OFFSET.x;
    let target_y = (tile[0] * TILESIZE) + ASH_OFFSET.y;
    
    let x_diff = target_x - ash_sprite.x;
    let y_diff = target_y - ash_sprite.y;

    if (Math.abs(x_diff) < 1e-3 && Math.abs(y_diff) < 1e-3) {
        ash_sprite.stop();
        return true;
    }

    // Update sprite animation
    if (x_diff > 0) {
        ash_sprite.x += ASH_SPEED;
        if (!ash_sprite.playing) {
            ash_sprite.textures = ash_sheet['walk_east'];
            ash_sprite.play();
        }
    } else if (x_diff < 0) {
        ash_sprite.x -= ASH_SPEED;
        if (!ash_sprite.playing) {
            ash_sprite.textures = ash_sheet['walk_west'];
            ash_sprite.play();
        }
    } else if (y_diff > 0) {
        ash_sprite.y += ASH_SPEED;
        if (!ash_sprite.playing) {
            ash_sprite.textures = ash_sheet['walk_south'];
            ash_sprite.play();
        }
    } else if (y_diff < 0) {
        ash_sprite.y -= ASH_SPEED;
        if (!ash_sprite.playing) {
            ash_sprite.textures = ash_sheet['walk_north'];
            ash_sprite.play();
        }
    }

    return false;
}

let input_map = prompt("Enter map:");

if (input_map) {
    input_map = input_map.split('\n');
    let n_tiles_vert = input_map.length;
    let n_tiles_horiz = input_map[0].length;

    // Load assets
    app.loader.add('ash_stand_back', '../assets/ash/ash_stand_back.png')
    app.loader.add('ash_stand_front', '../assets/ash/ash_stand_front.png')
    app.loader.add('ash_stand_left', '../assets/ash/ash_stand_left.png')
    app.loader.add('ash_stand_right', '../assets/ash/ash_stand_right.png')
    app.loader.add('ash_walk_back_1', '../assets/ash/ash_walk_back_1.png')
    app.loader.add('ash_walk_back_2', '../assets/ash/ash_walk_back_2.png')
    app.loader.add('ash_walk_front_1', '../assets/ash/ash_walk_front_1.png')
    app.loader.add('ash_walk_front_2', '../assets/ash/ash_walk_front_2.png')
    app.loader.add('ash_walk_left_1', '../assets/ash/ash_walk_left_1.png')
    app.loader.add('ash_walk_left_2', '../assets/ash/ash_walk_left_2.png')
    app.loader.add('ash_walk_right_1', '../assets/ash/ash_walk_right_1.png')
    app.loader.add('ash_walk_right_2', '../assets/ash/ash_walk_right_2.png')

    app.loader.add('forest', '../assets/map/forest.png')
    app.loader.add('dense_forest', '../assets/map/dense_forest_1.png')
    app.loader.add('free_path_1', '../assets/map/free_path_1.png')
    app.loader.add('free_path_2', '../assets/map/free_path_2.png')
    app.loader.add('free_path_3', '../assets/map/free_path_3.png')

    app.loader.load((_loader, resources) => {
        app.renderer.autoResize = true;
        app.renderer.resize(TILESIZE * n_tiles_horiz, TILESIZE * n_tiles_vert);

        let free_path_textures = [
            resources['free_path_1'].texture,
            resources['free_path_2'].texture,
            resources['free_path_3'].texture,
        ];

        // Generate map and grab start coordinates
        let start_coords = generateMap(input_map, 
            free_path_textures,
            resources.forest.texture,
            resources.dense_forest.texture);

        // Create and setup Ash's sprite
        let ash_sheet = {
            'stand_south': [
                resources['ash_stand_front'].texture
            ],
            'stand_north': [
                resources['ash_stand_back'].texture
            ],
            'stand_east': [
                resources['ash_stand_right'].texture
            ],
            'stand_west': [
                resources['ash_stand_left'].texture
            ],
            'walk_south': [
                resources['ash_walk_front_1'].texture,
                resources['ash_walk_front_2'].texture,
            ],
            'walk_north': [
                resources['ash_walk_back_1'].texture,
                resources['ash_walk_back_2'].texture,
            ],
            'walk_east': [
                resources['ash_walk_right_1'].texture,
                resources['ash_walk_right_2'].texture,
            ],
            'walk_west': [
                resources['ash_walk_left_1'].texture,
                resources['ash_walk_left_2'].texture,
            ],
        };

        let ash_sprite = new PIXI.AnimatedSprite(ash_sheet['stand_south']);
        ash_sprite.anchor.set(0.5);
        ash_sprite.scale.set(GLOBAL_SCALE);
        setTilePlacement(ash_sprite, start_coords.i, start_coords.j);

        // offset position to fit in tile
        ash_sprite.x += ASH_OFFSET.x;
        ash_sprite.y += ASH_OFFSET.y;
        ash_sprite.animationSpeed = .075;
        ash_sprite.loop = false;
        app.stage.addChild(ash_sprite);
        ash_sprite.play();

        // TODO: Should get the path at this point, but its hardcoded for now
        let path = [
            [start_coords.i, start_coords.j],
            [start_coords.i, start_coords.j - 1],
            [start_coords.i, start_coords.j - 2],
            [start_coords.i + 1, start_coords.j - 2],
            [start_coords.i + 1, start_coords.j - 3],
            [start_coords.i + 1, start_coords.j - 4],
            [start_coords.i + 1, start_coords.j - 5],
            [start_coords.i + 1, start_coords.j - 6],
            [start_coords.i + 1, start_coords.j - 7],
            [start_coords.i + 1, start_coords.j - 8],
            [start_coords.i, start_coords.j - 8],
            [start_coords.i - 1, start_coords.j - 8],
        ];
        let current_tile = 0;
        
        app.ticker.add(() => {
            if (current_tile + 1 < path.length) {
                if (walkToTile(ash_sprite, ash_sheet, path[current_tile + 1])) {
                    current_tile++;
                }
            } else {
                ash_sprite.textures = ash_sheet['stand_south'];
            } 
        });
    });    
} else {
    
}