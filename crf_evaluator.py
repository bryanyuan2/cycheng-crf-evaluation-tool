"""
CRF++ test result evaluation tool with confusion matrix analysis.
Enhanced for Python 3 with better architecture and unittest support.

Author: bryanyuan2
Email: bryanyuan2@gmail.com
Date: 2013-02-12
Updated: 2025-08-29
"""

from typing import List, Dict, Tuple, Optional
import os
from pathlib import Path


class CRFEvaluator:
    """
    A class for evaluating CRF (Conditional Random Field) test results
    by generating confusion matrices and calculating performance metrics.
    """
    
    def __init__(self, correct_labels: List[str], file_path: Optional[str] = None):
        """
        Initialize the CRF evaluator.
        
        Args:
            correct_labels: List of correct label names
            file_path: Path to the CRF test result file (optional)
        """
        self.correct_labels = correct_labels
        self.delimiter = "\t"
        
        # Initialize data structures
        self._init_data_structures()
        
        # Load data if file path is provided
        if file_path:
            self.load_data_from_file(file_path)
    
    def _init_data_structures(self) -> None:
        """Initialize internal data structures."""
        num_labels = len(self.correct_labels)
        
        # Confusion matrix (flattened 2D array)
        self.confusion_matrix = [0] * (num_labels * num_labels)
        
        # Label mapping for confusion matrix
        self.matrix_label_map = []
        for actual in self.correct_labels:
            for predicted in self.correct_labels:
                self.matrix_label_map.append(f"{actual}_{predicted}")
        
        # Results storage
        self.correct_predictions = []
        self.incorrect_predictions = []
        
        # Metrics
        self.precision_totals = [0] * num_labels
        self.recall_totals = [0] * num_labels
    
    def load_data_from_file(self, file_path: str) -> None:
        """
        Load CRF test results from a file.
        
        Args:
            file_path: Path to the test result file
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file format is invalid
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    self._process_line(line)
                except (IndexError, ValueError) as e:
                    raise ValueError(f"Invalid format at line {line_num}: {line}") from e
    
    def _process_line(self, line: str) -> None:
        """
        Process a single line from the CRF test result file.
        
        Args:
            line: A line from the test result file
        """
        data = line.split(self.delimiter)
        if len(data) < 2:
            raise ValueError("Line must contain at least 2 tab-separated columns")
        
        actual_label = data[-2]
        predicted_label = data[-1]
        
        # Store predictions
        if actual_label == predicted_label:
            self.correct_predictions.append(line)
        else:
            self.incorrect_predictions.append(line)
        
        # Update confusion matrix
        self._update_confusion_matrix(actual_label, predicted_label)
    
    def _update_confusion_matrix(self, actual: str, predicted: str) -> None:
        """
        Update the confusion matrix with a prediction.
        
        Args:
            actual: The actual label
            predicted: The predicted label
        """
        label_key = f"{actual}_{predicted}"
        try:
            index = self.matrix_label_map.index(label_key)
            self.confusion_matrix[index] += 1
        except ValueError:
            # Label not in our expected labels - could log this as warning
            pass
    
    def calculate_metrics(self) -> Dict[str, Dict[str, float]]:
        """
        Calculate precision, recall, F1-score, and accuracy.
        
        Returns:
            Dictionary containing metrics for each label and overall accuracy
        """
        num_labels = len(self.correct_labels)
        metrics = {}
        
        # Calculate totals for precision and recall
        self._calculate_precision_recall_totals()
        
        total_samples = sum(self.confusion_matrix)
        correct_predictions = 0
        
        for i, label in enumerate(self.correct_labels):
            # Get diagonal element (correct predictions for this label)
            diagonal_index = i * num_labels + i
            true_positives = self.confusion_matrix[diagonal_index]
            correct_predictions += true_positives
            
            # Calculate metrics
            precision = true_positives / self.precision_totals[i] if self.precision_totals[i] > 0 else 0.0
            recall = true_positives / self.recall_totals[i] if self.recall_totals[i] > 0 else 0.0
            f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
            
            metrics[label] = {
                'precision': precision,
                'recall': recall,
                'f1_score': f1_score,
                'true_positives': true_positives,
                'precision_total': self.precision_totals[i],
                'recall_total': self.recall_totals[i]
            }
        
        # Overall accuracy
        accuracy = correct_predictions / total_samples if total_samples > 0 else 0.0
        metrics['overall'] = {
            'accuracy': accuracy,
            'total_samples': total_samples,
            'correct_predictions': correct_predictions
        }
        
        return metrics
    
    def _calculate_precision_recall_totals(self) -> None:
        """Calculate totals needed for precision and recall calculations."""
        num_labels = len(self.correct_labels)
        
        # Reset totals
        self.precision_totals = [0] * num_labels
        self.recall_totals = [0] * num_labels
        
        for i in range(len(self.confusion_matrix)):
            actual_idx = i // num_labels
            predicted_idx = i % num_labels
            count = self.confusion_matrix[i]
            
            # For precision: sum of all predictions for this class
            self.precision_totals[predicted_idx] += count
            # For recall: sum of all actual occurrences of this class
            self.recall_totals[actual_idx] += count
    
    def get_confusion_matrix_2d(self) -> List[List[int]]:
        """
        Get the confusion matrix as a 2D array.
        
        Returns:
            2D list representing the confusion matrix
        """
        num_labels = len(self.correct_labels)
        matrix_2d = []
        
        for i in range(num_labels):
            row = []
            for j in range(num_labels):
                index = i * num_labels + j
                row.append(self.confusion_matrix[index])
            matrix_2d.append(row)
        
        return matrix_2d
    
    def print_confusion_matrix(self) -> None:
        """Print the confusion matrix in a readable format."""
        print("====\nConfusion Matrix\n====")
        
        # Header
        print(f"{self.delimiter}{self.delimiter}", end='')
        for label in self.correct_labels:
            print(f"{label}{self.delimiter}", end='')
        print(" [predicted class]")
        
        # Matrix rows
        matrix_2d = self.get_confusion_matrix_2d()
        for i, (label, row) in enumerate(zip(self.correct_labels, matrix_2d)):
            print(f"{label}{self.delimiter}{self.delimiter}", end='')
            for count in row:
                print(f"{count}{self.delimiter}", end='')
            print("")
        
        print("[actual class]")
    
    def print_metrics(self) -> None:
        """Print precision, recall, F1-score, and accuracy."""
        metrics = self.calculate_metrics()
        
        print("\n====\n(Precision, Recall, F1 score)\n====")
        for label in self.correct_labels:
            if label in metrics:
                m = metrics[label]
                print(f"{label} = ({m['precision']:.6f}, {m['recall']:.6f}, {m['f1_score']:.6f})")
        
        print(f"Accuracy = {metrics['overall']['accuracy']:.6f}")
    
    def save_prediction_analysis(self, correct_file: str = "correct_predictions.txt", 
                                wrong_file: str = "wrong_predictions.txt") -> None:
        """
        Save correct and incorrect predictions to separate files.
        
        Args:
            correct_file: Path for correct predictions file
            wrong_file: Path for incorrect predictions file
        """
        with open(correct_file, 'w', encoding='utf-8') as f:
            for prediction in self.correct_predictions:
                f.write(f"{prediction}\n")
        
        with open(wrong_file, 'w', encoding='utf-8') as f:
            for prediction in self.incorrect_predictions:
                f.write(f"{prediction}\n")
    
    def get_summary_stats(self) -> Dict[str, int]:
        """
        Get summary statistics.
        
        Returns:
            Dictionary with summary statistics
        """
        return {
            'total_predictions': len(self.correct_predictions) + len(self.incorrect_predictions),
            'correct_predictions': len(self.correct_predictions),
            'incorrect_predictions': len(self.incorrect_predictions),
            'num_labels': len(self.correct_labels)
        }
