import os
import sys
import json
import yaml
import glob
import subprocess
import re
import datetime
from typing import List, Dict, Any, Tuple, Set, Optional

# Configuration
DATASET_DIR = "DSA Dataset"
# Use timestamp for output directory
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_DIR = f"generated_rubrics_{timestamp}"
OPENAI_API_KEY = "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"  # Set your OpenAI API key

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

class RubricGenerator:
    def __init__(self, problem_path: str):
        """Initialize the rubric generator for a specific problem."""
        self.problem_path = problem_path
        self.problem_name = os.path.basename(problem_path)
        self.category_name = os.path.basename(os.path.dirname(problem_path))
        
        # Read the question and solution files
        self.question_text = self._read_file(os.path.join(problem_path, "Question.txt"))
        self.reference_solution = self._read_file(os.path.join(problem_path, "Solution.java"))
        
        # Get paths to correct and incorrect submissions
        self.correct_submissions = self._get_submissions("Correct")
        self.wrong_submissions = self._get_submissions("Wrong")
        self.tle_submissions = self._get_submissions("TLE")
        self.compilation_error_submissions = self._get_submissions("Compilation_error")

    def _read_file(self, file_path: str) -> str:
        """Read the contents of a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return ""

    def _get_submissions(self, submission_type: str) -> List[str]:
        """Get paths to all submissions of a specific type."""
        submission_dir = os.path.join(self.problem_path, "submissions")
        if submission_type == "Correct":
            # Specifically handle correct solutions 1, 2, and 3
            correct_solutions = []
            for i in range(1, 4):
                pattern = os.path.join(submission_dir, f"Correct_{i}", "Solution.java")
                solutions = glob.glob(pattern)
                if solutions:
                    correct_solutions.extend(solutions)
            return correct_solutions
        else:
            pattern = os.path.join(submission_dir, f"{submission_type}*", "Solution.java")
            return glob.glob(pattern)

    def _get_correct_solution_content(self, solution_number: int) -> str:
        """Get the content of a specific correct solution."""
        solution_path = os.path.join(self.problem_path, "submissions", f"Correct_{solution_number}", "Solution.java")
        return self._read_file(solution_path)

    def _extract_method_code(self, java_code: str, method_name: Optional[str] = None) -> str:
        """Extract the method code from a Java file."""
        if method_name is None:
            # Try to guess the method name from the question
            method_match = re.search(r"\b(\w+)\(.*?\)", self.question_text)
            if method_match:
                method_name = method_match.group(1)
            else:
                # Default to finding any method
                method_match = re.search(r"(\w+)\s+(\w+)\s*\(([^)]*)\)", java_code)
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

    def _analyze_solutions(self) -> Dict[str, Any]:
        """Analyze correct and incorrect solutions to identify key code patterns."""
        # Extract method code from reference solution
        reference_method = self._extract_method_code(self.reference_solution)
        
        # Extract method code from all three correct submissions
        correct_methods = []
        correct_patterns = []
        
        # Process each correct solution
        for solution_path in self.correct_submissions:
            solution_code = self._read_file(solution_path)
            method_code = self._extract_method_code(solution_code)
            if method_code:
                correct_methods.append(method_code)
                # Extract patterns from this solution
                solution_patterns = self._extract_patterns([method_code])
                correct_patterns.extend(solution_patterns)
        
        # Remove duplicates while preserving order
        correct_patterns = list(dict.fromkeys(correct_patterns))
        
        # Extract method code from incorrect submissions
        wrong_methods = [self._extract_method_code(self._read_file(sub)) for sub in self.wrong_submissions]
        wrong_patterns = self._extract_patterns(wrong_methods)
        
        # Analyze patterns
        analysis = {
            "reference_method": reference_method,
            "correct_methods": correct_methods,
            "wrong_methods": wrong_methods,
            "patterns": {
                "correct_patterns": correct_patterns,
                "wrong_patterns": wrong_patterns
            }
        }
        
        return analysis

    def _extract_patterns(self, methods: List[str]) -> List[str]:
        """Extract common code patterns from a list of methods."""
        if not methods:
            return []
            
        patterns = []
        
        # Look for common variable initializations
        for method in methods:
            init_matches = re.findall(r"(\w+)\s*=\s*([^;]+);", method)
            for var_name, var_value in init_matches:
                if var_name.lower() in ["max", "min", "sum", "result", "res", "ans", "curr", "current"]:
                    patterns.append(f"{var_name} = {var_value}")
        
        # Look for common loop patterns
        for method in methods:
            for_matches = re.findall(r"for\s*\(([^)]+)\)", method)
            for for_cond in for_matches:
                patterns.append(f"for({for_cond})")
                
        # Look for common if conditions
        for method in methods:
            if_matches = re.findall(r"if\s*\(([^)]+)\)", method)
            for if_cond in if_matches:
                patterns.append(f"if({if_cond})")
                
        # Look for Math.* functions
        for method in methods:
            math_matches = re.findall(r"Math\.(\w+)\s*\(([^)]+)\)", method)
            for math_func, math_args in math_matches:
                patterns.append(f"Math.{math_func}({math_args})")
                
        # Deduplicate patterns
        unique_patterns = list(set(patterns))
        
        return unique_patterns

    def _generate_rubric_items(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate rubric items based on the analysis."""
        rubric_items = []
        
        # Detect problem type based on problem name and extracted patterns
        problem_type = self._detect_problem_type()
        
        # Add initialization checks - consider patterns from all correct solutions
        init_patterns = [p for p in analysis["patterns"]["correct_patterns"] 
                        if "=" in p and not any(w in p for w in ["for(", "if(", "while("])]
        for i, pattern in enumerate(init_patterns[:3]):
            rubric_items.append({
                "item": f"[Variable initialization] {pattern}",
                "code_fragment": pattern,
                "blank": "1",
                "score": 1.0 if i == 0 else 0.5  # Primary initialization worth more
            })
        
        # Add loop structure checks - consider all loop variations
        loop_patterns = [p for p in analysis["patterns"]["correct_patterns"] if "for(" in p or "while(" in p]
        for i, pattern in enumerate(loop_patterns[:3]):  # Consider up to 3 loop patterns
            rubric_items.append({
                "item": f"[Loop structure] {pattern}",
                "code_fragment": pattern,
                "blank": "2",
                "score": 1.5 if i == 0 else 0.75  # Primary loop structure worth more
            })
        
        # Add conditional logic checks - consider all variations
        if_patterns = [p for p in analysis["patterns"]["correct_patterns"] if "if(" in p]
        for i, pattern in enumerate(if_patterns[:3]):  # Consider up to 3 if patterns
            rubric_items.append({
                "item": f"[Conditional logic] {pattern}",
                "code_fragment": pattern,
                "blank": "3",
                "score": 1.0 if i == 0 else 0.5  # Primary condition worth more
            })
        
        # Add Math function usage checks
        math_patterns = [p for p in analysis["patterns"]["correct_patterns"] if "Math." in p]
        for i, pattern in enumerate(math_patterns[:2]):
            rubric_items.append({
                "item": f"[Math function usage] {pattern}",
                "code_fragment": pattern,
                "blank": "4",
                "score": 1.0 if i == 0 else 0.5
            })
        
        # Add edge case handling specific to problem type
        edge_case_item = self._get_edge_case_item(problem_type)
        rubric_items.append(edge_case_item)
        
        # Add problem-specific logical correctness checks with clear points
        logical_correctness_items = self._get_logical_correctness_items(problem_type)
        rubric_items.extend(logical_correctness_items)
        
        # Add algorithm-specific correctness check with higher weight
        algo_correctness_item = self._get_algorithm_correctness_item(problem_type)
        algo_correctness_item["score"] = 3.0  # Increase score for algorithm correctness
        rubric_items.append(algo_correctness_item)
        
        # Add algorithm-specific efficiency check
        efficiency_item = self._get_efficiency_item(problem_type)
        efficiency_item["score"] = 2.0  # Increase score for efficiency
        rubric_items.append(efficiency_item)
        
        return rubric_items
        
    def _detect_problem_type(self) -> str:
        """Detect the type of problem based on problem name and characteristics."""
        problem_name_lower = self.problem_name.lower()
        
        # Check for common problem types
        if "kadane" in problem_name_lower or "maximum subarray" in problem_name_lower:
            return "kadane"
        elif "jump" in problem_name_lower:
            return "jump"
        elif "rain" in problem_name_lower or "water" in problem_name_lower or "trap" in problem_name_lower:
            return "trap_water"
        elif "binary search" in problem_name_lower or "sorted array" in problem_name_lower:
            return "binary_search"
        elif "graph" in problem_name_lower or "path" in problem_name_lower:
            return "graph"
        elif "dynamic" in problem_name_lower or "dp" in problem_name_lower:
            return "dynamic_programming"
        elif "anagram" in problem_name_lower or "string" in problem_name_lower:
            return "string"
        elif "list" in problem_name_lower or "linked" in problem_name_lower:
            return "linked_list"
        elif "tree" in problem_name_lower or "bst" in problem_name_lower:
            return "tree"
        elif "bit" in problem_name_lower or "xor" in problem_name_lower:
            return "bit_manipulation"
        else:
            return "general"
            
    def _get_edge_case_item(self, problem_type: str) -> Dict[str, Any]:
        """Get edge case handling item specific to problem type."""
        if problem_type == "kadane":
            return {
                "item": "[Edge case handling] Handles array with all negative numbers or empty array",
                "code_fragment": "arr.length == 0 || allNegative(arr)",
                "blank": "5",
                "score": 1.0
            }
        elif problem_type == "jump":
            return {
                "item": "[Edge case handling] Handles cases where jumps are not possible or array is small",
                "code_fragment": "arr.length <= 1 || arr[0] == 0",
                "blank": "5",
                "score": 1.0
            }
        elif problem_type == "binary_search":
            return {
                "item": "[Edge case handling] Handles empty array, single element array, or target not found",
                "code_fragment": "arr.length == 0 || arr == null || targetNotFound",
                "blank": "5",
                "score": 1.0
            }
        elif problem_type == "string":
            return {
                "item": "[Edge case handling] Handles empty strings, single character strings, or case sensitivity",
                "code_fragment": "s.length() == 0 || s.length() == 1",
                "blank": "5",
                "score": 1.0
            }
        elif problem_type == "linked_list":
            return {
                "item": "[Edge case handling] Handles null or single node list",
                "code_fragment": "head == null || head.next == null",
                "blank": "5",
                "score": 1.0
            }
        elif problem_type == "tree":
            return {
                "item": "[Edge case handling] Handles null tree or leaf node cases",
                "code_fragment": "root == null || isLeaf(root)",
                "blank": "5",
                "score": 1.0
            }
        else:
            return {
                "item": "[Edge case handling] Handles empty array or single element array",
                "code_fragment": "arr.length <= 1 || arr == null",
                "blank": "5",
                "score": 1.0
            }
            
    def _get_logical_correctness_items(self, problem_type: str) -> List[Dict[str, Any]]:
        """Get logical correctness items specific to problem type."""
        items = []
        
        if problem_type == "kadane":
            items = [
                {
                    "item": "[Logical correctness] Correctly initializes variables for tracking current sum and maximum sum",
                    "code_fragment": "int currSum = 0; int maxSum = arr[0];",
                    "blank": "1",
                    "score": 2.0
                },
                {
                    "item": "[Logical correctness] Properly iterates through the array elements",
                    "code_fragment": "for(int i = 0; i < arr.length; i++)",
                    "blank": "2",
                    "score": 2.0
                },
                {
                    "item": "[Logical correctness] Correctly updates current sum by adding current element or restarting from current element",
                    "code_fragment": "currSum = Math.max(arr[i], currSum + arr[i]);",
                    "blank": "3",
                    "score": 2.0
                },
                {
                    "item": "[Logical correctness] Updates maximum sum whenever current sum exceeds it",
                    "code_fragment": "maxSum = Math.max(maxSum, currSum);",
                    "blank": "Multiple",
                    "score": 2.0
                },
                {
                    "item": "[Logical correctness] Returns the maximum sum found",
                    "code_fragment": "return maxSum;",
                    "blank": "Multiple",
                    "score": 2.0
                }
            ]
        elif problem_type == "jump":
            items = [
                {
                    "item": "[Logical correctness] Correctly initializes variables for tracking jumps, steps, and maximum reach",
                    "code_fragment": "int jump = 0/1; int step = arr[0]; int maxReach = arr[0];",
                    "blank": "1",
                    "score": 2.0
                },
                {
                    "item": "[Logical correctness] Properly iterates through the array to calculate jumps",
                    "code_fragment": "for(int i = 1; i < arr.length; i++)",
                    "blank": "2",
                    "score": 2.0
                },
                {
                    "item": "[Logical correctness] Correctly updates maxReach based on current position and value",
                    "code_fragment": "maxReach = Math.max(maxReach, i + arr[i]);",
                    "blank": "3",
                    "score": 2.0
                },
                {
                    "item": "[Logical correctness] Properly updates jumps when steps are exhausted",
                    "code_fragment": "step--; if(step == 0) { jump++; }",
                    "blank": "Multiple",
                    "score": 2.0
                },
                {
                    "item": "[Logical correctness] Returns appropriate result based on whether destination is reachable",
                    "code_fragment": "if(i >= maxReach) return -1; return jump;",
                    "blank": "Multiple",
                    "score": 2.0
                }
            ]
        elif problem_type == "binary_search":
            items = [
                {
                    "item": "[Logical correctness] Correctly initializes left and right pointers for binary search",
                    "code_fragment": "int left = 0; int right = arr.length - 1;",
                    "blank": "1",
                    "score": 2.0
                },
                {
                    "item": "[Logical correctness] Properly implements binary search loop",
                    "code_fragment": "while(left <= right)",
                    "blank": "2",
                    "score": 2.0
                },
                {
                    "item": "[Logical correctness] Correctly calculates middle point and compares with target",
                    "code_fragment": "int mid = left + (right - left) / 2; if(arr[mid] == target)",
                    "blank": "3",
                    "score": 2.0
                },
                {
                    "item": "[Logical correctness] Properly updates search boundaries based on comparison",
                    "code_fragment": "if(arr[mid] < target) left = mid + 1; else right = mid - 1;",
                    "blank": "Multiple",
                    "score": 2.0
                },
                {
                    "item": "[Logical correctness] Returns appropriate result based on search outcome",
                    "code_fragment": "return found ? index : -1;",
                    "blank": "Multiple",
                    "score": 2.0
                }
            ]
        else:
            # Generic logical correctness items for other problem types
            items = [
                {
                    "item": "[Logical correctness] Correctly initializes variables before the main algorithm",
                    "code_fragment": "initialization pattern specific to this problem",
                    "blank": "1",
                    "score": 2.0
                },
                {
                    "item": "[Logical correctness] Properly implements the main loop structure",
                    "code_fragment": "main loop pattern specific to this problem",
                    "blank": "2",
                    "score": 2.0
                },
                {
                    "item": "[Logical correctness] Correctly handles conditional logic within the algorithm",
                    "code_fragment": "conditional logic pattern specific to this problem",
                    "blank": "3",
                    "score": 2.0
                },
                {
                    "item": "[Logical correctness] Updates variables correctly during algorithm execution",
                    "code_fragment": "variable update pattern specific to this problem",
                    "blank": "Multiple",
                    "score": 2.0
                },
                {
                    "item": "[Logical correctness] Returns the correct result",
                    "code_fragment": "return pattern specific to this problem",
                    "blank": "Multiple",
                    "score": 2.0
                }
            ]
            
        return items
        
    def _get_algorithm_correctness_item(self, problem_type: str) -> Dict[str, Any]:
        """Get algorithm correctness item specific to problem type."""
        if problem_type == "kadane":
            return {
                "item": "[Algorithm correctness] Correctly implements Kadane's algorithm for maximum subarray sum",
                "code_fragment": "currSum = Math.max(arr[i], currSum + arr[i]) _AND maxSum = Math.max(maxSum, currSum) _AND complete_loop_structure",
                "blank": "Multiple",
                "score": 3.0
            }
        elif problem_type == "jump":
            return {
                "item": "[Algorithm correctness] Correctly implements greedy approach for minimum jumps",
                "code_fragment": "maxReach = Math.max(maxReach, i + arr[i]) _AND step tracking _AND jump incrementation",
                "blank": "Multiple",
                "score": 3.0
            }
        elif problem_type == "binary_search":
            return {
                "item": "[Algorithm correctness] Correctly implements binary search algorithm",
                "code_fragment": "mid calculation _AND comparison with target _AND boundary updates",
                "blank": "Multiple",
                "score": 3.0
            }
        else:
            return {
                "item": "[Algorithm correctness] Correctly implements the core algorithm logic",
                "code_fragment": "Essential algorithm components for this problem type",
                "blank": "Multiple",
                "score": 3.0
            }
            
    def _get_efficiency_item(self, problem_type: str) -> Dict[str, Any]:
        """Get efficiency item specific to problem type."""
        if problem_type == "kadane":
            return {
                "item": "[Algorithm efficiency] Uses Kadane's algorithm with O(n) time complexity",
                "code_fragment": "Single pass _AND constant space _AND no nested loops",
                "blank": "Multiple",
                "score": 2.0
            }
        elif problem_type == "jump":
            return {
                "item": "[Algorithm efficiency] Uses efficient greedy approach with O(n) time complexity",
                "code_fragment": "Single pass _AND constant extra space",
                "blank": "Multiple",
                "score": 2.0
            }
        elif problem_type == "binary_search":
            return {
                "item": "[Algorithm efficiency] Uses binary search with O(log n) time complexity",
                "code_fragment": "Binary division _AND no linear scanning",
                "blank": "Multiple",
                "score": 2.0
            }
        else:
            return {
                "item": "[Algorithm efficiency] Uses an efficient approach with appropriate time complexity",
                "code_fragment": "Efficient algorithm pattern for this problem type",
                "blank": "Multiple",
                "score": 2.0
            }

    def generate_rubric(self) -> Dict[str, Any]:
        """Generate a rubric for the problem."""
        print(f"Generating rubric for {self.problem_name}...")
        
        # Analyze solutions
        analysis = self._analyze_solutions()
        
        # Generate rubric items
        rubric_items = self._generate_rubric_items(analysis)
        
        # Create the full rubric
        rubric = {
            "problem_name": self.problem_name,
            "category": self.category_name,
            "total_points": sum(item["score"] for item in rubric_items),
            "reference_solution": self.reference_solution,
            "rubric_items": rubric_items
        }
        
        return rubric

    def save_rubric(self, rubric: Dict[str, Any]) -> None:
        """Save the generated rubric to a YAML file."""
        # Validate the rubric structure
        validated_rubric = self._validate_rubric(rubric)
        
        filename = f"{self.category_name}_{self.problem_name}_rubric.yaml".replace(" ", "_")
        file_path = os.path.join(OUTPUT_DIR, filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(validated_rubric, f, default_flow_style=False)
            
        print(f"Rubric saved to {file_path}")
        
    def _validate_rubric(self, rubric: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and fix the rubric structure if needed."""
        # Create a copy to avoid modifying the original
        validated = rubric.copy()
        
        # Ensure required top-level fields exist
        required_fields = ["problem_name", "category", "total_points", "reference_solution", "rubric_items"]
        for field in required_fields:
            if field not in validated:
                if field == "problem_name":
                    validated[field] = self.problem_name
                elif field == "category":
                    validated[field] = self.category_name
                elif field == "total_points":
                    validated[field] = 0.0
                elif field == "reference_solution":
                    validated[field] = self.reference_solution
                elif field == "rubric_items":
                    validated[field] = []
        
        # Validate rubric items
        if "rubric_items" in validated and isinstance(validated["rubric_items"], list):
            valid_items = []
            for item in validated["rubric_items"]:
                if not isinstance(item, dict):
                    continue
                
                # Ensure each item has required fields
                valid_item = {}
                if "item" in item:
                    valid_item["item"] = item["item"]
                else:
                    valid_item["item"] = "Unnamed item"
                    
                if "code_fragment" in item:
                    valid_item["code_fragment"] = item["code_fragment"]
                else:
                    valid_item["code_fragment"] = ""
                    
                if "blank" in item:
                    # Ensure blank is a simple string
                    if isinstance(item["blank"], str) and ":" not in item["blank"]:
                        valid_item["blank"] = item["blank"]
                    else:
                        valid_item["blank"] = "1"
                else:
                    valid_item["blank"] = "1"
                    
                if "score" in item:
                    # Ensure score is a number
                    try:
                        valid_item["score"] = float(item["score"])
                    except (ValueError, TypeError):
                        valid_item["score"] = 1.0
                else:
                    valid_item["score"] = 1.0
                
                valid_items.append(valid_item)
            
            validated["rubric_items"] = valid_items
            
            # Recalculate total points
            validated["total_points"] = sum(item["score"] for item in valid_items)
        
        return validated

    def run(self) -> None:
        """Generate and save a rubric for the problem."""
        rubric = self.generate_rubric()
        self.save_rubric(rubric)


class EnhancedRubricGenerator(RubricGenerator):
    """Enhanced rubric generator that uses OpenAI API to improve the rubrics."""
    
    def generate_rubric(self) -> Dict[str, Any]:
        """Generate a rubric for the problem using OpenAI API."""
        import openai
        
        # Set up OpenAI API
        openai.api_key = OPENAI_API_KEY
        
        # Get basic rubric
        basic_rubric = super().generate_rubric()
        
        if not OPENAI_API_KEY:
            print("No OpenAI API key provided. Returning basic rubric.")
            return basic_rubric
        
        # Create a prompt for GPT
        prompt = f"""
        I need to create a detailed, specific rubric for grading a data structures and algorithms problem. The rubric will be used by an LLM to automatically grade student submissions our main concern is prioirty wise is logical correctness > time and space compelixty > syntax error.

        PROBLEM:
        {self.question_text}

        REFERENCE SOLUTION:
        {self.reference_solution}

        SUBMISSIONS:
        {self._get_submissions("correct"), self._get_submissions("Wrong"),
        self._get_submissions("TLE"), self._get_submissions("Compilation_error")}

        CURRENT BASIC RUBRIC:
        {yaml.dump(basic_rubric, default_flow_style=False)}

        Please improve this rubric by making it:
        1. MORE SPECIFIC: Replace generic criteria with algorithm-specific criteria
        2. MORE EXACT: Use precise code patterns that can be matched in student code
        3. CLEARER FOR LLM GRADING: An LLM will use this rubric to grade students, so be very explicit
        4. FOCUSED ON LOGICAL CORRECTNESS: Clearly evaluate each key logical step in the algorithm
        5. MEASURABLE: Each criterion should be clearly measurable through code pattern matching

        Each rubric item should:
        1. Have a clear description that precisely states what is being evaluated
        2. Have a specific code fragment that can be searched for in student code
        3. Clearly indicate which part of the algorithm it's evaluating
        4. Use score weights that reflect the importance of the item

        IMPORTANT FORMATTING REQUIREMENTS:
        1. Return ONLY valid YAML format
        2. For the "blank" field, use ONLY single values like "1", "2", "3", etc. or the string "Multiple" (without any colons after it)
        3. For each rubric item, include these fields: "item", "code_fragment", "blank", and "score"
        4. Make sure the "score" field contains only numeric values (e.g., 1.0, 2.0)
        5. Ensure the total points add up correctly
        6. Do not use any special characters or formatting that would break YAML parsing
        
        Return ONLY the YAML format of the improved rubric.
        """
        
        try:
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert in data structures and algorithms education."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.2
            )
            
            # Extract the response
            improved_rubric_text = response.choices[0].message.content
            
            # Try to parse the YAML
            try:
                # Remove any markdown code block formatting if present
                if "```yaml" in improved_rubric_text:
                    improved_rubric_text = improved_rubric_text.split("```yaml")[1].split("```")[0].strip()
                elif "```" in improved_rubric_text:
                    improved_rubric_text = improved_rubric_text.split("```")[1].strip()
                
                # Add additional preprocessing to ensure valid YAML
                # Fix common YAML issues that might occur in the response
                # 1. Ensure proper indentation for nested items
                lines = improved_rubric_text.split('\n')
                processed_lines = []
                for line in lines:
                    # Skip empty lines
                    if not line.strip():
                        continue
                    # Fix potential issues with "Multiple" blank field
                    if "blank: Multiple" in line and not line.endswith(':'):
                        line = line.rstrip() + ':'
                    processed_lines.append(line)
                
                improved_rubric_text = '\n'.join(processed_lines)
                
                # Try to load the YAML
                try:
                    improved_rubric = yaml.safe_load(improved_rubric_text)
                    print("Successfully generated enhanced rubric using OpenAI API.")
                    return improved_rubric
                except Exception as yaml_error:
                    print(f"Error in YAML parsing: {yaml_error}")
                    print("Attempting to fix the YAML structure...")
                    
                    # Fall back to extracting just the rubric_items if possible
                    try:
                        # Try to extract and parse just the rubric_items section
                        if "rubric_items:" in improved_rubric_text:
                            # Create a new rubric based on the basic one but with fixed items
                            fixed_rubric = basic_rubric.copy()
                            
                            # Parse just the rubric_items section
                            items_section = improved_rubric_text.split("rubric_items:")[1]
                            items_yaml = "rubric_items:" + items_section
                            parsed_items = yaml.safe_load(items_yaml)
                            
                            if parsed_items and "rubric_items" in parsed_items:
                                fixed_rubric["rubric_items"] = parsed_items["rubric_items"]
                                # Recalculate total points
                                fixed_rubric["total_points"] = sum(item.get("score", 0) for item in fixed_rubric["rubric_items"])
                                print("Successfully fixed and parsed rubric items.")
                                return fixed_rubric
                    except Exception:
                        pass
                    
                    # If all parsing attempts fail, return the basic rubric
                    print("Could not fix YAML structure. Returning basic rubric.")
                    return basic_rubric
            except Exception as e:
                print(f"Error preprocessing improved rubric: {e}")
                return basic_rubric
                
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return basic_rubric


def find_all_problems() -> List[str]:
    """Find all problem directories in the dataset."""
    problem_dirs = []
    
    # Walk through the dataset directory
    for category_dir in glob.glob(os.path.join(DATASET_DIR, "*")):
        if os.path.isdir(category_dir):
            # Look for problem directories in each category
            for problem_dir in glob.glob(os.path.join(category_dir, "*")):
                if os.path.isdir(problem_dir) and os.path.exists(os.path.join(problem_dir, "Question.txt")):
                    problem_dirs.append(problem_dir)
    
    return problem_dirs


def main():
    """Main function to generate rubrics for all problems."""
    print("AutoRubric Generator")
    print("===================")
    
    # Find all problem directories
    problem_dirs = find_all_problems()
    print(f"Found {len(problem_dirs)} problems in the dataset.")
    
    # Generate rubrics for each problem
    for problem_dir in problem_dirs:
        # If OpenAI API key is provided, use enhanced generator
        if OPENAI_API_KEY:
            generator = EnhancedRubricGenerator(problem_dir)
        else:
            generator = RubricGenerator(problem_dir)
            
        generator.run()
    
    print("\nRubric generation complete!")


if __name__ == "__main__":
    main() 