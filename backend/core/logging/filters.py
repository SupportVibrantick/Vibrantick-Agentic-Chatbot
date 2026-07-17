def context_filter(context: str):
    def filter(record):
        return record["extra"].get("context") == context

    return filter