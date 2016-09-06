import unittest
from should_dsl import *
from pdb import pdb


class PdbTest(unittest.TestCase):

    def setUp(self):
        self.pdb = pdb('./nescessary_files/1uij.pdb')
        self.pdb_fail = pdb('./nescessary_files/1uij_fail.pdb')

    def test_if_show_the_name_file_match_using_Nome_function(self):
        self.pdb.Nome() |should| equal_to('./nescessary_files/1uij.pdb')

    def test_if_show_the_name_file_match_using_nomedoarquivo_function(self):
        self.pdb.nomedoarquivo() |should| equal_to('./nescessary_files/1uij.pdb')

    def test_if_show_the_struct_name(self):
        self.pdb.NomedaEstrutura() |should| equal_to('1uij')

    def test_if_show_the_chains(self):
        self.pdb.chains() |should| equal_to(['A', 'B', 'C', 'D', 'E', 'F'])

#    def test_if_not_show_the_chains_if_field_CHAINS_not_found(self):
#        self.pdb_fail.chains() |should| equal_to(['A', 'B', 'C', 'D', 'E', 'F'])

    def test_the_number_of_the_first_line_that_contains_Chain(self):
        self.pdb.PrimeiraLinhaOndeTemEscritoChain() |should| equal_to(5)

    def test_if_the_template_contains_hetatms(self):
        self.pdb.hetatm() |should| equal_to(True)

    def test_if_the_template_not_contains_hetatms(self):
#        self.pdb.hetatm() |should| equal_to(True)
        pass

    def test_if_the_template_contain_HOH(self):
        self.pdb.hoh() |should| equal_to(True)

    def test_if_the_template_not_contain_HOH(self):
        pass

    def test_if_show_the_hetatms_in_PDB(self):
        self.pdb.HetatomsInPDB() |should| equal_to(['HOH'])

    def test_if_not_show_the_hetatms_in_PDB_because_not_have_hetatms(self):
#        self.pdb.HetatomsInPDB() |should| equal_to(['HOH'])
        pass
    def test_if_not_show_the_hetatms_contained_in_chains_because_not_have_hetatms(self):
        pass
    def test_if_show_the_hetatms_contained_in_chains(self):
        self.pdb.HetatomsInChain('F') |should| equal_to(['HOH'])

# parei na linha 68
if __name__ == '__main__':
    unittest.main()

