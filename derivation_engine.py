import argparse
import pathlib

from uvengine import UVEngine


def main(feature_model_path: str,
         configs_model_path: list[str],
         templates_paths: list[str],
         mapping_filepath: str | None = None
         ) -> None:
    uvengine = UVEngine(feature_model_path=feature_model_path,
                        configs_path=configs_model_path,
                        templates_paths=templates_paths,
                        mapping_model_filepath=mapping_filepath)
    resolved_templates = uvengine.resolve_variability()
    # Save the resolved templates to file
    for template_path, content in resolved_templates.items():
        outputfile = save_template(template_path, content)
        print(content)
        print(f'Resolved template saved to: {outputfile}')


def save_template(template_path: str, content: str) -> str:
    """Save the resolved template content to a file."""
    template_path = pathlib.Path(template_path)
    base_path = template_path.parent
    name = template_path.name.removesuffix(''.join(template_path.suffixes)) + '_resolved'
    suffixes = ''.join(template_path.suffixes).replace('.jinja', '')
    output_file = base_path / f'{name}{suffixes}'
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(content)
    return str(output_file)


def collect_files(paths: list[str]) -> list[str]:
    files = []
    for p in paths:
        path = pathlib.Path(p)
        if path.is_file():
            files.append(str(path))
        elif path.is_dir():
            files.extend([str(f) for f in path.glob('*') if f.is_file()])
        else:
            raise ValueError(f"Path '{p}' is not a valid file or directory.")
    return files


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='UVengine: Universal Variability resolution engine for UVL with Jinja templates.')
    parser.add_argument('-fm', '--feature_model', dest='feature_model', type=str, required=True, 
                        help='Feature model in UVL (.uvl).')
    parser.add_argument('-c', '--configs', dest='configs', type=str, nargs='+', required=True, 
                        help='Configurations files (.json) or directory with configurations.')
    parser.add_argument('-t', '--templates', dest='templates', type=str, nargs='+', required=True, 
                        help='Template files (.jinja) or directory with templates over which the variability is resolved.')
    parser.add_argument('-m', '--mapping', dest='mapping_file', type=str, required=False, 
                        help='File with the mapping between the features in the feature model and the variation points and variants in the templates (.csv).')
    args = parser.parse_args()

    # Get parameters
    feature_model_path = args.feature_model
    configs_paths = collect_files(args.configs)
    templates_pahts = collect_files(args.templates)
    mapping_file_path = args.mapping_file

    main(feature_model_path, configs_paths, templates_pahts, mapping_file_path)    

