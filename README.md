# Query Knowledge Graphs using Cypher — Virtual Lab

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## What this Virtual Lab demonstrates
- Knowledge graph nodes, relationships and properties
- Cypher MATCH, WHERE and RETURN concepts
- Node and property retrieval
- Relationship traversal
- Two-hop / multi-hop traversal
- Interactive graph visualization
- Query result tables
- Trial logging and CSV export
- Self-grading quiz
- PDF lab report generation

## Important implementation note
Neo4j is not required. The application uses a small in-memory educational graph
and a Python query simulator to demonstrate the semantics of the selected
Cypher patterns, in accordance with the graph-experiment instruction.

### This vlab has been deployed using Stramlit Cloud
https://query-knowledge-graphs-cypher-lmkcpmj5ugeb2dsuqyfqj7.streamlit.app/
