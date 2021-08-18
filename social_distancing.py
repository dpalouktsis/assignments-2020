from file_management import write_circle, write_segment, read_bounds
from file_management import file_management_close, file_management_init
from Circle import Circle
import random
import argparse


def run_algorithm(bounds_filename, items, r, seed, min_radius, max_radius, output_file):
    if bounds_filename:
        bounds = read_bounds(bounds_filename)
    else:
        bounds = []

    r = r

    random.seed(seed)
    min_radius = min_radius
    max_radius = max_radius
    circle_list = []
    metopo = []
    zwntanoi = set()

    first_r = round(random.random() *
                    (max_radius - min_radius) + min_radius, 2)
    c1 = Circle(0.00, 0.00, first_r)
    zwntanoi.add(c1)
    metopo.insert(0, c1)
    circle_list.append(c1)

    second_r = round(random.random() *
                     (max_radius - min_radius) + min_radius, 2)
    c2 = Circle(round(first_r + second_r, 2), 0.00, second_r)
    zwntanoi.add(c2)
    metopo.insert(0, c2)
    circle_list.append(c2)

    cm_index = find_cm(metopo, 0, 0, zwntanoi)
    cn_index = find_cn(cm_index, len(metopo))
    times = 2
    reset_undo = True

    while (len(zwntanoi) > 0):
        if items and times == items:
            break
        if reset_undo:
            old_metopo = metopo.copy()
            old_zwntanoi = zwntanoi.copy()
        if (r == -1):
            next_r = round(random.random() *
                           (max_radius - min_radius) + min_radius, 2)
        else:
            next_r = r

        ci = metopo[cm_index].find_adj_circle(
            metopo[cn_index], next_r)
        cj_result = try_new_cirle(metopo, cm_index, cn_index, ci)
        if cj_result == (-1):  # 5
            if circle_intersects_bounds(ci, bounds):
                zwntanoi = old_zwntanoi.copy()
                zwntanoi.discard(metopo[cm_index])
                metopo = old_metopo.copy()
            else:
                metopo.insert(0, ci)
                zwntanoi = set()
                for circle in metopo:
                    zwntanoi.add(circle)
                circle_list.append(ci)
                times = times + 1
            reset_undo = True
            cm_index = find_cm(metopo, 0, 0, zwntanoi)
            cn_index = find_cn(cm_index, len(metopo))
        else:  # 4
            cj_index = cj_result[0]
            before_cm = cj_result[1]
            reset_undo = False
            removed = []
            if (before_cm):
                if (cn_index == 0):
                    removed.extend(metopo[cj_index+1:])
                    del metopo[cj_index+1:]
                else:
                    if (cj_index > cn_index):
                        removed.extend(metopo[cj_index + 1:])
                        removed.extend(metopo[0: cn_index])
                        del metopo[cj_index + 1:]
                        del metopo[0: cn_index]
                    else:
                        removed.extend(metopo[cj_index+1:cn_index])
                        del metopo[cj_index+1:cn_index]
                for circle in removed:
                    zwntanoi.discard(circle)
                cm_index = cj_index
                cn_index = find_cn(cm_index, len(metopo))
            elif (cj_index == cm_index or cj_index == cn_index):
                print("cj = cm or cj = cn")
                exit(1)
            else:  # ii
                if (cj_index == 0):
                    removed.extend(metopo[cm_index+1:])
                    del metopo[cm_index+1:]
                else:
                    if (cj_index < cm_index):
                        removed.extend(metopo[cm_index+1:])
                        removed.extend(metopo[0: cj_index])
                        del metopo[cm_index + 1:]
                        del metopo[0: cj_index]
                    else:
                        removed.extend(metopo[cm_index+1:cj_index])
                        del metopo[cm_index+1:cj_index]
                cn_index = cj_index
    print(times)
    write_results(output_file, circle_list, metopo, bounds)


def circle_intersects_bounds(circle, bounds):
    if len(bounds) == 0:
        return False
    for segment in bounds:
        if circle.dist_circle_segment(segment[0], segment[1],
                                      segment[2], segment[3]) < circle.r:
            return True
    return False


def is_alive(zwntanoi, circle):
    return circle in zwntanoi


def find_cm(thismetopo, x, y, zwntanoi):
    w = thismetopo[0]
    deiktis = 0
    min = w.find_distance(x, y)
    for i in range(1, len(thismetopo)):
        if (is_alive(zwntanoi, thismetopo[i]) and thismetopo[i].find_distance(x, y) <= min):
            min = thismetopo[i].find_distance(x, y)
            deiktis = i
    return deiktis


def find_cn(cm_pointer, length_met):
    i = (cm_pointer + 1) % length_met
    return i


def test():
    c3 = Circle(-2.00, 0.00, 1.00)
    c4 = Circle(2.00, 0.00, 1.00)
    t1 = c3.find_distance(0, 0)
    print(t1)
    t2 = c3.find_adj_circle(c4, 1)
    print(t2)
    t3 = c3.dist_circle_segment(1, 1, 1, 1)
    print(t3)


def try_new_cirle(thismetopo, cm_index, cn_index, ci):
    found_cj = False
    cj_index = -1
    cj_index_tonos = -1
    for i in range(0, len(thismetopo)):
        current = (i + cn_index) % len(thismetopo)
        if ci.intersect(thismetopo[current]):
            if (found_cj):
                cj_index_tonos = current
                cj_cm = (len(thismetopo) - 1) - i
            else:
                cj_index = current
                cn_cj = i - 1
                found_cj = True
    if (not found_cj):
        return -1
    else:
        if (cj_index_tonos == -1):
            cj_index_tonos = cj_index
            if (cm_index < cj_index_tonos):
                cj_cm = len(thismetopo) - cj_index_tonos + cm_index - 1
            else:
                cj_cm = cm_index - cj_index - 1
        if (cj_cm <= cn_cj):
            return (cj_index_tonos, True)  # Before cm
        else:
            return (cj_index, False)  # After cn


def write_results(filename, circle_list, metopo, bounds):
    file_management_init(filename)
    write_circles(circle_list)
    #write_metopo(metopo)
    write_bounds(bounds)
    file_management_close()


def write_circles(circle_list):
    for circle in circle_list:
        write_circle(circle.x, circle.y, circle.r)


def write_metopo(metopo):
    for circle in metopo:
        write_circle(circle.x, circle.y, 1.00)


def write_bounds(bounds):
    for segment in bounds:
        write_segment(segment[0], segment[1], segment[2], segment[3])


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--items", type=int, help="ITEMS")
parser.add_argument("-r", "--radius", type=float,
                    help="RADIUS")
parser.add_argument("--min_radius", type=float, help="MIN_RADIUS")
parser.add_argument("--max_radius", type=float, help="MAX_RADIUS")
parser.add_argument("-b", "--boundary_file", type=str,
                    help="BOUNDARY_FILE")
parser.add_argument("-s", "--seed", type=int, help="SEED")
parser.add_argument("output_file", type=str)

args = parser.parse_args()

r = -1
if args.radius:
    r = args.radius
run_algorithm(args.boundary_file, args.items, r, args.seed,
              args.min_radius, args.max_radius, args.output_file)
