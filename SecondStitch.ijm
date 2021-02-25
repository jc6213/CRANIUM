#@ File (label="Input directory", style="directory") dir1
#@ String (label="Tile configuration input") TileCon
#@ File (label="Output directory", style="directory") dir2

run("Grid/Collection stitching", "type=[Positions from file] order=[Defined by TileConfiguration] directory="+dir1+" layout_file="+TileCon+" fusion_method=[Linear Blending] regression_threshold=0.30 max/avg_displacement_threshold=2.50 absolute_displacement_threshold=3.50 computation_parameters=[Save memory (but be slower)] image_output=[Write to disk] output_directory="+dir2);
