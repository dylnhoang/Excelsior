def validate_action_schema(action: dict, df_columns: list[str]) -> tuple[bool, str]:
    """
    Validates that the action has the expected keys and values.
    Returns (True, "") if valid, or (False, error_message) if not.
    """
    required_keys = {
        "sort": ["column"],
        "filter": ["column", "condition"],
        "update": ["column", "value"],
    }

    operation = action.get("operation")
    if not operation or operation not in required_keys:
        return False, f"Invalid or missing 'operation'. Got: {operation}"

    # Required keys for this operation
    for key in required_keys[operation]:
        if key not in action:
            return False, f"Missing key '{key}' for operation '{operation}'"

    # Column validity
    column = action.get("column")
    if column and column not in df_columns:
        return False, f"Column '{column}' not found in Excel sheet."

    # Filter condition structure
    if operation == "filter":
        cond = action.get("condition")
        if not isinstance(cond, dict):
            return False, "'condition' must be a dictionary"
        if "operator" not in cond or "value" not in cond:
            return False, "Filter condition must have 'operator' and 'value'"
        if cond["operator"] not in [">", "<", "==", "!="]:
            return False, f"Unsupported operator: {cond['operator']}"

    return True, ""