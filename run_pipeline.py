#!/usr/bin/env python
import os
import sys
import subprocess
import argparse
import time

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)

def run_command(command):
    """Run a shell command and print its output."""
    print(f"Running: {command}")
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    
    # Print output in real-time
    for line in process.stdout:
        print(line.strip())
        
    process.wait()
    return process.returncode

def main():
    """Run the full AutoRubric pipeline."""
    parser = argparse.ArgumentParser(description="Run the full AutoRubric pipeline")
    parser.add_argument("--openai-key", help="OpenAI API key for enhanced rubrics")
    parser.add_argument("--skip-rubric-gen", action="store_true", help="Skip rubric generation step")
    parser.add_argument("--skip-grading", action="store_true", help="Skip grading step")
    args = parser.parse_args()
    
    # Make sure required directories exist
    os.makedirs("generated_rubrics", exist_ok=True)
    os.makedirs("grading_results", exist_ok=True)
    
    start_time = time.time()
    
    # Step 1: Generate rubrics (if not skipped)
    if not args.skip_rubric_gen:
        print_header("STEP 1: GENERATING RUBRICS")
        
        # Inject OpenAI API key if provided
        if args.openai_key:
            with open("auto_rubric_generator.py", "r") as f:
                content = f.read()
                
            content = content.replace('OPENAI_API_KEY = ""', f'OPENAI_API_KEY = "{args.openai_key}"')
                
            with open("auto_rubric_generator.py", "w") as f:
                f.write(content)
            
            print("OpenAI API key set for enhanced rubric generation.")
        
        # Run the rubric generator
        return_code = run_command("python auto_rubric_generator.py")
        if return_code != 0:
            print("ERROR: Rubric generation failed!")
            return 1
    else:
        print_header("STEP 1: RUBRIC GENERATION SKIPPED")
    
    # Step 2: Grade submissions (if not skipped)
    if not args.skip_grading:
        print_header("STEP 2: GRADING SUBMISSIONS")
        
        # Run the auto grader
        return_code = run_command("python auto_grader.py")
        if return_code != 0:
            print("ERROR: Grading failed!")
            return 1
    else:
        print_header("STEP 2: GRADING SKIPPED")
    
    # Step 3: Generate summary report
    print_header("STEP 3: GENERATING SUMMARY REPORT")
    
    # Run the report generator (you would need to implement this)
    return_code = run_command("python generate_report.py")
    if return_code != 0:
        print("WARNING: Report generation failed or not implemented!")
    
    # Done!
    elapsed_time = time.time() - start_time
    print_header(f"PIPELINE COMPLETE in {elapsed_time:.2f} seconds")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 