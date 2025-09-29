import json
import argparse
if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Evaluation script for comparing_size task")
    parser.add_argument(
        '--answer', '-a',
        type=str,
        default='answer.json',
        help='Path to the answer JSON file (default: answer.json)'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='eval.json',
        help='Path to the output JSON file (default: eval.json)'
    )
    args = parser.parse_args()
    # Assuming your JSON data is stored in a file called 'results.json'
    with open(args.answer, 'r') as f:
        data = json.load(f)

    # Initialize variables to calculate accuracies
    correct_counts = 0
    total_counts = 0
    category_accuracies = {}

    # Iterate through the JSON data
    for entry in data:
        num_objects = entry['num_objects']
        order = entry['answer']    
        order = int(order)

        total_counts += 1

        # Calculate per-category accuracy
        if num_objects not in category_accuracies:
            category_accuracies[num_objects] = {'correct': 0, 'total': 0}

        category_accuracies[num_objects]['total'] += 1

        try:
            predicted_order = entry['Output']
            predicted_order = int(predicted_order)
        except:
            continue
        

        # Check if the prediction is correct
        if predicted_order == order:
            correct_counts += 1
            category_accuracies[num_objects]['correct'] += 1
        
        

    # Calculate overall accuracy
    overall_accuracy = correct_counts / total_counts * 100

    # Calculate accuracy for each category
    category_accuracy_percentages = {
        k: (v['correct'] / v['total'] * 100) for k, v in category_accuracies.items()
    }

    # Prepare results for saving
    eval_results = {
        "Overall Accuracy": overall_accuracy,
        "Category-wise Accuracy": category_accuracy_percentages
    }

    # Save results to eval.json
    with open(args.output, 'w') as eval_file:
        json.dump(eval_results, eval_file, indent=4)

    print("Evaluation results saved to " + args.output)
