import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import numpy as np

def plotting_wikiann(results, silver, gold_a, gold_b, colours):
    c1, c2 = colours
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

    ticks=[0,1,2,3,4,5,6]
    
    labels=["No ent (O)", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC"]

    comparison_df.plot(kind='bar', figsize=(6,4), width=0.8,
                      title="Class distribution of gold vs silver data",
                      xlabel="Class label", xticks=ticks, ylabel="Count", grid=True, cmap=c1)
    plt.xticks(ticks=[0,1,2,3,4,5,6], labels=["No ent (O)", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC"])
    plt.savefig("data-files_and_results/class_distribution.png", bbox_inches = "tight")

    #ax.xticks(rotation=45)
    #ax.grid(axis='y', linestyle='--', alpha=0.7)
    #ax.tight_layout()
    #ax.savefig("class_distribution.png", dpi=300)
    
    # Get consistent set of labels
    conf_labels = sorted(set(y_true) | set(y_pred))
    
    # Now safely compute and display the confusion matrix
    cm = confusion_matrix(y_true, y_pred, labels=conf_labels)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(xticks_rotation=45, cmap=c2)
             #title="Confusion Matrix: Silver vs Gold")
