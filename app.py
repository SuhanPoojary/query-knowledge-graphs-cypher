import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
from fpdf import FPDF
from datetime import datetime
from io import BytesIO
import html
import random
import re

# ============================================================
# VIRTUAL LAB: QUERY KNOWLEDGE GRAPHS USING CYPHER
# IIT Kharagpur-inspired academic layout (original implementation)
# ============================================================

st.set_page_config(
    page_title="Query Knowledge Graphs using Cypher | Virtual Lab",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------- STYLE -----------------------------
st.markdown("""
<style>
/* Overall academic / legacy VLab-inspired appearance */
html, body, [class*="css"] {
    font-family: Arial, Helvetica, sans-serif;
}

.stApp {
    background: #ffffff;
}

/* Hide Streamlit's default chrome where possible */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Top Virtual Labs bar */
.vlab-top {
    margin: -1rem -1rem 0 -1rem;
    height: 82px;
    border-bottom: 5px solid #f36f21;
    display: flex;
    align-items: center;
    padding: 0 28px;
    background: #ffffff;
}

.vlab-logo {
    width: 55px;
    height: 55px;
    border: 3px solid #74b82a;
    border-radius: 10px;
    margin-right: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #74b82a;
    font-size: 27px;
    font-weight: bold;
}

.vlab-brand {
    line-height: 1.0;
}

.vlab-brand .title {
    color: #2e86c1;
    font-size: 27px;
    font-weight: 600;
}

.vlab-brand .subtitle {
    color: #777777;
    font-size: 10px;
    margin-top: 5px;
}

.vlab-exp-title {
    margin-left: auto;
    text-align: right;
    color: #2e86c1;
    font-size: 18px;
    font-weight: 500;
}

/* Breadcrumb */
.breadcrumb {
    margin: 25px 0 12px 0;
    color: #2e86c1;
    font-size: 17px;
}
.breadcrumb span {
    color: #777;
}

/* Main title */
.page-title {
    color: #2e86c1;
    font-size: 30px;
    font-weight: 500;
    text-align: center;
    padding: 8px 0 14px 0;
    border-bottom: 1px solid #dddddd;
}

/* Section headings */
.vlab-h2 {
    color: #2e86c1;
    font-size: 25px;
    font-weight: 500;
    border-bottom: 1px solid #dddddd;
    padding-bottom: 8px;
    margin-top: 25px;
    margin-bottom: 18px;
}

.vlab-h3 {
    color: #333333;
    font-size: 19px;
    font-weight: 600;
    margin-top: 18px;
}

/* Academic content */
.vlab-text {
    color: #222222;
    font-size: 16px;
    line-height: 1.65;
}

.vlab-note {
    background: #f7fbfd;
    border-left: 4px solid #2e86c1;
    padding: 12px 16px;
    margin: 14px 0;
    color: #333;
}

.vlab-aim {
    background: #fffaf5;
    border-left: 4px solid #f36f21;
    padding: 15px 18px;
    font-size: 17px;
    line-height: 1.6;
}

/* Tables */
.vlab-table {
    border-collapse: collapse;
    width: 100%;
}
.vlab-table th {
    background: #2e86c1;
    color: white;
    padding: 9px;
    text-align: left;
}
.vlab-table td {
    border: 1px solid #d8d8d8;
    padding: 8px;
}

/* Simulation work area */
.sim-box {
    border: 1px solid #bfcbd4;
    background: #fbfdfe;
    padding: 16px;
    margin: 10px 0 18px 0;
}

.query-box {
    border: 1px solid #c8d6df;
    background: #f8fbfd;
    padding: 4px;
    margin: 12px 0;
}

.cypher-query {
    background: #f4f7f9;
    border: 1px solid #c8d6df;
    border-radius: 3px;
    color: #1f2933;
    font-family: Consolas, "Courier New", monospace;
    font-size: 14px;
    line-height: 1.6;
    overflow: visible;
    padding: 14px 16px;
    white-space: pre-wrap;
}

.cypher-keyword {
    border-bottom: 2px dotted #f36f21;
    color: #236b9d;
    cursor: help;
    font-weight: 700;
    position: relative;
}

.cypher-keyword::after {
    background: #263238;
    border-radius: 3px;
    top: calc(100% + 8px);
    color: #ffffff;
    content: attr(data-definition);
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12px;
    font-weight: 400;
    left: 50%;
    line-height: 1.35;
    opacity: 0;
    padding: 7px 9px;
    pointer-events: none;
    position: absolute;
    transform: translateX(-50%) translateY(4px);
    transition: opacity 0.15s ease, transform 0.15s ease;
    visibility: hidden;
    white-space: normal;
    width: 190px;
    z-index: 10;
}

.cypher-keyword:hover::after {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
    visibility: visible;
}

.result-box {
    border: 1px solid #b9d7b0;
    background: #fbfff9;
    padding: 14px;
}

/* Streamlit widget adjustments */
div[data-testid="stButton"] > button {
    border-radius: 2px;
    border: 1px solid #2e86c1;
    background: #2e86c1;
    color: white;
    font-weight: 500;
}

div[data-testid="stButton"] > button:hover {
    background: #236b9d;
    border-color: #236b9d;
}

[data-testid="stSidebar"] {
    background: #fafafa;
    border-right: 1px solid #dddddd;
}

[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #2e86c1;
}

/* Footer */
.vlab-footer {
    margin-top: 45px;
    padding: 15px;
    border-top: 4px solid #f36f21;
    text-align: center;
    color: #777;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

# ------------------------- DATA ------------------------------
NODES = [
    {"id": "alice", "label": "Student", "name": "Alice", "year": 3, "branch": "Computer Engineering"},
    {"id": "bob", "label": "Student", "name": "Bob", "year": 3, "branch": "Computer Engineering"},
    {"id": "charlie", "label": "Student", "name": "Charlie", "year": 4, "branch": "Computer Engineering"},
    {"id": "python", "label": "Course", "name": "Python", "credits": 4},
    {"id": "ml", "label": "Course", "name": "Machine Learning", "credits": 4},
    {"id": "graph", "label": "Course", "name": "Graph Analytics", "credits": 3},
    {"id": "college", "label": "Institution", "name": "Tech University"},
    {"id": "tcs", "label": "Company", "name": "TCS"},
]

EDGES = [
    ("alice", "ENROLLED_IN", "python"),
    ("alice", "ENROLLED_IN", "ml"),
    ("bob", "ENROLLED_IN", "ml"),
    ("bob", "ENROLLED_IN", "graph"),
    ("charlie", "ENROLLED_IN", "graph"),
    ("python", "RELATED_TO", "ml"),
    ("ml", "RELATED_TO", "graph"),
    ("alice", "STUDIES_AT", "college"),
    ("bob", "STUDIES_AT", "college"),
    ("charlie", "STUDIES_AT", "college"),
    ("charlie", "WORKED_AT", "tcs"),
]

NODE_BY_ID = {n["id"]: n for n in NODES}


def graph_from_csv(uploaded_file):
    """Build the lab graph from a relationship edge-list CSV."""
    frame = pd.read_csv(uploaded_file)
    required = {"source", "relationship", "target"}
    missing = required.difference(frame.columns)
    if missing:
        missing_columns = ", ".join(sorted(missing))
        raise ValueError(f"Missing required column(s): {missing_columns}")
    if frame.empty:
        raise ValueError("The CSV file does not contain any relationships.")

    nodes = {}

    def add_node(node_id, label, name):
        node_id = str(node_id).strip()
        if not node_id or node_id.lower() == "nan":
            raise ValueError("Node IDs cannot be empty.")
        nodes.setdefault(node_id, {
            "id": node_id,
            "label": str(label).strip() if pd.notna(label) else "Entity",
            "name": str(name).strip() if pd.notna(name) else node_id
        })

    edges = []
    for _, row in frame.iterrows():
        source = str(row["source"]).strip()
        target = str(row["target"]).strip()
        relationship = str(row["relationship"]).strip().upper()
        if not source or not target or not relationship:
            raise ValueError("Each row needs source, relationship and target values.")

        add_node(source, row.get("source_label"), row.get("source_name"))
        add_node(target, row.get("target_label"), row.get("target_name"))
        edges.append((source, relationship, target))

    return list(nodes.values()), edges

TITLE = "Query Knowledge Graphs using Cypher"

AIM = (
    "To understand and demonstrate how Cypher queries can be used to retrieve "
    "nodes, relationships and multi-hop connections from a knowledge graph."
)

REAL_WORLD_APPLICATIONS = [
    "Recommendation systems connect people, products, films or courses to suggest relevant items.",
    "Fraud detection follows networks of accounts, devices, merchants and transactions to reveal suspicious paths.",
    "Healthcare knowledge graphs connect patients, symptoms, medicines and research to support clinical discovery.",
    "Search engines use entities and relationships to understand people, places, organisations and topics.",
    "Social and professional platforms analyse connections to identify communities, experts and useful introductions.",
    "Supply-chain systems trace suppliers, parts, shipments and dependencies to locate delays or risks.",
]

OBJECTIVES = [
    "Understand nodes, labels, relationships and properties in a knowledge graph.",
    "Understand the basic syntax and purpose of the Cypher query language.",
    "Retrieve nodes and selected properties using Cypher patterns.",
    "Retrieve relationships between connected entities.",
    "Perform multi-hop traversal to discover indirect connections.",
    "Interpret graph-query results as meaningful information."
]

INTRODUCTION = """
A knowledge graph represents information as entities and the relationships
between those entities. In a graph, **nodes** represent entities, **relationships**
represent connections, and **properties** store attributes of nodes or relationships.

Cypher is a declarative graph query language used to describe graph patterns.
Instead of specifying a low-level traversal algorithm, the user describes the
pattern to be found and the information to return.

This Virtual Lab uses a small education-domain graph containing students,
courses, an institution and a company. It is intentionally small so that the
relationships and query results can be understood visually during an experiment.

The same ideas are used in real-world systems. Recommendation engines traverse
connections between users and products; fraud-monitoring systems follow links
between accounts, devices and transactions; healthcare knowledge graphs connect
symptoms, medicines and research; and search engines use entity relationships to
return more meaningful results. Learning Cypher therefore provides a practical
way to explore how connected data supports decisions in many domains.
"""

THEORY_SECTIONS = [
    ("Knowledge Graph", """
A knowledge graph stores connected information in the form of nodes and
relationships. For example, a Student can be connected to a Course through
an `ENROLLED_IN` relationship.
"""),
    ("Nodes and Labels", """
A node represents an entity. A label classifies a node. In this experiment,
`Student`, `Course`, `Institution`, and `Company` are labels.
"""),
    ("Relationships", """
A relationship represents a typed connection between two nodes. Examples in
this graph include `ENROLLED_IN`, `RELATED_TO`, `STUDIES_AT`, and `WORKED_AT`.
"""),
    ("Properties", """
Properties are key-value attributes. Alice has properties such as `name`,
`year`, and `branch`; a Course can have `name` and `credits`.
"""),
    ("Cypher MATCH and RETURN", """
`MATCH` is used to find graph patterns and `RETURN` specifies the information
to display.

Example:
`MATCH (s:Student) RETURN s`
"""),
    ("Filtering with WHERE", """
`WHERE` applies a condition to matched data.

Example:
`MATCH (s:Student) WHERE s.year = 3 RETURN s`
"""),
    ("Multi-hop Connections", """
A multi-hop query follows more than one relationship. For example:

`(s:Student)-[:ENROLLED_IN]->(c:Course)-[:RELATED_TO]->(c2:Course)`

This can reveal a related course indirectly connected to a student.
""")
]

PROCEDURE = [
    "Read the Aim, Introduction and Theory sections.",
    "Study the nodes, labels, properties and relationships in the sample graph.",
    "Open Simulation and select a Cypher query.",
    "Read the generated query and predict what it should return.",
    "Execute the query and inspect the result table.",
    "For relationship queries, inspect the highlighted graph path.",
    "Perform at least four different queries, including one multi-hop query.",
    "Record the trials and download the CSV if required.",
    "Complete the Exercises and Posttest.",
    "Generate the final PDF report."
]

QUERY_DEFS = {
    "Q1 — Retrieve all students": {
        "cypher": "MATCH (s:Student) RETURN s",
        "concept": "Node retrieval",
        "description": "Retrieves all nodes having the Student label."
    },
    "Q2 — Retrieve all courses": {
        "cypher": "MATCH (c:Course) RETURN c",
        "concept": "Label-based retrieval",
        "description": "Retrieves all Course nodes."
    },
    "Q3 — Retrieve Alice": {
        "cypher": 'MATCH (s:Student {name: "Alice"}) RETURN s',
        "concept": "Property matching",
        "description": "Matches the Student node whose name property is Alice."
    },
    "Q4 — Retrieve Alice's properties": {
        "cypher": 'MATCH (s:Student {name: "Alice"}) RETURN s.name, s.year, s.branch',
        "concept": "Property projection",
        "description": "Returns selected properties instead of the entire node."
    },
    "Q5 — Courses enrolled by Alice": {
        "cypher": 'MATCH (s:Student {name: "Alice"})-[:ENROLLED_IN]->(c:Course) RETURN s, c',
        "concept": "Relationship traversal",
        "description": "Follows Alice's ENROLLED_IN relationships to her courses."
    },
    "Q6 — All student-course relationships": {
        "cypher": "MATCH (s:Student)-[r:ENROLLED_IN]->(c:Course) RETURN s, r, c",
        "concept": "Relationship retrieval",
        "description": "Retrieves every Student → Course ENROLLED_IN connection."
    },
    "Q7 — Third-year students": {
        "cypher": "MATCH (s:Student) WHERE s.year = 3 RETURN s",
        "concept": "WHERE filtering",
        "description": "Returns students whose year property is 3."
    },
    "Q8 — Courses related to Machine Learning": {
        "cypher": 'MATCH (c:Course {name: "Machine Learning"})-[:RELATED_TO]->(c2:Course) RETURN c, c2',
        "concept": "Relationship pattern",
        "description": "Finds courses directly related to Machine Learning."
    },
    "Q9 — Two-hop discovery from Alice": {
        "cypher": 'MATCH (s:Student {name: "Alice"})-[:ENROLLED_IN]->(c:Course)-[:RELATED_TO]->(c2:Course) RETURN s, c, c2',
        "concept": "Two-hop traversal",
        "description": "Finds a course related to a course in which Alice is enrolled."
    },
    "Q10 — Return the multi-hop path": {
        "cypher": 'MATCH p=(s:Student {name: "Alice"})-[:ENROLLED_IN]->(c:Course)-[:RELATED_TO]->(c2:Course) RETURN p',
        "concept": "Path retrieval",
        "description": "Returns the complete Student → Course → Related Course path."
    },
    "Q11 — Students and their institution": {
        "cypher": "MATCH (s:Student)-[:STUDIES_AT]->(i:Institution) RETURN s, i",
        "concept": "Connected entity retrieval",
        "description": "Retrieves students and the institution they study at."
    },
    "Q12 — Students sharing an institution": {
        "cypher": "MATCH (s1:Student)-[:STUDIES_AT]->(i:Institution)<-[:STUDIES_AT]-(s2:Student) RETURN s1, i, s2",
        "concept": "Shared connection",
        "description": "Finds students connected through the same institution."
    },
    "Q13 — Charlie's work connection": {
        "cypher": 'MATCH (s:Student {name: "Charlie"})-[:WORKED_AT]->(c:Company) RETURN s, c',
        "concept": "Relationship retrieval",
        "description": "Retrieves Charlie's WORKED_AT connection."
    }
}

ACTIVE_QUERY_SPECS = {}


def build_csv_query_defs(nodes, edges):
    """Create query choices that match the labels and relationships in a CSV graph."""
    query_defs = {
        "CSV 1 — Retrieve all nodes": {
            "cypher": "MATCH (n) RETURN n",
            "concept": "Node retrieval",
            "description": "Retrieves every node in the uploaded graph.",
            "kind": "all_nodes"
        },
        "CSV 2 — Retrieve all relationships": {
            "cypher": "MATCH (a)-[r]->(b) RETURN a, r, b",
            "concept": "Relationship retrieval",
            "description": "Retrieves every relationship in the uploaded graph.",
            "kind": "all_edges"
        },
        "CSV 3 — Discover two-hop paths": {
            "cypher": "MATCH p=(a)-[r1]->(b)-[r2]->(c) RETURN p",
            "concept": "Multi-hop traversal",
            "description": "Finds paths that cross two consecutive relationships in the uploaded graph.",
            "kind": "two_hop"
        }
    }
    specs = {
        "CSV 1 — Retrieve all nodes": "all_nodes",
        "CSV 2 — Retrieve all relationships": "all_edges",
        "CSV 3 — Discover two-hop paths": "two_hop"
    }

    labels = sorted({node["label"] for node in nodes})
    for index, label in enumerate(labels, start=4):
        name = f"CSV {index} — Retrieve {label} nodes"
        query_defs[name] = {
            "cypher": f"MATCH (n:{label}) RETURN n",
            "concept": "Label-based retrieval",
            "description": f"Retrieves all nodes with the {label} label from the uploaded graph.",
            "kind": "label",
            "label": label
        }
        specs[name] = ("label", label)

    relationships = sorted({edge[1] for edge in edges})
    offset = len(labels) + 4
    for index, relationship in enumerate(relationships, start=offset):
        name = f"CSV {index} — Retrieve {relationship} relationships"
        query_defs[name] = {
            "cypher": f"MATCH (a)-[r:{relationship}]->(b) RETURN a, r, b",
            "concept": "Relationship traversal",
            "description": f"Retrieves every {relationship} relationship from the uploaded graph.",
            "kind": "relationship",
            "relationship": relationship
        }
        specs[name] = ("relationship", relationship)

    return query_defs, specs

CYPHER_KEYWORDS = {
    "MATCH": "Finds graph patterns that match the data.",
    "OPTIONAL MATCH": "Finds a pattern when possible without removing unmatched rows.",
    "WHERE": "Filters matched rows using a condition.",
    "RETURN": "Chooses the values or graph elements to display.",
    "CREATE": "Creates new nodes or relationships.",
    "MERGE": "Matches an existing pattern or creates it when absent.",
    "DELETE": "Deletes matched nodes or relationships.",
    "DETACH DELETE": "Deletes a node and its connected relationships.",
    "SET": "Adds or updates node and relationship properties.",
    "REMOVE": "Removes a property or label.",
    "WITH": "Passes selected results to the next query part.",
    "UNWIND": "Expands a list into separate rows.",
    "ORDER BY": "Sorts the returned results.",
    "LIMIT": "Restricts the number of returned rows.",
    "SKIP": "Skips a specified number of returned rows.",
    "AS": "Assigns an alias to a returned expression."
}


def render_cypher_query(query):
    """Render Cypher with hover definitions for recognized keywords."""
    escaped_query = html.escape(query)
    keyword_pattern = r"\b(?:" + "|".join(
        re.escape(keyword) for keyword in sorted(CYPHER_KEYWORDS, key=len, reverse=True)
    ) + r")\b"

    def replace_keyword(match):
        keyword = match.group(0)
        definition = html.escape(CYPHER_KEYWORDS[keyword])
        return (
            f'<span class="cypher-keyword" title="{definition}" data-definition="{definition}">'
            f"{keyword}</span>"
        )

    return re.sub(keyword_pattern, replace_keyword, escaped_query)

# ---------------------- QUERY ENGINE -------------------------
def execute_query(name):
    if name in ACTIVE_QUERY_SPECS:
        spec = ACTIVE_QUERY_SPECS[name]
        if spec == "all_nodes":
            return NODES, [], "All nodes in the uploaded graph were retrieved."
        if spec == "all_edges":
            rows = [
                {
                    "source": NODE_BY_ID[source]["name"],
                    "relationship": relationship,
                    "target": NODE_BY_ID[target]["name"]
                }
                for source, relationship, target in EDGES
            ]
            return rows, EDGES, "All relationships in the uploaded graph were retrieved."
        if spec == "two_hop":
            paths = [
                (first, second)
                for first in EDGES
                for second in EDGES
                if first[2] == second[0]
            ]
            rows = [
                {
                    "source": NODE_BY_ID[first[0]]["name"],
                    "first_relationship": first[1],
                    "middle": NODE_BY_ID[first[2]]["name"],
                    "second_relationship": second[1],
                    "target": NODE_BY_ID[second[2]]["name"]
                }
                for first, second in paths
            ]
            path_edges = [edge for path in paths for edge in path]
            return rows, path_edges, "Two-hop paths in the uploaded graph were retrieved."

        kind, value = spec
        if kind == "label":
            rows = [node for node in NODES if node["label"] == value]
            return rows, [], f"All {value} nodes in the uploaded graph were retrieved."
        if kind == "relationship":
            selected_edges = [edge for edge in EDGES if edge[1] == value]
            rows = [
                {
                    "source": NODE_BY_ID[source]["name"],
                    "relationship": relationship,
                    "target": NODE_BY_ID[target]["name"]
                }
                for source, relationship, target in selected_edges
            ]
            return rows, selected_edges, f"All {value} relationships in the uploaded graph were retrieved."

    if name == "Q1 — Retrieve all students":
        rows = [n for n in NODES if n["label"] == "Student"]
        return rows, [], "All Student nodes were retrieved."

    if name == "Q2 — Retrieve all courses":
        rows = [n for n in NODES if n["label"] == "Course"]
        return rows, [], "All Course nodes were retrieved."

    if name == "Q3 — Retrieve Alice":
        return [NODE_BY_ID["alice"]], [], "Alice was matched by the name property."

    if name == "Q4 — Retrieve Alice's properties":
        n = NODE_BY_ID["alice"]
        return [{"name": n["name"], "year": n["year"], "branch": n["branch"]}], [], "Selected properties were returned."

    if name == "Q5 — Courses enrolled by Alice":
        es = [e for e in EDGES if e[0] == "alice" and e[1] == "ENROLLED_IN"]
        rows = [{"student": NODE_BY_ID[e[0]]["name"], "course": NODE_BY_ID[e[2]]["name"]} for e in es]
        return rows, es, "Alice's ENROLLED_IN relationships were traversed."

    if name == "Q6 — All student-course relationships":
        es = [e for e in EDGES if e[1] == "ENROLLED_IN"]
        rows = [{"student": NODE_BY_ID[e[0]]["name"], "relationship": e[1], "course": NODE_BY_ID[e[2]]["name"]} for e in es]
        return rows, es, "All ENROLLED_IN relationships were retrieved."

    if name == "Q7 — Third-year students":
        rows = [n for n in NODES if n["label"] == "Student" and n["year"] == 3]
        return rows, [], "Students satisfying year = 3 were returned."

    if name == "Q8 — Courses related to Machine Learning":
        es = [e for e in EDGES if e[0] == "ml" and e[1] == "RELATED_TO"]
        rows = [{"course": NODE_BY_ID[e[0]]["name"], "related_course": NODE_BY_ID[e[2]]["name"]} for e in es]
        return rows, es, "The RELATED_TO connection from Machine Learning was retrieved."

    if name in ["Q9 — Two-hop discovery from Alice", "Q10 — Return the multi-hop path"]:
        paths = []
        for e1 in EDGES:
            if e1[0] == "alice" and e1[1] == "ENROLLED_IN":
                for e2 in EDGES:
                    if e2[0] == e1[2] and e2[1] == "RELATED_TO":
                        paths.append((e1, e2))
        rows = [{
            "student": "Alice",
            "course": NODE_BY_ID[a[2]]["name"],
            "related_course": NODE_BY_ID[b[2]]["name"]
        } for a, b in paths]
        es = [e for pair in paths for e in pair]
        return rows, es, "A two-hop Student → Course → Related Course path was traversed."

    if name == "Q11 — Students and their institution":
        es = [e for e in EDGES if e[1] == "STUDIES_AT"]
        rows = [{"student": NODE_BY_ID[e[0]]["name"], "institution": NODE_BY_ID[e[2]]["name"]} for e in es]
        return rows, es, "Students connected to the institution were retrieved."

    if name == "Q12 — Students sharing an institution":
        es = [e for e in EDGES if e[1] == "STUDIES_AT"]
        rows = []
        for i in range(len(es)):
            for j in range(i + 1, len(es)):
                if es[i][2] == es[j][2]:
                    rows.append({
                        "student_1": NODE_BY_ID[es[i][0]]["name"],
                        "institution": NODE_BY_ID[es[i][2]]["name"],
                        "student_2": NODE_BY_ID[es[j][0]]["name"]
                    })
        return rows, es, "Students sharing the same institution were identified."

    if name == "Q13 — Charlie's work connection":
        es = [e for e in EDGES if e[0] == "charlie" and e[1] == "WORKED_AT"]
        rows = [{"student": NODE_BY_ID[e[0]]["name"], "company": NODE_BY_ID[e[2]]["name"]} for e in es]
        return rows, es, "Charlie's WORKED_AT relationship was retrieved."

    return [], [], "No result."

# --------------------- GRAPH FIGURE --------------------------
POSITIONS = {
    "alice": (-3.2, 1.8),
    "bob": (-3.2, 0.0),
    "charlie": (-3.2, -1.8),
    "python": (-0.5, 1.8),
    "ml": (-0.5, 0.0),
    "graph": (-0.5, -1.8),
    "college": (2.3, 0.9),
    "tcs": (2.3, -1.3)
}

def graph_figure(highlight_edges=None, only_subgraph=False, subgraph_nodes=None, preview=False):
    """Return a Plotly figure.

    - If only_subgraph is True, draw only the nodes in `subgraph_nodes` and
      the relationships in `highlight_edges` (rendered exactly as the query
      returned them, Neo4j-style).
    - Otherwise draw the full graph and optionally highlight edges in
      `highlight_edges`.
    """
    highlight_edges = highlight_edges or []
    highlighted = {(e[0], e[2]) for e in highlight_edges}

    positions = POSITIONS
    graph_ids = set(NODE_BY_ID)
    if preview:
        positions = {
            "alice": (-2.8, 1.3), "bob": (-2.8, -0.1), "charlie": (-2.8, -1.5),
            "python": (0.0, 1.3), "ml": (0.0, -0.1), "graph": (0.0, -1.5),
            "college": (2.7, 0.7), "tcs": (2.7, -1.0)
        }
    if not graph_ids.issubset(positions):
        layout_graph = nx.Graph()
        layout_graph.add_nodes_from(graph_ids)
        layout_graph.add_edges_from((source, target) for source, _, target in EDGES)
        layout = nx.spring_layout(layout_graph, seed=7)
        positions = {node_id: (float(x) * 3.0, float(y) * 2.2) for node_id, (x, y) in layout.items()}

    fig = go.Figure()

    def draw_edge(s, rel, t, is_highlight=False):
        x1, y1 = positions[s]
        x2, y2 = positions[t]
        fig.add_trace(go.Scatter(
            x=[x1, x2], y=[y1, y2],
            mode="lines",
            line=dict(color="#999999" if not is_highlight else "#2e86c1", width=3 if is_highlight else 1.5),
            hoverinfo="text",
            hovertext=f"({NODE_BY_ID[s]['name']})-[:{rel}]->({NODE_BY_ID[t]['name']})",
            showlegend=False
        ))

        # Arrow head using annotation (directional)
        fig.add_annotation(
            x=x2, y=y2,
            ax=x1, ay=y1,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True,
            arrowhead=3,
            arrowsize=1.0,
            arrowwidth=2.0 if is_highlight else 1.2,
            opacity=0.9 if is_highlight else 0.6,
            standoff=8
        )

        # Relationship label placed midway
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        if not preview:
            fig.add_annotation(
                x=mx, y=my + 0.08,
                text=rel,
                showarrow=False,
                font=dict(size=10, color="#444444"),
                bgcolor="rgba(255,255,255,0.9)"
            )

    # If requested, show only the exact subgraph (nodes + edges)
    if only_subgraph and (highlight_edges or subgraph_nodes):
        nodes_to_draw = set(subgraph_nodes or [])
        # draw only the edges that connect the requested nodes
        for s, rel, t in highlight_edges:
            draw_edge(s, rel, t, is_highlight=True)

        # draw the nodes involved in the subgraph
        for nid in nodes_to_draw:
            n = NODE_BY_ID[nid]
            x, y = positions[nid]
            color = {
                "Student": "#74b82a",
                "Course": "#f36f21",
                "Institution": "#2e86c1",
                "Company": "#9b59b6"
            }.get(n["label"], "#7f8c8d")

            fig.add_trace(go.Scatter(
                x=[x], y=[y],
                mode="markers+text",
                marker=dict(size=64, color=color, line=dict(width=2, color="#333333")),
                text=[n["name"]],
                textposition="middle center",
                hovertext=f"<b>{n['name']}</b><br>Label: {n['label']}",
                hoverinfo="text",
                showlegend=False
            ))

        fig.update_layout(title=dict(text="Query Result (Neo4j-style view)", x=0.01, font=dict(size=16, color="#2e86c1")))
    else:
        # Draw the full graph, optionally highlighting edges
        for s, rel, t in EDGES:
            is_highlight = (s, t) in highlighted
            draw_edge(s, rel, t, is_highlight=is_highlight)

        # Node traces grouped by type
        type_order = ["Student", "Course", "Institution", "Company"]
        type_order.extend(sorted({n["label"] for n in NODES if n["label"] not in type_order}))
        color_map = {
            "Student": "#74b82a",
            "Course": "#f36f21",
            "Institution": "#2e86c1",
            "Company": "#9b59b6"
        }
        for label in type_order:
            group = [n for n in NODES if n["label"] == label]
            if not group:
                continue
            fig.add_trace(go.Scatter(
                x=[positions[n["id"]][0] for n in group],
                y=[positions[n["id"]][1] for n in group],
                mode="markers+text",
                text=[n["name"] for n in group],
                textposition="middle center",
                hovertext=["<b>" + n["name"] + "</b><br>Label: " + n["label"] for n in group],
                hoverinfo="text",
                marker=dict(size=56, color=color_map.get(label, "#7f8c8d"), line=dict(width=1.5, color="#333333")),
                name=label
            ))

        title = "Preview: Connected Data in the Virtual Lab" if preview else "Knowledge Graph used in the Experiment"
        fig.update_layout(title=dict(x=0.01, font=dict(size=18, color="#2e86c1")))

    fig.update_layout(
        height=520,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(visible=False, range=[-4.2, 3.3]),
        yaxis=dict(visible=False, range=[-2.7, 2.7]),
        legend=dict(orientation="h", y=1.08, x=0)
    )
    return fig

# -------------------------- QUIZ -----------------------------
QUIZ = [
    ("Which Cypher clause is used to find a graph pattern?",
     ["CREATE", "MATCH", "DELETE", "SET"], 1,
     "MATCH is used to search for graph patterns."),
    ("What does a node represent?",
     ["An entity", "Only a query", "A database table", "An operator"], 0,
     "Nodes represent entities such as students and courses."),
    ("What connects two nodes?",
     ["Property", "Label", "Relationship", "Variable"], 2,
     "A relationship represents a connection between nodes."),
    ("Which clause filters matched data?",
     ["WHERE", "RETURN", "MATCH", "CREATE"], 0,
     "WHERE applies a condition to matched data."),
    ("What is a multi-hop query?",
     ["A query with no nodes", "Traversal across multiple relationships",
      "A delete query", "A property-only query"], 1,
     "A multi-hop traversal follows two or more relationships."),
    ("In (s:Student)-[:ENROLLED_IN]->(c:Course), ENROLLED_IN is a:",
     ["Node", "Property", "Relationship type", "Label"], 2,
     "ENROLLED_IN is the relationship type."),
    ("Why are multi-hop queries useful?",
     ["They reveal indirect connections", "They remove relationships",
      "They disable traversal", "They only return one node"], 0,
     "They can reveal information through intermediate entities."),
    ("What is a property?",
     ["A connection", "An attribute stored on a graph element",
      "A database", "A query result"], 1,
     "Properties are key-value attributes such as name or year."),
    ("What does RETURN specify?",
     ["Output data", "New nodes", "Deleted nodes", "A database"], 0,
     "RETURN specifies what matched information should be displayed."),
    ("Why is a small local graph used here?",
     ["To avoid graph querying", "To demonstrate the experiment without requiring Neo4j",
      "To remove relationships", "To prevent visualization"], 1,
        "The assignment does not require Neo4j for the graph experiment."),
        ("Which symbol starts a node pattern in Cypher?",
        ["()", "[]", "{}", "<>"], 0,
        "Parentheses represent nodes in a Cypher pattern."),
        ("Which symbol represents a relationship pattern?",
        ["()", "[]", "{}", "//"], 1,
        "Square brackets represent relationships."),
        ("What does the arrow in a relationship pattern show?",
        ["Direction", "Property type", "Node label", "Query length"], 0,
        "An arrow shows the direction of a directed relationship."),
        ("Which clause creates new graph data?",
        ["MATCH", "CREATE", "RETURN", "WHERE"], 1,
        "CREATE is used to create nodes and relationships."),
        ("Which clause removes matched data?",
        ["DELETE", "MATCH", "WITH", "ORDER BY"], 0,
        "DELETE removes matched nodes or relationships."),
        ("Which clause changes a property?",
        ["SET", "RETURN", "MATCH", "UNWIND"], 0,
        "SET updates or adds properties."),
        ("What does a label describe?",
        ["A node category", "A relationship direction", "A numeric value", "A result row"], 0,
        "Labels classify nodes, such as Student or Course."),
        ("Which query returns every node?",
        ["MATCH (n) RETURN n", "MATCH ()-[]->()", "RETURN *", "CREATE (n)"], 0,
        "The pattern MATCH (n) matches nodes without requiring a label."),
        ("What does `s` represent in `(s:Student)`?",
        ["A variable", "A relationship", "A database", "A property"], 0,
        "s is the variable bound to the matched Student node."),
        ("What does `:Student` represent in `(s:Student)`?",
        ["A node label", "A property value", "A query alias", "A function"], 0,
        "Student is the label required for the node."),
        ("Which clause can sort query results?",
        ["ORDER BY", "SORT", "GROUP", "ARRANGE"], 0,
        "ORDER BY sorts returned rows."),
        ("Which clause limits the number of returned rows?",
        ["LIMIT", "CAP", "TOP", "COUNT"], 0,
        "LIMIT restricts the number of rows returned."),
        ("Which function counts matched rows?",
        ["count()", "total()", "sizeRows()", "number()"], 0,
        "count() returns the number of values or rows."),
        ("What does `RETURN s.name` produce?",
        ["The name property of s", "The whole database", "The relationship type", "A new node"], 0,
        "Property projection returns the selected name value."),
        ("What does `WHERE s.year = 3` do?",
        ["Filters by year", "Creates year 3", "Deletes year 3", "Renames the node"], 0,
        "The predicate keeps only matching rows."),
        ("What is a graph path?",
        ["A sequence of connected nodes and relationships", "A table column", "A label list", "A database backup"], 0,
        "A path records a traversal through a graph."),
        ("Why use variables in a Cypher pattern?",
        ["To refer to matched elements later", "To encrypt data", "To create indexes automatically", "To replace labels"], 0,
        "Variables allow nodes and relationships to be referenced in RETURN or WHERE."),
        ("Which pattern matches a student enrolled in a course?",
        ["(s:Student)-[:ENROLLED_IN]->(c:Course)", "[s:Student]->[c:Course]", "(s)-ENROLLED_IN-(c)", "Student => Course"], 0,
        "This pattern matches the directed relationship between the two labeled nodes."),
        ("What is an incoming relationship?",
        ["A relationship directed toward a node", "A deleted relationship", "A property", "A node label"], 0,
        "Incoming means the arrow points into the node being considered."),
        ("What is an outgoing relationship?",
        ["A relationship directed away from a node", "A relationship without a type", "A node property", "A query comment"], 0,
        "Outgoing means the arrow starts at the node."),
        ("Which pattern can match either direction?",
        ["(a)-[:RELATED_TO]-(b)", "(a)->(b)", "(a)<-(b)", "(a)[:RELATED_TO](b)"], 0,
        "An undirected pattern omits the arrow direction."),
        ("What is a relationship type?",
        ["A category of connection", "A node identifier", "A property value", "A query result"], 0,
        "Types name relationships such as ENROLLED_IN or WORKED_AT."),
        ("Which graph element can have properties?",
        ["Nodes and relationships", "Only labels", "Only arrows", "Only query clauses"], 0,
        "Both nodes and relationships can store key-value properties."),
        ("What is a knowledge graph especially good at representing?",
        ["Entities and their connections", "Only isolated numbers", "Only images", "Only sequential text"], 0,
        "Knowledge graphs make relationships between entities explicit."),
        ("What does a two-hop traversal contain?",
        ["Two relationship steps", "Two databases", "Two labels only", "No relationships"], 0,
        "A two-hop traversal follows two relationships from the starting point."),
        ("In the lab graph, what does Alice connect to directly?",
        ["Python and Machine Learning", "TCS only", "Graph Analytics only", "No courses"], 0,
        "Alice has ENROLLED_IN relationships to Python and Machine Learning."),
        ("Which entity is labeled Company in the lab graph?",
        ["TCS", "Python", "Tech University", "Alice"], 0,
        "TCS is the example Company node."),
        ("Which entity is labeled Institution in the lab graph?",
        ["Tech University", "TCS", "Graph Analytics", "Bob"], 0,
        "Tech University is the example Institution node."),
        ("What relationship connects Charlie to TCS?",
        ["WORKED_AT", "STUDIES_AT", "RELATED_TO", "ENROLLED_IN"], 0,
        "Charlie has a WORKED_AT relationship to TCS."),
        ("What relationship connects a student to a course in the lab?",
        ["ENROLLED_IN", "WORKED_AT", "STUDIES_AT", "RELATED_TO"], 0,
        "ENROLLED_IN connects students and courses."),
        ("What relationship connects courses in the lab?",
        ["RELATED_TO", "ENROLLED_IN", "WORKED_AT", "STUDIES_AT"], 0,
        "RELATED_TO connects related courses."),
        ("What relationship connects a student to the university?",
        ["STUDIES_AT", "RELATED_TO", "WORKED_AT", "ENROLLED_IN"], 0,
        "STUDIES_AT connects students and the institution."),
        ("What does a graph visualization help learners see?",
        ["Connections and paths", "Only source code", "Only quiz scores", "Database passwords"], 0,
        "A visualization makes graph structure and traversals easier to inspect."),
        ("Why does the simulator use an in-memory graph?",
        ["To demonstrate queries without a database server", "To hide all relationships", "To prevent results", "To replace Cypher syntax"], 0,
        "The small local graph keeps the experiment self-contained."),
        ("What is the purpose of a query result table?",
        ["To inspect matched values", "To define a new label", "To install Neo4j", "To draw a webpage"], 0,
        "The table presents the values returned by the simulated query."),
        ("What should a learner do before executing a query?",
        ["Predict its result", "Delete the graph", "Change every label", "Close the lab"], 0,
        "Prediction encourages understanding of the Cypher pattern."),
        ("Which query best demonstrates property projection?",
        ["RETURN s.name, s.year", "RETURN s", "CREATE (s)", "DELETE s"], 0,
        "Projection returns selected properties rather than the whole node."),
        ("Which query best demonstrates filtering?",
        ["MATCH (s:Student) WHERE s.year = 3 RETURN s", "MATCH (s) RETURN s", "CREATE (s)", "DELETE (s)"], 0,
        "WHERE filters matched students by their year property."),
        ("Which query best demonstrates path retrieval?",
        ["MATCH p=(a)-[]->(b) RETURN p", "MATCH (a) RETURN a", "SET a.x = 1", "DELETE a"], 0,
        "Naming the path as p and returning p displays the complete traversal."),
        ("What is the main benefit of a declarative query language?",
        ["Describe what data is wanted", "Manually implement every traversal step", "Avoid all data", "Remove graph structure"], 0,
        "Declarative queries focus on the desired pattern and result."),
]

# ---------------------- PDF REPORT ---------------------------
def make_pdf(name, roll, date_str, trials, score, observations, quiz_total):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    def _safe(s):
        if s is None:
            return ""
        if not isinstance(s, str):
            s = str(s)
        # Replace common unicode punctuation that FPDF (latin-1) can't render
        s = s.replace('\u2014', '-').replace('\u2013', '-').replace('\u2026', '...')
        try:
            s.encode('latin-1')
            return s
        except Exception:
            return s.encode('latin-1', 'replace').decode('latin-1')

    def _break_long_words(s, maxlen=40):
        import re
        def _insert_spaces(match):
            txt = match.group(0)
            parts = [txt[i:i+maxlen] for i in range(0, len(txt), maxlen)]
            return " ".join(parts)
        return re.sub(r"\S{" + str(maxlen) + r",}", _insert_spaces, s)

    def _write_multicell(text, w=0, h=5):
        # Prepare text: safe encoding and break extremely long words
        t = _safe(text)
        t = _break_long_words(t, maxlen=40)

        # Try writing; on failure, progressively reduce font size and retry
        try:
            pdf.multi_cell(w, h, t)
            return
        except Exception:
            # try smaller fonts
            original_family, original_style, original_size = pdf.font_family, pdf.font_style, pdf.font_size_pt
            for sz in (10, 9, 8, 7, 6):
                try:
                    pdf.set_font("Helvetica", "", sz)
                    pdf.multi_cell(w, h, t)
                    break
                except Exception:
                    continue
            # restore font (best-effort)
            try:
                pdf.set_font(original_family, original_style, max(int(original_size), 6))
            except Exception:
                pdf.set_font("Helvetica", "", 9)

    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(46, 134, 193)
    pdf.cell(0, 10, _safe(TITLE))
    pdf.ln(12)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, _safe(f"Student Name: {name}"))
    pdf.ln(6)
    pdf.cell(0, 6, _safe(f"Roll / ID: {roll}"))
    pdf.ln(6)
    pdf.cell(0, 6, _safe(f"Experiment Date: {date_str}"))
    pdf.ln(10)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 7, "Aim")
    pdf.ln(8)
    pdf.set_font("Helvetica", "", 9)
    _write_multicell(_safe(AIM), 0, 5)
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 7, "Learning Objectives")
    pdf.ln(8)
    pdf.set_font("Helvetica", "", 9)
    for obj in OBJECTIVES:
        _write_multicell(_safe("- " + obj), 0, 5)

    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 7, "Recorded Trials")
    pdf.ln(8)
    pdf.set_font("Helvetica", "", 8)

    if trials:
        for t in trials:
            _write_multicell(_safe(f"Trial {t['Trial']}: {t['Query']} | Concept: {t['Concept']} | Rows: {t['Rows']}"), 0, 5)
    else:
        pdf.cell(0, 5, "No trials recorded.")

    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 7, "Quiz Result")
    pdf.ln(8)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, f"Score: {score}/{quiz_total}")
    pdf.ln(10)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 7, "Observations and Conclusion")
    pdf.ln(8)
    pdf.set_font("Helvetica", "", 9)
    _write_multicell(_safe(observations), 0, 5)

    return bytes(pdf.output())

# ---------------------- SESSION STATE ------------------------
if "trials" not in st.session_state:
    st.session_state.trials = []
if "last_query" not in st.session_state:
    st.session_state.last_query = None
if "last_rows" not in st.session_state:
    st.session_state.last_rows = []
if "last_edges" not in st.session_state:
    st.session_state.last_edges = []
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = QUIZ[:10]

# --------------------------- HEADER --------------------------
st.markdown("""
<div class="vlab-top">
    <div class="vlab-logo">⚗</div>
    <div class="vlab-brand">
        <div class="title">Virtual Labs</div>
        <div class="subtitle">An Online Learning Initiative</div>
    </div>
    <div class="vlab-exp-title">Computer Science & Engineering<br>Knowledge Graph Experiment</div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="breadcrumb">Computer Science and Engineering '
    '<span>›</span> Data / Graph Analytics '
    '<span>›</span> Experiments</div>',
    unsafe_allow_html=True
)

st.markdown(f'<div class="page-title">{TITLE}</div>', unsafe_allow_html=True)

# -------------------------- SIDEBAR --------------------------
st.sidebar.markdown("### Experiment")
section = st.sidebar.radio(
    "Navigate",
    [
        "Aim",
        "Introduction",
        "Theory",
        "Simulation",
        "Procedure",
        "Exercises",
        "Posttest",
        "Report Generation",
        "References"
    ],
    label_visibility="collapsed"
)

if section == "Posttest" and st.session_state.get("previous_section") != "Posttest":
    st.session_state.quiz_questions = random.sample(QUIZ, 10)
    st.session_state.quiz_score = 0
    st.session_state.quiz_submitted = False
st.session_state.previous_section = section

st.sidebar.markdown("---")
st.sidebar.markdown("### Quiz Status")
if st.session_state.quiz_submitted:
    st.sidebar.success(f"Quiz: {st.session_state.quiz_score}/{len(st.session_state.quiz_questions)}")
else:
    st.sidebar.info("Quiz: Not submitted")

# ----------------------------- AIM ---------------------------
if section == "Aim":
    st.markdown('<div class="vlab-h2">Aim of the Experiment</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="vlab-aim">{AIM}</div>', unsafe_allow_html=True)

    st.markdown('<div class="vlab-h2">Virtual Lab Preview</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="vlab-text">The diagram below shows the kind of connected data '
        'that the virtual lab lets you inspect: students, courses, institutions and '
        'companies connected by typed relationships.</div>',
        unsafe_allow_html=True
    )
    st.plotly_chart(graph_figure(preview=True), use_container_width=True)

    st.markdown('<div class="vlab-h2">Objectives</div>', unsafe_allow_html=True)
    st.markdown('<div class="vlab-text">After completing this experiment you will be able to:</div>', unsafe_allow_html=True)
    for obj in OBJECTIVES:
        st.markdown(f"- {obj}")

    st.markdown('<div class="vlab-h2">Time Required</div>', unsafe_allow_html=True)
    st.write("Approximately 1.5–2 hours, including theory, simulation and assessment.")

# ----------------------- INTRODUCTION -----------------------
elif section == "Introduction":
    st.markdown('<div class="vlab-h2">Introduction</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="vlab-text">{INTRODUCTION}</div>', unsafe_allow_html=True)

    st.markdown('<div class="vlab-h2">Real-World Applications</div>', unsafe_allow_html=True)
    for application in REAL_WORLD_APPLICATIONS:
        st.markdown(f"- {application}")

    st.markdown('<div class="vlab-h2">Experiment Scope</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="vlab-note">
    This experiment demonstrates the <b>querying concepts of Cypher</b> using a
    small in-memory graph. Neo4j is not required. The displayed Cypher patterns
    represent the graph query that would be used in a graph database, while the
    simulator performs the equivalent traversal on the educational graph.
    </div>
    """, unsafe_allow_html=True)

# --------------------------- THEORY --------------------------
elif section == "Theory":
    st.markdown('<div class="vlab-h2">Objectives</div>', unsafe_allow_html=True)
    for obj in OBJECTIVES:
        st.markdown(f"- {obj}")

    st.markdown('<div class="vlab-h2">Theory</div>', unsafe_allow_html=True)
    for heading, body in THEORY_SECTIONS:
        st.markdown(f'<div class="vlab-h3">{heading}</div>', unsafe_allow_html=True)
        st.markdown(body)

    st.markdown('<div class="vlab-h2">Knowledge Graph used in this experiment</div>', unsafe_allow_html=True)
    st.dataframe(
        pd.DataFrame(NODES)[["label", "name"]].rename(
            columns={"label": "Node Label", "name": "Entity"}
        ),
        hide_index=True,
        use_container_width=True
    )

    # Show the full graph (nodes and relationships) used in the experiment
    st.markdown('<div class="vlab-h3">Full Knowledge Graph (Nodes & Relationships)</div>', unsafe_allow_html=True)
    st.plotly_chart(graph_figure(), use_container_width=True)

# ------------------------- SIMULATION ------------------------
elif section == "Simulation":
    st.markdown('<div class="vlab-h2">Simulation</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="vlab-note">
    <b>Instructions:</b> Select a query, study its Cypher pattern, predict the
    result, then click <b>Execute Query</b>. For relationship and multi-hop
    queries, the relevant graph connections are highlighted.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="vlab-h3">Use a CSV Graph</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="vlab-text">Upload a relationship edge-list CSV to replace the sample graph. '
        'Required columns are <b>source</b>, <b>relationship</b> and <b>target</b>; optional columns '
        'are <b>source_label</b>, <b>source_name</b>, <b>target_label</b> and <b>target_name</b>.</div>',
        unsafe_allow_html=True
    )
    with st.expander("CSV format example"):
        st.code(
            "source,relationship,target,source_label,target_label,source_name,target_name\n"
            "alice,ENROLLED_IN,python,Student,Course,Alice,Python\n"
            "python,RELATED_TO,ml,Course,Course,Python,Machine Learning",
            language="csv"
        )
    uploaded_graph = st.file_uploader("Upload graph CSV", type=["csv"], key="simulation_graph_csv")
    available_query_defs = QUERY_DEFS
    ACTIVE_QUERY_SPECS.clear()
    if uploaded_graph is not None:
        try:
            imported_nodes, imported_edges = graph_from_csv(uploaded_graph)
            NODES.clear()
            NODES.extend(imported_nodes)
            EDGES.clear()
            EDGES.extend(imported_edges)
            NODE_BY_ID.clear()
            NODE_BY_ID.update({node["id"]: node for node in NODES})
            available_query_defs, csv_query_specs = build_csv_query_defs(NODES, EDGES)
            ACTIVE_QUERY_SPECS.update(csv_query_specs)
            st.success(f"Loaded {len(NODES)} nodes and {len(EDGES)} relationships from {uploaded_graph.name}.")
        except (pd.errors.ParserError, ValueError) as error:
            st.error(f"Could not load the CSV graph: {error}")

    st.plotly_chart(graph_figure(), use_container_width=True)

    st.markdown('<div class="vlab-h3">Select Query</div>', unsafe_allow_html=True)
    query_name = st.selectbox("Choose a query", list(available_query_defs.keys()), label_visibility="collapsed")
    q = available_query_defs[query_name]

    st.markdown(f"""
    <div class="sim-box">
    <b>Concept demonstrated:</b> {q["concept"]}<br>
    <b>Expected behaviour:</b> {q["description"]}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Cypher Query**")
    st.markdown(
        f'<div class="cypher-query">{render_cypher_query(q["cypher"])}</div>',
        unsafe_allow_html=True
    )

    if st.button("Execute Query", type="primary", use_container_width=True):
        rows, edges, message = execute_query(query_name)
        st.session_state.last_query = query_name
        st.session_state.last_rows = rows
        st.session_state.last_edges = edges

        st.success(message)

        if rows:
            st.markdown("#### Query Result")
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        else:
            st.warning("No records were returned.")

        # If the query returned relationships (edges), draw the exact subgraph
        # (only the nodes and edges present in the query) using a Neo4j-like style.
        if edges:
            st.markdown("#### Resulting Relationship / Path")
            nodes_in_edges = {n for e in edges for n in (e[0], e[2])}
            st.plotly_chart(
                graph_figure(highlight_edges=edges, only_subgraph=True, subgraph_nodes=list(nodes_in_edges)),
                use_container_width=True
            )
        else:
            # If only nodes were returned (rows that contain full node dicts),
            # display those nodes alone.
            if rows and isinstance(rows[0], dict) and "id" in rows[0]:
                node_ids = [r["id"] for r in rows]
                st.markdown("#### Resulting Nodes")
                st.plotly_chart(graph_figure(only_subgraph=True, subgraph_nodes=node_ids), use_container_width=True)

    if st.session_state.last_query == query_name:
        if st.button("Record Current Trial", use_container_width=True):
            st.session_state.trials.append({
                "Trial": len(st.session_state.trials) + 1,
                "Query": query_name,
                "Concept": q["concept"],
                "Rows": len(st.session_state.last_rows),
                "Time": datetime.now().strftime("%H:%M:%S")
            })
            st.toast("Trial recorded.")

    st.markdown('<div class="vlab-h3">Experimental Data Log</div>', unsafe_allow_html=True)
    if st.session_state.trials:
        df_trials = pd.DataFrame(st.session_state.trials)
        st.dataframe(df_trials, hide_index=True, use_container_width=True)
        st.download_button(
            "Download Trial Log",
            df_trials.to_csv(index=False).encode("utf-8"),
            "cypher_trial_log.csv",
            "text/csv"
        )
    else:
        st.info("No trials recorded yet.")

# ------------------------- PROCEDURE -------------------------
elif section == "Procedure":
    st.markdown('<div class="vlab-h2">Procedure</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="vlab-text">
    Follow these steps to perform the experiment.
    </div>
    """, unsafe_allow_html=True)

    for i, step in enumerate(PROCEDURE, 1):
        st.markdown(f"**{i}.** {step}")

# ------------------------- EXERCISES ------------------------
elif section == "Exercises":
    st.markdown('<div class="vlab-h2">Exercises</div>', unsafe_allow_html=True)
    st.write("Perform the following tasks in the Simulation section and record your observations.")

    exercises = [
        ("Exercise 1", "Retrieve all Student nodes."),
        ("Exercise 2", "Retrieve all Course nodes."),
        ("Exercise 3", "Retrieve Alice's name, year and branch."),
        ("Exercise 4", "Find all courses in which Alice is enrolled."),
        ("Exercise 5", "Find all third-year students using WHERE."),
        ("Exercise 6", "Retrieve all Student → Course ENROLLED_IN relationships."),
        ("Exercise 7", "Find courses related to Machine Learning."),
        ("Exercise 8", "Perform a two-hop traversal from Alice through an enrolled course to a related course."),
        ("Exercise 9", "Find students who share the same institution."),
        ("Exercise 10", "Retrieve Charlie's WORKED_AT relationship.")
    ]

    for no, task in exercises:
        st.markdown(f"**{no}:** {task}")

    st.markdown('<div class="vlab-h3">Suggested Observation</div>', unsafe_allow_html=True)
    st.write(
        "Compare direct retrieval with relationship and multi-hop retrieval. "
        "Observe how adding relationships to a MATCH pattern changes the type "
        "of information obtained."
    )

# -------------------------- POSTTEST ------------------------
elif section == "Posttest":
    st.markdown('<div class="vlab-h2">Posttest</div>', unsafe_allow_html=True)
    st.write("Choose the correct answer for each of the 10 randomly selected questions and submit the quiz.")

    active_quiz = st.session_state.quiz_questions

    with st.form("posttest"):
        answers = []
        for i, (question, options, correct, explanation) in enumerate(active_quiz):
            st.markdown(f"**Q{i+1}. {question}**")
            answer = st.radio(
                "Select an option:",
                options,
                key=f"posttest_{i}",
                label_visibility="collapsed"
            )
            answers.append(options.index(answer))

        submitted = st.form_submit_button("Submit Quiz", type="primary")

    if submitted:
        score = sum(answers[i] == active_quiz[i][2] for i in range(len(active_quiz)))
        st.session_state.quiz_score = score
        st.session_state.quiz_submitted = True

        st.markdown('<div class="vlab-h3">Evaluation</div>', unsafe_allow_html=True)
        for i, (_, options, correct, explanation) in enumerate(active_quiz):
            if answers[i] == correct:
                st.success(f"Q{i+1}: Correct. {explanation}")
            else:
                st.error(f"Q{i+1}: Incorrect. Correct answer: {options[correct]}. {explanation}")

        st.info(f"Final Score: {score}/{len(active_quiz)} ({score / len(active_quiz) * 100:.0f}%)")

# ---------------------- REPORT GENERATION -------------------
elif section == "Report Generation":
    st.markdown('<div class="vlab-h2">Report Generation</div>', unsafe_allow_html=True)
    st.write("Enter your details and generate the experiment report.")

    c1, c2, c3 = st.columns(3)
    with c1:
        student_name = st.text_input("Student Name", "Student Name")
    with c2:
        student_roll = st.text_input("Roll / ID", "EXP-001")
    with c3:
        experiment_date = st.date_input("Experiment Date", datetime.now()).strftime("%Y-%m-%d")

    observations = st.text_area(
        "Observations / Conclusion",
        "The experiment demonstrated how Cypher patterns can retrieve nodes, "
        "relationships and multi-hop connections from a knowledge graph. "
        "The simulation showed that relationship-aware queries can reveal "
        "meaningful information through direct and indirect graph connections."
    )

    st.markdown('<div class="vlab-h3">Report Summary</div>', unsafe_allow_html=True)
    st.write(f"**Experiment:** {TITLE}")
    st.write(f"**Student:** {student_name}")
    st.write(f"**Roll / ID:** {student_roll}")
    st.write(f"**Quiz Score:** {st.session_state.quiz_score}/{len(st.session_state.quiz_questions)}")

    if st.session_state.trials:
        st.dataframe(
            pd.DataFrame(st.session_state.trials),
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("No trials have been recorded yet.")

    pdf = make_pdf(
        student_name,
        student_roll,
        experiment_date,
        st.session_state.trials,
        st.session_state.quiz_score,
        observations,
        len(st.session_state.quiz_questions)
    )

    st.download_button(
        "Download Experiment Report (PDF)",
        pdf,
        "Query_Knowledge_Graphs_Cypher_Report.pdf",
        "application/pdf",
        type="primary",
        use_container_width=True
    )

# ------------------------- REFERENCES -----------------------
elif section == "References":
    st.markdown('<div class="vlab-h2">References</div>', unsafe_allow_html=True)
    st.markdown("""
    1. [Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/current/)
    2. [Neo4j GraphAcademy](https://graphacademy.neo4j.com/)
    3. [openCypher Project](https://opencypher.org/)
    4. [Neo4j Graph Data Modeling Guidelines](https://neo4j.com/developer/guide-data-modeling/)
    5. [W3C RDF 1.1 Concepts](https://www.w3.org/TR/rdf11-concepts/)
    6. [W3C SPARQL 1.1 Query Language](https://www.w3.org/TR/sparql11-query/)
    7. [Wikidata: Introduction](https://www.wikidata.org/wiki/Wikidata:Introduction)
    8. [DBpedia Knowledge Base](https://www.dbpedia.org/)
    9. [Google: Introducing the Knowledge Graph](https://blog.google/products/search/introducing-knowledge-graph-things-not/)
    10. [Microsoft Graph Data Connect](https://learn.microsoft.com/en-us/graph/data-connect-concept-overview)
    11. [Stanford Encyclopedia of Philosophy: Knowledge Representation](https://plato.stanford.edu/entries/logic-knowledge-representation/)
    12. [Virtual Labs India](https://vlab.co.in/)
    """)

    st.markdown('<div class="vlab-h3">Credits</div>', unsafe_allow_html=True)
    st.write(
        "This student-developed Virtual Lab follows the educational structure "
        "of Virtual Labs while implementing an original Knowledge Graph and "
        "Cypher-query simulation for the assigned experiment."
    )

st.markdown("""
<div class="vlab-footer">
Virtual Laboratory Experiment • Query Knowledge Graphs using Cypher<br>
Designed for educational demonstration and assessment
</div>
""", unsafe_allow_html=True)
