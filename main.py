from telegram.ext import Updater, CommandHandler
import networkx as nx
import matplotlib.pyplot as plt
TOKEN = "TOKEN"
graphs = {}
weighted = {}
help_text = '/create_graph <directed> <weighted> - создать новый граф, ' \
            'оба аргумента должны быть числами 0 или 1\n/add_node(/an) ' \
            '<node_name1> <node_name2> ... - добавить в граф вершины с ' \
            'названиями node_name1, node_name2 ...\n/show_nodes - вывести все' \
            ' вершины графа\n/delete_graph - удалить граф\n/add_edge(/ae) ' \
            '<from> <to> (<weight>) - создать ребро из from в to (веса ' \
            'weight)\n/show_edges - вывести все ребра в графе\n/update_edge(' \
            '/ue) <from> <to> <weight> - обновить вес ребра или добавить ' \
            'такое ребро, если его не было\n/draw_graph - нарисовать граф'
algorithms_text = ''


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
        update.message.reply_text("У вас нет графа")
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


def add_edge(bot, update):
    """
    Adds an edge to graph
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
            temp = graphs[user_id][edge[0]][edge[1]]
            update.message.reply_text("Такое ребро уже есть")
        except KeyError:
            graphs[user_id].add_edge(edge[0], edge[1], weight=int(edge[2]))
            update.message.reply_text("Готово!")
    else:
        if len(edge) != 2:
            update.message.reply_text(
                "Вы ввели некорректные данные. Обратитесь к команде help")
            return
        if edge[0] not in graphs[user_id] or edge[1] not in graphs[user_id]:
            update.message.reply_text("Таких вершин нет")
            return
        try:
            temp = graphs[user_id][edge[0]][edge[1]]
            update.message.reply_text("Такое ребро уже есть")
        except KeyError:
            graphs[user_id].add_edge(edge[0], edge[1])
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
            update.message.reply_text("Ребра добавлено")
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


updater = Updater(TOKEN)

updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("add_node", add_node))
updater.dispatcher.add_handler(CommandHandler("help", help_func))
updater.dispatcher.add_handler(CommandHandler("create_graph", new_graph))
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

updater.start_polling()
updater.idle()
