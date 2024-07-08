METADATA =\
{
	'name': 'NextFace',
	'description': 'NextFace Studio is a revolutionary Windows application designed for facial manipulation in videos',
	'version': '1.0.0',
	'license': 'MIT',
	'author': 'Next Face',
	'url': 'https://nextface.art'
}


def get(key : str) -> str:
	return METADATA[key]
