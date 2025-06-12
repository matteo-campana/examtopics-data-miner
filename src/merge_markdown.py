import os


def merge_markdown_files(output_folder="output", merged_filename="merged_output.md"):
    md_files = [f for f in os.listdir(output_folder) if f.endswith(".md")]
    md_files = sorted(md_files)  # Ensure files are ordered by name

    merged_path = os.path.join(output_folder, merged_filename)
    with open(merged_path, "w", encoding="utf-8") as outfile:
        for fname in md_files:
            file_path = os.path.join(output_folder, fname)
            with open(file_path, "r", encoding="utf-8") as infile:
                outfile.write(
                    f"# {fname}\n\n"
                )  # Optional: add filename as section header
                outfile.write(infile.read())
                outfile.write("\n\n")

    print(f"Merged {len(md_files)} files into {merged_path}")


if __name__ == "__main__":
    merge_markdown_files()
