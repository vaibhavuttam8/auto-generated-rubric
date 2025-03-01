#!/usr/bin/env python
import os
import sys
import json
import glob
from typing import List, Dict, Any
import matplotlib.pyplot as plt
from collections import defaultdict
import pandas as pd

# Configuration
GRADING_RESULTS_DIR = "grading_results"
REPORT_DIR = "reports"

# Create reports directory if it doesn't exist
os.makedirs(REPORT_DIR, exist_ok=True)


def load_grading_results() -> List[Dict[str, Any]]:
    """Load all grading results from the results directory."""
    results = []
    
    for results_file in glob.glob(os.path.join(GRADING_RESULTS_DIR, "*.json")):
        try:
            with open(results_file, 'r', encoding='utf-8') as f:
                result = json.load(f)
                results.append(result)
        except Exception as e:
            print(f"Error loading file {results_file}: {e}")
    
    return results


def generate_text_report(results: List[Dict[str, Any]]) -> str:
    """Generate a text-based summary report."""
    if not results:
        return "No grading results found."
    
    # Group results by problem
    problems = {}
    for result in results:
        problem_key = f"{result.get('category', 'Unknown')}/{result.get('problem_name', 'Unknown')}"
        if problem_key not in problems:
            problems[problem_key] = []
        problems[problem_key].append(result)
    
    # Generate the report text
    report = "AutoRubric Grading Summary Report\n"
    report += "================================\n\n"
    
    # Overall statistics
    total_submissions = len(results)
    total_score = sum(result.get("score", 0) for result in results)
    total_possible = sum(result.get("total_points", 0) for result in results)
    overall_percentage = (total_score / total_possible) * 100 if total_possible > 0 else 0
    
    report += f"Total Submissions: {total_submissions}\n"
    report += f"Overall Score: {total_score:.2f}/{total_possible:.2f} ({overall_percentage:.2f}%)\n\n"
    
    # Problem-specific statistics
    report += "Problem Statistics:\n"
    report += "-----------------\n"
    
    for problem_key, problem_results in problems.items():
        avg_score = sum(r.get("score", 0) for r in problem_results) / len(problem_results)
        max_points = problem_results[0].get("total_points", 0)
        avg_percentage = (avg_score / max_points) * 100 if max_points > 0 else 0
        
        report += f"\n{problem_key}:\n"
        report += f"  Submissions: {len(problem_results)}\n"
        report += f"  Average Score: {avg_score:.2f}/{max_points:.2f} ({avg_percentage:.2f}%)\n"
        
        # Submission type statistics
        submission_types = defaultdict(int)
        for r in problem_results:
            path = r.get("submission_path", "")
            if "/Correct_" in path:
                submission_types["Correct"] += 1
            elif "/Wrong/" in path:
                submission_types["Wrong"] += 1
            elif "/TLE/" in path:
                submission_types["Time Limit Exceeded"] += 1
            elif "/Compilation_error/" in path:
                submission_types["Compilation Error"] += 1
            else:
                submission_types["Unknown"] += 1
        
        report += "  Submission Types:\n"
        for stype, count in submission_types.items():
            report += f"    {stype}: {count} ({(count/len(problem_results))*100:.2f}%)\n"
    
    return report


def generate_visualizations(results: List[Dict[str, Any]]) -> None:
    """Generate visualizations from grading results."""
    if not results:
        return
    
    # Extract data for plotting
    problem_data = defaultdict(list)
    for result in results:
        problem_key = f"{result.get('category', 'Unknown')}/{result.get('problem_name', 'Unknown')}"
        problem_data[problem_key].append({
            "score": result.get("score", 0),
            "total_points": result.get("total_points", 0),
            "percentage": result.get("percentage", 0),
            "submission_type": _get_submission_type(result.get("submission_path", ""))
        })
    
    # Plot distribution of scores for each problem
    for problem_key, data in problem_data.items():
        # Convert to DataFrame for easier plotting
        df = pd.DataFrame(data)
        
        # Create a figure with multiple subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Score distribution histogram
        ax1.hist(df["percentage"], bins=10, alpha=0.7)
        ax1.set_title(f"Score Distribution: {problem_key}")
        ax1.set_xlabel("Score Percentage")
        ax1.set_ylabel("Number of Submissions")
        
        # Submission type pie chart
        submission_counts = df["submission_type"].value_counts()
        ax2.pie(submission_counts, labels=submission_counts.index, autopct='%1.1f%%')
        ax2.set_title(f"Submission Types: {problem_key}")
        
        # Save the figure
        safe_key = problem_key.replace("/", "_").replace(" ", "_")
        plt.tight_layout()
        plt.savefig(os.path.join(REPORT_DIR, f"{safe_key}_stats.png"))
        plt.close()


def _get_submission_type(path: str) -> str:
    """Extract the submission type from a submission path."""
    if "/Correct_" in path:
        return "Correct"
    elif "/Wrong/" in path:
        return "Wrong"
    elif "/TLE/" in path:
        return "Time Limit Exceeded"
    elif "/Compilation_error/" in path:
        return "Compilation Error"
    else:
        return "Unknown"


def generate_html_report(results: List[Dict[str, Any]]) -> str:
    """Generate an HTML report from grading results."""
    if not results:
        return "<html><body><h1>No grading results found.</h1></body></html>"
    
    # Group results by problem
    problems = {}
    for result in results:
        problem_key = f"{result.get('category', 'Unknown')}/{result.get('problem_name', 'Unknown')}"
        if problem_key not in problems:
            problems[problem_key] = []
        problems[problem_key].append(result)
    
    # Start building the HTML content
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AutoRubric Grading Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .header { background-color: #f5f5f5; padding: 10px; border-radius: 5px; }
            .problem { margin-top: 30px; border-top: 1px solid #ccc; padding-top: 20px; }
            .chart-container { display: flex; justify-content: center; margin: 20px 0; }
            .chart { width: 45%; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #f9f9f9; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>AutoRubric Grading Summary Report</h1>
    """
    
    # Overall statistics
    total_submissions = len(results)
    total_score = sum(result.get("score", 0) for result in results)
    total_possible = sum(result.get("total_points", 0) for result in results)
    overall_percentage = (total_score / total_possible) * 100 if total_possible > 0 else 0
    
    html += f"""
            <p><strong>Total Submissions:</strong> {total_submissions}</p>
            <p><strong>Overall Score:</strong> {total_score:.2f}/{total_possible:.2f} ({overall_percentage:.2f}%)</p>
        </div>
    """
    
    # Problem-specific statistics
    for problem_key, problem_results in problems.items():
        safe_key = problem_key.replace("/", "_").replace(" ", "_")
        avg_score = sum(r.get("score", 0) for r in problem_results) / len(problem_results)
        max_points = problem_results[0].get("total_points", 0)
        avg_percentage = (avg_score / max_points) * 100 if max_points > 0 else 0
        
        html += f"""
        <div class="problem">
            <h2>{problem_key}</h2>
            <p><strong>Submissions:</strong> {len(problem_results)}</p>
            <p><strong>Average Score:</strong> {avg_score:.2f}/{max_points:.2f} ({avg_percentage:.2f}%)</p>
            
            <div class="chart-container">
                <img class="chart" src="{safe_key}_stats.png" alt="Statistics for {problem_key}">
            </div>
            
            <h3>Submission Details</h3>
            <table>
                <tr>
                    <th>Submission</th>
                    <th>Score</th>
                    <th>Percentage</th>
                    <th>Type</th>
                </tr>
        """
        
        # Add a row for each submission
        for result in problem_results:
            submission_name = os.path.basename(os.path.dirname(result.get("submission_path", "unknown")))
            score = result.get("score", 0)
            total = result.get("total_points", 0)
            percentage = result.get("percentage", 0)
            submission_type = _get_submission_type(result.get("submission_path", ""))
            
            html += f"""
                <tr>
                    <td>{submission_name}</td>
                    <td>{score}/{total}</td>
                    <td>{percentage:.2f}%</td>
                    <td>{submission_type}</td>
                </tr>
            """
        
        html += """
            </table>
        </div>
        """
    
    # Close the HTML
    html += """
    </body>
    </html>
    """
    
    return html


def main():
    """Generate reports from grading results."""
    print("Generating grading reports...")
    
    # Load all grading results
    results = load_grading_results()
    if not results:
        print("No grading results found. Please run the grading step first.")
        return 1
    
    print(f"Loaded {len(results)} grading results.")
    
    # Generate text report
    text_report = generate_text_report(results)
    with open(os.path.join(REPORT_DIR, "summary_report.txt"), 'w', encoding='utf-8') as f:
        f.write(text_report)
    print("Generated text report.")
    
    # Generate visualizations
    try:
        generate_visualizations(results)
        print("Generated visualizations.")
    except Exception as e:
        print(f"Error generating visualizations: {e}")
        print("Make sure matplotlib and pandas are installed.")
    
    # Generate HTML report
    html_report = generate_html_report(results)
    with open(os.path.join(REPORT_DIR, "summary_report.html"), 'w', encoding='utf-8') as f:
        f.write(html_report)
    print("Generated HTML report.")
    
    print(f"Reports saved to {REPORT_DIR}/ directory.")
    return 0


if __name__ == "__main__":
    sys.exit(main()) 