MERGE (MtPth_Map_003_m1_9_m1_11:Reaction{name:'MtPth_Map_003_m1_9_m1_11'})
ON CREATE
SET MtPth_Map_003_m1_9_m1_11.studyid = 'MtPth_Map_003', MtPth_Map_003_m1_9_m1_11.study_type = 'arabidopsis thaliana'
WITH MtPth_Map_003_m1_9_m1_11
MATCH (p:Molecule),(r:Molecule)
WHERE p.id = 'MtPth_Map_003_m1_11' AND r.id = 'MtPth_Map_003_m1_9'
MERGE (r)-[:REACTS_IN]->(MtPth_Map_003_m1_9_m1_11)-[:PRODUCES]->(p)
;
