from sklearn.metrics import f1_score, precision_score, recall_score
from collections import Counter

def calculate_accuracy(labels1, labels2):
    total_tokens = len(labels1)
    correct_tokens = sum(1 for label1, label2 in zip(labels1, labels2) if label1 == label2)
    accuracy = correct_tokens / total_tokens
    return accuracy

def calculate_accuracy2(predictions, references):
    correct = sum(p == r for p, r in zip(predictions, references))
    return correct / len(predictions)

def cohen_kappa(annotation1, annotation2):
    #how much of each annotation
    count1 = Counter(annotation1)
    count2 = Counter(annotation2)
    
    # Observed agreement (P_o)
    observed_agreement = sum((a == b) for a, b in zip(annotation1, annotation2)) / len(annotation1)
    
    # Expected agreement (P_e)
    total = len(annotation1)
    categories = set(annotation1).union(set(annotation2)) # categories that appear in either of annotations
    expected_agreement = 0
    
    for category in categories:
        p1 = count1.get(category, 0) / total
        p2 = count2.get(category, 0) / total
        expected_agreement += p1 * p2
    
    # Cohen's Kappa calculation
    kappa = (observed_agreement - expected_agreement) / (1 - expected_agreement) #from the formula
    return kappa

def classify_error(silver, label1, label2):
    try:
        silver = int(silver)
        label1 = int(label1)
        label2 = int(label2)
    except ValueError:
        return "Invalid label"

    def get_type(label):
        if label in [1, 2]:
            return "PER"
        elif label in [3, 4]:
            return "ORG"
        elif label in [5, 6]:
            return "LOC"
        else:
            return "O"

    silver_type = get_type(silver)
    gold1_type = get_type(label1)
    gold2_type = get_type(label2)

    if silver == label1 or silver == label2:
        return "Correct"
    if silver_type == "O" and (gold1_type != "O" or gold2_type != "O"):
        return "Critical: Missed entity"
    if silver_type != "O" and gold1_type == "O" and gold2_type == "O":
        return "Critical: False positive"
    if silver_type == "PER" and (gold1_type in {"ORG", "LOC"} or gold2_type in {"ORG", "LOC"}):
        return "Critical: PER↔ORG/LOC confusion"
    if silver_type in {"ORG", "LOC"} and (gold1_type == "PER" or gold2_type == "PER"):
        return "Critical: ORG/LOC↔PER confusion"
    return "Non-critical: Subtype or disagreement"
    

def inter_annotator(results_csv):
    results=pd.read_csv(results_csv, sep=';', encoding='utf-8')
    results=results.fillna('0')
    results['labels1']=results['labels1'].astype(int)
    results['labels2']=results['labels2'].astype(int)
    results['labels1']=results['labels1'].astype(str)
    results['labels2']=results['labels2'].astype(str)

    sentence=''
    YAY=0
    FALSEPOSNEG=0
    ORGLOCERR=0
    LOCSPLITERR=0
    locspliterrlist=[]
    OTHERERR=0
    weird_results=[]
    annotator1_results=[]
    annotator2_results=[]
    
    location=False
    for index, row in results.iterrows():
        
        token=row.iloc[0]
        label1=row.iloc[1]
        label2=row.iloc[2]
        
        if token[0]=='#':
            sentence=token[17:]
            continue
        annotator1_results.append(label1)
        annotator2_results.append(label2)
        
        if label1 == label2:
            YAY +=1
            
        else:
            if ( ( label1 in ['3','4'] ) and (label2 in ['5','6'] ) ) or ( ( label2 in ['3','4'] ) and (label1 in ['5','6'] ) ):
                ORGLOCERR+=1
    
            elif label1=='5' or label2=='5':
                location=True
                if label1=='0' or label2=='0':
                    FALSEPOSNEG+=1
                    continue
                    
            elif ( label1=='0' and label2 in ['5','6'] ) or ( label2=='0' and label1 in ['5','6'] ) or (label1 in ['5', '6'] and label2 in ['5', '6']):
                LOCSPLITERR+=1
                locspliterrlist.append((sentence, token, label1, label2))
    
            elif label1=='0' or label2=='0':
                FALSEPOSNEG+=1
            else:
                OTHERERR+=1
                weird_results.append((sentence, token, label1, label2))

    accuracy = calculate_accuracy(annotator1_results, annotator2_results)
    kappa = cohen_kappa(annotator1_results, annotator2_results)

    y_true= [ int(tag) for tag in annotator1_results]
    y_pred = [int(tag) for tag in annotator2_results]
    
    print("_____________First just some numbers_____________")
    print("Correct results: ", YAY)
    print("False positives or negatives: ", FALSEPOSNEG)
    print("Disagreements of organisation or location: ", ORGLOCERR)
    print("Location-splitting errors: ", LOCSPLITERR)
    print("Nr of other unidentified errors: ", OTHERERR)
    print("_________________________________________________\n")
    print("_____________Now, performance metrics_____________")
    print("Accuracy:", accuracy)
    print("Cohen's Kappa: ", kappa)
    print("\nMacro F1 (Annotator1 vs Annotator2):", f1_score(y_true, y_pred, average='macro'))
    print("Micro F1 (Annotator1 vs Annotator2):", f1_score(y_true, y_pred, average='micro'))
    print("Weighted F1 (Annotator1 vs Annotator2):", f1_score(y_true, y_pred, average='weighted'))
    print("Per-class F1 (Annotator1 vs Annotator2):", f1_score(y_true, y_pred, average=None))
    
    return annotator1_results, annotator2_results


def silver_data_metrics(gold_a, gold_b, silver_data):

    if not (len(silver_data_list) == len(annotator1_results) == len(annotator2_results)):
        print("⚠️ Warning: Your lists are not the same length.")
        print(f"silver: {len(silver)}, annotator1: {len(gold_a)}, annotator2: {len(gold_b)}")
        
    silver=[]
    for index, row in silver_data.iterrows():
        tokens=row.iloc[0]
        tags=row.iloc[1]
        for token, tag in zip(tokens, tags):
            tag=str(tag)
            silver_data_list.append(tag)

    y_true_relaxed = []
    y_pred_relaxed = []
     
    for i, pred in enumerate(silver):
        if pred == gold_a[i] or pred == gold_b[i]:
            y_true_relaxed.append(pred)  # it's a match, count it as correct
            y_pred_relaxed.append(pred)
        else:
            y_true_relaxed.append(gold_a[i])  # mark mismatch with one of the annotators
            y_pred_relaxed.append(pred)
            
    accuracy = calculate_accuracy2(silver_data_list, annotator1_results)

    # Calculate Cohen's Kappa
    kappa1 = cohen_kappa(silver, gold_a)
    kappa2 = cohen_kappa(silver, gold_b)
    kappa_avg = (kappa1+kappa2)/2
    print(f"Cohen's Kappa between our annotation and the silver data: {kappa_avg}")
    
    print("_____________accuracy, precision, recall_____________")
    print(f"Accuracy: {accuracy:.4f}")
    print("Precision (macro):", precision_score(y_true_relaxed, y_pred_relaxed, average='macro'))
    print("Recall (macro):", recall_score(y_true_relaxed, y_pred_relaxed, average='macro'))
    print("_____________________________________________________\n")
    print("_____________F1-score 4 different ways_______________")
    print("Macro F1:", f1_score(y_true_relaxed, y_pred_relaxed, average='macro'))
    print("Micro F1:", f1_score(y_true_relaxed, y_pred_relaxed, average='micro')) # good for imbalanced classes
    print("Weighted F1:", f1_score(y_true_relaxed, y_pred_relaxed, average='weighted'))
    print("Per-class F1:", f1_score(y_true_relaxed, y_pred_relaxed, average=None))
    
    # Count and track examples
    error_counts = Counter()
    example_errors = {}
    
    silver_data_index = 0
    
    for index, row in results.iterrows():
        token = row.iloc[0]
    
        if isinstance(token, str) and token.strip().startswith("#"):
            continue
    
        label1 = row.iloc[1]
        label2 = row.iloc[2]
    
        if silver_data_index >= len(silver_data_list):
            break
    
        silver_label = silver_data_list[silver_data_index]
        error_type = classify_error(silver_label, label1, label2)
    
        error_counts[error_type] += 1
    
        if error_type != "Correct" and error_type not in example_errors:
            example_errors[error_type] = {
                "Index": index,
                "Token": token,
                "Silver": silver_label,
                "Annotator1": label1,
                "Annotator2": label2
            }
    
        silver_data_index += 1
    
    # Print summary
    print("\n--- Error Type Counts ---")
    for etype, count in error_counts.items():
        print(f"{etype}: {count}")
    
    print("\n--- One Example per Error Type ---")
    for etype, example in example_errors.items():
        print(f"\n{etype}")
        print(f"Index: {example['Index']}")
        print(f"Token: {example['Token']}")
        print(f"Silver: {example['Silver']} | Annotator1: {example['Annotator1']} | Annotator2: {example['Annotator2']}")










