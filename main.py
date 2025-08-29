#!/usr/bin/env python3
"""
Main script for CRF evaluation tool.
"""

from crf_evaluator import CRFEvaluator


def main():
    """Main function to run CRF evaluation."""
    # Configuration
    correct_labels = ["I-NP", "B-NP", "B-ADJP", "I-ADJP"]
    test_file = "sample/sample_crf_output"
    
    try:
        # Create evaluator and load data
        evaluator = CRFEvaluator(correct_labels, test_file)
        
        # Print results
        evaluator.print_confusion_matrix()
        evaluator.print_metrics()
        
        # Optional: Save prediction analysis
        # evaluator.save_prediction_analysis()
        
        # Print summary
        stats = evaluator.get_summary_stats()
        print(f"\nSummary: {stats['correct_predictions']}/{stats['total_predictions']} correct predictions")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please make sure the test file exists.")
    except ValueError as e:
        print(f"Error: {e}")
        print("Please check the file format.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
