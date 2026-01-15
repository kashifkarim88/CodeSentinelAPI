import difflib

def generate_diff(original: str, fixed: str) -> str:
    diff = difflib.unified_diff(
        original.splitlines(),
        fixed.splitlines(),
        fromfile="Original",
        tofile="Fixed",
        lineterm=""
    )
    return "\n".join(diff)