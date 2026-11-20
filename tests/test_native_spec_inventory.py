import unittest
from tools.native_spec_inventory import task_inventory, parse_museum, parse_compliance, continuity


class InventoryTests(unittest.TestCase):
    def test_tasks_keep_checked_separate(self):
        self.assertEqual(task_inventory("- [x] T001 Done\n  - [ ] T001a Child\n"),
                         {"T001":"checked_unverified","T001a":"open"})
    def test_duplicate(self):
        with self.assertRaises(ValueError):
            task_inventory("- [x] T001 One\n- [ ] T001 Duplicate")
    def test_unparsed(self):
        with self.assertRaises(ValueError):
            task_inventory("- [ ] no ID")
    def test_nested_lost(self):
        old = {"project":"p","packages":{"a":{"tasks":{"T001":"open","T001a":"open"},"requirements":None}}}
        new = {"project":"p","packages":{"a":{"tasks":{"T001":"open"},"requirements":None}}}
        self.assertEqual(continuity(old,new), ["a/tasks/T001a: missing"])
    def test_package_lost(self):
        old = {"project":"p","packages":{"a":{"tasks":{},"requirements":{}}}}
        self.assertEqual(continuity(old,{"project":"p","packages":{}}), ["a: package disappeared"])
    def test_requirement_lost(self):
        old={"project":"p","packages":{"a":{"tasks":{},"requirements":{"FR-1":"open"}}}}
        new={"project":"p","packages":{"a":{"tasks":{},"requirements":{}}}}
        self.assertEqual(continuity(old,new),["a/requirements/FR-1: missing"])
    def test_compliance_definitions(self):
        self.assertEqual(parse_compliance("- FR-001: A\n- AT-001: B"),["AT-001","FR-001"])
        with self.assertRaises(ValueError):
            parse_compliance("- FR-001: A")
    def test_museum_exact_and_status(self):
        ids=[f"TZ-{i:03d}" for i in range(1,326)]
        registry="ID^Фактически готово\n"+"\n".join(f"{i}^Да" for i in ids)
        spec=" ".join(ids)
        acceptance="\n".join(f"| {i} | P1 | Да | x |" for i in ids)
        self.assertEqual(len(parse_museum(registry,spec,acceptance)),325)
        with self.assertRaises(ValueError):
            parse_museum(registry,spec,acceptance.replace("Да","Нет",1))
        with self.assertRaises(ValueError):
            parse_museum(registry,spec.replace("TZ-325",""),acceptance)
        with self.assertRaises(ValueError):
            parse_museum(registry,spec,acceptance+"\n| TZ-001 | P1 | Да | x |")


if __name__ == "__main__":
    unittest.main()
