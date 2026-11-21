import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent

class FrontPageContract(unittest.TestCase):
    def test_renderer_produces_dated_self_contained_svg(self):
        self.assertTrue((ROOT / 'main.py').exists(), 'entrypoint not implemented')
        spec = importlib.util.spec_from_file_location('edition', ROOT / 'main.py')
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        svg = module.compose()
        self.assertIn('20 NOVEMBER 2026', svg)
        self.assertIn('#F4EFE6', svg)
        self.assertNotIn('https://', svg)
        self.assertEqual(svg, module.compose())
        self.assertEqual(svg.count('<g transform='), 9)
        self.assertIn('verification pending', svg)
        self.assertIn('not enacted policy', svg)

    def test_png_validation_rejects_damage(self):
        import main
        png = (ROOT / 'frontpage.png').read_bytes()
        self.assertEqual(main.validate_png(png), (1024, 1024))
        for broken in [png[:-1], b'not png', png[:70] + bytes([png[70] ^ 1]) + png[71:]]:
            with self.assertRaises(ValueError):
                main.validate_png(broken)

if __name__ == '__main__':
    unittest.main()
