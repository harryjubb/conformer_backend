import json
from io import StringIO

from channels.generic.websocket import WebsocketConsumer
from rdkit import Chem
from rdkit.Chem import AllChem


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
        except:
            return

        try:
            original_mol_file_string = text_data_json['molfile']
        except:
            return

        try:
            mol = Chem.MolFromMolBlock(original_mol_file_string)
        except:
            return
        try:
            mol2 = Chem.AddHs(mol)
        except:
            return
        try:
            _ = AllChem.EmbedMolecule(mol2, AllChem.ETKDG())
        except:
            return

        try:
            new_mol_file_string = Chem.MolToPDBBlock(mol2)
        except:
            return

        try:
            self.send(text_data=json.dumps({
                'conformerMolfile': new_mol_file_string
            }))
        except:
            return
