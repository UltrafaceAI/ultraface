from typing import Optional
import gradio

from ultraface import metadata, wording

ABOUT_BUTTON: Optional[gradio.HTML] = None
DONATE_BUTTON: Optional[gradio.HTML] = None


def render() -> None:
	global ABOUT_BUTTON
	global DONATE_BUTTON

	ABOUT_BUTTON = gradio.Button(
		value=metadata.get('name') + ' ' + metadata.get('version'),
		variant='primary',
		link=metadata.get('url')
	)
