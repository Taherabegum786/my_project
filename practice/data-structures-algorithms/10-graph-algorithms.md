# Set 10 — Graph Algorithms (representations, BFS, DFS, topological sort, MST, shortest paths, maximum flow)

**40 questions** — High: 17, Medium: 22, Low: 1

Each question carries 2 marks, has exactly one correct option and no negative marking (UGC NET Paper II pattern). Click **Answer** to check.

---

**Q1.** `High`  
Match List I with List II.  
List I (Graph algorithm): A. Breadth-first search  B. Dijkstra's algorithm  C. Bellman-Ford algorithm  D. Floyd-Warshall algorithm  
List II (Time complexity): I. O(V³)  II. O(V + E)  III. O(VE)  IV. O((V + E) log V) with a binary heap

(1) A-IV, B-II, C-III, D-I  
(2) A-II, B-IV, C-III, D-I  
(3) A-II, B-IV, C-I, D-III  
(4) A-II, B-III, C-IV, D-I  

<details><summary>Answer</summary>

**(2)** — Standard time complexities of graph algorithms.

</details>

**Q2.** `High`  
For a graph with V vertices and E edges, the space needed by an adjacency matrix and by adjacency lists is

(1) O(V²) and O(V + E)  
(2) O(E) and O(V)  
(3) O(V + E) and O(V²)  
(4) O(V log V) and O(E)  

<details><summary>Answer</summary>

**(1)** — Adjacency lists are preferred for sparse graphs.

</details>

**Q3.** `High`  
The minimum spanning tree of the CLRS example graph with edges a-b 4, a-h 8, b-c 8, b-h 11, c-d 7, c-f 4, c-i 2, d-e 9, d-f 14, e-f 10, f-g 2, g-h 1, g-i 6, h-i 7 has total weight

(1) 35  
(2) 41  
(3) 37  
(4) 39  

<details><summary>Answer</summary>

**(3)** — Kruskal adds g-h 1, c-i 2, f-g 2, a-b 4, c-f 4, c-d 7, a-h 8 (or b-c 8), d-e 9.

</details>

**Q4.** `Medium`  
A graph has edges A-B 1, A-C 3, B-C 1, B-D 4, C-D 2, C-E 5, D-E 6, D-F 7, E-F 3. The weight of its minimum spanning tree is

(1) 13  
(2) 11  
(3) 12  
(4) 14  

<details><summary>Answer</summary>

**(3)** — A-B 1, B-C 1, C-D 2, E-F 3, C-E 5 = 12.

</details>

**Q5.** `High`  
Given below are two statements.  
Statement I: If all edge weights of a connected graph are distinct, its minimum spanning tree is unique.  
Statement II: A minimum spanning tree of a graph with V vertices has V edges.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — A spanning tree has V − 1 edges.

</details>

**Q6.** `High`  
Match List I with List II.  
List I (MST algorithm): A. Kruskal  B. Prim with a binary heap  C. Prim with a Fibonacci heap  
List II (Time): I. O(E + V log V)  II. O(E log E)  III. O(E log V)

(1) A-I, B-III, C-II  
(2) A-III, B-II, C-I  
(3) A-II, B-I, C-III  
(4) A-II, B-III, C-I  

<details><summary>Answer</summary>

**(4)** — Kruskal's time is dominated by sorting the edges.

</details>

**Q7.** `High`  
In the CLRS graph with edges s→t 10, s→y 5, t→x 1, t→y 2, y→t 3, y→x 9, y→z 2, x→z 4, z→s 7, z→x 6, Dijkstra's algorithm from s gives the shortest distances to t, x, y, z as

(1) 8, 9, 5, 7  
(2) 10, 11, 5, 7  
(3) 8, 13, 5, 7  
(4) 8, 9, 5, 6  

<details><summary>Answer</summary>

**(1)** — Vertices are extracted in the order s, y, z, t, x.

</details>

**Q8.** `Medium`  
In the CLRS graph with edges s→t 10, s→y 5, t→x 1, t→y 2, y→t 3, y→x 9, y→z 2, x→z 4, z→s 7, z→x 6, the order in which Dijkstra's algorithm from s finalizes the vertices is

(1) s, y, z, t, x  
(2) s, y, t, x, z  
(3) s, t, y, x, z  
(4) s, y, t, z, x  

<details><summary>Answer</summary>

**(1)** — y (5), z (7), t (8), x (9).

</details>

**Q9.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: Dijkstra's algorithm may give wrong results on graphs with negative edge weights.  
Reason R: Once a vertex is finalized, Dijkstra's algorithm never updates its distance, but a later negative edge could provide a shorter path.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — Bellman-Ford handles negative weights and detects negative cycles.

</details>

**Q10.** `High`  
Given below are two statements.  
Statement I: The Bellman-Ford algorithm can detect negative-weight cycles reachable from the source.  
Statement II: Bellman-Ford relaxes every edge V − 1 times.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — A V-th pass that still improves a distance reveals a negative cycle.

</details>

**Q11.** `Medium`  
Running Bellman-Ford from s on the CLRS graph with edges s→t 6, s→y 7, t→x 5, t→y 8, t→z −4, x→t −2, y→x −3, y→z 9, z→s 2, z→x 7 gives the shortest distance to z as

(1) 2  
(2) −4  
(3) 4  
(4) −2  

<details><summary>Answer</summary>

**(4)** — The path s → y → x → t → z has weight 7 − 3 − 2 − 4 = −2.

</details>

**Q12.** `High`  
BFS on an unweighted graph from a source s finds

(1) a minimum spanning tree  
(2) all strongly connected components  
(3) the shortest path (fewest edges) from s to every reachable vertex  
(4) a topological order  

<details><summary>Answer</summary>

**(3)** — It explores vertices in order of distance from s.

</details>

**Q13.** `High`  
For the undirected graph with adjacency lists A: B, C; B: A, D, E; C: A, F; D: B; E: B, F; F: C, E, the BFS and DFS orders starting from A (taking neighbours in list order) are

(1) BFS: A B C D E F; DFS: A B C F E D  
(2) BFS: A B C D E F; DFS: A B D E F C  
(3) BFS: A C B F E D; DFS: A B D E F C  
(4) BFS: A B D E F C; DFS: A B C D E F  

<details><summary>Answer</summary>

**(2)** — DFS goes A → B → D, backtracks to B → E → F, and then reaches C from F.

</details>

**Q14.** `High`  
Given below are two statements.  
Statement I: DFS of an undirected graph can produce cross edges.  
Statement II: A directed graph has a cycle if and only if DFS finds a back edge.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(4)** — In an undirected graph, DFS produces only tree edges and back edges.

</details>

**Q15.** `High`  
The number of topological orderings of the DAG with edges A→B, A→C, B→D, C→D, D→E is

(1) 2  
(2) 3  
(3) 1  
(4) 4  

<details><summary>Answer</summary>

**(1)** — A must come first and D, E last; B and C can appear in either order.

</details>

**Q16.** `Medium`  
The number of topological orderings of the DAG with edges 1→2, 1→3, 2→4, 3→4, 4→5, 4→6 is

(1) 8  
(2) 4  
(3) 6  
(4) 2  

<details><summary>Answer</summary>

**(2)** — 2 and 3 can be swapped, and so can 5 and 6: 2 × 2 = 4.

</details>

**Q17.** `High`  
A topological sort exists for a directed graph if and only if the graph is

(1) strongly connected  
(2) complete  
(3) acyclic  
(4) bipartite  

<details><summary>Answer</summary>

**(3)** — It can be computed by DFS (decreasing finishing times) or Kahn's algorithm in O(V + E).

</details>

**Q18.** `Medium`  
Kosaraju's algorithm finds the strongly connected components of a directed graph using

(1) one BFS  
(2) union-find  
(3) two DFS passes, the second on the transpose graph in decreasing order of finishing time  
(4) Dijkstra's algorithm  

<details><summary>Answer</summary>

**(3)** — It runs in O(V + E); Tarjan's algorithm uses a single DFS.

</details>

**Q19.** `High`  
The value of the maximum flow in the CLRS network with edges s→v1 16, s→v2 13, v1→v3 12, v2→v1 4, v2→v4 14, v3→v2 9, v3→t 20, v4→v3 7, v4→t 4 is

(1) 26  
(2) 19  
(3) 23  
(4) 29  

<details><summary>Answer</summary>

**(3)** — The minimum cut {s, v1, v2, v4} versus {v3, t} has capacity 12 + 7 + 4 = 23.

</details>

**Q20.** `Medium`  
A network has edges S→A 10, S→B 5, A→B 15, A→T 5, B→T 10. The maximum flow from S to T is

(1) 25  
(2) 20  
(3) 10  
(4) 15  

<details><summary>Answer</summary>

**(4)** — The cut separating T from the rest has capacity A→T 5 + B→T 10 = 15, and S→A→T 5, S→A→B→T 5, S→B→T 5 achieve it.

</details>

**Q21.** `High`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: The value of a maximum flow equals the capacity of a minimum cut.  
Reason R: When no augmenting path remains in the residual network, the vertices reachable from the source define a cut whose capacity equals the flow.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(1)** — This is the max-flow min-cut theorem.

</details>

**Q22.** `Medium`  
The Edmonds-Karp algorithm, which always augments along a shortest path found by BFS, runs in

(1) O(E log V)  
(2) O(VE²)  
(3) O(V³)  
(4) O(E |f*|)  

<details><summary>Answer</summary>

**(2)** — Ford-Fulkerson with arbitrary paths takes O(E |f*|) for integer capacities.

</details>

**Q23.** `Medium`  
Maximum bipartite matching can be solved by

(1) Huffman coding  
(2) reducing it to a maximum-flow problem  
(3) Dijkstra's algorithm  
(4) topological sorting  

<details><summary>Answer</summary>

**(2)** — Add a source to one side and a sink to the other with unit capacities.

</details>

**Q24.** `Medium`  
The Floyd-Warshall algorithm on the graph with distance matrix rows [0, 3, ∞, 7], [8, 0, 2, ∞], [5, ∞, 0, 1], [2, ∞, ∞, 0] gives the shortest distance from vertex 1 to vertex 4 as

(1) 6  
(2) 7  
(3) 8  
(4) 5  

<details><summary>Answer</summary>

**(1)** — 1 → 2 → 3 → 4: 3 + 2 + 1 = 6.

</details>

**Q25.** `High`  
The number of edges in a complete undirected graph with 10 vertices is

(1) 45  
(2) 20  
(3) 90  
(4) 100  

<details><summary>Answer</summary>

**(1)** — n(n − 1)/2 = 45.

</details>

**Q26.** `Medium`  
By Cayley's formula, the number of labelled spanning trees of the complete graph K5 is

(1) 25  
(2) 120  
(3) 60  
(4) 125  

<details><summary>Answer</summary>

**(4)** — n^(n − 2) = 5³ = 125.

</details>

**Q27.** `High`  
Given below are two statements.  
Statement I: A connected undirected graph has an Euler circuit if and only if every vertex has even degree.  
Statement II: Determining whether a graph has a Hamiltonian cycle can be done in polynomial time.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(3)** — The Hamiltonian-cycle problem is NP-complete.

</details>

**Q28.** `Medium`  
An undirected graph is bipartite if and only if it

(1) has an even number of vertices  
(2) is complete  
(3) contains no cycle of odd length  
(4) is a tree  

<details><summary>Answer</summary>

**(3)** — Bipartiteness can be tested by BFS 2-colouring in O(V + E).

</details>

**Q29.** `Medium`  
The sum of the degrees of all vertices of an undirected graph with E edges is

(1) E  
(2) 2E  
(3) V + E  
(4) E²  

<details><summary>Answer</summary>

**(2)** — Each edge contributes 1 to the degree of each of its two endpoints.

</details>

**Q30.** `Medium`  
An articulation point (cut vertex) of a connected undirected graph is a vertex whose removal

(1) disconnects the graph  
(2) creates a cycle  
(3) makes the graph complete  
(4) has no effect  

<details><summary>Answer</summary>

**(1)** — Articulation points and bridges can be found in O(V + E) with DFS low-link values.

</details>

**Q31.** `Medium`  
Johnson's algorithm for all-pairs shortest paths in sparse graphs with negative edges

(1) reweights edges using Bellman-Ford and then runs Dijkstra from every vertex  
(2) uses only BFS  
(3) cannot handle negative edges  
(4) uses Floyd-Warshall  

<details><summary>Answer</summary>

**(1)** — It runs in O(V² log V + VE).

</details>

**Q32.** `Medium`  
Given below are two statements.  
Statement I: Prim's algorithm grows a single tree from a starting vertex.  
Statement II: Kruskal's algorithm may maintain a forest of several trees during its execution.

(1) Both Statement I and Statement II are true  
(2) Both Statement I and Statement II are false  
(3) Statement I is true but Statement II is false  
(4) Statement I is false but Statement II is true  

<details><summary>Answer</summary>

**(1)** — Kruskal adds the cheapest edge connecting two different components.

</details>

**Q33.** `Medium`  
Warshall's algorithm computes

(1) shortest paths  
(2) a minimum spanning tree  
(3) maximum flow  
(4) the transitive closure of a directed graph in O(V³)  

<details><summary>Answer</summary>

**(4)** — It is Floyd-Warshall with Boolean OR and AND.

</details>

**Q34.** `Medium`  
Which data structure is used by Dijkstra's algorithm to select the next vertex efficiently?

(1) Hash table  
(2) Min-priority queue  
(3) Queue  
(4) Stack  

<details><summary>Answer</summary>

**(2)** — A Fibonacci heap gives O(E + V log V).

</details>

**Q35.** `Medium`  
DFS on a graph with V vertices represented by an adjacency matrix takes

(1) O(V + E)  
(2) O(E log V)  
(3) O(V²)  
(4) O(V³)  

<details><summary>Answer</summary>

**(3)** — Each vertex's row of V entries is scanned.

</details>

**Q36.** `Medium`  
In a directed graph, the vertex u is discovered at time 1 and finished at time 10, and v is discovered at 3 and finished at 6 during DFS. Which edge type is (u, v) if it exists and v was discovered through another path?

(1) It cannot exist  
(2) Forward edge  
(3) Cross edge  
(4) Back edge  

<details><summary>Answer</summary>

**(2)** — v is a descendant of u (its interval is nested inside u's), so a non-tree edge u → v is a forward edge.

</details>

**Q37.** `Medium`  
Given below are two statements: one is labelled as Assertion A and the other is labelled as Reason R.  
Assertion A: BFS finds shortest paths in any weighted graph with positive edge weights.  
Reason R: BFS minimizes the number of edges, not the total weight.

(1) Both A and R are true and R is the correct explanation of A  
(2) Both A and R are true but R is NOT the correct explanation of A  
(3) A is true but R is false  
(4) A is false but R is true  

<details><summary>Answer</summary>

**(4)** — Because of R, BFS is correct only for unweighted graphs (or equal weights); otherwise Dijkstra is needed.

</details>

**Q38.** `Low`  
A graph in which every pair of distinct vertices is joined by an edge is called a

(1) tree  
(2) complete graph  
(3) bipartite graph  
(4) planar graph  

<details><summary>Answer</summary>

**(2)** — K_n has n(n − 1)/2 edges.

</details>

**Q39.** `Medium`  
A network has edges S→A 3, S→B 2, A→B 1, A→T 2, B→T 3. The maximum flow from S to T is

(1) 4  
(2) 7  
(3) 6  
(4) 5  

<details><summary>Answer</summary>

**(4)** — The cut {S} has capacity 3 + 2 = 5, and S→A→T 2, S→A→B→T 1, S→B→T 2 achieves 5.

</details>

**Q40.** `Medium`  
The A* search algorithm finds an optimal path if its heuristic h is

(1) always zero only  
(2) admissible (never overestimates the true cost)  
(3) random  
(4) larger than the true cost  

<details><summary>Answer</summary>

**(2)** — With h = 0, A* reduces to Dijkstra's algorithm.

</details>
