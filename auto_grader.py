import os
import sys
import json
import yaml
import glob
import re
import subprocess
from typing import List, Dict, Any, Tuple, Set, Optional

# Configuration
DATASET_DIR = "DSA Dataset"
RUBRICS_DIR = "generated_rubrics"
OUTPUT_DIR = "grading_results"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)


class AutoGrader:
    def __init__(self, rubric_path: str):
        """Initialize the AutoGrader with a specific rubric."""
        self.rubric_path = rubric_path
        
        # Load the rubric
        with open(rubric_path, 'r', encoding='utf-8') as f:
            self.rubric = yaml.safe_load(f)
            
        # Extract problem details
        self.problem_name = self.rubric.get("problem_name", "Unknown")
        self.category_name = self.rubric.get("category", "Unknown")
        self.total_points = self.rubric.get("total_points", 0)
        self.rubric_items = self.rubric.get("rubric_items", [])
        
        # Store the reference solution for comparison
        self.reference_solution = self.rubric.get("reference_solution", "")
        
    def _read_file(self, file_path: str) -> str:
        """Read the contents of a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return ""
            
    def _extract_method_code(self, java_code: str, method_name: Optional[str] = None) -> str:
        """Extract the method code from a Java file."""
        # Try to guess the method name from the reference solution if not provided
        if method_name is None:
            method_match = re.search(r"(\w+)\s+(\w+)\s*\(([^)]*)\)", self.reference_solution)
            if method_match:
                method_name = method_match.group(2)
            else:
                return ""
        
        # Find the method in the code
        pattern = rf"{method_name}\s*\([^)]*\)\s*\{{(.*?)\}}"
        match = re.search(pattern, java_code, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""
        
    def _method_contains_pattern(self, method_code: str, pattern: str) -> bool:
        """Check if the method contains a specific pattern."""
        # Replace common Java operators with regex-safe versions
        safe_pattern = pattern.replace("(", r"\(").replace(")", r"\)").replace("[", r"\[").replace("]", r"\]").replace("*", r"\*").replace("+", r"\+")
        
        # Check if the pattern is contained in the method code
        return bool(re.search(safe_pattern, method_code))
        
    def _check_rubric_item(self, method_code: str, rubric_item: Dict[str, Any]) -> bool:
        """Check if a submission satisfies a rubric item."""
        code_fragment = rubric_item.get("code_fragment", "")
        
        # Handle boolean logic operators
        if "_AND" in code_fragment:
            parts = code_fragment.split("_AND")
            return all(self._evaluate_boolean_part(part.strip(), method_code) for part in parts)
        elif "_OR" in code_fragment:
            parts = code_fragment.split("_OR")
            return any(self._evaluate_boolean_part(part.strip(), method_code) for part in parts)
        elif "NOT(" in code_fragment:
            # Extract the pattern inside NOT()
            match = re.search(r"NOT\((.*?)\)", code_fragment)
            if match:
                inner_pattern = match.group(1)
                return not self._evaluate_boolean_part(inner_pattern, method_code)
            return False
        else:
            # Simple pattern check
            return self._method_contains_pattern(method_code, code_fragment)
            
    def _evaluate_boolean_part(self, part: str, method_code: str) -> bool:
        """Evaluate a boolean part of a rubric item."""
        if part.startswith("ITEM_") and part.endswith("_BOOL"):
            # This references another rubric item's result
            # In a real implementation, you'd need to track which items have been evaluated
            # For simplicity, we'll just return True here
            return True
        elif part.startswith("contains("):
            # Extract the pattern inside contains()
            match = re.search(r"contains\((.*?)\)", part)
            if match:
                inner_pattern = match.group(1)
                return self._method_contains_pattern(method_code, inner_pattern)
            return False
        else:
            # Simple pattern check
            return self._method_contains_pattern(method_code, part)
    
    def grade_submission(self, submission_path: str) -> Dict[str, Any]:
        """Grade a student submission against the rubric."""
        print(f"Grading submission: {submission_path}")
        
        # Read the submission
        submission_code = self._read_file(submission_path)
        if not submission_code:
            return {
                "error": "Could not read submission file",
                "score": 0,
                "total_points": self.total_points,
                "percentage": 0,
                "details": []
            }
            
        # Extract the method code
        method_code = self._extract_method_code(submission_code)
        if not method_code:
            return {
                "error": "Could not extract method code from submission",
                "score": 0,
                "total_points": self.total_points,
                "percentage": 0,
                "details": []
            }
            
        # Grade each rubric item
        score = 0
        details = []
        
        for item in self.rubric_items:
            item_name = item.get("item", "Unknown item")
            item_score = item.get("score", 0)
            
            # Check if the submission satisfies this rubric item
            satisfied = self._check_rubric_item(method_code, item)
            
            if satisfied:
                score += item_score
                details.append({
                    "item": item_name,
                    "score": item_score,
                    "satisfied": True,
                    "comment": "Requirement satisfied"
                })
            else:
                details.append({
                    "item": item_name,
                    "score": 0,
                    "satisfied": False,
                    "comment": "Requirement not satisfied"
                })
                
        # Calculate percentage
        percentage = (score / self.total_points) * 100 if self.total_points > 0 else 0
        
        # Return the grading result
        return {
            "submission_path": submission_path,
            "problem_name": self.problem_name,
            "category": self.category_name,
            "score": score,
            "total_points": self.total_points,
            "percentage": percentage,
            "details": details
        }
        
    def save_grading_result(self, result: Dict[str, Any]) -> None:
        """Save the grading result to a JSON file."""
        # Create a filename based on the submission path
        submission_path = result.get("submission_path", "unknown")
        base_name = os.path.basename(os.path.dirname(submission_path))
        filename = f"{self.category_name}_{self.problem_name}_{base_name}_result.json".replace(" ", "_")
        file_path = os.path.join(OUTPUT_DIR, filename)
        
        # Save the result
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
            
        print(f"Grading result saved to {file_path}")


def find_all_rubrics() -> List[str]:
    """Find all rubric files in the rubrics directory."""
    return glob.glob(os.path.join(RUBRICS_DIR, "*.yaml"))


def find_submissions_for_rubric(rubric_path: str) -> List[str]:
    """Find all submissions that match a rubric."""
    # Extract problem and category names from the rubric filename
    filename = os.path.basename(rubric_path)
    parts = filename.replace("_rubric.yaml", "").split("_", 1)
    
    if len(parts) < 2:
        return []
        
    category_name, problem_name = parts[0], parts[1]
    
    # Find submissions in the dataset
    problem_dir = os.path.join(DATASET_DIR, category_name, problem_name)
    if not os.path.exists(problem_dir):
        return []
        
    # Find all submission files
    submissions_dir = os.path.join(problem_dir, "submissions")
    if not os.path.exists(submissions_dir):
        return []
        
    # Get all solution files
    return glob.glob(os.path.join(submissions_dir, "**", "Solution.java"), recursive=True)


def main():
    """Main function to grade submissions using generated rubrics."""
    print("AutoGrader")
    print("==========")
    
    # Find all rubric files
    rubric_paths = find_all_rubrics()
    if not rubric_paths:
        print("No rubrics found in the rubrics directory.")
        return
        
    print(f"Found {len(rubric_paths)} rubrics.")
    
    # Process each rubric
    for rubric_path in rubric_paths:
        print(f"\nProcessing rubric: {rubric_path}")
        
        # Create a grader for this rubric
        grader = AutoGrader(rubric_path)
        
        # Find submissions for this rubric
        submission_paths = find_submissions_for_rubric(rubric_path)
        if not submission_paths:
            print("No submissions found for this rubric.")
            continue
            
        print(f"Found {len(submission_paths)} submissions to grade.")
        
        # Grade each submission
        for submission_path in submission_paths:
            result = grader.grade_submission(submission_path)
            grader.save_grading_result(result)
            
            # Print a short summary
            print(f"  {os.path.basename(os.path.dirname(submission_path))}: " +
                  f"{result['score']}/{result['total_points']} " +
                  f"({result['percentage']:.1f}%)")
    
    print("\nGrading complete!")


if __name__ == "__main__":
    main() 