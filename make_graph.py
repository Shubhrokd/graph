import os
import re
from prompt_input import entities, relationships
from loader import LoadGraphData
from tqdm import tqdm


def create_relationships(loader, title, e1, l1, e2, l2, R):
    query = f'MERGE (:Article {{name: "{title}"}})\
            MERGE (:{l1} {{name: "{e1}"}})\
            MERGE (:{l2} {{name: "{e2}"}})'
    loader.create(query)

    query = f'MATCH (t:Article {{name: "{title}"}})\
            MATCH (a:{l1} {{name: "{e1}"}})\
            MATCH (b:{l2} {{name: "{e2}"}})\
            MERGE (a)-[:{R}]->(b)\
            MERGE (a)-[:IN_ARTICLE]->(t)\
            MERGE (b)-[:IN_ARTICLE]->(t)'
    loader.create(query)


def make_graph(source, cleaned):
    loader = LoadGraphData("neo4j", "<password>", "bolt://localhost:7687")
    loader.delete_graph()

    history = []
    for results in tqdm(os.listdir(source)):
        with open(os.path.join(source, results)) as r:
            content = r.read()
            lines = content.split("\n")
        if len(lines) < 10:
            continue

        with open(
            os.path.join(cleaned, "cleaned_" + "_".join(results.split("_")[1:]))
        ) as c:
            cleaned_content = c.read()

        for line in lines:
            line = re.sub("^\d+\.", "", line).strip()
            splitted = line.split(",")
            if len(splitted) == 3:
                A = splitted[0]
                R = splitted[1].strip()
                B = splitted[2]

                if not ":" in A or not ":" in B:
                    continue

                e1, l1 = A.split(":")[0], A.split(":")[1]
                e2, l2 = B.split(":")[0], B.split(":")[1]
                e1, e2, l1, l2 = e1.strip(), e2.strip(), l1.strip(), l2.strip()

                if (
                    e1.lower() not in cleaned_content.lower()
                    or e2.lower() not in cleaned_content.lower()
                ):
                    continue

                if l1 == "Person":
                    for subname in e1.split()[::-1]:
                        if subname[0].upper() == subname[0]:
                            e1 = subname
                            break

                if l2 == "Person":
                    for subname in e2.split()[::-1]:
                        if subname[0].upper() == subname[0]:
                            e2 = subname
                            break

                if (
                    R == R.upper()
                    and R in relationships
                    and l1 in entities
                    and l2 in entities
                    and len(e1.split()) < 5
                    and len(e1) > 1
                    and len(e2.split()) < 5
                    and len(e2) > 1
                    and e1 != e2
                ):
                    if line not in history:
                        history.append(line)

                        l1 = l1.replace(" ", "_")
                        l2 = l2.replace(" ", "_")
                        e1 = e1.replace('"', "")
                        e2 = e2.replace('"', "")
                        title = results.split(".")[0].replace(" ", "_")
                        title = "_".join(title.split("_")[1:])

                        create_relationships(
                            loader=loader, title=title, e1=e1, l1=l1, e2=e2, l2=l2, R=R
                        )
