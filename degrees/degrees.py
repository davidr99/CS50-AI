import csv
import sys

from util import Node, StackFrontier, QueueFrontier
import networkx as nx
import matplotlib.pyplot as plt

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}

G = nx.Graph()

def load_data(directory):

    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"F:/Python/CS50/Search/degrees/{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                G.add_node("P" + row["id"])
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"F:/Python/CS50/Search/degrees/{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            G.add_node(row["id"])
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"F:/Python/CS50/Search/degrees/{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])

                G.add_edge(row["movie_id"], "P" + row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "small"

    show_graph = False

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    #source = person_id_for_name(input("Name: "))
    source = "Emma Watson"
    if source is None:
        sys.exit("Person not found.")
    #target = person_id_for_name(input("Name: "))
    target = "Jennifer Lawrence"
    if target is None:
        sys.exit("Person not found.")


    short_path = nx.shortest_path(G, "P" + person_id_for_name(source), "P" + person_id_for_name(target))
    print(short_path)

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None,  person_id_for_name(source))] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")

    print(short_path)
    if show_graph:
        nx.draw(G, with_labels=True, font_weight='bold')
        plt.show()


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    start_person_id = person_id_for_name(source)
    goal_person_id = person_id_for_name(target)

    start = Node(state=start_person_id, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)

    explored = set()
    num_explored = 0

    # Keep looping until solution found
    while True:

        # If nothing left in frontier, then no path
        if frontier.empty():
            raise Exception("no solution")

        # Choose a node from the frontier
        node = frontier.remove()
        num_explored += 1

        # Mark node as explored
        explored.add(node.state)

        # Add neighbors to frontier
        for action, state in neighbors_for_person(node.state):
            if not frontier.contains_state(state) and state not in explored:
                if state == goal_person_id:
                    solution = []
                    solution.append((action, state))
                    while node.parent is not None:
                        solution.append((node.action, node.state))
                        node = node.parent
                    
                    solution.reverse()
                    print(solution)
                    return solution

                child = Node(state=state, parent=node, action=action)
                frontier.add(child)


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
