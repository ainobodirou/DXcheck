from models import Component, DependencyGraph

class GraphBuilder:

        
    def _extract_nodes(
        self, sbom: dict
    ) -> dict[str, Component]:
        nodes: dict[str, Component] = {}
        for c in sbom["components"]:
            component = Component(
                bom_ref=c["bom-ref"],
                purl=c["purl"],
                name=c["name"],
                version=c["version"]
                )
            nodes[component.bom_ref] = component
        return nodes 

    def _extract_edges(
        self, sbom: dict
    ) -> set[tuple[str, str]]:
        edges: set[tuple[str,str]] = set()
        for d in sbom.get("dependencies", []):
            source = d["ref"]
            for target in d.get("dependsOn", []):
                edges.add((source,target))
        return edges

    def build(self, sbom: dict) -> DependencyGraph:
        nodes= self._extract_nodes(sbom)
        edges = self._extract_edges(sbom)

        self._validate_graph(nodes, edges)
        return DependencyGraph(
            nodes = nodes,
            edges = edges
            )

        

    def _validate_graph(self,
                    nodes: dict[str, Component],
                    edges: set[tuple[str,str]]) -> None:
        for source, target in edges:
            if source not in nodes or target not in nodes:
                raise ValueError(f"Invalid Dependancy edge: {source} -> {target}")
     

