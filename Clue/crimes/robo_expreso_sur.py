"""
robo_expreso_sur.py — El Robo en el Expreso del Sur

El collar de esmeraldas de la Marquesa desapareció del vagón privado del tren nocturno.
Elena fue vista en el vagón privado durante el robo; sus huellas están en el estuche de joyas.
Don Rodrigo fue grabado por la cámara de seguridad en el vagón de equipaje durante toda la noche.
El vagón de equipaje es el extremo opuesto al vagón privado; es imposible haber estado en ambos a la vez.
La Marquesa es la víctima directa del robo y presenció el incidente.
La Marquesa acusa a Elena.
Victor declara que Elena estuvo con él en el vagón comedor toda la noche.
Elena declara que Victor estuvo con ella en el vagón comedor toda la noche.

Como detective, he llegado a las siguientes conclusiones:
Quien fue grabado en cámara en un lugar alejado de la escena durante el crimen está descartado.
La víctima del crimen no tiene razón para mentir; es testigo imparcial.
La acusación de un testigo imparcial es creíble.
Quien estaba en la escena y es acusado de forma creíble es culpable.
Quien da coartada a un culpable lo está defendiendo.
Si dos personas se dan coartada mutuamente, tienen una alianza de coartadas entre sí.
"""

from src.crime_case import CrimeCase, QuerySpec
from src.predicate_logic import ExistsGoal, KnowledgeBase, Predicate, Rule, Term


def crear_kb() -> KnowledgeBase:
    """Construye la KB según la narrativa del módulo."""
    kb = KnowledgeBase()

    # Constantes del caso
    elena          = Term("elena")
    victor         = Term("victor")
    don_rodrigo    = Term("don_rodrigo")
    marquesa       = Term("marquesa")
    estuche_joyas  = Term("estuche_joyas")
    vagon_equipaje = Term("vagon_equipaje")

    # === YOUR CODE HERE ===
    # HECHOS
    kb.add_fact(Predicate("en_escena", (elena,)))
    kb.add_fact(Predicate("huellas", (elena, estuche_joyas)))

    kb.add_fact(Predicate("grabado_en", (don_rodrigo, vagon_equipaje)))
    kb.add_fact(Predicate("lejos_escena", (don_rodrigo,)))

    kb.add_fact(Predicate("victima", (marquesa,)))

    kb.add_fact(Predicate("acusa", (marquesa, elena)))

    kb.add_fact(Predicate("da_coartada", (victor, elena)))
    kb.add_fact(Predicate("da_coartada", (elena, victor)))


    # VARIABLES
    X = Term("$X")
    Y = Term("$Y")
    Z = Term("$Z")


    # REGLAS

    # 1. grabado lejos -> descartado
    kb.add_rule(Rule(
        (Predicate("lejos_escena", (X,)),),
        Predicate("descartado", (X,))
    ))

    # 2. víctima -> testigo imparcial
    kb.add_rule(Rule(
        (Predicate("victima", (X,)),),
        Predicate("testigo_imparcial", (X,))
    ))

    # 3. testigo imparcial + acusa -> acusación creíble
    kb.add_rule(Rule(
        (
            Predicate("testigo_imparcial", (X,)),
            Predicate("acusa", (X, Y))
        ),
        Predicate("acusacion_creible", (X, Y))
    ))

    # 4. en escena + acusación creíble -> culpable
    kb.add_rule(Rule(
        (
            Predicate("en_escena", (X,)),
            Predicate("acusacion_creible", (Y, X))
        ),
        Predicate("culpable", (X,))
    ))

    # 5. da coartada a culpable -> defiende
    kb.add_rule(Rule(
        (
            Predicate("da_coartada", (X, Y)),
            Predicate("culpable", (Y,))
        ),
        Predicate("defiende_al_culpable", (X,))
    ))

    # 6. coartada mutua -> alianza
    kb.add_rule(Rule(
        (
            Predicate("da_coartada", (X, Y)),
            Predicate("da_coartada", (Y, X))
        ),
        Predicate("alianza_coartadas", (X, Y))
    ))
    # === END YOUR CODE ===

    return kb


CASE = CrimeCase(
    id="robo_expreso_sur",
    title="El Robo en el Expreso del Sur",
    suspects=("elena", "victor", "don_rodrigo"),
    narrative=__doc__,
    description=(
        "El collar de la Marquesa desapareció en un tren nocturno. "
        "Don Rodrigo tiene coartada de cámara. Elena estaba en la escena con huellas en el estuche. "
        "La víctima la acusa. Victor y Elena se cubren mutuamente."
    ),
    create_kb=crear_kb,
    queries=(
        QuerySpec(
            description="¿Don Rodrigo está descartado?",
            goal=Predicate("descartado", (Term("don_rodrigo"),)),
        ),
        QuerySpec(
            description="¿La acusación de la Marquesa contra Elena es creíble?",
            goal=Predicate("acusacion_creible", (Term("marquesa"), Term("elena"))),
        ),
        QuerySpec(
            description="¿Elena es culpable?",
            goal=Predicate("culpable", (Term("elena"),)),
        ),
        QuerySpec(
            description="¿Victor defiende al culpable?",
            goal=Predicate("defiende_al_culpable", (Term("victor"),)),
        ),
        QuerySpec(
            description="¿Existe alianza de coartadas entre Elena y Victor?",
            goal=ExistsGoal("$X", Predicate("alianza_coartadas", (Term("$X"), Term("victor")))),
        ),
    ),
)
