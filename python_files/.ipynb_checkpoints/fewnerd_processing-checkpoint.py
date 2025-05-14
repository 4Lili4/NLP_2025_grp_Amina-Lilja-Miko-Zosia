def data_processing(input_path, output_path):
    started=False
    p_data=["-DOCSTART- -X- O O\n", "\n"]
    for line in open(input_path, encoding='utf-8'):
    
        if line=="\n":
            p_data.append(line)
            continue
            
        token, tag=line.split("\t")
        
        if tag=="O\n" or tag=="O":
            line=token+" _ _ O\n"
            started=False
        
        elif tag.startswith("art") or tag.startswith("product") or tag.startswith("event"):
            line=token+" _ _ O\n"
            started=False
            
        elif tag.startswith("building") or tag.startswith("location"):
            if started==False:
                line=token+" _ _ B-LOC\n"
                started=True
                
            else:
                line=token+" _ _ I-LOC\n"
            
        elif tag.startswith("organization"):
            if started==False:
                line=token+" _ _ B-ORG\n"
                started=True
                
            else:
                line=token+" _ _ I-ORG\n"
                
        elif tag.startswith("person"):
            if started==False:
                line=token+" _ _ B-PER\n"
                started=True
            else:
                line=token+" _ _ I-PER\n"
                
        elif tag.startswith("other"):
            if tag=="other-god":
                if started==False:
                    line=token+" _ _ B-PER\n"
                    started=True
                else:
                    line=token+" _ _ I-PER\n"
            else:
                line=token+" _ _ O\n"
                started=False
                
        else:
            print("Problematic input, see details")
            print(line)
            print(token, tag)
        p_data.append(line)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("".join(p_data))