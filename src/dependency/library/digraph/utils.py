from dependency.core.injection import Injectable, ProviderInjection

def find_first_parent(
    provider: ProviderInjection,
    visited: set[ProviderInjection] | None = None,
    injectable_to_provider: dict[Injectable, ProviderInjection] = {},
) -> str:
    if visited is None:
        visited = set()
    if provider in visited:
        return "fallback"
    visited.add(provider)

    if provider.parent is not None:
        if provider.parent.name not in ("RootInternal", "FallbackInternal"):
            return provider.parent.name

    scores: dict[str, int] = {}
    for dependent in provider.injectable.dependent:
        dep_provider = injectable_to_provider.get(dependent)
        if dep_provider is None:
            continue
        result = find_first_parent(dep_provider, visited, injectable_to_provider)
        if result != "fallback":
            scores[result] = scores.get(result, 0) + 1

    if scores:
        return max(scores, key=lambda k: scores[k])
    return "fallback"
