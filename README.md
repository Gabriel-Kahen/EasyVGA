# Visiblity Graph Analysis Overview

This code performs a simple [visiblity graph analysis](https://en.wikipedia.org/wiki/Visibility_graph_analysis). The further to the right on the colormap below, the more visible.

![jetcolormap](https://i.imgur.com/QLmNLR2.png)

## Examples

### t intersection
- **Input:** `test_imgs/t_in.png`
- **Output:** `test_imgs/t_out.png`

| Input Image | Output Image |
|-------------|--------------|
| <img src="test_imgs/t_in.png" width="600"> | <img src="test_imgs/t_out.png" width="600"> |

### Squares
- **Input:** `test_imgs/squares_in.png`
- **Output:** `test_imgs/squares_out.png`

| Input Image | Output Image |
|-------------|--------------|
| <img src="test_imgs/squares_in.png" width="600"> | <img src="test_imgs/squares_out.png" width="600"> |

### Floor Plan
- **Input:** `test_imgs/floorplan_in.png`
- **Output:** `test_imgs/floorplan_out.png`

| Input Image | Output Image |
|-------------|--------------|
| <img src="test_imgs/floorplan_in.png" width="600"> | <img src="test_imgs/floorplan_out.png" width="600"> |

### Streets (using coordinates)
- Coordinate Input: 40.7611, -73.6533 | 40.7490, -73.6773 | (shown in `test_imgs/streets_in.png`)
- **Output:** `test_imgs/streets_out.png`

| Input Image | Output Image |
|-------------|--------------|
| <img src="test_imgs/streets_in.png" width="600"> | <img src="test_imgs/streets_out.png" width="400"> |

## Usage

To use the code, simply run `run.py`. 
I recommend [Open Street Map](https://www.openstreetmap.org/export) for finding coordinates, but you can use whatever you prefer.
