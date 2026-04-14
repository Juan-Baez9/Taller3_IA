"""
model_checking.py

Este modulo contiene las funciones de model checking proposicional.

Hint: Usa las funciones get_atoms() y evaluate() de logic_core.py.
"""

from __future__ import annotations

from src.logic_core import Formula


def get_all_models(atoms: set[str]) -> list[dict[str, bool]]:
    """
    Genera todos los modelos posibles (asignaciones de verdad).
    Para n atomos, genera 2^n modelos.

    Args:
        atoms: Conjunto de nombres de atomos proposicionales.

    Returns:
        Lista de diccionarios, cada uno mapeando atomos a valores booleanos.

    Ejemplo:
        >>> get_all_models({'p', 'q'})
        [{'p': True, 'q': True}, {'p': True, 'q': False},
         {'p': False, 'q': True}, {'p': False, 'q': False}]

    Hint: Piensa en como representar los numeros del 0 al 2^n - 1 en binario.
          Cada bit corresponde al valor de verdad de un atomo.
    """
    # === YOUR CODE HERE ===
# VERSION INICIAL
# def get_all_models(atoms: set[str]) -> list[dict[str, bool]]:
#     atoms = list(atoms)
#     modelos = []
#
#     total_modelos = 2 ** len(atoms)
#
#     for i in range(total_modelos):
#         binario = bin(i)[2:].zfill(len(atoms))
#         modelo = {}
#
#         for j in range(len(atoms)):
#             if binario[j] == '1':
#                 modelo[atoms[j]] = True
#             else:
#                 modelo[atoms[j]] = False
#
#         modelos.append(modelo)
#
#     return modelos
#
# Prompt usado con IA:
# "Hola Chat, necesito que me ayudes a revisar esta version de mi funcion get_all_models.
# quiero saber si tiene errores y como podria mejorarla sin cambiar demasiado la idea original..."


    atom_list = sorted(atoms)
    models = []

    total_models = 2 ** len(atom_list)

    for i in range(total_models):
        binary = bin(i)[2:].zfill(len(atom_list))
        model = {}

        for j, atom in enumerate(atom_list):
            model[atom] = binary[j] == '1'

        models.append(model)

    return models

    # === END YOUR CODE ===


def check_satisfiable(formula: Formula) -> tuple[bool, dict[str, bool] | None]:
    """
    Determina si una formula es satisfacible.

    Args:
        formula: Formula logica a verificar.

    Returns:
        (True, modelo) si encuentra un modelo que la satisface.
        (False, None) si es insatisfacible.

    Ejemplo:
        >>> check_satisfiable(And(Atom('p'), Not(Atom('p'))))
        (False, None)

    Hint: Genera todos los modelos con get_all_models(), luego evalua
          la formula en cada uno usando evaluate().
    """
    # === YOUR CODE HERE ===
    
# VERSION INICIAL
#def check_satisfiable(formula: Formula) -> tuple[bool, dict[str, bool] | None]:
#    atoms = formula.get_atoms()
#    modelos = get_all_models(atoms)
#
#    resultado = False
#    modelo_encontrado = None
#
#    for modelo in modelos:
#        valor = formula.evaluate(modelo)
#        if valor == True and resultado == False:
#            resultado = True
#            modelo_encontrado = modelo

#    return (resultado, modelo_encontrado) 
# 
# Chat hize esta version de la funcion check_satisfiable, quiero que me ayudes a revisarla
# y mejorarla y ver si depronto me falto incluir algo 

    atoms = formula.get_atoms()
    all_models = get_all_models(atoms)

    for model in all_models:
        if formula.evaluate(model):
            return True, model

    return False, None
# # === END YOUR CODE ===


def check_valid(formula: Formula) -> bool:
    """
    Determina si una formula es una tautologia (valida en todo modelo).

    Args:
        formula: Formula logica a verificar.

    Returns:
        True si la formula es verdadera en todos los modelos posibles.

    Ejemplo:
        >>> check_valid(Or(Atom('p'), Not(Atom('p'))))
        True

    Hint: Una formula es valida si y solo si su negacion es insatisfacible.
          Alternativamente, verifica que sea verdadera en TODOS los modelos.
    """
    # === YOUR CODE HERE ===
#
# def check_valid(formula: Formula) -> bool:
#     atoms = formula.get_atoms()
#     modelos = get_all_models(atoms)
#
#     resultado = True
#
#     for modelo in modelos:
#         valor = formula.evaluate(modelo)
#         if valor == False:
#             resultado = False
#
#     return resultado"    
# 
#PROMTP USADO CON IA:
# "Hola Chat, necesito que me ayudes a mejorar y ver si tengo errores en esta version
# de mi funcion check_valid. Necesito que me ayudes a mejorarla y si tiene errores
# que me los digas para mejorar el codigo


    atoms = formula.get_atoms()
    modelos = get_all_models(atoms)

    for modelo in modelos:
        if not formula.evaluate(modelo):
            return False

    return True 
# === END YOUR CODE ===


def check_entailment(kb: list[Formula], query: Formula) -> bool:
    """
    Determina si KB |= query (la base de conocimiento implica la consulta).

    Args:
        kb: Lista de formulas que forman la base de conocimiento.
        query: Formula que queremos verificar si se sigue de la KB.

    Returns:
        True si la query es verdadera en todos los modelos donde la KB es verdadera.

    Ejemplo:
        >>> kb = [Implies(Atom('p'), Atom('q')), Atom('p')]
        >>> check_entailment(kb, Atom('q'))
        True

    Hint: KB |= q  si y solo si  KB ^ ~q es insatisfacible.
          Es decir, no existe un modelo donde toda la KB sea verdadera
          y la query sea falsa.
    """
    # === YOUR CODE HERE ===
#
# def check_entailment(kb: list[Formula], query: Formula) -> bool:
#     atoms = query.get_atoms()
#
#     for formula in kb:
#         atoms = atoms.union(formula.get_atoms())
#
#     modelos = get_all_models(atoms)
#     resultado = True
#
#     for modelo in modelos:
#         kb_verdadera = True
#
#         for formula in kb:
#             if formula.evaluate(modelo) == False:
#                 kb_verdadera = False
#
#         if kb_verdadera == True:
#             if query.evaluate(modelo) == False:
#                 resultado = False
#
#     return resultado"

#PROMTP USADO CON IA:
# Hola chat siento que hay alguna manera de optimizar esta funcion check_entailment, 
# quiero que me ayudes a revisar esta version y mejorarla porfa

    atoms = set()

    for formula in kb:
        atoms.update(formula.get_atoms())
    atoms.update(query.get_atoms())

    models = get_all_models(atoms)

    for model in models:
        if all(formula.evaluate(model) for formula in kb):
            if not query.evaluate(model):
                return False

    return True
# === END YOUR CODE ===


def truth_table(formula: Formula) -> list[tuple[dict[str, bool], bool]]:
    """
    Genera la tabla de verdad completa de una formula.

    Args:
        formula: Formula logica.

    Returns:
        Lista de tuplas (modelo, resultado) para cada modelo posible.

    Ejemplo:
        >>> truth_table(And(Atom('p'), Atom('q')))
        [({'p': True, 'q': True}, True),
         ({'p': True, 'q': False}, False),
         ({'p': False, 'q': True}, False),
         ({'p': False, 'q': False}, False)]

    Hint: Combina get_all_models() y evaluate().
    """
    # === YOUR CODE HERE ===
#
# def truth_table(formula: Formula) -> list[tuple[dict[str, bool], bool]]:
#     atoms = formula.get_atoms()
#     modelos = get_all_models(atoms)
#     tabla = []
#
#     for modelo in modelos:
#         resultado = formula.evaluate(modelo)
#         fila = (modelo, resultado)
#         tabla.append(fila)
#
#     return tabla"    
# 
# Prompt usado con IA:
# "Hola Chat necesito que me ayudes a mejorar esta funcion para ver si puede
# o ser mas optimizada o mejor planteada.
    atoms = formula.get_atoms()
    models = get_all_models(atoms)
    table = []

    for model in models:
        table.append((model, formula.evaluate(model)))

    return table

# === END YOUR CODE ===
