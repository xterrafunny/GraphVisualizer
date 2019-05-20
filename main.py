from telegram.ext import Updater, CommandHandler
import graphs

with open('token', 'r') as file:
    TOKEN = file.readline()


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


def start(bot, update):
    """
    Answer to "/start"
    """
    update.message.reply_text("Привет, я визуализатор графов")


def add_node(bot, update):
    """
    Adds node to graph 1936
    """
    user_id = update.message.from_user.id
    node_names = update.message.text.split()[1:]
    update.message.reply_text(graphs.add_node(user_id, node_names))


def new_graph(bot, update):
    """
    Creates new graph
    """
    graph = update.message.text.split()[1:]
    user_id = update.message.from_user.id
    update.message.reply_text(graphs.create_graph(user_id, graph))


def show_nodes(bot, update):
    """
    Sends all nodes from graph
    """
    user_id = update.message.from_user.id
    update.message.reply_text(graphs.show_nodes(user_id))


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
    graphs.delete_graph(user_id)
    update.message.reply_text("Готово!")


def show_edges(bot, update):
    """
    Sends all edges from graph
    """
    user_id = update.message.from_user.id
    update.message.reply_text(graphs.show_edges(user_id))


def update_edge(bot, update):
    """
    Updates weight of edge in graph or creates one
    """
    user_id = update.message.from_user.id
    edge = update.message.text.split()[1:]
    update.message.reply_text(graphs.update_edge(user_id, edge))


def draw_graph(bot, update):
    """
    Sends picture with current graph
    """
    user_id = update.message.from_user.id
    ans = graphs.draw_graph(user_id)
    if ans != "OK":
        update.message.reply_text(ans)
    update.message.reply_photo(photo=open('temp.png', 'rb'))


def delete_node(bot, update):
    """
    Deletes node from graph
    """
    user_id = update.message.from_user.id
    node_names = update.message.text.split()[1:]
    update.message.reply_text(graphs.delete_node(user_id, node_names))


def sssp(bot, update):
    """
    Applies Dijkstra or Ford-Bellman algorithm for this graph
    """
    user_id = update.message.from_user.id
    start_node = update.message.text.split()[1:]
    update.message.reply_text(graphs.dijkstra(user_id, start_node))


def mst(bot, update):
    user_id = update.message.from_user.id
    source = update.message.text.split()[1:]
    update.message.reply_text(graphs.mst(user_id, source))


def mst_draw(bot, update):
    user_id = update.message.from_user.id
    source = update.message.text.split()[1:]
    ans = graphs.draw_mst(user_id, source)
    if ans != "OK":
        update.message.reply_text(ans)
        return
    update.message.reply_photo(photo=open('temp.png', 'rb'))


def add_edge(bot, update):
    user_id = update.message.from_user.id
    lines = update.message.text.split('\n')
    update.message.reply_text(graphs.add_edges(user_id, lines))


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
