from telegram.ext import Updater, CommandHandler
import networkx as nx
import matplotlib.pyplot as plt

with open('token', 'r') as file:
    TOKEN = file.readline()

graphs = {}
weighted = {}
help_text = ('/graph <directed> <weighted> - создать новый граф, оба '
             'аргумента должны быть числами 0 или 1\n/add_node(/an) '
             '<node_name1> <node_name2> ... - добавить в граф вершины с '
             'названиями node_name1, node_name2 ...\n/show_nodes - вывести все '
             'вершины графа\n/delete_graph - удалить граф\n/add_edge(/ae) '
             '<from> <to> (<weight>) - создать ребро из from в to (веса weight)'
             '\n/show_edges - вывести все ребра в графе\n/update_edge(/ue)'
             ' <from> <to> <weight> - обновить вес ребра или добавить такое '
             'ребро, если его не было\n/draw_graph - нарисовать граф\n'
             '/delete_node <node_name1> <node_name2>,... - удалить вершины '
             'node_name1, node_name2, ...\n/algo - справка про алгоритмы')
algorithms_text = ('/sssp <source> - найти кратчайшие расстояния от данной '
                   'вершины до всех достижимых\n/mst_edges (<source>) - найти'
                   ' ребра, входящие в MST(из вершины source для '
                   'ориентированного графа)\n/mst_draw (<source>) - '
                   'нарисовать MST данного графа(из вершины source для '
                   'ориентированного графа)')


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


def start(bot, update):
    """
    Answer to "/start"
    """
    update.message.reply_text("Привет, я визуализатор графов")


def add_node(bot, update):
    """
    Adds node to graph
    """
    user_id = update.message.from_user.id
    node_names = update.message.text.split()[1:]
    if len(node_names) > 100000:
        update.message.reply_text("Вы пытаетесь добавить слишком много вершин")
        return
    if user_id not in graphs:
        update.message.reply_text("У вас еще нет графа")
        return
    for node_name in node_names:
        if node_name in graphs[user_id].nodes:
            update.message.reply_text("В графе уже есть одна из этих вершин")
            return
    for node_name in node_names:
        graphs[user_id].add_node(node_name)
    update.message.reply_text("Готово!")


def new_graph(bot, update):
    """
    Creates new graph
    """
    graph = update.message.text.split()[1:]
    user_id = update.message.from_user.id
    correct = True
    for i in range(len(graph)):
        if i > 2 or not is_0_or_1(graph[i]):
            correct = False
            break
        graph[i] = int(graph[i])
    if not correct:
        update.message.reply_text(
            "Вы ввели некорректные данные. Обратитесь к команде help")
        return
    if graph[0] == 0:
        graphs[user_id] = nx.Graph()
    else:
        graphs[user_id] = nx.DiGraph()
    weighted[user_id] = bool(graph[1])
    update.message.reply_text("Готово!")


def show_nodes(bot, update):
    """
    Sends all nodes from graph
    """
    user_id = update.message.from_user.id
    if user_id not in graphs:
        update.message.reply_text("У вас еще нет графа")
        return
    nodes = ""
    for node in graphs[user_id].nodes:
        nodes += "{} ".format(node)
    update.message.reply_text(nodes)


def help_func(bot, update):
    """
    Answer to "/help" command
    """
    update.message.reply_text(help_text)


def delete_graph(bot, update):
    """
    Deletes graph
    """
    user_id = update.message.from_user.id
    if user_id in graphs:
        graphs.pop(user_id)
        weighted.pop(user_id)
    update.message.reply_text("Готово!")


def show_edges(bot, update):
    """
    Sends all edges from graph
    """
    user_id = update.message.from_user.id
    if user_id not in graphs:
        update.message.reply_text("У вас еще нет графа")
        return
    if weighted[user_id]:
        edges = ""
        for edge in graphs[user_id].edges:
            edges += "{} {} {}\n".format(edge[0], edge[1], graphs[user_id][
                edge[0]][edge[1]]['weight'])
    else:
        edges = ""
        for edge in graphs[user_id].edges:
            edges += "{} {}\n".format(edge[0], edge[1])
    update.message.reply_text(edges)


def update_edge(bot, update):
    """
    Updates weight of edge in graph or creates one
    """
    user_id = update.message.from_user.id
    if user_id not in graphs:
        update.message.reply_text("У вас еще нет графа")
        return
    edge = update.message.text.split()[1:]
    if weighted[user_id]:
        if len(edge) != 3 or not is_integer(edge[2]):
            update.message.reply_text(
                "Вы ввели некорректные данные. Обратитесь к команде help")
            return
        if edge[0] not in graphs[user_id] or edge[1] not in graphs[user_id]:
            update.message.reply_text("Таких вершин нет")
            return
        try:
            graphs[user_id][edge[0]][edge[1]]['weight'] = int(edge[2])
            update.message.reply_text("Вес ребра изменён")
        except KeyError:
            graphs[user_id].add_edge(edge[0], edge[1], weight=int(edge[2]))
            update.message.reply_text("Ребро добавлено")
    else:
        update.message.reply_text("У вас невзвешенный граф")


def draw_graph(bot, update):
    """
    Sends picture with current graph
    """
    user_id = update.message.from_user.id
    if user_id not in graphs:
        update.message.reply_text("У вас еще нет графа")
        return
    pos = nx.spring_layout(graphs[user_id])
    nx.draw(graphs[user_id], pos)
    nx.draw_networkx_labels(graphs[user_id], pos)
    weights = nx.get_edge_attributes(graphs[user_id], 'weight')
    nx.draw_networkx_edge_labels(graphs[user_id], pos, edge_labels=weights)
    plt.savefig('temp.png', dpi=300)
    plt.close()
    update.message.reply_photo(photo=open('temp.png', 'rb'))


def delete_node(bot, update):
    """
    Deletes node from graph
    """
    user_id = update.message.from_user.id
    if user_id not in graphs:
        update.message.reply_text("У вас еще нет графа")
        return
    node_names = update.message.text.split()[1:]
    for node_name in node_names:
        if node_name not in graphs[user_id]:
            update.message.reply_text("Одной из вершин нет в графе")
            return
    for node_name in node_names:
        graphs[user_id].remove_node(node_name)
    update.message.reply_text("Готово!")


def sssp(bot, update):
    """
    Applies Dijkstra or Ford-Bellman algorithm for this graph
    """
    user_id = update.message.from_user.id
    if user_id not in graphs:
        update.message.reply_text("У вас еще нет графа")
        return
    start_node = update.message.text.split()[1:]
    if len(start_node) != 1:
        update.message.reply_text(
            "Вы ввели некорректные данные. Обратитесь к команде help")
        return
    if start_node[0] not in graphs[user_id].nodes:
        update.message.reply_text("Такой вершины нет в графе")
        return
    sssp = nx.shortest_path_length(graphs[user_id], source=start_node[0],
                                   weight='weight')
    result = ''
    for node in sssp.keys():
        result += '{}: {}\n'.format(node, sssp[node])
    update.message.reply_text(result)


def mst(bot, update):
    user_id = update.message.from_user.id
    if user_id not in graphs:
        update.message.reply_text("У вас еще нет графа")
        return
    if not weighted[user_id]:
        update.message.reply_text("У вас невзвешенный граф")
        return
    if isinstance(graphs[user_id], nx.DiGraph):
        source = update.message.text.split()[1:]
        if len(source) != 1:
            update.message.reply_text(
                "Вы ввели некорректные данные. Обратитесь к команде help")
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
    update.message.reply_text(edges)


def mst_draw(bot, update):
    user_id = update.message.from_user.id
    if user_id not in graphs:
        update.message.reply_text("У вас еще нет графа")
        return
    if not weighted[user_id]:
        update.message.reply_text("У вас невзвешенный граф")
        return
    if isinstance(graphs[user_id], nx.DiGraph):
        source = update.message.text.split()[1:]
        if len(source) != 1:
            update.message.reply_text(
                "Вы ввели некорректные данные. Обратитесь к команде help")
            return
        source = source[0]
        graphs[user_id].add_node('Extra_node_for_algo')
        graphs[user_id].add_edge('Extra_node_for_algo', source, weight=-1)
        t = nx.minimum_spanning_arborescence(graphs[user_id], attr='weight')
        t.remove_node('Extra_node_for_algo')
        graphs[user_id].remove_node('Extra_node_for_algo')
    else:
        t = nx.minimum_spanning_tree(graphs[user_id])
    pos = nx.spring_layout(t)
    nx.draw(t, pos)
    nx.draw_networkx_labels(t, pos)
    weights = nx.get_edge_attributes(t, 'weight')
    nx.draw_networkx_edge_labels(t, pos, edge_labels=weights)
    plt.savefig('temp.png', dpi=300)
    plt.close()
    update.message.reply_photo(photo=open('temp.png', 'rb'))



def add_edge(bot, update):
    user_id = update.message.from_user.id
    if user_id not in graphs:
        update.message.reply_text("У вас еще нет графа")
        return
    lines = update.message.text.split('\n')
    if weighted[user_id]:
        params_of_edge = 3
    else:
        params_of_edge = 2
    lines[0] = ' '.join(lines[0].split()[1:])
    for line in lines:
        line = line.split()
        if len(line) != params_of_edge:
            update.message.reply_text(
                "Вы ввели некорректные данные. Обратитесь к команде help")
            return
        if params_of_edge == 3 and not is_integer(line[2]):
            update.message.reply_text(
                "Вы ввели некорректные данные. Обратитесь к команде help")
            return
        if line[0] not in graphs[user_id] or line[1] not in graphs[user_id]:
            update.message.reply_text("Таких вершин нет")
            return
        try:
            temp = graphs[user_id][line[0]][line[1]]
            update.message.reply_text("Такое ребро уже есть")
            return
        except KeyError:
            pass
    for line in lines:
        line = line.split()
        if params_of_edge == 3:
            graphs[user_id].add_edge(line[0], line[1], weight=int(line[2]))
        else:
            graphs[user_id].add_edge(line[0], line[1])
    update.message.reply_text("Готово!")


def algo_help(bot, update):
    update.message.reply_text(algorithms_text)


updater = Updater(TOKEN)

updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("add_node", add_node))
updater.dispatcher.add_handler(CommandHandler("help", help_func))
updater.dispatcher.add_handler(CommandHandler("graph", new_graph))
updater.dispatcher.add_handler(CommandHandler("show_nodes", show_nodes))
updater.dispatcher.add_handler(CommandHandler("delete_graph", delete_graph))
updater.dispatcher.add_handler(CommandHandler("an", add_node))
updater.dispatcher.add_handler(CommandHandler("add_edge", add_edge))
updater.dispatcher.add_handler(CommandHandler("ae", add_edge))
updater.dispatcher.add_handler(CommandHandler("show_edges", show_edges))
updater.dispatcher.add_handler(CommandHandler("update_edge", update_edge))
updater.dispatcher.add_handler(CommandHandler("ue", update_edge))
updater.dispatcher.add_handler(CommandHandler("draw_graph", draw_graph))
updater.dispatcher.add_handler(CommandHandler("delete_node", delete_node))
updater.dispatcher.add_handler(CommandHandler("sssp", sssp))
updater.dispatcher.add_handler(CommandHandler("MST_edges", mst))
updater.dispatcher.add_handler(CommandHandler("MST_draw", mst_draw))
updater.dispatcher.add_handler(CommandHandler("algo", algo_help))

updater.start_polling()
updater.idle()
