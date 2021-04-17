const app = new PIXI.Application();

// CONSTANTS
const TILESIZE = 16;

// The application will create a canvas element for you that you
// can then insert into the DOM
document.body.appendChild(app.view);

function setTilePlacement(current_tile, i, j) {
    current_tile.x = TILESIZE * j;
    current_tile.y = TILESIZE * i;
}

function genMap(input_map, scale, free_path_textures, forest_texture, d_forest_texture) {
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
            current_tile.scale.set(scale)
            
            app.stage.addChild(current_tile);
        }
    }
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
            resources.free_path_1.texture,
            resources.free_path_2.texture,
            resources.free_path_3.texture
        ];

        genMap(input_map, TILESIZE / 32, 
            free_path_textures,
            resources.forest.texture,
            resources.dense_forest.texture);
    });    

} else {
    
}