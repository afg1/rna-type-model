import networkx as nx


import obonet

SO_GRAPH = obonet.read_obo("./rna_type/utils/so.obo")

BASE_SO_TERMS = ["SO:0000655", "SO:0000188", "SO:0000836", "SO:0000673"]

NCBI_GRAPH = obonet.read_obo("./rna_type/utils/ncbitaxon.obo")


def specificity(term: str) -> int:
    """
    Get the 'specificity' of a given term. This is basically the minimum path length from a base term to
    the term in question through the SO.

    NaN signifies no path
    """
    spec = 9999
    for base in BASE_SO_TERMS:
        try:
            path = nx.shortest_path(SO_GRAPH, term, base)
            dist = len(path)
        except nx.NetworkXNoPath:
            continue
        if spec > dist:
            spec = dist

    if spec == 9999:
        return np.nan
    else:
        return spec


def is_child_of(parent: str, child: str) -> bool:
    """
    Is child a child of the proposed parent node?
    """
    return child in list(nx.ancestors(SO_GRAPH, parent))


def lowest_common_ancestor(node1, node2) -> str:
    """
    Need to rewrite the lca algorithm since the ontology works upsode down
    """
    ## Get the nodes in the path from root to each node
    path_1 = nx.descendants(NCBI_GRAPH, node1)
    path_2 = nx.descendants(NCBI_GRAPH, node2)

    ## intersect the sets to find the common nodes
    common_path = path_1.intersection(path_2)

    ## now find the path length from root for each common node -
    ## longest is the lowest common ancestor
    lengths = {
        len(nx.shortest_path(NCBI_GRAPH, p, "NCBITaxon:1")): p for p in common_path
    }

    longest = max(lengths.keys())

    lca = NCBI_GRAPH.nodes[lengths[longest]]

    return lca


def distance(graph: nx.MultiDiGraph, node1: str, node2: str) -> int:
    """
    Calculate the distance through the graph from one node to another

        |            |
        |           / \
       / \         |   \
      /   \       / \   \
      A    B     C  D   E

    A-B distance should be 4 (2 up, 2 down)
    C-D distance should be 2 (1 up, 1 down)
    C-E distance should be 6 (3 up, 3 down)
    """
    path_1 = nx.descendants(graph, node1)
    path_2 = nx.descendants(graph, node2)
    uncommon_path = path_1.symmetric_difference(path_2)  ## XOR operation

    ## This will exclude the lowest common ancestor, so add 1 to get
    ## the right distance
    return len(uncommon_path) + 1


def same_domain(accession: str, model: str) -> bool:
    """
    Is the accession in the same domain as the model?

    Use superkingdom taxrank instead of domain

    TODO: check this works ok for viruses!
    """
    ## Get the nodes in the path from root to each node
    try:
        path_1 = nx.descendants(NCBI_GRAPH, f"NCBITaxon:{accession}")
        path_2 = nx.descendants(NCBI_GRAPH, f"NCBITaxon:{model}")
    except nx.exception.NetworkXError as e:
        return False

    ## intersect the sets to find the common nodes
    common_path = path_1.intersection(path_2)

    ## Loop on the common nodes and look for a superkingdom node
    for node in common_path:
        if (
            "NCBITaxon:superkingdom"
            in NCBI_GRAPH.nodes[node].get("property_value", [""])[0]
        ):
            return True
    return False
