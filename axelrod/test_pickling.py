import unittest
import pickle
import axelrod as axl
from axelrod.strategy_transformers import FlipTransformer
from axelrod.my_t import transformed, TestFlip


C, D = axl.Action.C, axl.Action.D


class TestPickle(unittest.TestCase):
    def test_parameterized_player(self):
        p1 = axl.Cooperator()
        p2 = axl.Cycler('DDCCDD')

        p1.play(p2)

        reconstituted_1 = pickle.loads(pickle.dumps(p1))
        reconstituted_2 = pickle.loads(pickle.dumps(p2))

        self.assertEqual(p2, reconstituted_2)

        self.assertEqual(reconstituted_1.clone(), p1.clone())
        self.assertEqual(reconstituted_2.clone(), p2.clone())

    def test_sequence_player(self):
        player = axl.ThueMorse()
        player.play(axl.Cooperator())

        reconstituted = pickle.loads(pickle.dumps(player))
        self.assertEqual(reconstituted, player)

    def test_final_transformer_called(self):
        player = axl.Alexei()
        copy = pickle.loads(pickle.dumps(player))
        match = axl.Match((player, copy), turns=3)
        results = match.play()
        self.assertEqual(results, [(C, C), (C, C), (D, D)])

    def test_all(self):
        for s in axl.strategies:
            player = s()
            player.play(axl.Cooperator())

            reconstituted = pickle.loads(pickle.dumps(player))

            self.assertEqual(reconstituted, player)

    def test_pickling_transformers(self):
        player = transformed[0]()
        print(player.__dict__)
        print(player.__class__.original_class)

        for s in transformed:
            player = s()
            player.play(axl.Cooperator())
            # print(player.name, player.__class__.__name__)
            reconstituted = pickle.loads(pickle.dumps(player))

            self.assertEqual(reconstituted, player)

    def test_created(self):
        x = FlipTransformer()(axl.Cooperator)
        x = FlipTransformer()(x)
        x = FlipTransformer()(x)()
        # print(x.__reduce__())
        # print('created')
        # print(repr(pickle.dumps(x)))
        z = pickle.loads(pickle.dumps(x))
        # print(z)
        # print(z.__dict__)
        self.assertEqual(x, z)

    def test_created_two(self):
        # print('created_two')
        x = TestFlip()
        # print(x.__dict__)
        # print(x.__class__.__dict__)
        # print(x.__class__.__name__)
        # print(x.__dir__())
        z = pickle.dumps(x)
        self.assertEqual(x, pickle.loads(z))

    # def test_reconsitutor(self):
    #     x = TestFlip()
    #     print('reconstructor')
    #     print(x.decorator, x.original_class)
    #     y = Reconstitutor()(x.decorator, x.original_class, x.__class__.__name__)
    #     print(type(y))
    #     y.__dict__.update(x.__dict__)
    #     print(y.name)
    #     print(y.__class__.__name__)
    #     self.assertEqual(y, x)
