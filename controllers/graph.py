import graphviz as gv

dot = gv.Digraph('Árbol de derivación', format='svg')
dot.attr(label='Árbol de derivación', fontcolor='black', fontsize='30', fontname='arial', style='filled', fillcolor='white', rankdir='TB')

def make_graph():
    dot.render('graphs.gv')
    dot.view()