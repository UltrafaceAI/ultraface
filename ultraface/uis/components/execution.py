from typing import List, Optional
import gradio
import onnxruntime

import ultraface.globals
from ultraface import wording
from ultraface.face_analyser import clear_face_analyser
from ultraface.processors.frame.core import clear_frame_processors_modules
from ultraface.execution import encode_execution_providers, decode_execution_providers

EXECUTION_PROVIDERS_CHECKBOX_GROUP : Optional[gradio.CheckboxGroup] = None


def render() -> None:
	global EXECUTION_PROVIDERS_CHECKBOX_GROUP

	EXECUTION_PROVIDERS_CHECKBOX_GROUP = gradio.CheckboxGroup(
		label = wording.get('uis.execution_providers_checkbox_group'),
		choices = encode_execution_providers(onnxruntime.get_available_providers()),
		value = encode_execution_providers(ultraface.globals.execution_providers)
	)


def listen() -> None:
	EXECUTION_PROVIDERS_CHECKBOX_GROUP.change(update_execution_providers, inputs = EXECUTION_PROVIDERS_CHECKBOX_GROUP, outputs = EXECUTION_PROVIDERS_CHECKBOX_GROUP)


def update_execution_providers(execution_providers : List[str]) -> gradio.CheckboxGroup:
	clear_face_analyser()
	clear_frame_processors_modules()
	execution_providers = execution_providers or encode_execution_providers(onnxruntime.get_available_providers())
	ultraface.globals.execution_providers = decode_execution_providers(execution_providers)
	return gradio.CheckboxGroup(value = execution_providers)
