# Graph Report - gtk1-forecast  (2026-10-25)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 537 nodes · 1589 edges · 27 communities (24 shown, 3 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 38 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f49498c6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 5
- Community 6
- Community 7
- Community 8
- Community 9
- Community 10
- Community 11
- Community 12
- Community 13
- Community 14
- Community 15
- Community 16
- Community 17
- Community 18
- Community 19
- Community 20
- Community 21
- Community 22
- Community 23
- Community 24
- Community 25
- Community 26

## God Nodes (most connected - your core abstractions)
1. `load_anomalies()` - 21 edges
2. `normalize()` - 19 edges
3. `load_anom()` - 18 edges
4. `main()` - 18 edges
5. `raw()` - 17 edges
6. `match_win()` - 16 edges
7. `build()` - 16 edges
8. `build()` - 15 edges
9. `main()` - 12 edges
10. `run()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `read_any()` --calls--> `_apply_tolerant_xlrd()`  [INFERRED]
  experiments/e18_drop_reeval.py → src/gtk1/io.py
- `read_rows()` --calls--> `_apply_tolerant_xlrd()`  [INFERRED]
  experiments/ingest_npk.py → src/gtk1/io.py
- `_read_excel()` --calls--> `_apply_tolerant_xlrd()`  [INFERRED]
  experiments/ingest_tuesday.py → src/gtk1/io.py
- `read_sheets()` --calls--> `_apply_tolerant_xlrd()`  [INFERRED]
  experiments/inventory_npk.py → src/gtk1/io.py
- `evaluate()` --calls--> `build()`  [INFERRED]
  experiments/e18_drop_reeval.py → src/gtk1/features.py

## Import Cycles
- None detected.

## Communities (27 total, 3 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (39): ap_ci(), fhash(), load_anom(), match(), norm(), pr_at(), run(), seg_labels() (+31 more)

### Community 1 - "Community 1"
Cohesion: 0.07
Nodes (28): libreoffice_open(), main(), nfc(), reader_open(), compare(), csv_digest(), grid_digest(), kind() (+20 more)

### Community 2 - "Community 2"
Cohesion: 0.09
Nodes (31): audit(), main(), charcol(), dist_csv(), dist_xlsx(), run(), find_col(), grid_counts() (+23 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (19): main(), main(), cell(), main(), read_sheets(), exact_ci(), frame(), main() (+11 more)

### Community 4 - "Community 4"
Cohesion: 0.11
Nodes (23): col_idx(), inflate(), load_strings(), main(), parse_cells(), salvage_rows(), salvage_sheet(), show() (+15 more)

### Community 5 - "Community 5"
Cohesion: 0.14
Nodes (8): danger_col(), main(), search(), search(), search(), quad_search(), main(), search()

### Community 6 - "Community 6"
Cohesion: 0.12
Nodes (16): _apply_fat_salvage(), column_inventory(), discover_pipe_key(), join_coverage(), _looks_mojibake(), main(), normalize_tool_info(), pipe_key_set() (+8 more)

### Community 7 - "Community 7"
Cohesion: 0.14
Nodes (12): header_index(), main(), num(), parse_info(), parse_section(), read_rows(), to_hours(), col_letters() (+4 more)

### Community 8 - "Community 8"
Cohesion: 0.15
Nodes (13): build(), corridor_point(), haversine_km(), main(), analyze_pair(), clean(), extract_ranking(), extract_worst() (+5 more)

### Community 9 - "Community 9"
Cohesion: 0.16
Nodes (9): folds_with_guard(), run(), ap(), ap_lift_ci(), count_mae(), paired_delta_ci(), precision_at_k(), rank_corr() (+1 more)

### Community 10 - "Community 10"
Cohesion: 0.22
Nodes (10): _clean(), coverage(), evaluate(), find_col(), find_file(), load_survey(), main(), manual_frame() (+2 more)

### Community 11 - "Community 11"
Cohesion: 0.17
Nodes (6): build(), match_win(), load(), run(), load_anom(), run()

### Community 12 - "Community 12"
Cohesion: 0.26
Nodes (6): audit_csv(), audit_xls(), audit_xlsx(), main(), check(), main()

### Community 13 - "Community 13"
Cohesion: 0.26
Nodes (8): clean(), one_pair(), rate(), run(), git_hash(), main(), per_cell_counts(), run_triple_cells()

### Community 14 - "Community 14"
Cohesion: 0.18
Nodes (5): main(), cell_abc(), load_anomalies(), load_anom(), run()

### Community 15 - "Community 15"
Cohesion: 0.18
Nodes (10): pk1, flag_top_k, review_band_score, status, survey_basis, True, flag_top_k, review_band_score (+2 more)

### Community 16 - "Community 16"
Cohesion: 0.25
Nodes (4): load(), run(), _find(), normalize()

### Community 17 - "Community 17"
Cohesion: 0.27
Nodes (4): cell_key(), run(), run_cut(), labels()

### Community 18 - "Community 18"
Cohesion: 0.31
Nodes (6): load(), test_lift_cis_lower_above_zero(), test_on_frozen(), test_pk1_frozen(), test_srto_frozen(), _walk()

### Community 19 - "Community 19"
Cohesion: 0.43
Nodes (5): agg(), clean(), greedy_pairs(), one_pair(), run()

### Community 20 - "Community 20"
Cohesion: 0.43
Nodes (6): cells_of(), clean(), group_stats(), load_all(), main(), run_pair()

### Community 21 - "Community 21"
Cohesion: 0.48
Nodes (5): b1score(), clean(), load_one(), main(), score_pair()

### Community 22 - "Community 22"
Cohesion: 0.53
Nodes (4): clean(), load(), main(), run_pair()

### Community 23 - "Community 23"
Cohesion: 0.60
Nodes (3): load_year(), main(), run_triple()

## Knowledge Gaps
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `_apply_tolerant_xlrd()` connect `Community 1` to `Community 3`, `Community 6`, `Community 7`, `Community 10`, `Community 14`, `Community 16`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.07828967178560675 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `Community 7` to `Community 1`, `Community 2`, `Community 3`, `Community 5`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.07397959183673469 - nodes in this community are weakly interconnected._
- **Why does `load_anomalies()` connect `Community 14` to `Community 1`, `Community 2`, `Community 3`, `Community 5`, `Community 7`, `Community 9`, `Community 11`, `Community 13`, `Community 16`, `Community 19`, `Community 20`, `Community 21`, `Community 22`, `Community 23`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.08843537414965986 - nodes in this community are weakly interconnected._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.07751937984496124 - nodes in this community are weakly interconnected._