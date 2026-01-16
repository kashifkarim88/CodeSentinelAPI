import difflib

def generate_diff(original: str, fixed: str) -> str:
    # Ensure both inputs are strings to avoid "'dict' object has no attribute 'splitlines'"
    if not isinstance(original, str):
        original = str(original) if original is not None else ""
        
    if not isinstance(fixed, str):
        # If 'fixed' is a dict or None, convert it to a string or empty string
        fixed = str(fixed) if fixed is not None else ""

    diff = difflib.unified_diff(
        original.splitlines(),
        fixed.splitlines(),
        fromfile="Original",
        tofile="Fixed",
        lineterm=""
    )
    return "\n".join(diff)