def needs_clarification(entities: dict):
    missing = [k for k, v in entities.items() if v is None]
    return len(missing) > 0
