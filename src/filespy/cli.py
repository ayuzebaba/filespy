import click
from filespy.analyzer import count_lines, count_words, get_file_size, get_extension


@click.group()
def main():
    """Filespy - A file analysis tool."""
    pass


@main.command()
@click.argument('filepath')
def analyze(filepath):
    """Analyze a single file and show its stats."""
    lines = count_lines(filepath)
    words = count_words(filepath)
    size = get_file_size(filepath)
    ext = get_extension(filepath)

    click.echo(f"File:       {filepath}")
    click.echo(f"Lines:      {lines}")
    click.echo(f"Words:      {words}")
    click.echo(f"Size:       {size} KB")
    click.echo(f"Extension:  {ext}")


@main.command()
@click.argument('folder')
@click.option('--extension', '-e', default=None, help='Filter by extension e.g. .txt')
def scan(folder, extension):
    """Scan a folder and analyze all files in it."""
    import os
    files = os.listdir(folder)

    for filename in files:
        if extension and not filename.endswith(extension):
            continue
        filepath = os.path.join(folder, filename)
        if os.path.isfile(filepath):
            click.echo(f"\n--- {filename} ---")
            click.echo(f"Lines:      {count_lines(filepath)}")
            click.echo(f"Words:      {count_words(filepath)}")
            click.echo(f"Size:       {get_file_size(filepath)} KB")