import graphviz as gv

dot = gv.Digraph('Árbol de derivación', format='pdf')
dot.attr(label='Árbol de derivación', fontcolor='black', fontsize='30', fontname='arial', style='filled', fillcolor='white', rankdir='TB')

def make_graph():
    dot.render('graphs')
    dot.view()