import networkx as nx
import matplotlib.pyplot as plt

graphs = {}
weighted = {}


def is_0_or_1(a):
    """
    This function checks, is given value 0 or 1
    :return: bool
    """
    try:
        b = int(a)
        return b == 0 or b == 1
    except ValueError:
        return False


def is_integer(a):
    """
    This function checks, is given value integer
    :return: bool
    """
    try:
        int(a)
        return True
    except ValueError:
        return False


def add_node(user_id, node_names):
    if len(node_names) > 100000:
        return "Вы пытаетесь добавить слишком много вершин"
    if user_id not in graphs:
        return "У вас еще нет графа"
    for node_name in node_names:
        if node_name in graphs[user_id].nodes:
            return "В графе уже есть одна из этих вершин"
    for node_name in node_names:
        graphs[user_id].add_node(node_name)
    return "Готово!"


def create_graph(user_id, graph):
    correct = True
    for i in range(len(graph)):
        if i > 2 or not is_0_or_1(graph[i]):
            correct = False
            break
        graph[i] = int(graph[i])
    if not correct:
        return "Вы ввели некорректные данные. Обратитесь к команде help"
    if graph[0] == 0:
        graphs[user_id] = nx.Graph()
    else:
        graphs[user_id] = nx.DiGraph()
    weighted[user_id] = bool(graph[1])
    return "Готово!"


def show_nodes(user_id):
    if user_id not in graphs:
        return "У вас еще нет графа"
    nodes = ""
    for node in graphs[user_id].nodes:
        nodes += "{} ".format(node)
    return nodes


def delete_graph(user_id):
    if user_id in graphs:
        graphs.pop(user_id)
        weighted.pop(user_id)


def show_edges(user_id):
    if user_id not in graphs:
        return "У вас еще нет графа"
    if weighted[user_id]:
        edges = ""
        for edge in graphs[user_id].edges:
            edges += "{} {} {}\n".format(edge[0], edge[1], graphs[user_id][
                edge[0]][edge[1]]['weight'])
        return edges
    else:
        edges = ""
        for edge in graphs[user_id].edges:
            edges += "{} {}\n".format(edge[0], edge[1])
        return edges


def update_edge(user_id, edge):
    if user_id not in graphs:
        return "У вас еще нет графа"
    if weighted[user_id]:
        if len(edge) != 3 or not is_integer(edge[2]):
            return "Вы ввели некорректные данные. Обратитесь к команде help"
        if edge[0] not in graphs[user_id] or edge[1] not in graphs[user_id]:
            return "Таких вершин нет"
        try:
            graphs[user_id][edge[0]][edge[1]]['weight'] = int(edge[2])
            return "Вес ребра изменён"
        except KeyError:
            graphs[user_id].add_edge(edge[0], edge[1], weight=int(edge[2]))
            return "Ребро добавлено"
    else:
        return "У вас невзвешенный граф"


def draw_graph(user_id):
    if user_id not in graphs:
        return "У вас еще нет графа"
    pos = nx.spring_layout(graphs[user_id])
    nx.draw(graphs[user_id], pos)
    nx.draw_networkx_labels(graphs[user_id], pos)
    weights = nx.get_edge_attributes(graphs[user_id], 'weight')
    nx.draw_networkx_edge_labels(graphs[user_id], pos, edge_labels=weights)
    plt.savefig('temp.png', dpi=300)
    plt.close()
    return "OK"


def delete_node(user_id, node_names):
    if user_id not in graphs:
        return "У вас еще нет графа"
    for node_name in node_names:
        if node_name not in graphs[user_id]:
            return "Одной из вершин нет в графе"
    for node_name in node_names:
        graphs[user_id].remove_node(node_name)
    return "Готово!"


def dijkstra(user_id, start_node):
    if user_id not in graphs:
        return "У вас еще нет графа"
    if len(start_node) != 1:
        return "Вы ввели некорректные данные. Обратитесь к команде help"
    if start_node[0] not in graphs[user_id].nodes:
        return "Такой вершины нет в графе"
    sssp = nx.shortest_path_length(graphs[user_id], source=start_node[0],
                                   weight='weight')
    result = ''
    for node in sssp.keys():
        result += '{}: {}\n'.format(node, sssp[node])
    return result


def mst(user_id, source=()):
    if user_id not in graphs:
        return "У вас еще нет графа"
    if not weighted[user_id]:
        return "У вас невзвешенный граф"
    if isinstance(graphs[user_id], nx.DiGraph):
        if len(source) != 1:
            return "Вы ввели некорректные данные. Обратитесь к команде help"
        source = source[0]
        graphs[user_id].add_node('Extra_node_for_algo')
        graphs[user_id].add_edge('Extra_node_for_algo', source, weight=-1)
        t = nx.minimum_spanning_arborescence(graphs[user_id], attr='weight')
        t.remove_node('Extra_node_for_algo')
        graphs[user_id].remove_node('Extra_node_for_algo')
    else:
        t = nx.minimum_spanning_tree(graphs[user_id])
    edges = ""
    for edge in t.edges:
        edges += "{} {} {}\n".format(edge[0], edge[1], t[edge[0]][edge[1]][
            'weight'])
    return edges


def draw_mst(user_id, source=()):
    if user_id not in graphs:
        return "У вас еще нет графа"
    if not weighted[user_id]:
        return "У вас невзвешенный граф"
    if isinstance(graphs[user_id], nx.DiGraph):
        if len(source) != 1:
            return "Вы ввели некорректные данные. Обратитесь к команде help"
        source = source[0]
        graphs[user_id].add_node('Extra_node_for_algo')
        graphs[user_id].add_edge('Extra_node_for_algo', source, weight=-1)
        t = nx.minimum_spanning_arborescence(graphs[user_id], attr='weight')
        t.remove_node('Extra_node_for_algo')
        graphs[user_id].remove_node('Extra_node_for_algo')
    else:
        t = nx.minimum_spanning_tree(graphs[user_id])
    edges = ""
    for edge in t.edges:
        edges += "{} {} {}\n".format(edge[0], edge[1], t[edge[0]][edge[1]][
            'weight'])
    pos = nx.spring_layout(t)
    nx.draw(t, pos)
    nx.draw_networkx_labels(t, pos)
    weights = nx.get_edge_attributes(t, 'weight')
    nx.draw_networkx_edge_labels(t, pos, edge_labels=weights)
    plt.savefig('temp.png', dpi=300)
    plt.close()
    return "OK"


def add_edges(user_id, lines):
    if user_id not in graphs:
        return "У вас еще нет графа"
    if weighted[user_id]:
        params_of_edge = 3
    else:
        params_of_edge = 2
    lines[0] = ' '.join(lines[0].split()[1:])
    for line in lines:
        line = line.split()
        if len(line) != params_of_edge:
            return "Вы ввели некорректные данные. Обратитесь к команде help"
        if params_of_edge == 3 and not is_integer(line[2]):
            return "Вы ввели некорректные данные. Обратитесь к команде help"
        if line[0] not in graphs[user_id] or line[1] not in graphs[user_id]:
            return "Таких вершин нет"
        try:
            temp = graphs[user_id][line[0]][line[1]]
            return "Такое ребро уже есть"
        except KeyError:
            pass
    for line in lines:
        line = line.split()
        if params_of_edge == 3:
            graphs[user_id].add_edge(line[0], line[1], weight=int(line[2]))
        else:
            graphs[user_id].add_edge(line[0], line[1])
    return "Готово!"
