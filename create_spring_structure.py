import click
import os
import yaml


@click.command()
@click.option("-d", "--default", is_flag=True, help="Use default structure")
@click.option(
    "-e",
    "--with-example-files",
    is_flag=True,
    help="Create example files in directories",
)
@click.argument("name", required=False)  # Class name is now optional
@click.option("--help", is_flag=True, help="Show this message and exit")
def create_spring_structure(default, with_example_files, name, help):
    if help:
        click.echo("Create Spring Project Structure CLI")
        click.echo("Usage:")
        click.echo("  create-spring-structure [OPTIONS] [NAME]")
        click.echo("\nOptions:")
        click.echo("  -d, --default           Use default structure")
        click.echo("  -e, --with-example-files Create example files in directories")
        click.echo("  --help                  Show this message and exit")
        return

    if default:
        # Read the default structure and excluded directories from a YAML file
        config_path = "cli-config/default_structure.yml"
        with open(config_path, "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        directories = data.get("default", [])  # Get the list under 'default' key
        exclude_defaults = data.get(
            "exclude_defaults", []
        )  # Get the list of excluded directories

    if not directories:
        click.echo("No directories specified.")
        return

    # Create the specified directories and generate classes
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        click.echo(f"Created directory: {directory}")

        if with_example_files and directory not in exclude_defaults:
            class_name = name.capitalize() if name else "Example"
            generate_class(directory, class_name)


def generate_class(directory, name):
    filename = f"{name}{directory.capitalize()}.java"

    template_file = f"cli-config/templates/{directory}_Template"  # Template file based on directory name

    with open(template_file, "r") as template:
        content = template.read()
        content = content.replace("{{ClassName}}", name)

    with open(os.path.join(directory, filename), "w") as file:
        file.write(content)

        click.echo(f"Created example file: {os.path.join(directory, filename)}")


if __name__ == "__main__":
    create_spring_structure()
