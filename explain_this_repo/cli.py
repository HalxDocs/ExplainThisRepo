import sys
from explain_this_repo.github import fetch_repo, fetch_readme
from explain_this_repo.prompt import build_prompt
from explain_this_repo.generate import generate_explanation
from explain_this_repo.writer import write_output


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: explainthisrepo owner/repo [--detailed]")
        sys.exit(1)

    target = sys.argv[1]
    detailed = False

    if len(sys.argv) == 3:
        if sys.argv[2] != "--detailed":
            print("Unknown option:", sys.argv[2])
            print("Usage: explainthisrepo owner/repo [--detailed]")
            sys.exit(1)
        detailed = True

    if "/" not in target or target.count("/") != 1:
        print("Invalid format. Use owner/repo")
        sys.exit(1)

    owner, repo = target.split("/")

    if not owner or not repo:
        print("Invalid format. Use owner/repo")
        sys.exit(1)

    print(f"Fetching {owner}/{repo}…")

    try:
        repo_data = fetch_repo(owner, repo)
        readme = fetch_readme(owner, repo)
    except Exception as e:
        print(str(e))
        sys.exit(1)

    prompt = build_prompt(
        repo_name=repo_data.get("full_name"),
        description=repo_data.get("description"),
        readme=readme,
        detailed=detailed,
    )

    print("Generating explanation…")

    try:
        output = generate_explanation(prompt)
    except Exception:
        print("Failed to generate explanation.")
        print("Check your API key or try again later.")
        sys.exit(1)

    print("Writing EXPLAIN.md…")
    write_output(output)

    word_count = len(output.split())

    print("EXPLAIN.md generated successfully 🎉")
    print(f"Words: {word_count}")
    print("\nOpen EXPLAIN.md to read it.")


if __name__ == "__main__":
    main()
