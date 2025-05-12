def read_from_hf_and_save_to_pkl(link, save_as, subset_size):
    splits = {'validation': 'en/validation-00000-of-00001.parquet', 'test': 'en/test-00000-of-00001.parquet', 'train': 'en/train-00000-of-00001.parquet'}
    train = pd.read_parquet(link + splits["train"])
    
    interval=len(train)/subset_size
    subset=train[train.index % interval == 0].copy()
    
    subset=subset[['tokens', 'ner_tags']]
    with open('subset_of_wikiann.pkl', 'wb') as f:
        dill.dump(subset, f)


def divide_and_conquer(pkl_link, grp_mmbrs):
    
    with open(pkl_link, 'rb') as f:
        silver_data=dill.load(f)
    sentences=[]
    
    for index, row in silver_data.iterrows():
        sent=" ".join(row['tokens'])
        sent="# New sentence = "+sent
        sentences.append(sent)
        
    expanded=silver_data.copy()
    for i, sentence in reversed(list(enumerate(sentences))):
        line=pd.DataFrame({'tokens':sentence, 'ner_tags':[0], 'langs':['en'], 'spans':['']})
        expanded=pd.concat([expanded.iloc[:i], line, expanded.iloc[i:]]).reset_index(drop=True)
    
    A=expanded[0:1000]
    B=expanded[1000:2000]
    C=expanded[2000:3000]
    D=expanded[3000:4000]
    
    Am=pd.concat([A, D])
    Amina=Am.explode('tokens')
    Amina['labels']=0
    Amina=Amina[['tokens', 'labels']]

    Li=pd.concat([A,B])
    Lilja=Li.explode('tokens')
    Lilja['labels']=0
    Lilja=Lilja[['tokens', 'labels']]

    Mi=pd.concat([B,C])
    Miko=Mi.explode('tokens')
    Miko['labels']=0
    Miko=Miko[['tokens', 'labels']]
    
    Zo=pd.concat([C,D])
    Zosia=Zo.explode('tokens')
    Zosia['labels']=0
    Zosia=Zosia[['tokens', 'labels']]
    
    return silver_data













    