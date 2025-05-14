import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import numpy as np

def plotting_wikiann(results, silver, gold_a, gold_b):
    # Count occurrences of each class in gold and silver
    gold_counts = results['labels1'].value_counts().sort_index()
    silver_counts = results['labels2'].value_counts().sort_index()
    
    # Combine into a DataFrame
    comparison_df = pd.DataFrame({
        'Gold': gold_counts,
        'Silver': silver_counts
    }).fillna(0).astype(int)

    # Missed ORG
    missed_org = results[(results['labels1'] == 'ORG') & (results['labels2'] != 'ORG')]
    
    # Hallucinated ORG (predicted ORG where it shouldn't be)
    hallucinated_org =results[(results['labels1'] != 'ORG') & (results['labels2'] == 'ORG')]
    
    # Misclassified ORG (could be either direction)
    misclassified_org = results[(results['labels1'] == 'ORG') & (results['labels2'] != 'ORG')]
    
    # Drop rows with missing labels
    df_clean = results.dropna(subset=['labels1', 'labels2'])
    
    # Extract gold and silver labels
    y_true = df_clean['labels1']
    y_pred = df_clean['labels2']
    
    labels=["No ent (O)", "Per (1)", "Per (2)", "Org (3)", "Org (4)", "Loc (5)", "Loc (6)"]

    comparison_df.plot(kind='bar', figsize=(6,6), width=0.8,
                      title="Class distribution of gold vs silver data",
                      xlabel="Class label", ylabel="Count", grid=True, cmap="Blues")
    

    #ax.xticks(rotation=45)
    #ax.grid(axis='y', linestyle='--', alpha=0.7)
    #ax.tight_layout()
    #ax.savefig("class_distribution.png", dpi=300)
    
    # Get consistent set of labels
    labels = sorted(set(y_true) | set(y_pred))
    
    # Now safely compute and display the confusion matrix
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(xticks_rotation=45, cmap='Blues')
             #title="Confusion Matrix: Silver vs Gold")
