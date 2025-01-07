#Aplikacja do predykcji rozpuszczalności związków chemicznych

import streamlit as st
import pandas as pd
from sklearn.svm import SVR
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem import Crippen
from rdkit import RDLogger
from rdkit.Chem import Draw
from sklearn.preprocessing import StandardScaler
from PIL import Image
RDLogger.DisableLog('rdApp.*') # Disabling rdkit warnings
import pickle

svr = SVR()

with open(r'C:\Users\kacpe\Desktop\folder\Studia\III rok\podstawy uczenia maszynowego\pum-24\model.pkl', 'rb') as f:
    model = pickle.load(f)

class Featurizer:
    def __init__(self, train):
        scaler = StandardScaler()
        tdf = pd.DataFrame()
        tdf['SMILES'] = train
        tdf['mol'] = tdf['SMILES'].apply(Chem.MolFromSmiles)
        # Now we can calculate the molecular descriptors
        tdf['mol_wt'] = tdf['mol'].apply(rdMolDescriptors.CalcExactMolWt)  # Molecular weight
        tdf['logp'] = tdf['mol'].apply(Crippen.MolLogP)  # LogP (lipophilicity)
        tdf['num_heavy_atoms'] = tdf['mol'].apply(rdMolDescriptors.CalcNumHeavyAtoms)  # Number of heavy atoms
        tdf['num_HBD'] = tdf['mol'].apply(rdMolDescriptors.CalcNumHBD)  # Number of hydrogen bond donors
        tdf['num_HBA'] = tdf['mol'].apply(rdMolDescriptors.CalcNumHBA)  # Number of hydrogen bond acceptors
        tdf['aromatic_rings'] = tdf['mol'].apply(rdMolDescriptors.CalcNumAromaticRings)  # Number of aromatic rings
        relevant_col = ['mol_wt', 'logp', 'num_heavy_atoms', 'num_HBD', 'num_HBA', 'aromatic_rings']
        tdf = tdf[relevant_col]
        self.train_df = tdf
        self.scaler = scaler.fit(tdf)

    def featurize(self, smiles):
        df = pd.DataFrame()
        df['SMILES'] = smiles
        df['mol'] = df['SMILES'].apply(Chem.MolFromSmiles)
        # Now we can calculate the molecular descriptors
        df['mol_wt'] = df['mol'].apply(rdMolDescriptors.CalcExactMolWt)  # Molecular weight
        df['logp'] = df['mol'].apply(Crippen.MolLogP)  # LogP (lipophilicity)
        df['num_heavy_atoms'] = df['mol'].apply(rdMolDescriptors.CalcNumHeavyAtoms)  # Number of heavy atoms
        df['num_HBD'] = df['mol'].apply(rdMolDescriptors.CalcNumHBD)  # Number of hydrogen bond donors
        df['num_HBA'] = df['mol'].apply(rdMolDescriptors.CalcNumHBA)  # Number of hydrogen bond acceptors
        df['aromatic_rings'] = df['mol'].apply(rdMolDescriptors.CalcNumAromaticRings)  # Number of aromatic rings
        relevant_col = ['mol_wt', 'logp', 'num_heavy_atoms', 'num_HBD', 'num_HBA', 'aromatic_rings']
        df = df[relevant_col]
        dft = self.scaler.transform(df)
        data_scaled = pd.DataFrame(dft, index=df.index, columns=df.columns)
        return data_scaled




with open(r'C:\Users\kacpe\Desktop\folder\Studia\III rok\podstawy uczenia maszynowego\pum-24\featurizer.pkl', 'rb') as q:
    featurizer = pickle.load(q)







st.title("Solubility predictor")
# image = Image.open('obrazek.jpg')
# st.image(image)
inp = st.text_input('👇 Type SMILES:')

some_SMILES = [inp]

result = st.button('Click')
if result:
     mol = Chem.MolFromSmiles(str(some_SMILES[0]))
     if mol is not None:
        vals = featurizer.featurize(some_SMILES)
        pred = model.predict(vals)
        st.write(f'Predicted value: {10**pred[0]} mol/L')
        img = Draw.MolToImage(mol)
        st.image(img)
     else:
        st.write('Invalid input')






