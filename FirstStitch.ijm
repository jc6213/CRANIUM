#@ File (label="Input directory", style="directory") dir1
#@ String (label="File names") FileNames
#@ String (label="Tile configuration output name") TileCon
#@ File (label="Output directory", style="directory") dir2


run("Grid/Collection stitching", "type=[Grid: snake by rows] order=[Right & Down                ] grid_size_x=4 grid_size_y=3 tile_overlap=8.5 first_file_index_i=1 directory="+dir1+" file_names=["+FileNames+"] output_textfile_name="+TileCon+" fusion_method=[Linear Blending] regression_threshold=0.30 max/avg_displacement_threshold=2.50 absolute_displacement_threshold=3.50 compute_overlap computation_parameters=[Save memory (but be slower)] image_output=[Write to disk] output_directory="+dir2);
