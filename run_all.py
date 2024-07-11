import subprocess

scripts = [
    "processes/1_start.py",
    "processes/2_separate.py",
    "processes/3_merge.py",
    "processes/4_create_df.py",
    "processes/5_remove_break_rounds.py",
    "processes/6_no_blanks.py",
    "processes/7_player_performance_per_round.py",
    "processes/8_round_score_summary.py",
    "processes/9_ignore_suicides.py",
    "processes/10_player_performance_per_round_adjusted.py",
    "processes/11_round_score_summary_suicide_adjusted.py"
]

for script in scripts:
    print(f"Running {script}...")
    result = subprocess.run(["python3", script], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running {script}: {result.stderr}")
    else:
        print(f"{script} completed successfully.")
    print(result.stdout)