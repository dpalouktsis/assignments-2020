file1 = None


def write_circle(x, y, r):
    global file1
    x1 = str(x)
    y1 = str(y)
    r1 = str(r)
    arg = x1+" "+y1+" "+r1
    file1.write(arg + '\n')


def write_segment(x1, y1, x2, y2):
    global file1
    print(x1, y1, x2, y2, file=file1)


def file_management_init(text_name):
    global file1
    file1 = open(text_name, "w")


def file_management_close():
    global file1
    file1.close()


def read_bounds(file_name):
    bounds = []
    bounds_file = open(file_name, "r")
    for line in bounds_file:
        bound_coords = line.split()
        bounds.append((float(bound_coords[0]), float(bound_coords[1]),
                       float(bound_coords[2]), float(bound_coords[3])))
    bounds_file.close()
    return bounds
