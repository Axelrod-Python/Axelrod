import axelrod.strategy_transformers as st
import axelrod as axl

C, D = axl.Action.C, axl.Action.D


@st.FlipTransformer()
@st.FlipTransformer()
class TestFlip(axl.Cooperator):
    pass


@st.ApologyTransformer([D], [C])
class Apology(axl.Cooperator):
    pass


@st.DeadlockBreakingTransformer(name_prefix=None)
class DeadlockBreaking(axl.Cooperator):
    pass

@st.DualTransformer(name_prefix=None)
class Dual(axl.Cooperator):
    pass

@st.FlipTransformer(name_prefix=None)
class Flip(axl.Cooperator):
    pass

@st.FinalTransformer((D, D), name_prefix=None)
class Final(axl.Cooperator):
    pass

@st.ForgiverTransformer(0.2, name_prefix=None)
class Forgiver(axl.Cooperator):
    pass

@st.GrudgeTransformer(3, name_prefix=None)
class Grudge(axl.Cooperator):
    pass

@st.InitialTransformer((C, D), name_prefix=None)
class Initial(axl.Cooperator):
    pass

@st.JossAnnTransformer((0.2, 0.2), name_prefix=None)
class JossAnn(axl.Cooperator):
    pass


strategies = [axl.Grudger, axl.TitForTat]
probability = [.2, .3]

@st.MixedTransformer(probability, strategies, name_prefix=None)
class Mixed(axl.Cooperator):
    pass

@st.NiceTransformer(name_prefix=None)
class Nice(axl.Cooperator):
    pass

@st.NoisyTransformer(0.2, name_prefix=None)
class Noisy(axl.Cooperator):
    pass

@st.RetaliationTransformer(3, name_prefix=None)
class Retaliation(axl.Cooperator):
    pass

@st.RetaliateUntilApologyTransformer(name_prefix=None)
class RetaliateUntilApology(axl.Cooperator):
    pass

@st.TrackHistoryTransformer(name_prefix=None)
class TrackHistory(axl.Cooperator):
    pass

transformed = [Apology, DeadlockBreaking, Flip, Final, Forgiver, Grudge,
               Initial, JossAnn, Mixed, Nice, Noisy, Retaliation,
               RetaliateUntilApology, TrackHistory]
fails = [Dual]


