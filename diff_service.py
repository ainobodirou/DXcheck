from models import DependencyGraph,Component, NodeChanges, EdgeChanges, ChangeType, GraphDiff

class DiffService():

    ## Normalize graphs: constructed DependancyGraph contains version suffixes in nodes keys.
    ## while version is also contained in component model field.
    ## version upgrade of the same component is not component removal or addition
    ## to effectively compare diff of two dependancy graphs ->
    ## create deduplicated collections of graph nodes and edges by component name

    def normalize_graph(self, graph: DependencyGraph) -> DependencyGraph:

        norm_nodes: dict[str, Component] = {}
        norm_edges: set[tuple[str,str]] = set()
        ref_mapping: dict[str,str] = {}

        for bom_ref, component in graph.nodes.items():
            norm_key = component.purl.split("@",1)[0]

            if norm_key in norm_nodes:
                raise ValueError(f"Duplicate package identity: {norm_key}")
            
            norm_nodes[norm_key] = component
            ref_mapping[bom_ref] = norm_key

        for source, target in graph.edges:
            norm_edges.add((
                ref_mapping[source],
                ref_mapping[target]
            ))

        return DependencyGraph(
            nodes = norm_nodes,
            edges = norm_edges
        )

    def _compare_nodes(self, base: DependencyGraph, head: DependencyGraph) -> list[NodeChanges]:
        base_keys = base.nodes.keys()
        head_keys = head.nodes.keys()
        changes: list[NodeChanges] = []

        for key in base_keys & head_keys:
            if base.nodes[key].version != head.nodes[key].version:
                changes.append(
                    NodeChanges(
                        name = head.nodes[key].name,
                        purl = head.nodes[key].purl,
                        change_type=ChangeType.UPDATED,
                        previous_version=base.nodes[key].version,
                        new_version=head.nodes[key].version
                    )
                )

        added_nodes = head_keys - base_keys
        removed_nodes = base_keys - head_keys 

        for key in sorted(added_nodes):
            component = head.nodes[key]
            changes.append(
                NodeChanges(
                    name=component.name,
                    purl=component.purl,
                    change_type=ChangeType.ADDED,
                    new_version=component.version
                )
            )
        for key in sorted(removed_nodes):
            component = base.nodes[key]
            changes.append(
                NodeChanges(
                    name = component.name,
                    purl = component.purl,
                    change_type=ChangeType.REMOVED,
                    previous_version=component.version
                )
            )
        return changes

    def _compare_edges(self, base: DependencyGraph, head: DependencyGraph) -> list[EdgeChanges]:

        added_edges = head.edges - base.edges
        removed_edges = base.edges - head.edges 
        changes: list[EdgeChanges] = []

        for source, target in added_edges:
            changes.append(
                EdgeChanges(
                    source = source,
                    target = target,
                    change_type=ChangeType.ADDED
                )
            )
        for source,target in removed_edges:
            changes.append(
                EdgeChanges(
                    source = source,
                    target = target,
                    change_type=ChangeType.REMOVED
                )
            )
        return changes

    def get_diff(self, base: DependencyGraph, head: DependencyGraph) -> GraphDiff:

        norm_base = self.normalize_graph(base)
        norm_head = self.normalize_graph(head)

        node_changes = self._compare_nodes(norm_base, norm_head)
        edge_chagnes = self._compare_edges(norm_base, norm_head)

        return GraphDiff(
            node_changes=node_changes,
            edge_changes=edge_chagnes
        )



        











 



