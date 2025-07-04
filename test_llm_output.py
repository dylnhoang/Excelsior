from services.formula_generator import generate_action_from_prompt

prompt = "Filter all rows where Profit is greater than 300"
result = generate_action_from_prompt(prompt)

print("[FINAL OUTPUT]", result)