from shapely.geometry import Point as geometryPoint


def get_rectangle_in_an_image(matrix, rectangle):
    # @Todo Add a documentation

    return matrix[rectangle[1]: rectangle[1] + rectangle[3],
           rectangle[0]: rectangle[0] + rectangle[2]]


def fill_pixel_if_belongs_to_polygon(matrix,
                                     polygon,
                                     row_idx,
                                     column_idx,
                                     pixel_value):
    # @Todo Add a documentation
    point = geometryPoint(column_idx, row_idx)
    if polygon.contains(point):
        matrix[row_idx][column_idx] = pixel_value
